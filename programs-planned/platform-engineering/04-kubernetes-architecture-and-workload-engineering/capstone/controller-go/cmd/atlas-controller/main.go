package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"
	"os/signal"
	"reflect"
	"syscall"
	"time"

	"platform.bijux.dev/atlas-controller/internal/atlas"
	"platform.bijux.dev/atlas-controller/internal/kubeclient"
)

func main() {
	childrenReady := flag.Bool("children-ready", false, "render Ready=True status")
	once := flag.Bool("once", false, "run one in-cluster reconciliation pass")
	interval := flag.Duration("interval", 5*time.Second, "in-cluster poll interval")
	flag.Parse()
	command := "render"
	if flag.NArg() > 0 {
		command = flag.Arg(0)
	}
	switch command {
	case "render":
		render(*childrenReady)
	case "serve":
		serve(*once, *interval)
	default:
		fatal(fmt.Errorf("unknown command %q", command))
	}
}

func render(childrenReady bool) {
	raw, err := io.ReadAll(os.Stdin)
	if err != nil {
		fatal(err)
	}
	var object atlas.AtlasWorkload
	if err := json.Unmarshal(raw, &object); err != nil {
		fatal(err)
	}
	out, err := atlas.Reconcile(object, childrenReady)
	if err != nil {
		fatal(err)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(out); err != nil {
		fatal(err)
	}
}

func serve(once bool, interval time.Duration) {
	client, err := kubeclient.NewInCluster()
	if err != nil {
		fatal(err)
	}
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()
	for {
		if err := reconcileAll(ctx, client); err != nil {
			fmt.Fprintln(os.Stderr, "reconcile:", err)
		}
		if once {
			return
		}
		select {
		case <-ctx.Done():
			return
		case <-time.After(interval):
		}
	}
}

func reconcileAll(ctx context.Context, client *kubeclient.Client) error {
	workloads, err := client.ListAtlasWorkloads(ctx)
	if err != nil {
		return err
	}
	for _, workload := range workloads {
		out, err := atlas.Reconcile(workload, false)
		if err != nil {
			return err
		}
		if workload.Metadata.DeletionTimestamp != nil {
			// The course has no external release-reservation service. Child cleanup is
			// owner-reference driven; only then is the course finalizer removed.
			if kubeclient.HasFinalizer(workload.Metadata.Finalizers, atlas.Finalizer) {
				if err := client.PatchFinalizers(ctx, workload, kubeclient.RemoveFinalizer(workload.Metadata.Finalizers, atlas.Finalizer)); err != nil {
					return err
				}
			}
			continue
		}
		if out.FinalizerRequired && !kubeclient.HasFinalizer(workload.Metadata.Finalizers, atlas.Finalizer) {
			if err := client.PatchFinalizers(ctx, workload, kubeclient.AddFinalizer(workload.Metadata.Finalizers, atlas.Finalizer)); err != nil {
				return err
			}
		}
		for _, child := range out.Children {
			if err := client.ApplyDeployment(ctx, child); err != nil {
				return err
			}
		}
		if !reflect.DeepEqual(workload.Status, out.Status) {
			if err := client.PatchStatus(ctx, workload, out.Status); err != nil {
				return err
			}
		}
	}
	return nil
}

func fatal(err error) { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
