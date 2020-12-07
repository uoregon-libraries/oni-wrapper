package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"time"
)

type statusInfo struct {
	Start          time.Time
	Error          string `json:",omitempty"`
	Success        bool
	URL            string
	ResponseBody   []byte `json:"-"`
	Words          string
	ResultCount    int64 `json:",omitempty"`
	DurationMillis int64 `json:",omitempty"`
}

func (s *statusInfo) Print(out io.Writer) {
	var data, err = json.Marshal(s)
	if err != nil {
		panic("error marshaling statusInfo: " + err.Error())
	}
	fmt.Fprintln(out, string(data))
}

func (s *statusInfo) get() {
	s.Start = time.Now()
	var c = &http.Client{Timeout: time.Second * 60}
	var resp, err = c.Get(s.URL)
	if err != nil {
		s.Error = fmt.Sprintf("failed: %s", err)
		return
	}

	s.DurationMillis = time.Since(s.Start).Milliseconds()
	defer resp.Body.Close()
	s.ResponseBody, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		s.Error = fmt.Sprintf("failed: %s", err)
	}
}
