package main

import (
	"encoding/json"
	"fmt"
	"os"
	cni "platform.example/atlas-cni-lab"
)

func main() {
	deps := map[string]bool{"ipam": true, "routes": true}
	out := map[string]any{"cniVersion": "1.1.0", "status": cni.Status(deps), "commands": []string{"ADD", "CHECK", "DEL", "GC", "STATUS", "VERSION"}}
	if err := json.NewEncoder(os.Stdout).Encode(out); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
