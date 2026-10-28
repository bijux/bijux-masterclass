---
module_id: SARCH-019
program: Software Engineering: Software Architecture
level: 1
module_number: 19
title: Usability and Accessibility as System Qualities
status: complete
last_verified: 2026-09-06
---

# Usability and Accessibility as System Qualities

## One-Page Review

### Governing question

How should architecture enable people with diverse capabilities, technologies, languages, environments, and constraints to complete intended work effectively, efficiently, safely, and with appropriate control?

### Essential definitions

- **usability** is the extent to which specified users achieve specified goals effectively, efficiently, and satisfactorily in a specified context of use.
- **accessibility** is the extent to which products, systems, services, environments, and facilities can be used by people with the widest range of characteristics and capabilities to achieve goals in context.
- A **context of use** includes users, goals, tasks, equipment, physical and social environment, and temporal conditions.
- **assistive technology** supports interaction through capabilities such as screen reading, magnification, alternative input, voice control, captions, or switch access.
- **semantic structure** identifies roles, names, states, relationships, and reading or interaction order in machine-perceivable form.
- **focus** identifies the current interaction target for sequential or programmatic input.
- **error recovery** enables a person to detect, understand, correct, undo, or safely resume after a problem.
- **reasonable accommodation** and legal conformance are jurisdictional determinations; technical standards and automated checks do not decide them alone.
- **inclusive design** considers human diversity and situational constraints throughout discovery, design, implementation, operation, and evaluation.

### Central model, mechanism, or theorem

For user group $g$, task $k$, and context $c$, define an outcome predicate $Success(u,k,c)$ from correct completion, safety, time, error, and assistance criteria. Observed task success is

$$
S_{gkc}=\frac{|\{u\in U_g:Success(u,k,c)\}|}{|U_g|},\qquad |U_g|>0.
$$

Architecture supports equitable task outcomes by preserving semantic information, multiple input and output paths, recoverable state, adaptable timing, accessible identity and support, localization, predictable operation, and end-to-end evidence. Aggregate success cannot replace subgroup and context analysis.

### Critical invariants

- define users, goals, tasks, contexts, hazards, and acceptable outcomes without treating one persona as universal;
- preserve roles, names, states, relationships, order, errors, and live changes across presentation and assistive interfaces;
- support keyboard and alternative input without focus traps or pointer-only actions;
- provide equivalent information without relying only on color, sound, motion, position, or memory;
- let people review, correct, undo, save, extend, pause, or resume where consequence and policy permit;
- preserve entered data and authoritative transaction state through validation, timeout, failure, and authentication;
- localize language, direction, units, dates, names, addresses, and content without inventing semantics;
- make authentication, consent, help, support, recovery, and emergency paths accessible;
- combine automated checks with assistive-technology, user, operational, and qualified domain evaluation;
- bind claims to tasks, populations, contexts, standards versions, platforms, and evidence.

### Common failures

Common failures include treating accessibility as colors and labels added after implementation; replacing native semantics with generic clickable containers; pointer-only drag or hover actions; focus moved invisibly or trapped; color-only status; timeouts that erase work; errors announced visually but not programmatically; CAPTCHAs without an accessible path; identity recovery requiring the inaccessible factor; localization by string substitution alone; accessible pages around an inaccessible payment or support dependency; overlay products claimed to guarantee conformance; and aggregate completion rates that hide excluded groups.

### Compact example

A modal dialog appears visually but keyboard focus remains behind it. A keyboard user activates hidden controls, and a screen-reader user receives no dialog context. Use a semantic dialog with an accessible name, move focus to an appropriate element, constrain sequential navigation while open, support documented dismissal, preserve state, and restore focus to the invoking control. Test keyboard order, assistive announcement, zoom, errors, and nested interruptions.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) supplies user and external-system boundaries; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-012](012-performance-and-latency-tactics.md) supplies interaction timing; [SARCH-014](014-security-and-privacy-tactics.md) supplies accessible protection and consent; [SARCH-017](017-interoperability-tactics.md) supplies localization and semantic exchange; and [SARCH-018](018-observability-and-operability-tactics.md) supplies privacy-safe task and failure evidence.

## Governing Question

