package main

import (
	"context"
	"encoding/json"
	"log/slog"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"
)

func heartbeat(path string) error {
	body, _ := json.Marshal(map[string]any{"release": "1.0.0", "time": time.Now().UTC().Format(time.RFC3339Nano)})
	tmp := path + ".tmp"
	if err := os.WriteFile(tmp, append(body, '\n'), 0o640); err != nil {
		return err
	}
	return os.Rename(tmp, path)
}

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	root := "/var/lib/atlas"
	_ = os.MkdirAll(filepath.Join(root, "spool"), 0o770)
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	logger.Info("atlas worker starting")
	for {
		select {
		case <-ctx.Done():
			logger.Info("atlas worker stopping")
			return
		case <-ticker.C:
			if err := heartbeat(filepath.Join(root, "worker-heartbeat.json")); err != nil {
				logger.Error("heartbeat failed", "error", err)
			}
		}
	}
}
