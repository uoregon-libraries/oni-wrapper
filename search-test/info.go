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
	Error          string
	Success        bool
	URL            string
	ResponseBody   []byte `json:"-"`
	Words          string
	ResultCount    int64
	DurationMillis int64
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
	var resp, err = http.Get(s.URL)
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
