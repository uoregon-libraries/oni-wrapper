package main

import (
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"
)

type config struct {
	printBody bool
	insecure  bool
	host      string
	path      string
	url       *url.URL
}

type nullWriter struct{}

func (w nullWriter) Write(data []byte) (int, error) { return len(data), nil }

// We create a new command-line flag parser instead of using the default.
// Default package-level vars may or may not be set up how we want, but they
// often present a small security risk.
var cmdFlags = flag.NewFlagSet(os.Args[0], flag.ContinueOnError)

func getArgs() *config {
	var c = new(config)

	cmdFlags.BoolVar(&c.insecure, "insecure", false, "set to true to use http instead of https")
	cmdFlags.StringVar(&c.host, "host", "localhost", "hostname for the search")
	cmdFlags.StringVar(&c.path, "path", "/search/pages/results", "base path to the search URL to test")
	cmdFlags.BoolVar(&c.printBody, "print", false, "print the web page's body to STDOUT")

	// flag.FlagSet force-writes to output, so to keep output sane and easy to
	// parse, we have to set up a fake.  Oh, I should just set output to the
	// actual nil value?  Nope.  They just switch to os.Stderr in that case....
	//
	// TIL built-in flag package is just trash if you don't <3 the defaults
	var null nullWriter
	cmdFlags.SetOutput(null)

	var err = cmdFlags.Parse(os.Args[1:])
	if err != nil {
		usage(err)
	}

	c.url = new(url.URL)
	c.url.Scheme = "https"
	c.url.Host = c.host
	c.url.Path = c.path
	if c.insecure {
		c.url.Scheme = "http"
	}
	log.Printf("INFO - using %q for search test", c.url.String())

	return c
}

func usage(err error) {
	var code int

	if err != flag.ErrHelp {
		fmt.Fprintf(os.Stderr, "Error: %s\n\n", err)
		code = 2
	}

	fmt.Fprintf(os.Stderr, "Usage: %s [OPTION]\n\n", cmdFlags.Name())
	// To make use of the built-in function, we must now set output again
	cmdFlags.SetOutput(os.Stderr)
	cmdFlags.PrintDefaults()

	os.Exit(code)
}
