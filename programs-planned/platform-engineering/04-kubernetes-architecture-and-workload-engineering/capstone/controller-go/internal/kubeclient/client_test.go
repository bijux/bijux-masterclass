package kubeclient

import "testing"

func TestFinalizerHelpers(t *testing.T) {
	values := AddFinalizer([]string{"a"}, "b")
	if len(values) != 2 || !HasFinalizer(values, "b") {
		t.Fatal(values)
	}
	again := AddFinalizer(values, "b")
	if len(again) != 2 {
		t.Fatal(again)
	}
	removed := RemoveFinalizer(again, "b")
	if HasFinalizer(removed, "b") {
		t.Fatal(removed)
	}
}
