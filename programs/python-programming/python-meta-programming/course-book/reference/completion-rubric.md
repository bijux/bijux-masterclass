# Completion Rubric

Use this page when you need to judge whether metaprogramming understanding has become
real design judgment rather than fascination with stronger runtime tools.

## Completion standard

You should be able to do all of the following:

- name the lowest-power runtime tool that honestly solves the current problem
- explain what extra blast radius a stronger mechanism would introduce
- preserve runtime evidence such as names, signatures, or manifest shape when a wrapper claims transparency
- distinguish descriptor, decorator, class-customization, and metaclass pressure clearly
- review a runtime mechanism by readability, inspectability, and governance instead of novelty

## Course outcomes

| Area | Completion signal |
| --- | --- |
| runtime observation | you can inspect runtime shape without changing it unnecessarily |
| transparent wrappers | you can explain what metadata survived and why that matters |
| descriptor design | you can name which invariant belongs to attribute access itself |
| metaclass escalation | you can say which lower-power tool almost worked and why it failed |
| governance | you can justify one runtime mechanism choice in a way a reviewer could approve without a live walkthrough |

## Capstone evidence

Use these as the minimum capstone evidence:

1. `make PROGRAM=python-programming/python-meta-programming manifest`
2. `make PROGRAM=python-programming/python-meta-programming registry`
3. `make PROGRAM=python-programming/python-meta-programming capstone-walkthrough`

Running them is not enough if you cannot explain which runtime boundary each route made visible.

## Reviewer questions

- What lower-power tool almost solved this problem?
- What runtime fact still stays inspectable from the public surface?
- Which mechanism owns class-creation-time invariants here?
- Which proof route would fail first if this mechanism stopped being worth its cost?
