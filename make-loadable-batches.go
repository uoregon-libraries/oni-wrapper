package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

const oniDir = "/opt/openoni"
const scriptPath = "/tmp/load-all.sh"
const liveBatchPath = "/mnt/libfiles"
const oldBatchPath = "/opt/old-batches"

func main() {
	var f, err = os.Create(scriptPath)
	if err != nil {
		log.Fatalf("Error creating output script %q: %s", scriptPath, err)
	}

	fmt.Fprintf(f, "cd %s\n", oniDir)
	fmt.Fprintf(f, "source %s/ENV/bin/activate\n", oniDir)

	var infos []os.FileInfo
	infos, err = ioutil.ReadDir(liveBatchPath)
	if err != nil {
		log.Fatalf("Unable to read batch path %q: %s", liveBatchPath, err)
	}

	for _, info := range infos {
		var batchDest = getBatchDest(info)
		if batchDest != "" {
			fmt.Fprintf(f, "./manage.py load_batch %s\n", batchDest)
		}
	}
}

func getBatchDest(batchInfo os.FileInfo) string {
	var batchName = batchInfo.Name()
	if !batchInfo.IsDir() {
		log.Printf("Skipping %q: not a directory", batchName)
		return ""
	}
	if !strings.HasPrefix(batchName, "batch_") {
		log.Printf("Skipping %q: not a batch", batchName)
		return ""
	}

	var fullPath = filepath.Join(liveBatchPath, batchName)

	// Check for need to fake a data dir
	var missingDatadir bool
	var dataPath = filepath.Join(fullPath, "data")
	var _, err = os.Stat(dataPath)
	if os.IsNotExist(err) {
		missingDatadir = true
	}

	// Check for need to fake a version
	var missingVersion bool
	var l = len(batchName) - 2
	var verSuffix = batchName[:l]
	if !strings.HasSuffix(verSuffix, "ver") {
		missingVersion = true
	}

	if !missingVersion && !missingDatadir {
		return fullPath
	}

	var linkSource = fullPath
	var linkDest = filepath.Join(oldBatchPath, batchName)
	if missingVersion {
		linkDest = filepath.Join(oldBatchPath, batchName+"_ver01")
	}
	if missingDatadir {
		linkDest = filepath.Join(linkDest, "data")
	}

	var info os.FileInfo
	info, err = os.Lstat(linkDest)
	if os.IsNotExist(err) {
		log.Printf("Symlinking %q to %q", linkSource, linkDest)
		// Create the parent dir(s)
		var dir = filepath.Dir(linkDest)
		err = os.MkdirAll(dir, 0755)
		if err != nil {
			log.Fatalf("Error making symlink's parent directory: %s", err)
		}
		err = os.Symlink(linkSource, linkDest)
		if err != nil {
			log.Fatalf("Error making symlink: %s", err)
		}
		return linkDest
	}
	if err != nil {
		log.Fatalf("Unable to check for existing symlink %q: %s", linkDest, err)
	}
	if info.Mode()&os.ModeSymlink != 0 {
		log.Printf("NOT linking %q: already a symlink", linkDest)
		return ""
	}

	log.Fatalf("Unable to symlink: %q to %q: destination mode: %q", linkSource, linkDest, info.Mode())
	return ""
}
