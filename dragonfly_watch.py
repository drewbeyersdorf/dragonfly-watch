#!/usr/bin/env python3
"""dragonfly-watch: see everything, interrupt almost nothing.

A dragonfly's compound eyes track hundreds of moving things at once and
it strikes only when the intercept is certain. The watch does the same:
every signal is seen, almost none are raised. A raise must clear the bar:
fresh, load-bearing, and actionable by someone named. Otherwise it is
logged, dimmed, and left alone. Quiet is the default state of a good watch.

Demo: python3 dragonfly_watch.py demo
"""
import json, time

class Watch:
    def __init__(self, stale_after: float = 60.0):
        self.seen: list[dict] = []
        self.stale_after = stale_after

    def observe(self, source: str, signal: str, load_bearing: bool,
                actionable_by: str = "", now: float | None = None) -> dict:
        now = now if now is not None else time.time()
        s = {"source": source, "signal": signal, "at": now,
             "load_bearing": load_bearing, "actionable_by": actionable_by}
        self.seen.append(s)
        return s

    def triage(self, now: float | None = None) -> dict:
        """The compound-eye sweep: everything is seen; almost nothing is raised."""
        now = now if now is not None else time.time()
        raised, dimmed = [], []
        for s in self.seen:
            fresh = (now - s["at"]) <= self.stale_after
            if s["load_bearing"] and s["actionable_by"] and fresh:
                raised.append({"signal": s["signal"], "to": s["actionable_by"],
                               "age_s": round(now - s["at"], 1)})
            else:
                why = ("stale" if not fresh else
                       "not load-bearing" if not s["load_bearing"] else "no owner")
                dimmed.append({"signal": s["signal"], "why": why})
        return {"raised": raised, "dimmed": dimmed,
                "raise_rate": round(len(raised) / max(len(self.seen), 1), 3)}

def demo():
    w = Watch(stale_after=0.5)
    t0 = time.time()
    w.observe("board", "card-58 unclaimed 2h", True, "dozer", now=t0)
    w.observe("x", "like count moved", False, now=t0)              # noise
    w.observe("flow", "render at 40%", False, now=t0)              # routine
    w.observe("board", "old card still dim", True, "skid", now=t0 - 10)  # stale
    w.observe("leases", "write lease free", True, "")              # no owner
    print(json.dumps(w.triage(now=t0), indent=1))

if __name__ == "__main__":
    demo()
