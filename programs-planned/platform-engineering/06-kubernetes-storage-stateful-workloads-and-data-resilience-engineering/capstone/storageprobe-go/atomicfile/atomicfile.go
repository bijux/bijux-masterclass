package atomicfile

import (
	"fmt"
	"os"
	"path/filepath"
)

// Write replaces path atomically on one filesystem after syncing file and directory.
func Write(path string, data []byte, mode os.FileMode) error {
	directory := filepath.Dir(path)
	if err := os.MkdirAll(directory, 0o750); err != nil {
		return err
	}
	temporary, err := os.CreateTemp(directory, ".atlas-tmp-")
	if err != nil {
		return err
	}
	tempName := temporary.Name()
	cleanup := func() { _ = os.Remove(tempName) }
	defer cleanup()
	if err := temporary.Chmod(mode); err != nil {
		_ = temporary.Close()
		return err
	}
	if _, err := temporary.Write(data); err != nil {
		_ = temporary.Close()
		return err
	}
	if err := temporary.Sync(); err != nil {
		_ = temporary.Close()
		return err
	}
	if err := temporary.Close(); err != nil {
		return err
	}
	if err := os.Rename(tempName, path); err != nil {
		return fmt.Errorf("atomic rename: %w", err)
	}
	handle, err := os.Open(directory)
	if err != nil {
		return err
	}
	defer handle.Close()
	return handle.Sync()
}
