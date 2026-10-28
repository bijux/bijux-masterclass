"""A bounded GraphQL document parser used by dependency-light course proofs.

The parser understands the operation, field, alias, argument, fragment, inline
fragment, and directive shapes exercised by the released Course 9 operations.
It is intentionally not described as a standards-complete GraphQL parser; the
optional framework proof uses a production GraphQL implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import ValidationError


PUNCTUATORS = set("!$&():=@[]{|}")


@dataclass(frozen=True)
class FieldNode:
    name: str
    alias: str | None = None
    selections: tuple["Selection", ...] = ()
    arguments: tuple[str, ...] = ()


@dataclass(frozen=True)
class FragmentSpread:
    name: str


@dataclass(frozen=True)
class InlineFragment:
    type_condition: str | None
    selections: tuple["Selection", ...]


Selection = FieldNode | FragmentSpread | InlineFragment


@dataclass(frozen=True)
class FragmentDefinition:
    name: str
    type_condition: str
    selections: tuple[Selection, ...]


@dataclass(frozen=True)
class OperationDefinition:
    operation_type: str
    name: str | None
    selections: tuple[Selection, ...]


@dataclass(frozen=True)
class Document:
    operations: tuple[OperationDefinition, ...]
    fragments: dict[str, FragmentDefinition] = field(default_factory=dict)


def tokenize(source: str) -> list[str]:
    """Tokenize the bounded document grammar used by this course."""

    tokens: list[str] = []
    index = 0

    while index < len(source):
        character = source[index]

        if character in " \t\r\n,":
            index += 1
            continue

        if character == "#":
            while index < len(source) and source[index] not in "\r\n":
                index += 1
            continue

        if source.startswith("...", index):
            tokens.append("...")
            index += 3
            continue

        if character in PUNCTUATORS:
            tokens.append(character)
            index += 1
            continue

        if character == '"':
            start = index
            index += 1
            escaped = False
            terminated = False

            while index < len(source):
                current = source[index]
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == '"':
                    index += 1
                    terminated = True
                    break
                index += 1

            if not terminated:
                raise ValidationError("unterminated string")
            tokens.append(source[start:index])
            continue

        if character.isalpha() or character == "_":
            start = index
            index += 1
            while index < len(source):
                current = source[index]
                if not (current.isalnum() or current == "_"):
                    break
                index += 1
            tokens.append(source[start:index])
            continue

        if character.isdigit() or character == "-":
            start = index
            index += 1
            while index < len(source):
                current = source[index]
                if not (current.isdigit() or current in ".eE+-"):
                    break
                index += 1
            tokens.append(source[start:index])
            continue

        raise ValidationError(
            f"unexpected GraphQL token at character {index}"
        )

    return tokens


class Parser:
    """Recursive-descent parser for the course's bounded document grammar."""

    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.index = 0

    def peek(self, value: str | None = None) -> bool:
        if self.index >= len(self.tokens):
            return False
        return value is None or self.tokens[self.index] == value

    def take(self, value: str | None = None) -> str:
        if self.index >= len(self.tokens):
            raise ValidationError("unexpected end of document")

        token = self.tokens[self.index]
        if value is not None and token != value:
            raise ValidationError(
                f"expected {value!r}, got {token!r}"
            )
        self.index += 1
        return token

    def skip_balanced(self, opening: str, closing: str) -> None:
        self.take(opening)
        depth = 1
        while depth:
            token = self.take()
            if token == opening:
                depth += 1
            elif token == closing:
                depth -= 1

    def skip_directives(self) -> None:
        while self.peek("@"):
            self.take("@")
            self.take()
            if self.peek("("):
                self.skip_balanced("(", ")")

    def selection_set(self) -> tuple[Selection, ...]:
        self.take("{")
        selections: list[Selection] = []

        while not self.peek("}"):
            if self.peek("..."):
                self.take("...")
                if self.peek("on"):
                    self.take("on")
                    type_condition = self.take()
                    self.skip_directives()
                    selections.append(
                        InlineFragment(
                            type_condition=type_condition,
                            selections=self.selection_set(),
                        )
                    )
                else:
                    name = self.take()
                    self.skip_directives()
                    selections.append(FragmentSpread(name=name))
                continue

            first = self.take()
            alias: str | None = None
            name = first

            if self.peek(":"):
                self.take(":")
                alias = first
                name = self.take()

            arguments: list[str] = []
            if self.peek("("):
                start = self.index
                self.skip_balanced("(", ")")
                arguments = self.tokens[start:self.index]

            self.skip_directives()
            nested = self.selection_set() if self.peek("{") else ()
            selections.append(
                FieldNode(
                    name=name,
                    alias=alias,
                    selections=nested,
                    arguments=tuple(arguments),
                )
            )

        self.take("}")
        return tuple(selections)

    def parse(self) -> Document:
        operations: list[OperationDefinition] = []
        fragments: dict[str, FragmentDefinition] = {}

        while self.peek():
            if self.peek("fragment"):
                self.take("fragment")
                name = self.take()
                self.take("on")
                type_condition = self.take()
                self.skip_directives()

                if name in fragments:
                    raise ValidationError("duplicate fragment")
                fragments[name] = FragmentDefinition(
                    name=name,
                    type_condition=type_condition,
                    selections=self.selection_set(),
                )
                continue

            if self.peek("{"):
                operations.append(
                    OperationDefinition(
                        operation_type="query",
                        name=None,
                        selections=self.selection_set(),
                    )
                )
                continue

            operation_type = self.take()
            if operation_type not in {
                "query",
                "mutation",
                "subscription",
            }:
                raise ValidationError("unknown operation type")

            if self.peek("{") or self.peek("(") or self.peek("@"):
                name = None
            else:
                name = self.take()

            if self.peek("("):
                self.skip_balanced("(", ")")
            self.skip_directives()

            operations.append(
                OperationDefinition(
                    operation_type=operation_type,
                    name=name,
                    selections=self.selection_set(),
                )
            )

        if not operations:
            raise ValidationError("document contains no operation")

        return Document(
            operations=tuple(operations),
            fragments=fragments,
        )


def parse_document(source: str) -> Document:
    """Parse one dependency-light course operation document."""

    return Parser(source).parse()
