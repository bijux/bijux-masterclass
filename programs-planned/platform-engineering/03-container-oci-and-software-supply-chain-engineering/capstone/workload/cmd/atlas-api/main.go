package main

import (
	"context"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	mux := http.NewServeMux()
	mux.HandleFunc("/live", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]any{"status": "live", "release": "1.0.0"})
	})
	mux.HandleFunc("/ready", func(w http.ResponseWriter, _ *http.Request) {
		if _, err := os.Stat("/var/lib/atlas/spool"); err != nil {
			http.Error(w, "spool unavailable", http.StatusServiceUnavailable)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]any{"status": "ready", "release": "1.0.0"})
	})
	server := &http.Server{
		Addr:              ":8080",
		Handler:           mux,
		ReadHeaderTimeout: 3 * time.Second,
		IdleTimeout:       30 * time.Second,
	}
	stopped := make(chan error, 1)
	go func() {
		logger.Info("atlas api starting", "address", server.Addr)
		err := server.ListenAndServe()
		if errors.Is(err, http.ErrServerClosed) {
			err = nil
		}
		stopped <- err
	}()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGTERM, syscall.SIGINT)
	select {
	case sig := <-signals:
		logger.Info("atlas api draining", "signal", sig.String())
		ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
		defer cancel()
		_ = server.Shutdown(ctx)
	case err := <-stopped:
		if err != nil {
			logger.Error("atlas api failed", "error", err)
			os.Exit(1)
		}
	}
}
