---
module_id: OOP-003
program: Programming Languages: Object-Oriented Programming
level: 1
module_number: 3
title: Messages, Methods, and Dynamic Dispatch
status: complete
last_verified: 2026-08-29
---

# Messages, Methods, and Dynamic Dispatch

## One-Page Review

### Governing question

When an operation is requested from an object, how does the language determine which implementation runs while preserving the receiver, arguments, effects, and failure behavior?

### Essential definitions

- A **message** or **request** describes an operation sought from a receiver; it normally contains a selector and arguments.
- A **receiver** is the object relative to which an object operation is requested.
- A **selector** identifies the requested operation within a lookup protocol. It may be a name alone or participate in a richer signature.
- A **method** is an implementation associated with an object, class, prototype, generic function, or other dispatch owner.
- **Lookup** finds candidate methods according to the language's object model.
- **Binding** supplies the receiver as `self`, `this`, or an equivalent implicit parameter to the selected method.
- **Dispatch** selects the implementation for an invocation. In **single dispatch**, the receiver's runtime classification is the principal dynamic input.
- **Dynamic dispatch** delays at least part of implementation selection until runtime; **static dispatch** determines the target without runtime receiver-based selection.
- **Overloading** chooses among same-named declarations, commonly from static argument types; **overriding** supplies descendant behavior for an inherited operation. They are different mechanisms.

### Central model, mechanism, or theorem

For a single-dispatch model with dynamic class $class_H(o)$, selector $m$, arguments $\bar v$, and deterministic class linearization $L(C)$, define

$$
lookup(C,m)=\text{the first }D\in L(C)\text{ whose method table defines }m.
$$

Then an ordinary send reduces as

$$
send(o,m,\bar v,H)\Downarrow
apply(method(lookup(class_H(o),m),m),o,\bar v,H).
$$

Selection starts from the receiver's runtime class, while the selected body receives the original receiver. A language may elaborate, restrict, or replace this model, but must define selection and failure precisely.

### Critical invariants

- Evaluate the receiver and arguments according to the language's specified order and number of times.
- Begin ordinary dynamic lookup from the receiver's runtime classification, not merely the variable's declared type.
- Make lookup deterministic, or reject ambiguity explicitly.
- Preserve the original receiver during inherited-method execution.
- Treat `super` as a language-defined continuation or qualified lookup, not as a different parent object.
- Keep overload resolution, access checking, lookup, and dynamic target selection conceptually distinct even if an implementation combines them.
- Preserve specified results, effects, exceptions, and synchronization when optimizing dispatch.
- Define missing-message behavior; never silently choose an unrelated method.

### Common failures

Frequent errors include equating a message with a method body, assuming every member call is dynamic, confusing overloading with overriding, starting lookup from a declared type, believing `super` changes `self`, ignoring multiple-inheritance ambiguity, detaching a method and losing its receiver, trusting reflective selector strings from untrusted input, and treating a vtable sketch as the language semantics.

### Compact example

Suppose `Savings` inherits `Account`. `Account` defines `kind` and `fee`; `Savings` overrides only `fee`. Sending `kind` to a `Savings` object searches `Savings` then `Account`, selects `Account.kind`, and executes it with the original savings object as receiver. Sending `fee` selects `Savings.fee`. A `super` send written in `Savings` begins after `Savings` but still binds the savings object as receiver.

### Connections

[OOP-001](001-objects-as-state-behavior-and-identity.md) supplies receiver identity and state; [OOP-002](002-classes-as-construction-and-classification-mechanisms.md) separates declared type from runtime class. Later chapters develop [interfaces, overriding, overloading, and multiple dispatch](../ROADMAP.md), while the runtime block treats virtual dispatch and inline caches. Formal evaluation connects to [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md).

## Governing Question

What exactly happens between writing an object operation such as `account.fee()` and entering one particular method body?

The surface expression looks like an ordinary function call with a prefix. Its meaning is richer. The receiver must be evaluated. The requested operation must be identified. Static rules may determine whether the request is admissible and may narrow a candidate set. Runtime rules may inspect the receiver's class or delegation chain. A method is selected, the receiver is bound for the body, arguments are transferred, and the result or failure returns under the language's control-flow rules. Each step matters when inheritance, dynamic loading, reflection, proxies, or optimization enters the system.

