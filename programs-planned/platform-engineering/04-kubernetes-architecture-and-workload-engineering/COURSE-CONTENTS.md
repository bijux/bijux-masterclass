# Complete course contents

## Learner product

- **Course:** Kubernetes Architecture and Workload Engineering
- **Position:** Course 4 of the Platform Engineering program
- **Cumulative system:** Atlas Kubernetes Runtime 1.0
- **Course-book pages:** 97
- **Course-book words:** 40,089
- **Numbered modules:** 10 plus orientation
- **Exercises:** 120
- **Worked answers:** 120
- **Failure-oriented labs:** 10
- **Evidence checkpoints:** 10

## Executable teaching material

- deterministic Python API/control-plane model;
- standard-library Go controller core and in-cluster Kubernetes API adapter;
- production-intent Kubernetes manifests;
- optional kind observation lane;
- exact Course 3 predecessor package;
- exact Course 5 networking handoff;
- ten planted defects;
- six categorical release candidates;
- 66 Python tests;
- six Go tests across two packages;
- cumulative capstone tour.

## Source inventory before release manifests

- Markdown files: 116
- Python files: 41
- Go files: 6
- YAML files: 36
- JSON files: 40
- Manifest-controlled payload files: 246
- Total course files including the course manifest pair: 248

## Directory map

```text
04-kubernetes-architecture-and-workload-engineering/
├── course-book/                 authoritative reader-facing course
├── capstone/
│   ├── predecessor/             exact Course 3 handoff
│   ├── atlas_kube/              Python semantic control plane
│   ├── controller-go/           Go reconciliation core and API adapter
│   ├── manifests/               base, lab, and controller resources
│   ├── kind/                    optional local observation lane
│   ├── architecture/            ownership and responsibility contracts
│   ├── planted-defects/         ten failure candidates
│   ├── releases/                accepted/rejected/review/not-executed corpus
│   ├── handoff/                 exact Course 5 connectivity contract
│   └── tests/                   executable regressions
├── assessment/                  final project and rubric
├── instructor/                  facilitation and reset material
├── scripts/                     proof, packaging, and verification routes
├── Makefile
├── mkdocs.yml
├── course.json
└── tool-versions.json
```
