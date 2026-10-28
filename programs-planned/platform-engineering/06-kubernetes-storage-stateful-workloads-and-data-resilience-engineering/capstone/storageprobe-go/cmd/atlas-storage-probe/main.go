package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"example.invalid/atlas/storageprobe/atomicfile"
)

type report struct {
	Path   string `json:"path"`
	Bytes  int    `json:"bytes"`
	SHA256 string `json:"sha256"`
}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "usage: atlas-storage-probe PATH VALUE")
		os.Exit(2)
	}
	path := filepath.Clean(os.Args[1])
	data := []byte(os.Args[2])
	if err := atomicfile.Write(path, data, 0o640); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	sum := sha256.Sum256(data)
	output, _ := json.Marshal(report{path, len(data), hex.EncodeToString(sum[:])})
	fmt.Println(string(output))
}