Object-oriented reasoning begins with a useful separation: the caller states **what operation it requests**, while the receiver's object model participates in determining **which implementation answers**. Smalltalk makes this separation especially visible through message syntax. Java, C++, C#, Python, ECMAScript, Ruby, and other languages expose different combinations of member access, function values, static resolution, dynamic lookup, and receiver binding. The vocabulary is portable only when those differences remain explicit.

## Why This Matters

Dynamic dispatch supports open-ended variation. A client can ask an `Account` to calculate a fee without a central type switch over every account variant. A later class can provide a compatible implementation while the caller retains the same request. This is one basis of subtype polymorphism and separately compiled extension.

The same indirection creates risk. A call site may execute code not visible at that site. A subclass can violate assumptions. A constructor can invoke behavior before descendant state is ready. A proxy can reinterpret a request as network activity. A mock can make tests pass with behavior no production receiver supplies. A reflective dispatcher can expose every public method as an accidental remote API. Performance can vary with the runtime receiver population.

Production review therefore needs a semantic trace, not the slogan “polymorphism happens.” For a call, reviewers should be able to state the evaluated receiver, the statically admitted operation, the runtime lookup start, the applicable lookup order, the selected implementation, the bound receiver, the expected effects and failures, and the evidence supporting those claims.

This chapter establishes that trace. It introduces overriding, multiple inheritance, and dispatch optimization only enough to locate their roles. Their complete type rules, behavioral obligations, and machine mechanisms belong to later OOP modules.

## Prerequisites and Retrieval

You should understand functions, parameters, scopes, objects, classes, inheritance at an introductory level, and the difference between a variable's declared type and an object's runtime class. Retrieve these facts:

1. An object has identity even when another object has equal state.
2. A reference designates a receiver; evaluating a receiver expression can itself have effects.
3. A class can classify objects and associate shared behavior without copying method code into every instance.
4. A descendant object can have a declared supertype at a call site and a more specific runtime class.
5. A deterministic relation needs either a unique answer or a specified ambiguity failure.
6. A language specification defines observable behavior; a common implementation technique does not replace that definition.

## Learning Objectives

After completing this module, you should be able to:

- distinguish messages, selectors, methods, member access, invocation, lookup, binding, and dispatch;
- trace a single-dispatch invocation from source expression to selected method body;
- distinguish static overload resolution from runtime overriding and dynamic binding;
- calculate method lookup over a simple inheritance or prototype chain;
- explain why an inherited method receives the original descendant object as `self` or `this`;
- explain `super` without inventing a separate parent instance;
- identify dispatch rules that vary across Java, C++, Python, ECMAScript, Smalltalk, and generic-function systems;
- state failure and security policies for absent or reflectively selected operations;
- test dispatch by observable behavior without coupling a test to an assumed table layout;
- review a dispatch claim with explicit assumptions, traces, boundary cases, and evidence.

## Core Exposition

A **message** is a request description, not executable method code. In a simple model it is a pair $(m,\bar v)$ of selector and argument tuple. The **receiver** is separate. A **method** is one possible implementation that can answer the selector for some receiver population. Several classes may define methods for the same selector; one method can answer many receiver objects. Saying “call the message” or “send the method” collapses distinctions needed to explain lookup.

Terminology varies. Smalltalk uniformly describes sending messages to objects. Java specifies method invocation expressions with compile-time and runtime stages. Python normally evaluates an attribute, whose descriptor behavior can create a bound method, and then calls the resulting callable. ECMAScript evaluates property references and calls function objects with a `this` value; a property containing a function is not intrinsically a permanently bound method. CLOS invokes a generic function and can select methods from multiple argument classes. The shared abstraction is a request-to-implementation selection process, not identical syntax or identical semantics.

A **selector** may be just a method name in a pedagogical model. Real languages can incorporate arity, parameter types, labels, generic instantiation, receiver qualifiers, visibility, and other information at different stages. In Java, overload resolution is largely a compile-time process that chooses a method signature from static information; runtime lookup can then choose an overriding implementation for that signature. If `Printer.print(Object)` and `Printer.print(String)` are overloads, a variable statically typed `Object` can cause `print(Object)` to be chosen even when its runtime value is a string. That is not a failure of dynamic dispatch: the overload was selected earlier.

