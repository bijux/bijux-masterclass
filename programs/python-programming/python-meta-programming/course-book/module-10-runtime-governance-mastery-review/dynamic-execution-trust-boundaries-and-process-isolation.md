# Dynamic Execution, Trust Boundaries, and Process Isolation

Module 10 begins with the mechanism that most often tempts developers into making claims
the runtime cannot honestly support.

That mechanism is dynamic execution.

## The sentence to keep

`compile`, `eval`, and `exec` are only defensible when the input is trusted and the review
story stays honest about process boundaries, observability, and fallback designs.

Everything else on this page hangs from that sentence.

## The only honest security line

If the input is untrusted, do not run it with `eval` or `exec` inside the current Python
process.

Not with restricted globals.
Not with a tiny builtins dictionary.
Not with a partial AST filter that claims to be a sandbox.

If the trust boundary is real, the protection boundary must be real too. That means
separate-process isolation, not wishful thinking about a namespace mapping.

## What the runtime primitives actually do

The core pieces are mechanical:

- `compile(source_or_ast, filename, mode)` produces a code object
- `eval(code, globals, locals)` evaluates an expression and returns a value
- `exec(code, globals, locals)` executes statements and returns `None`

Those are powerful but limited facts. They do not imply safety.

## `globals` and `locals` are execution context, not a sandbox

Reviewers often see a narrowed `globals` mapping and assume the risk has been handled.

That assumption is wrong.

The mappings control names. They do not create a process boundary, a syscall boundary, or
an honest promise against hostile input.

One detail matters enough to remember precisely:

- if `globals` does not define `__builtins__`, Python may insert it for you

That means controlled execution should always set `__builtins__` explicitly even for
trusted internal inputs.

## A narrow, honest internal use

This is the sort of case the runtime can support honestly: a trusted internal expression
language evaluated against a controlled name set.

```python
co = compile("x * 2 + 1", "<trusted-expression>", "eval")

globals_ = {"__builtins__": {}, "x": 10}
result = eval(co, globals_, {})

print(result)  # 21
```

This example is not "safe for attackers." It is simply narrow and explicit for trusted
configuration that the team owns.

## Compiling statements is a different kind of power

`exec` changes state rather than returning a single expression value.

That wider surface means the review cost is higher immediately:

```python
co = compile("x = 42\ny = x * 2", "<trusted-statements>", "exec")

globals_ = {"__builtins__": {}}
locals_ = {}

exec(co, globals_, locals_)

print(locals_["y"])  # 84
```

Once statements enter the design, reviewers should ask why ordinary Python code or a
declarative config format did not stay the clearer owner.

## AST filtering is about narrowing syntax, not creating safety

Parsing expressions into an AST and rejecting forbidden nodes can be useful for a tiny
internal DSL. It does not convert untrusted code execution into a secure design.

```python
import ast

ALLOWED = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Constant,
    ast.Name,
    ast.Load,
)


def evaluate_expression(expr: str, names: dict[str, object]) -> object:
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED):
            raise ValueError(f"forbidden syntax: {type(node).__name__}")
    return eval(compile(tree, "<expression-dsl>", "eval"), {"__builtins__": {}, **names}, {})
```

That pattern can prevent accidental complexity. It does not justify the sentence "we
safely execute user code in-process."

## Strong alternatives are usually less magical

Before approving dynamic execution, compare it against lower-power options:

- data plus normal code, such as JSON or TOML driving explicit dispatch
- callables selected from a trusted registry
- a small parser or interpreter for the exact operations you support
- out-of-process execution when the input boundary is genuinely hostile

The right alternative is often less impressive and more maintainable. That is a benefit,
not a loss.

## What process isolation changes

Separate-process execution does not make arbitrary code morally harmless. It does change
the ownership story:

- the current process no longer shares memory and globals with the code being evaluated
- operating-system controls can restrict filesystem, network, and process access
- timeouts, cleanup, and logging become explicit operational concerns

That is the first honest place where "sandboxing" language can start to mean something.

## Review rules for dynamic execution

When `compile`, `eval`, or `exec` appear in code review, ask these questions first:

- where does the input come from, and who controls it?
- why can this not be represented as data plus explicit program logic?
- is `__builtins__` set explicitly?
- is compilation happening once or inside a hot path?
- what evidence shows forbidden syntax and failure cases are tested?
- if the input is not fully trusted, where is the separate-process boundary?

If those answers feel vague, the design is not ready.

## What this page is really teaching

The lesson is not "never use dynamic execution under any circumstance."

The lesson is:

- dynamic execution is a review and operations problem before it is a Python trick
- namespace control is weaker than many designs pretend
- real trust boundaries require real isolation boundaries

That judgment matters more than memorizing the function signatures.

## What to practice from this page

Try these before moving on:

1. Rewrite one `eval`-style idea as explicit data plus normal code.
2. Build one tiny trusted-expression evaluator and name exactly what it does not promise.
3. Write one sentence explaining why restricted globals are not a sandbox.

If those feel ordinary, the next step is interface governance: which runtime contracts can
be named honestly with ABCs, protocols, and `__subclasshook__`.

## Continue through Module 10

- Previous: [Overview](index.md)
- Next: [Interface Contracts with ABCs, Protocols, and `__subclasshook__`](interface-contracts-with-abcs-protocols-and-subclasshook.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
