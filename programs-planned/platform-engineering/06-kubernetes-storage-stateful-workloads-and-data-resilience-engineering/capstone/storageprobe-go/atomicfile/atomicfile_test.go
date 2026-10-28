package atomicfile

import (
	"os"
	"path/filepath"
	"testing"
)

func TestWriteReplacesContent(t *testing.T) {
	root := t.TempDir()
	path := filepath.Join(root, "state", "value")
	if err := Write(path, []byte("one"), 0o640); err != nil {
		t.Fatal(err)
	}
	if err := Write(path, []byte("two"), 0o640); err != nil {
		t.Fatal(err)
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if string(data) != "two" {
		t.Fatalf("got %q", data)
	}
}
