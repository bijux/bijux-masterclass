package main

import (
	"encoding/json"
	"os"
	"syscall"
)

type Result struct {
	PID           int    `json:"pid"`
	UID           int    `json:"uid"`
	GID           int    `json:"gid"`
	Hostname      string `json:"hostname"`
	TmpWritable   bool   `json:"tmpWritable"`
	StateWritable bool   `json:"stateWritable"`
	EtcWritable   bool   `json:"etcWritable"`
	Release       string `json:"release"`
}

func tryWrite(path string) bool {
	err := os.WriteFile(path, []byte("atlas\n"), 0o600)
	if err == nil {
		_ = os.Remove(path)
		return true
	}
	return false
}

func main() {
	host, _ := os.Hostname()
	result := Result{
		PID:           syscall.Getpid(),
		UID:           syscall.Getuid(),
		GID:           syscall.Getgid(),
		Hostname:      host,
		TmpWritable:   tryWrite("/tmp/atlas-probe"),
		StateWritable: tryWrite("/var/lib/atlas/atlas-probe"),
		EtcWritable:   tryWrite("/etc/atlas-probe"),
		Release:       "1.0.0",
	}
	_ = json.NewEncoder(os.Stdout).Encode(result)
}
