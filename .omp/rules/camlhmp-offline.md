---
description: camlhmp pipelines run offline; no network in tests
condition: '(?i)\b(requests|urlopen|httpx|urllib)\b'
scope: [tool:edit(**/*.py), tool:write(**/*.py)]
---
CTX-CAMLHMP-1 MUST keep pipeline execution offline; a test that needs the network is an integration test.
Why: the pipeline runs inside containers with no egress.