For ordinary **single dispatch**, the receiver is the distinguished dynamic argument. Let `Account a = new Savings()` and suppose the admitted operation is virtual `fee()`. The static type `Account` establishes whether the expression is well-formed and what contract the caller may rely on. At runtime, `Savings` participates in selecting the overriding body. Static admission and dynamic selection answer different questions.

Not every apparent member call is dynamically dispatched. Java static methods are selected without receiver-based overriding, and private methods have special non-overriding rules. C++ non-virtual member calls depend on static type, while virtual calls use the final overrider under specified conditions. A qualified C++ call can suppress virtual dispatch. Languages may devirtualize a dynamic call only when the optimized program preserves the specified behavior. Review the language rule and the declaration, not punctuation alone.

Lookup in a single-inheritance class model starts at the runtime class and follows parent links until it finds a matching method. If `Savings` does not define `kind`, but `Account` does, `Savings` objects inherit that answer. Crucially, the chosen `Account.kind` executes with the savings object as receiver. It can invoke another dynamically dispatched operation on `self`, which may return to a `Savings` override. This phenomenon, sometimes called open recursion, is powerful and can expose partially initialized or unexpectedly specialized behavior.

A `super` expression does not change the receiver into a parent object. It changes where a particular lookup begins or which inherited declaration is selected, according to language rules. The body still observes the original object as `self` or `this`. In a simple chain, a `super.fee()` inside `Savings` starts after `Savings`, selects `Account.fee`, and binds the savings object. In multiple inheritance, “the parent” may be meaningless; Python's `super` follows the class's method resolution order, and cooperative methods must forward consistently.

Prototype delegation uses related but distinct machinery. In ordinary ECMAScript property lookup, if an own property is absent, `[[Get]]` follows the prototype chain while retaining the original receiver for accessor calls. After a function-valued property is obtained through a reference such as `obj.f`, calling that reference supplies `obj` as `this`. Extracting the value and later calling it as a plain function can lose that receiver relationship. Therefore “methods live in classes” is not a universal account of receiver binding.

Python adds another separation. Evaluating `obj.method` performs attribute lookup. A function stored on the class is a descriptor; its `__get__` behavior produces a bound method carrying `obj`. Calling that bound method supplies the instance. An instance attribute, data descriptor, custom `__getattribute__`, metaclass, or special-method lookup can change parts of the story. The useful review question is whether a value is being looked up, bound, and called, rather than whether syntax looks familiar.

Multiple inheritance requires a lookup policy. A naive depth-first search can make behavior depend unintuitively on graph shape and can visit shared ancestors poorly. Some languages reject ambiguous final overriders; others compute a linearization. The policy must produce a deterministic sequence or an explicit error. This chapter uses an already supplied linearization $L(C)$; constructing and evaluating competing policies belongs to OOP-024.

Single dispatch is not universal. CLOS generic functions determine applicable methods from specializers on multiple required arguments and can combine methods. Julia also centers multiple dispatch. A visitor can emulate a limited two-stage choice by one virtual call followed by another, but that is not the same semantic mechanism as a generic function whose applicability rule jointly considers several arguments. OOP-015 and OOP-057 treat those systems directly.

Missing lookup is part of the contract. Statically checked languages often reject absent members before execution, although dynamic loading or binary linkage can still fail. Dynamic languages may raise an exception, return `undefined` for a missing property before a later call fails, or invoke a missing-method hook. Such hooks can implement proxies and forwarding, but they also turn spelling mistakes into delayed failures and enlarge the observable protocol. A fallback must not silently convert an unrecognized security-sensitive request into arbitrary execution.

Reflective dispatch such as `getattr(target, name)(*args)` or indexing `target[name]` should not be treated as a harmless replacement for a conditional. If `name` crosses a trust boundary, the receiver's full reflective surface can become callable. An allowlist should map external operation identifiers to narrow capabilities, validate arguments, and define authorization, time, resource, failure, and audit policies. Visibility keywords alone do not establish remote authority.

Dispatch optimization belongs below the semantic contract. A runtime may use linear search, hash tables, virtual function tables, interface tables, inline caches, devirtualization, speculative inlining, or whole-program specialization. The safe criterion is observational equivalence under the language's permitted mutations, loading, reflection, concurrency, exceptions, and memory model. A successful benchmark or disassembly inspection establishes a property of one build and workload, not a universal dispatch guarantee.

The following executable model makes the core stages visible. It is a deliberately tiny class-table interpreter, not an implementation of Python's object protocol or a claim about physical method-table layout.

