#!/usr/bin/env python3
"""retention.py - liest den Zuschauerbindungs-Export aus YouTube Studio und findet die Lecks.

    python3 retention.py retention.csv
    python3 retention.py retention.csv --transcript transkript.srt   # zeigt, was an jedem Einbruch gesagt wurde
    python3 retention.py retention.csv --duration 600 --json

Datei aus Studio: Analytics -> Video -> Interaktion -> Diagramm "Zuschauerbindung" -> Download-Symbol.
Zwei Spalten: eine Position (Prozent oder Sekunden) und der Anteil, der noch zuschaut.
Deutsche Exporte mit Dezimalkomma ("45,3") werden erkannt.

Drei Dinge, weil es drei verschiedene Probleme mit drei verschiedenen Lösungen sind:
  HOOK-VERLUST  was in den ersten 30 Sekunden verloren geht
  ABSTÜRZE      einzelne steile Einbrüche - ein bestimmter Moment, an dem Leute gegangen sind
  RUTSCHEN      der gleichmäßige Verlust im flachen Mittelteil

Mit --transcript steht dabei, was du an jedem Absturz gesagt hast. Nur so kannst du den Bericht
umsetzen, ohne das Video selbst durchzuspulen.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT).
"""
import csv, json, os, re, sys

def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        # deutsche Exporte trennen oft mit Semikolon, weil das Komma das Dezimalzeichen ist
        delim = ";" if ";" in fh.readline() else ","
        fh.seek(0)
        for r in csv.reader(fh, delimiter=delim):
            nums = []
            for c in r:
                c = c.strip().replace("%", "").replace("\u202f", "").replace(" ", "")
                # Dezimalkomma (deutscher Export) vs. Tausenderkomma (englischer Export)
                c = c.replace(",", ".") if re.fullmatch(r"-?\d+,\d+", c) else c.replace(",", "")
                try: nums.append(float(c))
                except ValueError: nums.append(None)
            vals = [n for n in nums if n is not None]
            if len(vals) >= 2: rows.append((vals[0], vals[1]))
    return rows

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    tr = a[a.index("--transcript") + 1] if "--transcript" in a else None
    files = [x for x in a if not x.startswith("--") and x != tr]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = load_csv(files[0])
    if len(rows) < 8: print("konnte aus der CSV keine 8 Datenpunkte lesen"); sys.exit(1)
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    dur = None
    if "--duration" in a: dur = float(a[a.index("--duration") + 1])
    def at(x): return (x / 100.0 * dur) if (pct_axis and dur) else x
    start = ys[0] or 100.0
    # HOOK: die ersten 30 Sekunden, oder die ersten 10 %, wenn die Achse in Prozent ist und die Dauer fehlt
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = start - hook_end
    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        span = xs[i] - xs[i - 1] or 1
        drops.append((d / span, xs[i - 1], xs[i], d))
    drops.sort(reverse=True)
    cliffs = [{"from": round(a1, 2), "to": round(b1, 2), "lost": round(d, 2),
               "at_seconds": round(at(a1), 1) if (not pct_axis or dur) else None}
              for _, a1, b1, d in drops[:5] if d > 0.8]
    mid = [d for d, x0, _, _ in [(r[0], r[1], r[2], r[3]) for r in drops] if x0 > cutoff]
    slide = sum(mid) / len(mid) if mid else 0
    said = {}
    if tr and os.path.exists(tr):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
        from deadair import load as load_cues
        cues = load_cues(tr)
        for c in cliffs:
            if c["at_seconds"] is None: continue
            t = c["at_seconds"]
            near = [q[2] for q in cues if q[0] <= t + 4 and q[1] >= t - 4]
            said[str(c["from"])] = " ".join(near)[:140]
    out = {"points": len(rows), "start": start, "hook_leak": round(hook_leak, 2),
           "end": ys[-1], "cliffs": cliffs, "slide_per_unit": round(slide, 3), "said": said}
    if as_json: print(json.dumps(out, indent=1)); return
    print(f"\n  {files[0]}   {len(rows)} Punkte   {ys[0]:.1f}% -> {ys[-1]:.1f}%\n")
    verdict = "gesund" if hook_leak < 25 else "undicht" if hook_leak < 40 else "kritisch"
    print(f"  HOOK-VERLUST {hook_leak:.1f}% am Anfang verloren   [{verdict}]")
    print(f"               unter 25 ist gesund. Den ersten Satz vor allem anderen verbessern.\n")
    print("  ABSTÜRZE     die Momente, an denen Leute wirklich gegangen sind")
    for c in cliffs:
        where = f"{c['at_seconds']:.0f}s" if c["at_seconds"] is not None else f"{c['from']}"
        print(f"    -{c['lost']:5.1f}%  bei {where:>8}" + (f"   \"{said.get(str(c['from']),'')}\"" if said else ""))
    if not cliffs: print("    keiner steiler als 0,8 % - der Verlust ist reines Rutschen, keine einzelnen Momente")
    print(f"\n  RUTSCHEN     {slide:.3f}% pro Einheit im Mittelteil")
    print( "               flaches Rutschen ist Tempo, nicht Inhalt. Kürz die Mitte, schreib sie nicht um.\n")

if __name__ == "__main__":
    main()
