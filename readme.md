---
title: Trust Triage Env
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# TrustTriageEnv

A risk-aware decision environment for uncertain incoming claims.

This environment simulates a real-world trust and safety / fact-triage workflow where an AI agent must decide how to handle a newly arriving claim under uncertainty.

## Objective

The agent must choose one of the following actions:

- ACCEPT
- REJECT
- VERIFY
- DEFER
- ESCALATE

The environment rewards safe, rational, and efficient decisions while penalizing dangerous or wasteful ones.

## Tasks

This environment includes 3 benchmark tasks:

- **easy_1** — obvious false viral claim
- **medium_1** — breaking news under uncertainty
- **hard_1** — high-risk partially supported claim

## Observation Space

Each observation includes:

- `claim_text`
- `source_reliability`
- `evidence_count`
- `contradiction_score`
- `verifier_confidence`
- `risk_level`
- `time_step`
- `history`
- `done`

## Action Space

The agent can choose:

- `ACCEPT`
- `REJECT`
- `VERIFY`
- `DEFER`
- `ESCALATE`

## Run Locally

```bash
uvicorn app.server:app --reload