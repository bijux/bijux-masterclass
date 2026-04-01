# Python Metaprogramming I

---

## Module 0 – Overview and Introduction

This module is the entry point for the course. It has two roles:

1. **Course map** – a high-level outline of all modules and cores.
2. **Conceptual introduction** – scope, audience, and what “metaprogramming” means in this context.

Use this file as the top-level index; individual modules are self-contained and can be read linearly or selectively.

---

## Course Map (Modules and Cores)

### Module 1 – Everything Is an Object
1. Functions as Objects  
2. Classes as Objects  
3. Modules as Objects  
4. Instances as Objects  
5. Capstone: `__code__`-based Source Recovery Heuristic

### Module 2 – Basic Introspection: Looking Without Breaking
6. `dir()`, `vars()`, `__dict__` – What Is Visible and What Is Hidden  
7. `getattr` / `setattr` / `delattr` / `hasattr` – Dynamic Access Done Right  
8. `type()`, `isinstance()`, `issubclass()` – When to Use Which (and Performance Notes)  
9. `callable()` and the `__call__` Protocol (Preview)  
10. Capstone: Universal `debug_print(self)` Mixin – Safe Recursion for Slots and Properties

### Module 3 – The inspect Module: Python’s Built-in Endoscope
11. `inspect.signature()`, `inspect.Parameter`, and Runtime Argument Introspection  
12. `inspect.getsource()`, `inspect.getfile()`, `inspect.getmodule()` – Provenance Tracking  
13. `inspect.getmembers()` with Predicates – Selective Member Enumeration  
14. `inspect.stack()` and Frame Introspection – Debugging and Diagnostics Only  
15. Capstone: Safe, Signature-Guided `__repr__` (`ReprMixin`)

### Module 4 – Decorators I: Function Transformation Basics
16. Nested Functions → Functions That Return Functions  
17. `@decorator` Syntax Is Just `func = decorator(func)`  
18. First Real Decorators: `@timer`, `@once`, `@deprecated`  
19. `functools.wraps` and Writing Your Own Identity-Preserving Wrapper  
20. Capstone: `@cache` – Didactic Memoization from Scratch

### Module 5 – Decorators II: Real-World and Typing-Aware
21. Decorator Factories (Parameterized Decorators)  
22. `@retry`, `@timeout`, `@rate_limited` – Patterns from `httpx`, Celery, etc.  
23. Preserving and Using Annotations at Runtime (`typing.get_type_hints` inside Decorators)  
24. How `@lru_cache` Is Really Implemented Under the Hood  
25. Capstone: `@validated` – Partial Runtime Type Contract Checker

### Module 6 – Class Decorators, `@property`, and the Typing Bridge
26. Class Decorators – Transformation Post-Construction  
27. `@dataclass` Dissected – What It Actually Generates  
28. `@property` / `@<name>.setter` / `@<name>.deleter` – The Friendly Face of Descriptors  
29. Runtime Type Hints as a Declarative Aid for Attribute Management  
30. Capstone: `@frozen` – Surface Immutability and Hashability

### Module 7 – The Descriptor Protocol: The True Engine (Part I)
31. Full Protocol: `__get__`, `__set__`, `__delete__`, `__set_name__`  
32. Data vs Non-Data Descriptors – The Precedence Rule That Makes Everything Work  
33. How Functions Become Bound Methods (The Hidden Descriptor)  
34. First Reusable Descriptors: `String()`, `Positive()`, `Email()`, etc.  
35. Capstone: `Quantity` – Didactic Unit-Aware Length Descriptor

### Module 8 – The Descriptor Protocol: The True Engine (Part II – Framework-Grade)
36. Lazy / Computed / Cached Descriptors with Invalidation  
37. External-Storage Descriptors  
38. Descriptor Composition and Meta-Descriptors  
39. Runtime Validation and Coercion Using Type Hints  
40. Capstone: Mini-Relational Demo – Educational ORM Only

### Module 9 – Metaclasses: When Everything Else Is Not Enough
41. `type(name, bases, dict)` – Dynamic Class Creation  
42. `class X(metaclass=MyMeta)` – Syntax and Execution Timing  
43. `__new__` vs `__init__` in Metaclasses  
44. `__prepare__` – Custom Namespace Mapping  
45. Capstone: `PluginMeta` – Automatic Plugin Registry

### Module 10 – Professional Responsibility and the Outer Darkness
46. Dynamic Code Execution – `eval` / `exec` / `compile`, Code Objects, Safe Patterns, and Restricted Namespaces  
47. `ABCMeta`, `Protocol`, `__subclasshook__` – Structural Typing and Virtual Base Classes  
48. Metaprogramming Responsibly – Preserving Stack Traces, Performance Costs, Debugger Transparency, Avoiding Global State, and When Monkey-Patching Is Justified  
49. Import Hooks, `sys.meta_path`, AST Transformation – When Libraries Actually Use Them (e.g. `coverage.py`, `macropy`, Hy)  
50. Capstone: Full Plugin Architecture Comparison (Decorator vs Metaclass vs Import Hook)

---

## Introduction – *Python Metaprogramming I: Runtime Mechanisms*

**Metaprogramming** is the practice of writing code that manipulates or generates other code at runtime. In Python this takes the form of runtime introspection, dynamic transformation, and extension of the language’s own objects and execution model—distinct from compile-time macro systems in languages such as C or Rust.

This course is a systematic, first-principles exploration of Python’s runtime object model and the metaprogramming facilities built on top of it, organised into **ten modules** with roughly fifty focused **cores**. Each core isolates a single concept, provides a precise definition, examines its code-level consequences and common failure modes, and concludes with exercises. Every module ends with a capstone that synthesises the preceding cores into a coherent, runnable example, followed by a concise glossary.

The progression is deliberate:

- Modules 1–3 establish the object model and safe introspection.
- Modules 4–5 cover function and class decorators.
- Modules 6–8 develop the descriptor protocol from basic properties to framework-grade patterns.
- Module 9 introduces metaclasses.
- Module 10 closes with professional responsibility: performance, debuggability, security, and when *not* to use these tools.

Throughout **Volume I** we deliberately restrict ourselves to mainstream CPython 3.10+ in a single-interpreter, synchronous context. This is by design: concurrency, async/await integration, multiprocessing, deep static-typing tooling (mypy plugins, `dataclass_transform`), and distributed systems are postponed to **Volume II**.

By the end of this first volume you will be able to read, understand, and confidently write production-grade decorators, descriptors, and (when truly necessary) metaclasses. Equally important, you will know when these tools are overkill and a simpler solution is preferable.

**Volume II** will extend this foundation with async-aware metaprogramming, advanced static typing integration, performance profiling of meta-heavy code, testing strategies, security considerations for plugin systems, AST-based code generation, and in-depth case studies of major frameworks. **Volume I** gives you the precise runtime vocabulary; **Volume II** shows how to architect large, type-safe, performant systems on top of it.
