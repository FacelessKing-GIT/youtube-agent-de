#!/usr/bin/env python3
"""swipe.py - rankt gesammelte Videos danach, wie weit jedes seinen EIGENEN Kanal übertroffen hat,
und benennt die Formel.

    python3 swipe.py gesammelt.json
    python3 swipe.py gesammelt.json --min 2.0 --json

Eingabe ist eine Liste, die du gesammelt hast - ein Objekt pro Video:

    [{"channel":"Ein Kanal","title":"...","views":412000,"url":"...","duration":613}, ...]

Reine Aufrufzahlen messen die Kanalgröße, nicht die Idee. 400.000 Aufrufe auf einem Kanal mit
2 Millionen Abos sind ein normaler Dienstag; 400.000 auf einem Kanal mit 30.000 im Median sind das,
was sich zu studieren lohnt. Deshalb wird jedes Video als VIELFACHES DES MEDIANS SEINES KANALS
bewertet. Dafür braucht es mindestens vier Videos pro Kanal - das Werkzeug sagt es, statt still
auf Rauschen zu ranken.

Die Formel kommt aus skills/yt-script/hooks.json, abgeglichen mit dem TITEL. Das ist eine Einschätzung
der Wörter, keine Aussage darüber, warum das Video funktioniert hat.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT).
"""
import json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "..", "yt-script", "hooks.json"), encoding="utf-8"))["hooks"]

def classify(title):
    scored = []
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, title, re.I))
        if n: scored.append((n, f["name"]))
    scored.sort(reverse=True)
    return scored[0][1] if scored else "Keine Formel"

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    lo = float(a[a.index("--min") + 1]) if "--min" in a else 1.5
    files = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = json.load(open(files[0], encoding="utf-8-sig"))
    if isinstance(rows, dict): rows = rows.get("videos", [])
    by = {}
    for r in rows: by.setdefault(r.get("channel", "?"), []).append(r)
    out, thin = [], []
    for ch, vids in by.items():
        views = [float(v.get("views", 0) or 0) for v in vids]
        med = statistics.median(views) if views else 0
        if len(vids) < 4:
            thin.append((ch, len(vids)))
            continue
        for v in vids:
            m = (float(v.get("views", 0) or 0) / med) if med else 0
            out.append({"channel": ch, "title": v.get("title", ""), "views": int(v.get("views", 0) or 0),
                        "median": int(med), "multiple": round(m, 2),
                        "formula": classify(v.get("title", "")), "url": v.get("url", "")})
    out = [r for r in out if r["multiple"] >= lo]
    out.sort(key=lambda r: -r["multiple"])
    if as_json: print(json.dumps({"outliers": out, "skipped_thin_channels": thin}, indent=1)); return
    print(f"\n  {len(rows)} Videos aus {len(by)} Kanälen, Ausreißer ab {lo}x\n")
    for r in out[:25]:
        print(f"    {r['multiple']:5.2f}x  {r['views']:>9,}  vs {r['median']:>9,} Median   {r['channel'][:22]:<22} {r['title'][:52]}")
        print(f"            {r['formula']}")
    if not out: print("    nichts über der Schwelle - sammle mehr pro Kanal oder senke --min")
    if thin:
        print(f"\n  {len(thin)} Kanal/Kanäle übersprungen, weniger als 4 Videos gesammelt - ein Median aus")
        print( "  ein oder zwei Videos ist kein Median: " + ", ".join(f"{c} ({n})" for c, n in thin[:6]))
    counts = {}
    for r in out: counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    if counts:
        print("\n  Formeln unter den Ausreißern")
        for f, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {n:2d}x  {f}")
    print()

if __name__ == "__main__":
    main()
