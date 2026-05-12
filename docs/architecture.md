# Architecture

## Purpose

`knowledge-memory-workbench` turns scattered operator knowledge into memory packets that can be ranked and reused quickly.

The repo focuses on:

- context aging
- trust and freshness
- retrieval scoring
- domain clustering
- briefing-safe recovery paths

## System Shape

The service is local-first and dependency-light:

- Python `http.server` JSON API
- in-repo sample memory packets
- retrieval engine for keyword, freshness, and confidence scoring
- demo runner for report output
- screenshot proof layer for the README

## Memory Model

Each packet carries:

- `domain`
- `owner`
- `freshness_days`
- `confidence`
- `staleness_risk`
- `summary`
- `keywords`

The retrieval engine then scores packets against a prompt and a freshness budget.

## Why It Fits The Portfolio

This repo expands the portfolio toward AI-adjacent operator memory systems rather than another workflow or policy surface. It pairs well with:

- `executive-briefing-studio`
- `briefing-intelligence-engine`
- `signal-orchestration-lab`
- `mobile-briefing-companion`

