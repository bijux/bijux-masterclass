package cni

import "testing"

func TestReplayAndGC(t *testing.T) {
	s := NewState()
	a, err := s.Add("a", 1, "10.0.0.2")
	if err != nil {
		t.Fatal(err)
	}
	b, err := s.Add("a", 1, "10.0.0.2")
	if err != nil || a.Address != b.Address {
		t.Fatal("replay failed")
	}
	s.Add("b", 2, "10.0.0.3")
	removed := s.GC(map[string]int{"b": 2})
	if len(removed) != 1 || removed[0] != "a" {
		t.Fatalf("removed %#v", removed)
	}
	s.Del("a")
	s.Del("a")
}
func TestStatus(t *testing.T) {
	if !Status(map[string]bool{"ipam": true, "routes": true}) {
		t.Fatal("expected ready")
	}
	if Status(map[string]bool{"ipam": true, "routes": false}) {
		t.Fatal("expected not ready")
	}
}