A visually polished screen can be unusable with a keyboard, screen reader, zoom, low bandwidth, cognitive load, tremor, bright sunlight, or a different language. An accessible front end can still lead to an inaccessible identity provider, timeout, document, payment, support channel, or manual process. What system structure preserves usable outcomes across the whole task?

The governing question is how user diversity and context become architectural drivers for semantics, workflow state, timing, interaction modes, content, identity, dependencies, recovery, support, and evidence. Accessibility is not a property inferred from one automated score or one interface snapshot.

## Why This Matters

People interact with workflows, not components. Registration may cross identity, forms, documents, payment, notification, and support. If any required step excludes a user, the capability is inaccessible even if every team reports local conformance.

Architecture determines whether state can be saved, errors are attributable to fields, timeouts can be extended, content has semantic structure, messages announce changes, documents have alternatives, and another channel preserves the same authority. These decisions are expensive to retrofit after contracts and data models harden.

Usability and accessibility interact with safety, security, privacy, performance, and cost. Removing authentication can simplify interaction but expose users. Automatic timeout can protect privacy but erase work. Voice input can help some users and harm privacy in shared spaces. Trade-offs require explicit contexts and alternatives.

## Prerequisites and Retrieval

Retrieve user, goal, task, workflow, context of use, effectiveness, efficiency, error, recovery, assistive technology, semantic role, accessible name, state, focus, keyboard, contrast, caption, transcript, localization, authentication, consent, timeout, support, and evidence limitation.

From earlier modules, retrieve stakeholders, quality scenarios, ASRs, trade-offs, performance budgets, security threats, privacy purposes, semantic contracts, observability, and operational controls. You should be able to distinguish technical conformance from task success and a visual arrangement from programmatic structure.

## Learning Objectives

After completing this module, you should be able to:

1. frame usability and accessibility scenarios by users, tasks, contexts, and outcomes;
2. identify end-to-end architectural barriers across dependencies and channels;
3. preserve semantic structure, focus, status, errors, and interaction order;
4. support multiple input, output, timing, and navigation modes;
5. design recoverable workflows with save, review, correction, undo, and resume;
6. integrate accessibility with authentication, privacy, safety, and support;
7. localize language, direction, units, time, identity, and content correctly;
8. measure task outcomes without hiding subgroups or collecting excessive data;
9. combine automation, assistive-technology checks, user evaluation, and domain review;
10. state conformance and usability evidence without guarantees or overgeneralization.

## Core Exposition

**Model contexts, not an average user.** Identify goals, tasks, prior knowledge, language, literacy, disability, age-related change, device, input and output technology, network, environment, interruption, assistance, and consequence. Avoid inferring individual capability from a demographic label.

Permanent, temporary, and situational constraints can require the same design capability. Captions assist Deaf users, a person in noise, and someone learning a language. Large targets assist motor impairment and one-handed use. Design reusable capabilities rather than exceptional “special” flows where possible.

**Trace complete tasks.** Map every required step, system, document, message, timeout, external provider, manual approval, and support handoff from intent to confirmed outcome. Identify authority and state at each step. Include cancellation, correction, failure, recovery, and dispute—not only the happy path.

A separate accessible channel is equivalent only if it provides comparable outcome, timeliness, cost, privacy, dignity, and authority. Requiring a phone call during narrow hours is not automatically equivalent to an independent online workflow.

**Use native and programmatic semantics.** Prefer platform-native controls whose role, name, state, value, keyboard behavior, and accessibility mapping are defined. Custom controls must reproduce every relevant semantic and interaction behavior across supported technologies.

Structure headings, regions, lists, tables, labels, instructions, errors, and relationships programmatically. Visual proximity alone does not communicate association to a nonvisual interface. Keep source and focus order aligned with meaningful task order; CSS placement should not create a contradictory sequence.

**Manage focus deliberately.** Every interactive element needs a reachable, visible focus state. Opening dialogs, routing between views, inserting errors, deleting focused elements, and restoring prior context require focus rules. Avoid positive tab-index ordering that becomes a second fragile navigation model.

Keyboard support includes activation, dismissal, selection, adjustment, drag alternatives, and escape from composite widgets. Test without a pointer and at high zoom, not only by inspecting attributes.

