# Skill Authoring Rules

## Required Structure

```
skill-name/
+-- SKILL.md
+-- references/
```

`references/` is optional, but use it for detailed rubrics and examples.

## Frontmatter

Use portable YAML:

```yaml
---
name: skill-name
description: What the skill does. Use when ...
---
```

Rules:

- `name` must match the folder name.
- Use lowercase letters, digits, and hyphens.
- Keep `description` direct and trigger-rich.
- Do not rely on fields that only one client understands.

## Body

Good `SKILL.md` bodies:

- Start with the core job.
- Give a short workflow.
- Point to reference files only when needed.
- Define expected output shape.
- State evidence and safety rules.

Avoid:

- Project history.
- Long background essays.
- Installation guides.
- Client-specific assumptions.
- Duplicating the same instructions in several files.

## Validation Checklist

- Folder name equals frontmatter `name`.
- `description` says both what the skill does and when to use it.
- The skill can run from its files alone.
- Detailed data is in references, not the main file.
- The skill does not ask the agent to invent citations, metrics, or facts.
- Private student data is never added to shared resources.
