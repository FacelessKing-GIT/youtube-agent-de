#!/usr/bin/env python3
"""chapters.py - YouTube-Kapitel aus einem Transkript mit Zeitstempeln.

    python3 chapters.py transkript.srt            # oder .vtt / Whisper-.json
    python3 chapters.py transkript.srt --target 8 --json

Gibt einen Block aus, den du direkt in die Beschreibung einfügen kannst. YouTubes eigene Regeln werden
geprüft statt angenommen: Die Liste beginnt bei 00:00, hat mindestens drei Einträge, und jedes Kapitel
ist mindestens 10 Sekunden lang. Ein Block, der eine davon verletzt, wird stillschweigend nicht zu
Kapiteln, deshalb wird geprüft statt vertraut.

Die Grenzen kommen aus den Pausen, die du wirklich gemacht hast, bewertet nach Pausenlänge und danach,
wie stark sich der Wortschatz davor und danach ändert. Ein erster Entwurf zum Umbenennen.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT). Deutsche Stoppwörter ergänzt.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
from deadair import load, parse_ts  # noqa: E402  (same parser, one implementation)

STOP = set("the a an of for to in on and or is are was were be been with this that it as at by from "
           "you your i my we our they them he she but so if then than there here what which who how "
           "when where why not no yes do does did just really very like about into over out up down "
           "can could will would should have has had get got make made go going went one two".split()) | set(
    "der die das den dem des ein eine einen einem einer eines und oder aber auch noch schon nur sehr "
    "dass wenn weil dann denn doch also halt eben ganz mal jetzt hier dort heute sind waren wird "
    "werden wurde haben hatte habe sein bist kann können könnte muss müssen soll sollte will wollen "
    "mich dich mein meine dein deine seine unser euer ihre ihren ihrem nicht kein keine keinen nichts "
    "von vom für auf aus bei nach über unter vor zum zur durch gegen ohne warum welche welcher dieser "
    "diese dieses diesen einfach eigentlich quasi genau okay irgendwie wirklich immer machen macht "
    "gemacht gehen geht kommt kommen sagen sagt gesagt eins zwei drei".split())

def keywords(text):
    return {w for w in re.findall(r"[a-zäöüß']{4,}", text.lower()) if w not in STOP}

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    target = int(a[a.index("--target") + 1]) if "--target" in a else 7
    a = [x for x in a if not x.startswith("--") and not x.isdigit()]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if len(cues) < 6: print("zu wenige Abschnitte für Kapitel"); sys.exit(1)
    dur = cues[-1][1]
    cand = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        before = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after = " ".join(c[2] for c in cues[i:i + 12])
        kb, ka = keywords(before), keywords(after)
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, cues[i][0], i))
    cand.sort(reverse=True)
    picked, MIN = [0.0], 10.0
    for _, t, i in cand:
        if len(picked) >= target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN:
            picked.append(t)
    picked.sort()
    chapters = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        kw = [w for w in keywords(text)]
        kw.sort(key=lambda w: -text.lower().count(w))
        title = " ".join(w.capitalize() for w in kw[:3]) or "Abschnitt"
        chapters.append({"start": round(t, 2), "label": mmss(t), "draft_title": title,
                         "seconds": round(end - t, 2)})
    ok = len(chapters) >= 3 and chapters[0]["start"] == 0 and all(c["seconds"] >= MIN for c in chapters)
    if as_json:
        print(json.dumps({"valid": ok, "chapters": chapters}, indent=1)); return
    print()
    for c in chapters: print(f"  {c['label']} {c['draft_title']}")
    print(f"\n  {len(chapters)} Kapitel"
          f"{'' if ok else '  -- UNGÜLTIG: YouTube braucht 3+, einen ersten Eintrag bei 00:00 und je mindestens 10s'}")
    print("  Benenne jede Zeile vor dem Einfügen um. Das sind Themenwörter, nicht deine Worte.\n")

if __name__ == "__main__":
    main()