**Expose state and change.** Users need to perceive selected, expanded, invalid, busy, pending, completed, and unavailable states. Programmatic state must agree with visual state. Announce important dynamic changes through appropriate mechanisms without flooding assistive output.

Do not rely on color, position, shape, sound, or animation alone. Provide text or semantic alternatives. Permit reduction of nonessential motion and prevent flashing or sensory patterns that create harm.

**Design perceptible content.** Provide text alternatives for meaningful nontext content; captions and appropriate transcripts for media; adaptable layout and reflow; scalable text; sufficient contrast; and content that remains meaningful when presentation changes. Decorative content should not add noise.

For relative luminances $L_1\ge L_2$, contrast ratio is $(L_1+0.05)/(L_2+0.05)$ under the WCAG definition. Black and white yield $(1+0.05)/(0+0.05)=21:1$. A ratio meeting one threshold does not prove readability for every person or context.

**Support understanding.** Use clear language, consistent naming, predictable navigation, visible consequences, and progressive disclosure. Define domain terms and preserve help near the task. Do not make memory the only storage: show requirements, selected values, progress, and review state.

Error messages should identify what failed, why when safe, where, what remains preserved, and how to correct it. Associate errors programmatically with fields and provide a summary for long forms. Do not clear valid data after one invalid field.

**Support input and recovery.** Accept multiple input modalities and tolerate reasonable variation without guessing dangerous meaning. Provide large enough targets and alternatives to path-based gestures or drag. Avoid requiring precise timing or simultaneous actions when an equivalent sequential path exists.

For consequential submissions, allow review, confirmation, correction, undo, cancellation, or compensation as the domain permits. Preserve stable operation identity so retry after timeout does not duplicate payment, booking, or consent.

**Govern time.** Warn before session or task expiry, state consequences, allow extension where policy permits, save progress, and restore context after reauthentication. Some real-time events cannot be extended; provide advance notice, alternative access, and recovery rather than silently failing.

Security timeouts need context. A banking session on a shared device differs from a long benefits application. Separate credential validity from draft preservation so privacy protection does not require destroying legitimate work.

**Design accessible authentication.** Support password managers and paste where credentials are used; offer accessible multifactor and recovery options; avoid cognitive-function tests as the only path; and make errors, timeouts, device enrollment, and support perceivable and operable.

Security questions based on personal history can be inaccessible, insecure, or culturally inappropriate. Recovery is an authority path and needs equal or stronger protection plus usable alternatives. Evaluate fraud and abuse without punishing assistive or shared-device patterns.

**Localize structure and meaning.** Externalize language while preserving context, grammar, plural forms, direction, length, fonts, names, addresses, sorting, units, numbers, currency, dates, calendars, and time zones. Avoid concatenating sentence fragments that cannot reorder grammatically.

Layout must tolerate expansion and bidirectional text. User-visible dates need locale and zone; authoritative instants need unambiguous storage and exchange. Translation quality and cultural meaning require qualified review, not machine substitution alone.

**Preserve accessibility across content and dependencies.** Documents, emails, charts, maps, support tools, identity providers, payment widgets, consent managers, and error pages are part of the task. Contract for accessibility, test real integrations, provide fallback, monitor regressions, and assign remediation authority.

Third-party conformance statements have scope and date. They do not prove the integrated task or future versions. Prevent suppliers from becoming unowned exceptions.

**Build responsive and resilient interaction.** Long operations need progress, cancellation where safe, background continuation, and clear final status. Offline or intermittent workflows need explicit freshness, conflict, pending, synchronization, and recovery semantics.

Performance affects accessibility: delays increase cognitive load, timeouts, repeated input, and assistive-technology confusion. Preserve semantic skeleton and focus across progressive loading. Do not reorder content unexpectedly when late data arrives.

**Instrument outcomes carefully.** Measure task success, time, errors, abandonment, retries, help, recovery, and support by declared context. Segment where needed to detect exclusion, but minimize data, obtain appropriate authority, protect sensitive disability and behavior information, and avoid turning analytics into surveillance.

An aggregate can hide harm. If 95 of 100 users in one group and 5 of 10 in another succeed, overall success is 100/110≈90.9%, while the smaller group's success is 50%. Report both and investigate context rather than attributing outcome to people.

