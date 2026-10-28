# Worked answers

## 1. Why is name alone insufficient to identify one object lifetime?

A name can be reused after deletion. The UID distinguishes the original object from a replacement with the same namespace and name. Owner references and deletion preconditions use UID to avoid adopting or deleting the wrong lifetime. Evidence that records only the name can therefore misattribute a child or a destructive action.

## 2. How should a controller retry a resource-version conflict?

It should re-read the latest object, recompute the desired change against that state, and submit a new update. Replaying the old payload with a new resourceVersion can overwrite the concurrent actor. The retry unit is the reconciliation decision, and the decisive evidence is the latest object plus the fields each workflow is authorized to own.

## 3. Why should status include observedGeneration?

A condition can survive while spec changes. Without observedGeneration, `Available=True` might describe the previous desired image or replica count. Tying the condition to the processed generation lets readers distinguish current convergence from stale status. The controller should update it only after evaluating that generation.

## 4. What is wrong with writing a new timestamp on every reconcile?

It turns an idempotent observation into continuous object mutation. The status update triggers another watch event, causes another reconcile, and obscures when the condition actually changed. Last transition time should change only when condition status changes; messages and reasons should also be stable enough for automation.

## 5. When is forcing a server-side apply conflict justified?

Only when the operator intentionally transfers field ownership and understands the displaced manager. A release controller may force a field it exclusively governs, but a human should not force replicas if an autoscaler owns them. The evidence must name both managers, the field set, the authority decision, and the expected behavior of the displaced workflow.

## 6. How do owner references differ from “created by” annotations?

Owner references are API-recognized lifecycle relationships used by garbage collection and controller adoption. An annotation is inert metadata unless a controller interprets it. A child can be created by one process but controlled by another object; the controlling owner should reflect desired-state ownership, not merely historical creation.

## 7. Why can a finalizer deadlock deletion?

The API will not remove the object while finalizers remain. If the responsible controller is absent, unauthorized, non-idempotent, or waiting on an impossible external action, deletion remains pending. A safe design has bounded, retryable cleanup, observable conditions, and a documented break-glass path. Removing the finalizer blindly may leak external resources or authority.

## 8. Should AtlasWorkload finalizers delete its Deployment children?

Normally no. Kubernetes owner references and garbage collection already express child lifecycle. A custom finalizer should exist only for an obligation not represented by normal object ownership, such as releasing external authority. Duplicating built-in garbage collection increases deadlock and race risk.

## 9. Why are labels more dangerous to change than descriptive annotations?

Labels participate in selectors used by controllers, Services, policies, scheduling, and tooling. A changed selector can orphan Pods or route traffic to the wrong set. Annotations are not selected by built-in mechanisms unless a controller deliberately interprets them. Both need governance, but label changes can alter control behavior immediately.

## 10. What does deleting with UID preconditions protect against?

It prevents a client that read an old object from deleting a newly recreated object with the same name. The API performs the destructive action only if the current UID matches. This is especially important in automation where a name can be rapidly reused after controller recovery or release rollback.

## 11. Why should users not update status through the main object payload?

Spec and status have different owners and often different authorization. A user replacing the full object could erase controller observations; a controller updating status could overwrite desired state. The status subresource isolates these workflows and reduces conflict. The object’s API design should make the boundary explicit.

## 12. What evidence is required before manually removing a finalizer?

Preserve the object, finalizer owner, deletion timestamp, controller logs, external resource state, authorization failure, retry history, and the consequence of abandoning cleanup. Record who authorized the break-glass action and the residual resource or data risk. Manual removal is a policy decision, not a generic kubectl trick.
