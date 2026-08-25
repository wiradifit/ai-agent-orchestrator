# 🤖 AI Agent Orchestrator

A production-grade framework for operating **multi-company software organizations run as AI-native systems**.

This is what powers a real holding company — **20+ named agent roles**, 2 production servers, 14 scheduled automation workflows, and governance built in from day one. Open-sourced so other teams can replicate it without starting from scratch.

> All agent identities below are **role aliases**, not real names — the pattern matters, not the personas.

## What This Is

When you hire humans, you organize them with org charts, runbooks, escalation paths, and weekly meetings. When you operate an organization of AI agents, you need the same discipline — automated, observable, and cost-controlled.

- **Role-based agent personas**, each with a persistent `BRAIN.md` (mission, authority bounds, escalation path)
- **Rate-limit governance** — a treasury-agent watches shared LLM quotas across every agent and throttles automatically on breach
- **Scheduled orchestration** — cron-driven pipelines: content publishing windows, daily self-learning loops, weekly board meetings
- **Multi-server operations** — PostgreSQL 16 + Redis 7 hub on Oracle Cloud ARM, hardened edge node on Tencent Cloud (Caddy, fail2ban, weekly patching)

## Architecture

```
~/.hermes/
├── AGENTS.md                  # Unified framework protocols
├── executives/                # One directory per agent role
│   ├── group-cto/             # Systems & cloud architecture
│   ├── infra-lead/            # DevOps & infrastructure
│   ├── token-cfo/             # LLM budget treasury + rate-limit sentinel
│   ├── security-sentinel/     # Firewall, SSH, audit watchdogs
│   ├── market-intel/          # Competitor & trend research
│   ├── social-ops/            # Content pipeline scheduling
│   ├── docs-writer/           # Technical writing & proofing
│   └── qa-gate/               # Review gates before anything ships
├── scripts/                   # Cron-driven pipelines
│   ├── multi-account-scheduler.py
│   ├── trending-research.sh
│   ├── daily-self-learning.py
│   └── weekly-bod-meeting.py
└── platforms/                 # Platform gateways with token-bucket schedulers
```

Each `BRAIN.md` follows the same contract:

```markdown
# <Role Alias>
**Role:** <title> of <company/unit>
**Mission:** <what this agent owns, and what it must never do>
**Escalates to:** <parent role> when <condition>
**Owns:** <systems, budgets, or pipelines under its authority>
```

## Server Stack

| Node | Role | Stack |
|---|---|---|
| Oracle Cloud ARM | Main hub | PostgreSQL 16 · Redis 7 · Ollama (local embeddings) · systemd services · Fluentd monitoring |
| Tencent Cloud | Edge node | Caddy reverse proxy · fail2ban · UFW-hardened · weekly-patch cron |

## Quick Start

```bash
git clone https://github.com/wiradifit/ai-agent-orchestrator.git
cd ai-agent-orchestrator

# 1. Define an agent role
mkdir -p ~/.hermes/executives/group-cto
cp templates/BRAIN.md ~/.hermes/executives/group-cto/
# edit mission + escalation

# 2. Wire a schedule
crontab -e
# 15 */6 * * * /path/to/scripts/trending-research.sh

# 3. Enable the budget sentinel
python3 scripts/rate_limit_sentinel.py --daemon
```

Templates for BRAIN.md, cron layouts, and systemd units live in [`templates/`](templates/) and [`scripts/`](scripts/).

## Governance Model

| Control | Mechanism |
|---|---|
| Cost control | Treasury agent tracks per-provider token spend; breaches auto-throttle lower-priority agents |
| Security | Key-only SSH, UFW deny-lists, fail2ban jails, daily audit scans |
| Quality | QA-gate reviews before publish; cross-check watcher re-verifies deliveries |
| Accountability | Every agent logs decisions to its own journal; weekly board meeting aggregates |

## Who Is This For

- Founders running lean companies with autonomous agent squads
- Platform teams standardizing multi-agent ops with real governance
- Engineers who want AI-assisted leverage **beyond a chat window** — schedules, budgets, firewalls included

## License

PolyForm Noncommercial 1.0.0 — free to use, modify, and contribute for research and noncommercial purposes; commercialization requires separate permission. Built something with it? I'd love to see it.

---

**Prawira Hadi Fitrajaya** · Senior iOS Engineer @ Ajaib  
[GitHub](https://github.com/wiradifit) · [Portfolio](https://wiradifit.github.io) · [Threads](https://www.threads.com/@wrdft)