**Use layered evaluation.** Automated checks efficiently find some missing names, invalid relationships, contrast, and structure. Static checks cannot determine meaningful alt text, logical task flow, cognitive load, or whether a screen reader interaction is understandable.

Add keyboard inspection, zoom and reflow, multiple assistive technologies and platform combinations, expert review, usability evaluation with relevant participants, content and language review, security and privacy review, and operational exercises. Test failure, timeout, recovery, notification, support, and external dependencies.

The W3C's [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is a current web content accessibility Recommendation, and [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/) defines accessibility semantics for web content. Conformance to a technical standard has a defined scope; it does not establish that every user can complete every task, that legal obligations are met, or that custom ARIA is preferable to native HTML.

**Govern continuously.** Put accessibility acceptance criteria in product, design, engineering, content, procurement, testing, release, monitoring, and incident work. Maintain accessible component patterns, but test their composition and content. Assign owners for defects and external dependencies.

Treat inaccessible production paths as quality incidents according to consequence. Preserve user reports and assistive context safely, remediate, verify with affected workflows, and update architectural decisions. Accessibility can regress when content, data, dependencies, or operations change without code.

## Definitions and Notation

For group $g$, task $k$, context $c$, and observed participant set $U_g$, define

$$
S_{gkc}=\frac{|\{u\in U_g:Success(u,k,c)\}|}{|U_g|},\qquad |U_g|>0.
$$

`Success` must encode correct outcome, safety, assistance policy, time, error, and completion semantics. It is not inferred merely from reaching a page or emitting a request. Report population, recruitment, environment, task, sample size, and uncertainty; do not interpret an empty group as 100% success.

For relative luminance $L_1\ge L_2$ in $[0,1]$, define contrast ratio

$$
C=\frac{L_1+0.05}{L_2+0.05},
$$

so $1\le C\le21$. Apply the standard's color-space conversion and thresholds rather than estimating luminance from raw color codes.

Let end-to-end task path $P$ contain required steps. If any required step has no usable path for a context, local conformance elsewhere cannot establish path success. This is a conjunction over required outcomes, not a multiplication of unsupported probabilities.

## Mechanisms, Invariants, or Proof Structure

Use this usability and accessibility mechanism.

1. **Frame contexts:** identify users, goals, tasks, capabilities, technologies, environments, hazards, and outcomes.
2. **Trace paths:** map every required interface, dependency, document, message, manual action, failure, and support route.
3. **Preserve semantics:** expose role, name, state, relationship, order, errors, progress, and dynamic change.
4. **Diversify interaction:** support keyboard, alternatives to pointer and gesture, adaptable presentation, captions, text, and reduced motion.
5. **Preserve control:** support review, correction, undo, save, extension, cancellation, resume, and stable side-effect identity.
6. **Integrate qualities:** align accessibility with security, privacy, performance, availability, safety, and localization.
7. **Constrain dependencies:** contract, test, monitor, and provide governed alternatives for required external steps.
8. **Measure outcomes:** evaluate success, time, errors, recovery, and support without hiding subgroups or overcollecting data.
9. **Verify layers:** combine automation, keyboard, zoom, assistive technology, expert, user, content, and operational evaluation.
10. **Govern change:** include accessibility in procurement, release, monitoring, incidents, remediation, and decision records.

The governing invariants are contextual task outcomes, programmatic semantics, multiple operable paths, perceivable state, recoverable work, accessible protection and support, meaningful localization, end-to-end dependency coverage, privacy-safe evidence, and bounded conformance claims.

## Alternatives and Trade-Offs

**Native control or custom widget.** Native controls provide mature semantics and platform behavior but may constrain visual design. Custom widgets permit specialized interaction but inherit keyboard, focus, state, accessibility, compatibility, and testing obligations.

**Automatic timeout or user-controlled extension.** Timeout protects unattended sensitive sessions and resources. Warning, extension, draft preservation, and reauthentication protect legitimate work. Choose by threat and task consequence.

**One adaptable path or separate alternative.** An adaptable primary path preserves parity and maintainability. A separate channel may address a genuine context but risks delay, stigma, inconsistent authority, and drift. Compare complete outcomes.

**Rich dynamic update or stable presentation.** Live updates can provide timely feedback but disrupt focus and cognitive continuity. Batch, announce, pause, or let users request updates according to task.

