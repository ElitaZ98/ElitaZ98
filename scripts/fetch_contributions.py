#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public, unauthenticated
contributions endpoint (the same fragment the profile page itself uses) and
write data/contributions.json with the raw days plus derived stats
(current streak, longest streak, best day, monthly totals).

No token, no auth, no GraphQL -- just the public HTML GitHub already serves.
Run daily by .github/workflows/update-profile-art.yml.
"""
import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "ElitaZ98")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "ElitaZ98-profile-readme/1.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if len(cells) < 300:
        raise RuntimeError(f"GitHub contribution calendar markup missing or incomplete ({len(cells)} days)")

    tooltip_map = {}
    for tip in soup.select("tool-tip[for]"):
        tooltip_map[tip.get("for")] = tip.get_text(" ", strip=True)

    days = []
    dates = set()
    for td in cells:
        date = td.get("data-date")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date or ""):
            raise RuntimeError(f"Invalid contribution date: {date}")
        if date in dates:
            raise RuntimeError(f"Duplicate contribution date: {date}")
        dates.add(date)
        level = int(td.get("data-level", 0))
        desc = tooltip_map.get(td.get("id"), "") or td.get("aria-label", "") or td.get("title", "")
        if re.search(r"\bno contributions?\b", desc, re.I):
            count = 0
        else:
            match = re.search(r"\b([\d,]+)\s+contribution(?:s)?\b", desc, re.I)
            if match:
                count = int(match.group(1).replace(",", ""))
            elif td.has_attr("data-count"):
                count = int(td["data-count"])
            elif level == 0:
                count = 0
            else:
                raise RuntimeError(f"Active contribution cell on {date} has no readable exact count; refusing wrong stats")
        days.append({"date": date, "count": count, "level": max(0,min(4,level))})

    days.sort(key=lambda d: d["date"])
    for prev, nxt in zip(days, days[1:]):
        a = datetime.date.fromisoformat(prev["date"])
        b = datetime.date.fromisoformat(nxt["date"])
        if (b-a).days != 1:
            raise RuntimeError("Contribution calendar has missing dates")
    return days


def compute_current_streak(days):
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1  # today isn't over yet -- don't break the streak on it
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


if __name__ == "__main__":
    days = fetch_days()
    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT_PATH}: {data['total_contributions']} contributions, "
          f"current streak {data['current_streak']['length']}, "
          f"longest streak {data['longest_streak']['length']}")
