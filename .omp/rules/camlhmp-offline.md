---
description: camlhmp pipelines run offline; no network in tests
---
CTX-CAMLHMP-1 MUST keep pipeline execution offline; a test that needs the network is an integration test.
Why: the pipeline runs inside containers with no egress.