**Detailed analytics or data minimization.** Segmented evidence can expose exclusion but may collect sensitive capability and behavior data. Use the least data and most protective aggregation sufficient for a legitimate improvement decision.

## Failure Modes and Misconceptions

- **“Accessibility is a front-end concern.”** Identity, state, content, dependencies, support, and operations shape the task.
- **“Automated checks passed.”** Many semantic, cognitive, workflow, and assistive interactions require other evidence.
- **“ARIA makes custom controls accessible.”** Semantics alone do not supply complete behavior or usability.
- **“Keyboard means Tab works.”** Activation, focus, order, escape, and composite interaction remain.
- **“Color contrast proves readability.”** Typography, context, motion, cognition, and content also matter.
- **“The phone channel is equivalent.”** Availability, delay, privacy, cost, dignity, and authority may differ.
- **“Timeout is purely security.”** It can erase work and make the task impossible.
- **“Localization is translation.”** Direction, grammar, identity, units, dates, and cultural meaning remain.
- **“One screen-reader test covers users.”** Tools, platforms, tasks, skills, and impairments vary.
- **“Accessibility overlays guarantee conformance.”** Integrated semantics and workflows still require engineering and evaluation.
- **“Aggregate success is equitable success.”** Smaller or affected contexts can disappear in averages.
- **“Conformance guarantees legal compliance.”** Jurisdiction, scope, process, and qualified interpretation remain.

## Worked Examples

### Example 1

**Question:** A modal is visible but focus remains on the page behind it. What must change?

**Reasoning:** Use semantic dialog structure and name, move focus to an appropriate dialog element, constrain sequential navigation while open, expose state, support dismissal when allowed, preserve entered data, and restore focus to the invoker. Test keyboard, screen reader, zoom, validation, and interruptions.

**Conclusion:** Focus behavior is an architectural interaction contract, not visual polish.

### Example 2

**Question:** White text has luminance 1 and black background luminance 0. What contrast ratio follows?

**Reasoning:** $C=(1+0.05)/(0+0.05)=1.05/0.05=21:1$. This is the maximum ratio under the model. It does not prove appropriate typography, readability, content, motion, or task success.

**Conclusion:** Contrast is one precisely measurable condition within a broader outcome.

### Example 3

**Question:** A status table uses green and red dots without text. Is the state accessible?

**Reasoning:** Not to users who cannot distinguish the colors or access the visual shape. Add programmatic and visible status text, semantic association to each row, and optional icon shape. Verify forced colors, grayscale, screen reader navigation, zoom, and sorting.

**Conclusion:** Never make a sensory channel the sole carrier of meaning.

### Example 4

**Question:** A 30-minute benefits form times out after 10 minutes and deletes input. What system change is needed?

**Reasoning:** Separate sensitive session validity from draft state. Warn accessibly, permit extension where authorized, save minimal encrypted progress, reauthenticate without losing the draft, state retention, and provide an accessible recovery channel. Evaluate shared-device and privacy threats.

**Conclusion:** Security and accessibility must be composed rather than traded implicitly.

### Example 5

**Question:** Group A has 95 successes among 100 participants and group B has 5 among 10. What do the rates show?

**Reasoning:** $S_A=95\%$, $S_B=50\%$, and aggregate success is $100/110\approx90.9\%$. The aggregate looks strong while group B experiences a severe barrier. Sample uncertainty and context still limit inference.

**Conclusion:** Report relevant groups and contexts instead of hiding exclusion in totals.

### Example 6

**Question:** A validation error appears in red above a form, and valid fields are cleared. How should recovery work?

**Reasoning:** Preserve all safe valid input, mark invalid fields programmatically, associate specific instructions, move or announce focus predictably, provide an error summary, and retain entered context after reauthentication. Avoid exposing sensitive rejected values in logs or URLs.

**Conclusion:** Error handling must make correction perceivable, operable, and state preserving.

### Example 7

**Question:** A price `1,234` is displayed internationally. Is its meaning clear?

**Reasoning:** No. Separators differ by locale and currency is absent. Store exact amount and currency, format for locale, expose currency text or code, and preserve rounding and accounting meaning. Test bidirectional layout, long labels, zoom, and speech output.

**Conclusion:** Localization requires semantic data, not string replacement.

