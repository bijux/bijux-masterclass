package atlas

import (
	"reflect"
	"testing"
)

const apiImage = "platform/atlas-api@sha256:6e3b38e88f6ef4252b635b6d199095db46233d7b6f85f3be4384d746386317a7"
const workerImage = "platform/atlas-worker@sha256:bbd52b30969ebb6fb3568d2ce5c1ebfb420c7bd7a80001f2a1014feaa4d7a036"

func fixture() AtlasWorkload {
	return AtlasWorkload{
		APIVersion: "platform.bijux.dev/v1alpha1",
		Kind:       "AtlasWorkload",
		Metadata:   ObjectMeta{Name: "atlas", Namespace: "atlas-system", UID: "uid-1", Generation: 3},
		Spec: AtlasWorkloadSpec{
			APIImage: apiImage, WorkerImage: workerImage,
			APIReplicas: 3, WorkerReplicas: 1,
			ConfigurationRef: "atlas-config", AvailabilityClass: "critical",
		},
	}
}

func TestReconcileIsDeterministic(t *testing.T) {
	in := fixture()
	first, err := Reconcile(in, false)
	if err != nil {
		t.Fatal(err)
	}
	in.Status = first.Status
	second, err := Reconcile(in, false)
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(first, second) {
		t.Fatalf("steady state changed:\n%#v\n%#v", first, second)
	}
}

func TestWorkerRemainsOneReplica(t *testing.T) {
	in := fixture()
	in.Spec.WorkerReplicas = 2
	if _, err := Reconcile(in, false); err == nil {
		t.Fatal("expected worker replica validation error")
	}
}

func TestChildrenPreserveDigestAndSecurity(t *testing.T) {
	out, err := Reconcile(fixture(), true)
	if err != nil {
		t.Fatal(err)
	}
	if len(out.Children) != 2 {
		t.Fatalf("children=%d", len(out.Children))
	}
	for _, child := range out.Children {
		if child.Container.RunAsUser != 65532 || !child.Container.ReadOnlyRootFilesystem {
			t.Fatalf("insecure child: %#v", child)
		}
		if child.Container.AllowPrivilegeEscalation {
			t.Fatal("privilege escalation enabled")
		}
		if child.Container.Image == "" {
			t.Fatal("missing image")
		}
	}
}

func TestConditionTransitionTimePreserved(t *testing.T) {
	in := fixture()
	first, err := Reconcile(in, true)
	if err != nil {
		t.Fatal(err)
	}
	in.Status = first.Status
	second, err := Reconcile(in, true)
	if err != nil {
		t.Fatal(err)
	}
	if first.Status.Conditions[0].LastTransitionTime != second.Status.Conditions[0].LastTransitionTime {
		t.Fatal("transition time churned")
	}
}

func TestDeletionRequestsCleanup(t *testing.T) {
	in := fixture()
	ts := "2026-08-09T00:00:00Z"
	in.Metadata.DeletionTimestamp = &ts
	out, err := Reconcile(in, false)
	if err != nil {
		t.Fatal(err)
	}
	if !out.DeleteChildren || !out.FinalizerRequired {
		t.Fatalf("invalid deletion result: %#v", out)
	}
}
