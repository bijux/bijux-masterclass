package probe

import (
	"context"
	"net"
	"testing"
	"time"
)

func TestResolveLocalhost(t *testing.T) {
	result, err := Resolve(context.Background(), net.DefaultResolver, "localhost")
	if err != nil {
		t.Fatal(err)
	}
	if len(result.Addresses) == 0 {
		t.Fatal("expected at least one localhost address")
	}
}

func TestTCPRefusesClosedPort(t *testing.T) {
	_, err := TCP(context.Background(), "tcp", "127.0.0.1:1", 50*time.Millisecond)
	if err == nil {
		t.Fatal("expected a connection failure")
	}
}