### Example 8

**Question:** A live search announces every keystroke and result count to a screen reader. Is more announcement better?

**Reasoning:** No. It can interrupt input and flood output. Debounce appropriate updates, announce meaningful status after a pause, preserve focus, let results be navigated structurally, and expose loading and errors. Test multiple input speeds and assistive technologies.

**Conclusion:** Dynamic semantics must balance timely state with cognitive and interaction continuity.

### Example 9

**Question:** Authentication requires dragging a puzzle piece. What alternative is required?

**Reasoning:** Provide a non-drag, nonvisual, non-cognitive-function-dependent method with equivalent protection, such as supported device or credential authentication plus accessible recovery. Keep pointer alternatives, focus, instructions, timeout, and error semantics. Evaluate abuse without blocking assistive behavior.

**Conclusion:** A security challenge must not make one interaction mode the only authority path.

### Example 10

**Question:** How should usability and accessibility be architected for an emergency-evacuation service?

**Reasoning:** Support visual, auditory, text, tactile, language, low-bandwidth, offline, and assisted channels; preserve location and alert provenance; expose severity, time, route, change, and cancellation; and provide accessible acknowledgment and help. Test stress, noise, darkness, mobility, cognition, device loss, network failure, and public displays. No external emergency-management, accessibility, disability-community, safety, geospatial, telecommunications, regulatory, security, human-factors, or practitioner review is claimed; named qualified authorities and affected users must validate tasks, hazards, evidence, release, and residual risk.

**Conclusion:** High-consequence accessibility requires equivalent actionable outcomes across diverse real contexts.

## Cross-Program Connections

