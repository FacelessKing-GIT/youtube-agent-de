#!/usr/bin/env python3
"""deadair.py - eine Schnittliste aus einem Transkript mit Zeitstempeln.

    python3 deadair.py transkript.srt            # oder .vtt oder Whisper-.json
    python3 deadair.py transkript.srt --floor 0.35 --json

Findet drei Dinge und listet die Schnitte so, dass du sie direkt umsetzen kannst:
  LEER    Pausen zwischen gesprochenen Abschnitten, länger als die Schwelle
  FÜLL    Abschnitte, die nur aus Füllwörtern bestehen ("äh", "also ja", "quasi")
  NEU     ein neu angefangener Satz - der zweite Versuch desselben Anfangs

WAS ES NICHT TUT. Es schneidet die Datei nicht. Es gibt eine Schnittliste aus, wie viel wegfiele und
welche Laufzeit übrig bliebe. Umsetzen musst du sie in deinem Schnittprogramm.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT). Deutsche Füllwörter ergänzt.
"""
import json, os, re, sys

FILLER_ONLY = re.compile(r"^[\s,.-]*((äh+m*|öh+m*|ehm+|hm+|mh+|also|ja|naja|okay|ok|genau|gut|so|halt|quasi|sozusagen|"
                         r"irgendwie|eigentlich|einfach|weißt du|wie gesagt|moment|warte|"
                         r"um+|uh+|er+|ah+|right|yeah|like|basically|actually|you know|i mean)[\s,.-]*)+$", re.I)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", d if isinstance(d, list) else [])
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

def norm(t): return re.sub(r"[^a-zäöüß ]", "", t.lower()).split()

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    floor = float(a[a.index("--floor") + 1]) if "--floor" in a else 0.45
    a = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if not cues: print("keine Abschnitte gefunden - ist das eine srt, vtt oder Whisper-json?"); sys.exit(1)
    dur = cues[-1][1]
    cuts = []
    for i, (s, e, t) in enumerate(cues):
        if FILLER_ONLY.match(t):
            cuts.append({"kind": "FÜLL", "start": s, "end": e, "why": t.strip()[:48]})
        if i:
            gap = s - cues[i - 1][1]
            if gap > floor:
                keep = floor / 2
                cuts.append({"kind": "LEER", "start": round(cues[i - 1][1] + keep, 3),
                             "end": round(s - keep, 3), "why": f"{gap:.2f}s Pause"})
        # Ein Neuansatz wird mit dem letzten Abschnitt verglichen, der wirklich SPRACHE war. Der
        # Vergleich mit dem direkt vorherigen verpasst jeden Neuansatz mit einem "äh" dazwischen,
        # und das sind die meisten.
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()): j -= 1
            if j >= 0:
                a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({"kind": "NEU", "start": cues[j][0], "end": cues[j][1],
                                 "why": f'Neuansatz von "{" ".join(a1)}"'})
    cuts = [c for c in cuts if c["end"] > c["start"]]
    cuts.sort(key=lambda c: c["start"])
    removed = sum(c["end"] - c["start"] for c in cuts)
    if as_json:
        print(json.dumps({"source": a[0], "duration": dur, "cuts": cuts,
                          "removed": round(removed, 3), "out": round(dur - removed, 3)}, indent=1)); return
    print(f"\n  {a[0]}   {dur:.2f}s gesamt, {len(cues)} Abschnitte, Pausen-Schwelle {floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<7} {c['start']:8.2f} -> {c['end']:8.2f}   {c['end']-c['start']:5.2f}s   {c['why']}")
    print(f"\n  {len(cuts)} Schnitte, {removed:.2f}s entfernt, {dur - removed:.2f}s übrig "
          f"({removed / dur * 100:.1f}% kürzer)\n")

if __name__ == "__main__":
    main()
