---
description: Framework edits ship the schema and catalog together
condition: '(?i)schema_version|schema\.json'
globs: ["**/*.json", "**/*.py"]
---
CTX-CAMLHMP-2 MUST bump the framework schema version and regenerate `catalog.json` in the same commit as a framework change.
Why: the schema and the catalog drift silently otherwise.
