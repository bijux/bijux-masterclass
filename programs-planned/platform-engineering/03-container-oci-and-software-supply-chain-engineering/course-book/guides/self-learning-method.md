# Self-learning method — learn the object, then the tool

Container courses often fail self-learners in one of two ways. Some begin with dozens of commands and leave the learner unable to explain what the commands created. Others remain conceptual and never force a claim to survive contact with bytes, processes, or failure. This course uses a repeated but non-mechanical learning cycle:

```text
model the object
→ identify owner and stable identity
→ inspect one real instance
→ predict a failure
→ falsify the prediction
→ preserve evidence
→ state the bounded conclusion
```

The cycle applies differently in every module. A namespace is inspected through process state. An OCI image is traversed through descriptors and blobs. A cache claim is tested through controlled rebuilds. A registry reference is resolved and then pinned by digest. A provenance statement is verified against a subject and identity policy. The method is stable; the evidence is not interchangeable.

## Begin with one engineering question

Before reading a chapter, write the module’s question in your own words. For Module 3, a useful question is:

> Which exact bytes and ordered filesystem changes constitute this image, and how can I prove the graph is internally consistent?

Do not replace it with “How do I build an image?” The narrower question guides what you should remember and what output matters.

## Draw the state and authority boundary

For each mechanism, write four fields:

| Field | Example for a registry tag |
|---|---|
| owner | repository/tag writer authority |
| stable identity | none; the tag is mutable |
| state transition | retarget from digest A to digest B |
| decisive evidence | protected-tag audit plus resolved digest |

Do the same for a layer, runtime bundle, user namespace, SBOM, signing key, or release record. This prevents a tool from becoming the owner merely because it exposes the command.

## Read the chapter in two passes

### First pass: argument

Ignore commands. Identify:

- the problem the mechanism solves;
- the objects involved;
- the invariants;
- the attractive wrong model;
- the failure evidence;
- what the next module depends on.

### Second pass: implementation

Follow the linked capstone files. Trace names and digests across code and data. The Python semantic implementation is intentionally readable; it is not presented as a replacement for BuildKit, runc, or a production registry.

## Answer exercises before reading solutions

Write an answer that includes:

1. conclusion;
2. governing mechanism;
3. failure or counterexample;
4. decisive evidence;
5. operational consequence.

For example, “tags are mutable” is not enough. A complete answer explains that a tag is repository metadata, that two resolutions can return different manifests, that the release must record the digest resolved under review, and that deployment/promotion should continue by digest.

Compare your reasoning with the worked answer. Do not grade by wording. Check whether you identified the same owner, invariant, and proof layer.

## Use the lab as an experiment

A lab is not a list of steps to copy. Before executing the controlled action:

- record the baseline;
- predict the first failing phase;
- predict the error/evidence;
- name what would disprove your explanation.

If the outcome differs, stop. Do not continue until you can explain why. A surprising result is often the most educational event in the course.

## Preserve an evidence journal

For each lab, record:

```text
claim
subject identity
input versions
environment fingerprint
action
raw evidence
interpretation
strongest justified conclusion
unexecuted stronger proof
cleanup result
```

Store raw output separately from your narrative. Never edit raw output to make the result cleaner. A release decision must be reproducible from retained evidence.

## Practice retrieval, not recognition

At the end of each day, reconstruct from memory:

- the object graph or state machine;
- three independent identities;
- one failure that passes superficial validation;
- the strongest evidence produced;
- a claim the module deliberately did not prove.

If you can recognize a diagram but cannot redraw it, the model is not yet available under pressure.

## Use one primary tool lane and one independent lane

The dependency-light implementation gives transparency. Choose one native lane for independent evidence:

- BuildKit/Docker or Podman for builds;
- runc or crun for runtime bundles;
- ORAS/Skopeo/Crane for registry objects;
- Syft/Grype or another pair for inventory/scanning;
- Cosign/Sigstore for signing and verification.

Do not run five tools and count five green results as five independent guarantees. Ask which implementation, data source, and trust root each uses.

## Know when to stop

You have completed a module when you can:

- explain the mechanism without product names;
- locate the capstone implementation and evidence;
- make the planted defect fail for the expected reason;
- defend the checkpoint decision;
- state what remains environment-backed.

You have not completed it merely because the happy path ran.