- [Software Engineering: Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns iterative discovery, planning, stakeholder feedback, and lifecycle change.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns accessibility testing, usability evaluation, automation, and evidence methods.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns release gates, monitoring, incidents, and remediation workflows.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns identity, authentication, abuse resistance, privacy, and security verification.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects human interaction to physical systems, hazards, operators, environments, and lifecycle assurance.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns service semantics that support accessible clients, stable state, errors, and recovery.

## References

1. ISO. [ISO 9241-11:2018, Ergonomics of human-system interaction—Part 11: Usability: Definitions and concepts](https://www.iso.org/standard/63500.html), second edition, March 2018. Usability, goals, outcomes, and context of use; consulted 2026-09-06.
2. ISO. [ISO 9241-210:2019, Ergonomics of human-system interaction—Part 210: Human-centred design for interactive systems](https://www.iso.org/standard/77520.html), second edition, July 2019. Human-centered lifecycle activities; consulted 2026-09-06.
3. W3C. [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/), W3C Recommendation, 5 October 2023. Perceivable, operable, understandable, and robust web content criteria; consulted 2026-09-06.
4. W3C. [Accessible Rich Internet Applications (WAI-ARIA) 1.2](https://www.w3.org/TR/wai-aria-1.2/), W3C Recommendation, 6 June 2023. Roles, states, properties, accessibility-tree semantics, and host-language use; consulted 2026-09-06.
5. W3C Web Accessibility Initiative. [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/), current pattern and practice resource. Keyboard, focus, naming, and widget patterns; consulted 2026-09-06.
6. Jonathan Lazar, Daniel F. Goldstein, and Anne Taylor. *Ensuring Digital Accessibility through Process and Policy*. Morgan Kaufmann, 2015. Accessibility processes, policy, evaluation, procurement, and organizational governance.
7. Donald A. Norman. *The Design of Everyday Things*, revised and expanded edition. Basic Books, 2013. Affordances, signifiers, mappings, feedback, constraints, and human error.
8. Jakob Nielsen. *Usability Engineering*. Morgan Kaufmann, 1993. Usability attributes, evaluation, iterative design, and empirical methods.

## Exercises

### Exercise 1

Define an end-to-end accessibility scenario for booking a medical appointment, including dependencies, failure, and support.

### Exercise 2

Group A records 180 successes among 200 task attempts and group B records 12 among 20. Compute group and aggregate rates, then state the interpretation limits.

### Exercise 3

Diagnose a workflow with clickable generic containers, color-only errors, pointer drag, invisible focus, eight-minute timeout, cleared form state, puzzle authentication, PDF-only confirmation, and phone-only support.

### Exercise 4

Compare a native control, a custom ARIA widget, and a separate alternative channel for a complex date selection task. Address semantics, interaction, localization, maintenance, parity, privacy, and evidence.

### Exercise 5

Design usability and accessibility assurance for an unfamiliar regional emergency-food distribution system. Separate automation, assistive-technology and user evaluation, operational exercises, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

For patients using supported keyboard, screen reader, magnification, voice, touch, switch, low-bandwidth, and translated contexts, define successful discovery, provider and time selection, identity, consent, booking, confirmation, change, cancellation, and help. Include identity provider, schedule service, forms, messages, documents, payment if any, and support. Require correct authoritative appointment state, perceivable progress and errors, operable focus, saved work, bounded response, accessible reauthentication, and equivalent recovery after dependency failure.

Test representative devices, browsers, assistive technologies, zoom, text spacing, languages, direction, time zones, network loss, session expiry, duplicate submission, provider unavailability, notification failure, and support handoff. Combine automation with keyboard, assistive-technology, content, security, privacy, operational, and relevant-user evaluation. Record exact task, context, versions, outcome, assistance, and limits.

### Answer 2

$$
S_A=180/200=90\%,\qquad S_B=12/20=60\%.
$$

Aggregate success is $(180+12)/(200+20)=192/220\approx87.27\%$. The aggregate conceals a 30-percentage-point observed gap. These samples do not establish population rates without recruitment, context, task, assistance, uncertainty, and confounding analysis. Do not infer that group membership caused failure; inspect barriers and contexts, protect sensitive data, and expand evidence appropriately.

### Answer 3

Generic containers lack native role and behavior. Color-only errors hide meaning. Drag excludes non-pointer and imprecise input. Invisible focus destroys navigation context. Timeout and state clearing erase work. Puzzle authentication blocks interaction and cognitive modes. PDF-only output and phone-only support may break semantics, availability, privacy, and parity.

Use native semantic controls where possible; add visible and programmatic errors; provide keyboard and sequential alternatives; manage visible focus; warn, extend, save, and resume securely; supply accessible authentication and recovery; issue semantic responsive confirmation plus an accessible document when needed; and offer comparable accessible support routes. Trace the whole task and test failure and recovery, not each page alone.

### Answer 4

A native date control may provide platform semantics and input behavior cheaply, but behavior and localization vary and may not meet a complex domain need. A custom ARIA widget can express specialized range or availability selection but must implement naming, state, focus, keyboard, touch, speech, errors, zoom, direction, calendars, and compatibility continuously. A separate channel may support a context the primary cannot, but can impose delay, disclosure, cost, dependence, or weaker authority.

Prefer a native or simple composed control when it supports the required task. Add text-entry and structured alternatives for complex selection. Build custom behavior only with a justified requirement and sustained test matrix. Judge any separate channel by equivalent outcome, timeliness, privacy, dignity, and authority. Evaluate with automation, keyboard, assistive technologies, localization, users, failure, and support operations.

### Answer 5

Identify recipients, households, dietary and medical needs, mobility, language, literacy, identity constraints, locations, inventory, eligibility, queues, delivery, pickup, caregivers, support, and emergency authority. Minimize sensitive data; provide multiple accessible registration and notification paths; preserve draft and authoritative allocation; expose wait, change, error, and cancellation; support low bandwidth and offline sites; localize semantics; and prevent duplicate or discriminatory allocation.

Automation can check structure, names, relationships, keyboard reachability, focus, contrast candidates, schemas, localization bounds, state transitions, authorization, and evidence freshness. Assistive-technology and relevant-user evaluation must cover real tasks, stress, devices, languages, and recovery. Operational exercises should test surge, site outage, network loss, depleted inventory, identity failure, caregiver action, manual service, correction, and reconciliation.

No external humanitarian, nutrition, medical, safeguarding, accessibility, disability-community, equity, privacy, regulatory, security, logistics, human-factors, or practitioner review is claimed. Named qualified authorities and affected communities must own eligibility, accommodation, safety, equitable service, evaluation, release, and residual risk. Inaccessible required step, erased application, discriminatory queueing, ambiguous allocation, unavailable support, failed offline path, or unresolved high-severity harm blocks readiness.
