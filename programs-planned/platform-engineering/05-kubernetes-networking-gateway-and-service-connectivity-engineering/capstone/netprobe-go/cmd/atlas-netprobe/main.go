package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"time"

	"example.invalid/atlas/netprobe/internal/probe"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: atlas-netprobe resolve NAME | tcp HOST:PORT | http URL")
		os.Exit(2)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	var result probe.Result
	var err error
	switch os.Args[1] {
	case "resolve":
		result, err = probe.Resolve(ctx, net.DefaultResolver, os.Args[2])
	case "tcp":
		result, err = probe.TCP(ctx, "tcp", os.Args[2], 3*time.Second)
	case "http":
		result, err = probe.HTTP(ctx, &http.Client{Timeout: 4 * time.Second}, os.Args[2])
	default:
		err = fmt.Errorf("unknown command %q", os.Args[1])
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