<!-- bijux-verify: {"id":"single-dispatch-lookup","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selector=kind path=Savings->Account owner=Account result=account:100\nselector=fee path=Savings owner=Savings result=1\nsuper_selector=fee path=Account owner=Account result=5\nmissing_selector=close path=Savings->Account->Object outcome=message-not-understood\n","stderr":""}} -->
```python
def object_kind(receiver):
    return "object"


def account_kind(receiver):
    return "account:" + str(receiver["balance"])


def account_fee(receiver):
    return 5


def savings_fee(receiver):
    return 1


classes = {
    "Object": {"parent": None, "methods": {"kind": object_kind}},
    "Account": {
        "parent": "Object",
        "methods": {"kind": account_kind, "fee": account_fee},
    },
    "Savings": {"parent": "Account", "methods": {"fee": savings_fee}},
}


def lookup(start_class, selector):
    path = []
    current = start_class
    while current is not None:
        path.append(current)
        methods = classes[current]["methods"]
        if selector in methods:
            return current, methods[selector], path
        current = classes[current]["parent"]
    return None, None, path


def send(receiver, selector, start_class=None):
    start = receiver["class"] if start_class is None else start_class
    owner, body, path = lookup(start, selector)
    if body is None:
        return owner, None, path
    return owner, body(receiver), path


account = {"class": "Savings", "balance": 100}

owner, result, path = send(account, "kind")
print("selector=kind path=" + "->".join(path) + " owner=" + owner + " result=" + result)

owner, result, path = send(account, "fee")
print("selector=fee path=" + "->".join(path) + " owner=" + owner + " result=" + str(result))

owner, result, path = send(account, "fee", classes["Savings"]["parent"])
print("super_selector=fee path=" + "->".join(path) + " owner=" + owner + " result=" + str(result))

owner, result, path = send(account, "close")
print("missing_selector=close path=" + "->".join(path) + " outcome=message-not-understood")
```

The output verifies four claims about this model: inherited lookup retains the receiver, an override wins at the first matching class, a super-style lookup starts later without changing the receiver, and absence is explicit. It does not verify Python, Java, C++, ECMAScript, Smalltalk, CLOS, real object layout, access control, concurrency, optimization, behavioral substitutability, or production safety.

## Definitions and Notation

Let:

