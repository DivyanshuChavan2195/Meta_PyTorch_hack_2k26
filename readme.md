# TrustTriageEnv

A risk-aware decision environment where an AI agent must decide how to handle uncertain incoming claims.

## Actions
- ACCEPT
- REJECT
- VERIFY
- DEFER
- ESCALATE

## Tasks
- easy_1: obvious false claim
- medium_1: uncertain breaking news
- hard_1: high-risk ambiguous claim

## Run locally
uvicorn app.server:app --reload

## Run inference
python inference.py