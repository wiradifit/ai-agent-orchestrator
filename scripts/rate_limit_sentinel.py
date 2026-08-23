#!/usr/bin/env python3
"""Company-wide LLM budget sentinel.

Watches per-provider token spend (or any counter you feed it) and throttles
lower-priority agents when the daily budget is at risk. Ships as a template:
wire `read_spend()` to your provider's usage API or local ledger.

Usage:
    python3 rate_limit_sentinel.py --budget 5.00 --interval 300
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sentinel")

STATE_FILE = Path.home() / ".agent_orchestrator" / "sentinel_state.json"


def read_spend() -> float:
    """Return spend-so-far-today in USD.

    Replace with your provider's usage endpoint, e.g. OpenRouter's
    /api/v1/credits, or read from a local append-only ledger written by
    each agent after every LLM call.
    """
    ledger = Path.home() / ".agent_orchestrator" / "spend_ledger.jsonl"
    if not ledger.exists():
        return 0.0
    total = 0.0
    for line in ledger.read_text().splitlines():
        try:
            entry = json.loads(line)
            total += float(entry.get("cost_usd", 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            continue
    return total


def write_state(throttled_agents: list[str]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "updated_at": time.time(),
        "throttled": throttled_agents,
    }, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, required=True, help="Daily budget in USD")
    ap.add_argument("--threshold", type=float, default=0.8, help="Throttle trigger ratio")
    ap.add_argument("--low-priority", nargs="*", default=["social-ops", "market-intel"],
                    help="Agent roles throttled first when over threshold")
    ap.add_argument("--interval", type=int, default=300, help="Check interval seconds")
    args = ap.parse_args()

    while True:
        spend = read_spend()
        ratio = spend / args.budget if args.budget else 0.0
        if ratio >= 1.0:
            log.warning("BUDGET EXCEEDED: $%.2f / $%.2f — suspending all non-critical agents",
                        spend, args.budget)
            write_state(args.low_priority)
        elif ratio >= args.threshold:
            log.info("Budget %.0f%% used ($%.2f/$%.2f) — throttling %s",
                     ratio * 100, spend, args.budget, ", ".join(args.low_priority))
            write_state(args.low_priority)
        else:
            if write_state and STATE_FILE.exists():
                prev = json.loads(STATE_FILE.read_text())
                if prev.get("throttled"):
                    log.info("Budget back under threshold ($%.2f/$%.2f) — releasing throttle", spend, args.budget)
            write_state([])
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