- $I$ be receiver identities and $H$ the heap;
- $C$ be runtime classes or lookup owners;
- $M$ be selectors;
- $V^*$ be argument tuples;
- $class_H:I\rightharpoonup C$ give a live receiver's runtime class;
- $parent:C\rightharpoonup C$ describe simple inheritance;
- $methods:C\to(M\rightharpoonup Body)$ be method tables;
- $L(C)=[C,C_1,\ldots,C_n]$ be the language-defined lookup linearization;
- $apply(b,o,\bar v,H)\Downarrow(r,H',t)$ execute body $b$ with receiver $o$, producing result $r$, heap $H'$, and observable trace $t$.

For a selector $m$, define

$$
owner(C,m)=\min_{L(C)}\{D\mid m\in dom(methods(D))\},
$$

where the minimum is the first class in lookup order. If the set is empty, lookup yields $miss$. If the language does not define a total order for competing candidates, it must apply an ambiguity rule before invocation.

Ordinary send is

$$
\frac{class_H(o)=C\quad owner(C,m)=D\quad methods(D)(m)=b\quad
apply(b,o,\bar v,H)\Downarrow(r,H',t)}
{send(o,m,\bar v,H)\Downarrow(r,H',t)}.
$$

The occurrence of $o$ in `apply` is the receiver-preservation property. Method ownership $D$ and receiver class $C$ can differ.

For a method lexically defined in $C$, a simple super lookup uses a specified successor $next(L(class_H(o)),C)$ as its starting position. This notation is intentionally conditional: languages define `super` differently, and some qualified calls suppress ordinary virtual dispatch rather than perform cooperative continuation.

A static judgment $\Gamma\vdash e.m(\bar a):T$ means a source call is admitted and assigned result type $T$. It does not alone identify the runtime body. Conversely, runtime lookup does not excuse a call rejected by the language's static rules. A complete account can therefore contain both a static selection $sig_\Gamma(e,m,\bar a)$ and a runtime selection $body(class_H(o),sig)$.

## Mechanisms, Invariants, or Proof Structure

**Unique first match.** If $L(C)$ is finite, contains no repeated lookup position relevant to selection, and the rule chooses its first definition of $m$, then `owner(C,m)` is unique. Determinism follows from the total order. If inheritance supplies incomparable candidates without a linearization or dominance rule, uniqueness is not established and the language must reject or disambiguate.

**Receiver preservation.** Suppose $owner(Savings,kind)=Account$. The send rule passes $o$, not a newly allocated `Account`, to `Account.kind`. Therefore object identity, descendant fields, and later virtual self-sends remain those of $o$. Changing the lookup owner does not change the receiver.

**Most-specific shadowing in a chain.** If `Savings` defines `fee`, it precedes `Account` in $L(Savings)$. The first-match rule selects `Savings.fee`. Removing that definition makes `Account` the first owner. This is a structural lookup result only; behavioral compatibility of the override needs a separate contract argument.

**Static/dynamic separation.** Let the declared type of $x$ be `Account` and $class_H(x)=Savings$. Static checking can select admitted signature `Account.fee()`. Runtime selection can choose `Savings.fee`. No contradiction exists because signature admission and body selection occur at distinct semantic stages.

**Evaluation preservation.** Replacing a dynamic send with a direct call is sound only if it preserves receiver evaluation, argument evaluation order, target choice, receiver binding, returned values, exceptions, effects, synchronization, and all permitted reflective observations. Proving one likely receiver class is insufficient if another class can reach the call site.

**Super continuation.** In the simple model, a super send from the lexical owner `Savings` begins at its successor `Account`. It still passes $o$ into `apply`. Therefore `super` changes lookup position, not receiver identity. In a cooperative multiple-inheritance system, hard-coding one named parent can violate the linearization and cause an ancestor to run twice or not at all.

**Failure totality.** Extend lookup's result to `Hit(D,b)` or `Miss(path)`. Every finite search then produces evidence of either selection or absence. A language-level hook may transform `Miss` into another computation, but that hook is an explicit semantic branch, not a successful lookup of the missing selector.

**Mutation and caches.** If classes, prototypes, method dictionaries, or loaders can change, a cached selection is valid only while its guarding assumptions hold. The runtime must invalidate, version, or guard cached results. This is a runtime invariant; source-level callers should not infer cache stability from repeated behavior.

## Alternatives and Trade-Offs

**Static versus dynamic dispatch.** Static calls expose a fixed target to analysis and optimization. Dynamic calls support receiver-specific extension and substitution. A compiler may optimize a dynamic call to a direct call under a proof or guard; the source abstraction remains dynamic when alternative receiver classes are semantically allowed.

**Single versus multiple dispatch.** Single dispatch makes one receiver central and fits member-call notation. Multiple dispatch selects from several runtime arguments and can express symmetric operations without visitor scaffolding. It needs applicability, specificity, ambiguity, and method-combination rules that are more global than one class chain.

**Inheritance versus delegation.** Class inheritance obtains behavior through a class relation. Prototype or explicit-object delegation forwards lookup or requests through objects. Delegation permits per-object composition but can make authority and mutation of the chain more dynamic. Both require a termination and ambiguity policy.

**Open versus sealed method sets.** Open hierarchies and method dictionaries allow later extension, plugins, and runtime adaptation. Sealed or final declarations improve exhaustive reasoning, compatibility control, and optimization. Sealing is an API decision, not merely a performance hint.

**Missing-message hook versus immediate failure.** A hook supports forwarding, proxies, dynamic adapters, and domain-specific protocols. Immediate failure catches spelling and protocol errors closer to their source. If a hook exists, make its accepted namespace, authorization, observability, and failure semantics narrow.

**Direct method references versus bound callables.** A bound method packages a receiver for later invocation and is convenient for callbacks. An unbound function plus explicit receiver makes data flow visible. Languages differ on whether extraction preserves binding; APIs should not rely on intuition transferred from another language.

**Behavioral test versus implementation inspection.** A test can construct two receiver variants and verify the selected outcomes. Table or assembly inspection can explain cost in one runtime. The former supports semantic compatibility; the latter supports an implementation-specific performance claim. Neither alone proves behavioral substitutability for all states.

## Failure Modes and Misconceptions

1. **“A message is a method.”** The request and the implementation are different entities; one selector can reach different methods.
2. **“Dot syntax means dynamic dispatch.”** Static members, non-virtual functions, qualified calls, property reads, and function-valued fields can use similar syntax.
3. **“The declared type selects the final body.”** It often governs admissibility while the receiver's runtime class selects an override.
4. **“Overloading is runtime polymorphism.”** Many languages resolve overloads from compile-time types before dynamic overriding occurs.
5. **“An inherited method runs on a parent object.”** It runs with the original receiver unless the language explicitly creates or designates another object.
6. **“`super` means my direct parent.”** Multiple inheritance and language-specific rules make it a lookup construct, often relative to lexical context and a linearization.
7. **“A same-named descendant method must override.”** Signature, visibility, staticness, receiver qualifiers, and language rules can instead produce hiding or an unrelated overload.
8. **“Missing lookup always raises the same error.”** Static rejection, linkage error, exception, `undefined`, and missing-method hooks differ.
9. **“Extracting `obj.method` always preserves `obj`.”** Python bound methods often do; a detached ECMAScript function value ordinarily does not preserve the base reference by itself.
10. **“A vtable is dynamic dispatch.”** It is one possible implementation technique and cannot define languages with prototype mutation, generic functions, proxies, or different virtual rules.
11. **“Reflection respects business authorization.”** Discoverability or public visibility does not grant an external caller authority.
12. **“A passing mock proves production dispatch.”** A mock can omit loader, proxy, lifecycle, default-method, or fallback behavior that controls the real target.

## Worked Examples

### Example 1

**Question:** A variable is declared `Account` but refers to a `Savings` object. Both classes define virtual `fee()`. Which facts belong to compile time and runtime?

**Reasoning:** Static analysis admits `fee()` through the `Account` interface and establishes the result contract visible to the caller. Runtime lookup begins from `Savings` and selects its override. The caller may rely only on the admitted contract, not on undocumented details of the savings implementation.

**Conclusion:** Static type admits the request; runtime class can select the answering body.

### Example 2

**Question:** Why does inherited `Account.kind()` still see fields of a `Savings` receiver?

**Reasoning:** Lookup owner and receiver are different roles. Lookup finds the body in `Account`, but invocation binds the original savings identity as `this` or `self`. The body can read state available through its valid account view and can issue further virtual requests to that same object.

**Conclusion:** Inheritance reuses a body without substituting a parent instance for the receiver.

### Example 3

**Question:** What does the executable class-table model establish?

**Reasoning:** Its deterministic output records the lookup path and selected owner for inherited, overridden, super-style, and missing selectors. Inspection also shows the same receiver dictionary enters every selected function. The model omits static types, access control, descriptors, multiple inheritance, mutation during lookup, and concurrency.

**Conclusion:** Executable evidence supports the stated miniature semantics only, not universal language behavior.

### Example 4

**Question:** Java has overloads `show(Object)` and `show(String)`. A variable statically typed `Object` contains a string. Which overload is chosen?

**Reasoning:** Java overload resolution uses compile-time rules and the expression's static type to select an applicable signature, so `show(Object)` is selected. If that selected instance method is overridden in the receiver's runtime class, runtime lookup can then choose the overriding body for `show(Object)`; it does not restart overload resolution with runtime argument classes.

**Conclusion:** Overload selection and override dispatch are sequentially distinct.

### Example 5

**Question:** Why can `const f = obj.render; f()` behave differently from `obj.render()` in ECMAScript?

**Reasoning:** The member call retains a reference whose base supplies the `this` argument. The assignment extracts the property value; the later plain call lacks that original base relationship. A lexical arrow, explicit `bind`, wrapper, or explicit receiver parameter changes the outcome under its own rules.

**Conclusion:** Function lookup and receiver binding are separate operations in ECMAScript.

### Example 6

**Question:** What does `super().save()` mean in a cooperative Python hierarchy?

**Reasoning:** It creates a proxy that continues lookup after a specified class in the receiver's method resolution order. It does not necessarily name the class's textual first base as a permanent target. Each cooperative implementation must accept compatible arguments and call onward consistently if the chain is to compose.

**Conclusion:** Cooperative `super` follows a linearized protocol, not a parent-object metaphor.

### Example 7

**Question:** A C++ base pointer designates a derived object. When does `p->f()` use the derived implementation?

**Reasoning:** If the relevant member function is virtual, final-overrider rules use the most-derived object under the standard's conditions. If it is non-virtual, selection depends on the static type. Qualified calls and construction or destruction contexts have further specified rules.

**Conclusion:** Dynamic receiver type matters only where the language grants virtual dispatch.

### Example 8

**Question:** Two parent branches define the same operation and neither dominates the other. May a runtime pick whichever it encounters first?

**Reasoning:** Only if the language specifies that exact deterministic order. C++ can reject a class with more than one final overrider; a linearizing language computes a method resolution order; another language may require qualification. An implementation's incidental traversal order is not a valid semantic policy.

**Conclusion:** Ambiguity requires a language-defined resolution or rejection rule.

### Example 9

**Question:** Is mapping an HTTP field `action` directly to `getattr(service, action)()` a safe dispatcher?

**Reasoning:** The mapping may expose diagnostic, mutation, lifecycle, inherited, or magic methods beyond the intended remote protocol. A safe boundary maps a small external operation enum to explicit handlers, authenticates and authorizes each capability, validates arguments, limits resources, and records results and failures.

**Conclusion:** Reflective reachability is not authorization.

### Example 10

**Question:** A payment framework claims any plugin overriding `authorize` is production-compatible. What review evidence is required before accepting that claim?

**Reasoning:** A language-semantics reviewer must verify signature admission, runtime selection, receiver binding, default/super behavior, and loader boundaries. A domain reviewer must verify amount, currency, idempotency, authorization, and failure obligations. A security reviewer must examine plugin authority and untrusted inputs. A reliability reviewer must test timeouts, retries, partial failure, and observability. Representative executable integration tests should exercise at least two implementations plus missing, duplicate, and failing plugins. Only named human review records may establish external expert approval; this chapter records none.

**Conclusion:** Correct lookup is necessary but insufficient for a production plugin contract.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) formalizes evaluation, environments, operational semantics, and observable equivalence.
- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) contrasts receiver-directed methods with first-class functions, closures, and algebraic decomposition.
- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) uses polymorphic behavior to allocate domain responsibilities without central type tests.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) treats plugins, dependency direction, and runtime binding at component scale.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authority, validation, and threat models for reflective dispatch and plugin execution.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) explains lowering, call-site representation, devirtualization, and generated machine code.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) distinguishes behavioral conformance tests from implementation-specific dispatch inspection.

