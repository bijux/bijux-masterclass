# Reference — Delivery state model

Atlas stores source, render, release, live, health, journey, and data states separately. Source identifies reviewed inputs. Render identifies produced objects. Release records promotion authority. Live state records observed Kubernetes objects. Health interprets resource status. Journey measures externally useful behavior. Data gates preserve migration and recovery constraints.

A transition may advance one population without advancing the others. A commit can exist before rendering; rendering can pass before admission; sync can complete before health; health can pass before business validation. Incident records should identify the earliest population whose expected transition did not occur.

## Extended reader notes

A useful delivery state model records distinct subjects rather than one aggregate status. **Source state** names the repository and immutable commit. **Artifact state** names every OCI or chart digest. **Render state** names the renderer, dependency subjects, input values, and canonical object-set digest. **Controller state** names the resolved source artifact, inventory, field manager, and last reconciliation result. **Live state** records current objects and managed fields. **Health state** records resource-specific conditions at an observed generation. **Journey state** records user-visible assertions. **Data state** records migration phase, writer authority, backup, restore, and fencing evidence.

Transitions can fail independently. A controller may fetch the right commit but use an unexpected plugin version. It may apply the reviewed set while a webhook mutates a security field. A Deployment can become Ready while the candidate writes data that the stable revision cannot read. Diagnose the earliest transition whose evidence contradicts the release claim.

The state model is also a responsibility map. Git owns desired declarations; it does not own business facts. Kubernetes controllers own selected object transitions; they do not own data retirement. Progressive delivery owns traffic exposure; it does not own schema rollback. Store these limits in the release dossier so that incident responders do not grant authority to whichever tool has a convenient button.
