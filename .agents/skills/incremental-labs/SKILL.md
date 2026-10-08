---
name: incremental-labs
description: Maintain labs and add new examples to labs.
---

# Incremental labs

Use this skill when writing, completing, or extending course labs.

## Establish the starting point

Read the repository's `AGENTS.md`, the target lab, and the preceding labs in
one language. Assume the English and Russian versions have identical content;
there is no need to read both to understand the lessons. Identify what students
already know and which syntax has only been mentioned without explanation.
Use the first few labs as style references.

List the requested concepts and explicit exclusions before drafting. Keep new
topics outside that scope as suggestions to the user; add them only after the
user approves. Resolve ordinary example-writing choices yourself.

## Build a sequence of puzzles

Introduce one new concept per example. Follow it with a small variation that
lets students test their understanding. Later examples may combine concepts
already introduced, like a puzzle game using familiar pieces in a new way.

Keep the code small and use familiar names, types, and syntax. Change as little
as possible between related examples so the cause of the different behavior is
visible. Avoid introducing unrelated syntax to demonstrate the target concept.

Use fresh variables in separate blocks for separate cases instead of reassigning
result variables. Keep an object across cases only when its continuing state is
part of the puzzle. Save intentionally ignored return values in local variables
marked `[[maybe_unused]]` so the decision to leave them unused is explicit.

Ask students to predict whether the program compiles, what it prints, or which
objects change. Hide the answer in an HTML `<details>` block with a localized
`<summary>Answer</summary>`. Explain the rule and trace the concrete values or
objects that justify the answer. Intentional compilation errors are valid
puzzles; explain the offending expression and a minimal correction.

Put secondary syntax details in a collapsed note, not a separate example,
when the user says they should not be the focus. Distinguish related concepts
precisely, such as copying an object versus copying its address, or a read-only
access path versus an object that cannot change.

Place integrations in the earliest lab where their prerequisites are taught.
If C arrays precede a concept and `std::array` follows it, use C arrays in the
concept lab and add the `std::array` integrations to the later array lab.
Cross-link those lessons when useful. Do not teach template definitions just
to show an already-used library type's template argument.

## Keep the course consistent

Wrap authored Markdown prose at 120 characters. Prefer line breaks before new
sentences; when a sentence needs multiple lines, avoid short trailing lines or
single words on a line. Preserve code and generated website backlinks.

Update both `en/` and `ru/` versions with the same examples, code, order, and
meaning, unless the user explicitly requests one language. Translate naturally
and preserve the existing frontmatter and website backlinks.

Verify runnable examples with a standard C++ compiler and compare their output
with the answers. Use strict standard conformance when teaching compile-time
array sizes: compiler extensions must not make invalid examples appear valid.
Check that intentionally invalid examples fail for the stated reason.
