package atlas

import "time"

type ObjectMeta struct {
	Name              string   `json:"name"`
	Namespace         string   `json:"namespace"`
	UID               string   `json:"uid,omitempty"`
	Generation        int64    `json:"generation,omitempty"`
	DeletionTimestamp *string  `json:"deletionTimestamp,omitempty"`
	Finalizers        []string `json:"finalizers,omitempty"`
}

type AtlasWorkload struct {
	APIVersion string              `json:"apiVersion"`
	Kind       string              `json:"kind"`
	Metadata   ObjectMeta          `json:"metadata"`
	Spec       AtlasWorkloadSpec   `json:"spec"`
	Status     AtlasWorkloadStatus `json:"status,omitempty"`
}

type AtlasWorkloadSpec struct {
	APIImage          string `json:"apiImage"`
	WorkerImage       string `json:"workerImage"`
	APIReplicas       int32  `json:"apiReplicas"`
	WorkerReplicas    int32  `json:"workerReplicas"`
	ConfigurationRef  string `json:"configurationRef"`
	AvailabilityClass string `json:"availabilityClass"`
}

type Condition struct {
	Type               string `json:"type"`
	Status             string `json:"status"`
	Reason             string `json:"reason"`
	Message            string `json:"message"`
	ObservedGeneration int64  `json:"observedGeneration"`
	LastTransitionTime string `json:"lastTransitionTime"`
}

type AtlasWorkloadStatus struct {
	ObservedGeneration int64       `json:"observedGeneration"`
	ChildDeployments   []string    `json:"childDeployments"`
	Conditions         []Condition `json:"conditions"`
}

type Container struct {
	Name                     string            `json:"name"`
	Image                    string            `json:"image"`
	Port                     int32             `json:"port,omitempty"`
	RunAsUser                int64             `json:"runAsUser"`
	ReadOnlyRootFilesystem   bool              `json:"readOnlyRootFilesystem"`
	AllowPrivilegeEscalation bool              `json:"allowPrivilegeEscalation"`
	DropCapabilities         []string          `json:"dropCapabilities"`
	Requests                 map[string]string `json:"requests"`
	Limits                   map[string]string `json:"limits"`
}

type Deployment struct {
	Name              string            `json:"name"`
	Namespace         string            `json:"namespace"`
	OwnerUID          string            `json:"ownerUID"`
	Replicas          int32             `json:"replicas"`
	Labels            map[string]string `json:"labels"`
	ServiceAccount    string            `json:"serviceAccount"`
	AutomountToken    bool              `json:"automountToken"`
	TerminationGrace  int32             `json:"terminationGraceSeconds"`
	Container         Container         `json:"container"`
	DurableClaimNames []string          `json:"durableClaimNames,omitempty"`
}

type ReconcileOutput struct {
	FinalizerRequired bool                `json:"finalizerRequired"`
	DeleteChildren    bool                `json:"deleteChildren"`
	Children          []Deployment        `json:"children,omitempty"`
	Status            AtlasWorkloadStatus `json:"status"`
}

func now() string { return time.Now().UTC().Format(time.RFC3339) }