## References

1. Adele Goldberg and David Robson, [*Smalltalk-80: The Language and Its Implementation*](https://rmod-files.lille.inria.fr/FreeBooks/BlueBook/Bluebook.pdf), Addison-Wesley, 1983. Foundational account of objects, messages, classes, and methods.
2. Alan C. Kay, [“The Early History of Smalltalk”](https://doi.org/10.1145/155360.155364), *History of Programming Languages II*, 1993. Historical design rationale for messaging and object-oriented computation.
3. Oracle, [*The Java Language Specification*, §15.12 Method Invocation Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.12), Java SE 25. Normative compile-time and runtime method-invocation stages.
4. ISO C++ working draft, [§11.7.3 Virtual Functions](https://timsong-cpp.github.io/cppwp/class.virtual). Normative-style specification of overriding, final overriders, and dynamic binding in C++.
5. Python Software Foundation, [Python 3 Data Model: Descriptors and Invocation](https://docs.python.org/3/reference/datamodel.html#invoking-descriptors). Official description of attribute lookup, bound methods, descriptors, and `super` binding.
6. Python Software Foundation, [The Python 2.3 Method Resolution Order](https://www.python.org/download/releases/2.3/mro/). Authoritative explanation of C3 linearization and cooperative lookup; the algorithm remains relevant to current Python MRO.
7. Ecma International, [ECMAScript Language Specification: Ordinary Object Internal Methods](https://tc39.es/ecma262/multipage/ordinary-and-exotic-objects-behaviours.html#sec-ordinary-object-internal-methods-and-internal-slots). Normative `[[Get]]`, prototype, receiver, and ordinary-object rules.
8. ANSI Common Lisp, [HyperSpec §7.6 Generic Functions and Methods](https://www.lispworks.com/documentation/HyperSpec/Body/07_f.htm). Standard method applicability, selection, inheritance, and combination model.
9. Kim Barrett et al., [“A Monotonic Superclass Linearization for Dylan”](https://doi.org/10.1145/236337.236343), OOPSLA 1996. Primary presentation of the C3 superclass-linearization problem and algorithm.
10. Martín Abadi and Luca Cardelli, [*A Theory of Objects*](https://doi.org/10.1007/978-1-4419-8598-9), Springer, 1996. Formal object calculi for method invocation, self, update, and object types.

## Exercises

### Exercise 1

Consider classes `Object <- Vehicle <- Bicycle`. `Object` defines `describe`; `Vehicle` defines `move` and overrides `describe`; `Bicycle` overrides `move`. For a receiver whose runtime class is `Bicycle`, give the lookup path, selected owner, and bound receiver for `describe` and `move`.

### Exercise 2

Explain why a Java-style call can use static argument types to select an overload and still use the receiver's runtime class to select an overriding implementation. Give a counterexample to the claim that runtime argument classes always choose the overload.

### Exercise 3

A language has multiple inheritance but defines neither a linearization nor an ambiguity error. Construct a diamond-shaped hierarchy in which two branches define `audit`. Explain why “search until one is found” is not a sufficient deterministic specification.

### Exercise 4

Design a safe external command dispatcher for `start`, `status`, and `stop` without reflectively exposing every method of its receiver. State the allowlist, receiver-binding rule, argument checks, authorization point, missing-command behavior, and one audit event.

### Exercise 5

Prepare a verification plan for a dynamically loaded tax-calculation plugin interface. Cover static or load-time admission, runtime dispatch, behavioral obligations, `super` or default behavior, missing and duplicate plugins, failure containment, performance evidence, security review, and the boundary between automated evidence and named human review.

## Answers to the Exercises

### Answer 1

For `describe`, lookup follows `Bicycle -> Vehicle`, selects `Vehicle.describe`, and binds the original `Bicycle` receiver. It does not allocate or substitute a `Vehicle`. For `move`, lookup finds `Bicycle.move` immediately and binds the same bicycle receiver. If either body sends another virtual message to `self`, lookup begins again from the receiver's runtime class under ordinary rules.

### Answer 2

The stages answer different questions. Suppose `Renderer` overloads `render(Object)` and `render(String)`, while `FastRenderer` overrides `render(Object)`. With `Renderer r = new FastRenderer(); Object x = "text"; r.render(x);`, static overload resolution selects signature `render(Object)` because `x` is declared `Object`. Runtime lookup then selects `FastRenderer.render(Object)` for receiver `r`. The runtime class `String` of `x` does not retroactively select `render(String)`.

### Answer 3

Let `Root` have children `Logged` and `Compliant`; both define `audit`; `Service` inherits both. For a `Service` receiver, a left-first traversal selects `Logged.audit`, while a right-first traversal selects `Compliant.audit`. Source-file order, hash-map iteration, loader order, or compiler traversal could change the result unless the language elevates one to a rule. A sufficient specification must compute a stable linearization, define dominance, require qualification, combine methods, or reject the ambiguity.

### Answer 4

Define an immutable map `{start: start_handler, status: status_handler, stop: stop_handler}` whose values are narrow bound capabilities or functions receiving one explicit service object. Parse the external identifier as an enum; reject all other strings before lookup. Validate each command's typed arguments, authenticate the principal, authorize that principal for the selected operation, impose resource and timeout limits, and return a structured `unknown-command` error for misses. Record principal, operation, receiver identity, request correlation ID, outcome, and duration without secrets. No external name is evaluated as an attribute.

### Answer 5

Automated checks should verify plugin metadata and version compatibility, load each representative implementation in isolation, assert that the correct receiver implementation answers each interface operation, exercise default behavior intentionally, and reject missing or duplicate registrations deterministically. Contract suites should cover tax rounding, jurisdiction, currency, effective dates, idempotency, boundary amounts, malformed inputs, timeouts, exceptions, and resource limits. Security tests should attempt unapproved loading and authority escalation. Benchmarks must record toolchain, plugin set, workload distribution, warmup, and uncertainty; they do not prove universal latency.

A named language/runtime reviewer must assess loader and dispatch assumptions; a named tax-domain reviewer must approve semantic rules and legal scope; a named security reviewer must assess plugin authority and provenance; and a named reliability reviewer must assess failure containment and observability. Each record should identify version, evidence, limitations, date, and decision. Automated success cannot be relabeled as legal, security, or production approval, and this answer claims no external review.
