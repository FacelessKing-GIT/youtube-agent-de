#!/usr/bin/env python3
"""title.py - prüft Titel und Thumbnail eines YouTube-Videos als Paar, bevor du veröffentlichst.

    python3 title.py --title "..." --thumb "KI MACHT ES"
    python3 title.py titles.txt            # einer pro Zeile, gerankt
    python3 title.py --title "..." --json

Die Einheit ist das Paar, nicht der Titel. Ein Titel, der den Thumbnail-Text wiederholt, verschenkt
die halbe Klickfläche, und genau das ist der häufigste Fehler, den dieses Werkzeug findet.

Länge: YouTube schneidet in der Desktop-Suche etwa bei 60 Zeichen ab, im Startseiten-Feed am Handy
etwa bei 40. Beides wird gemeldet, weil es verschieden scheitert: Am Desktop geht das Ende verloren,
am Handy womöglich das Thema.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT).
"""
import json, re, sys, os

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"krass","unglaublich","wahnsinn","wahnsinnig","verrückt","riesig","mega","ultimativ","ultimative",
         "beste","besten","mächtig","geheim","geheimnis","revolutionär","episch","perfekt","perfekte",
         "komplett","komplette","alles","genial","unfassbar"}
STOP = {"der","die","das","den","dem","des","ein","eine","einen","einem","einer","und","oder","für","mit",
        "in","im","an","am","auf","zu","zum","zur","von","vom","ist","sind","dein","deine","deinen","du",
        "mein","meine","ich","so","wie","was","warum","dieser","diese","dieses","es","nicht","mehr"}
WORD = re.compile(r"[a-zäöüß0-9']+")

def words(t): return WORD.findall(t.lower())

def check(title, thumb=None):
    t = title.strip()
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("länge", f"{n} Zeichen - YouTubes hartes Limit ist {HARD}"))
    elif n > DESKTOP: issues.append(("länge", f"{n} Zeichen - die Desktop-Suche schneidet bei etwa {DESKTOP} ab"))
    else: good.append(f"{n} Zeichen, innerhalb der {DESKTOP}-Zeichen-Grenze am Desktop")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("handy", f'der Handy-Feed zeigt etwa "{head}..." - prüf, ob das Thema übrig bleibt'))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2: issues.append(("geschrei", f"{len(caps)} Wörter in Großbuchstaben - zwei sind die Grenze, danach wirkt es wie Spam"))
    elif caps: good.append(f"{len(caps)} Wort in Großbuchstaben zur Betonung")
    v = [w for w in words(t) if w in VAGUE]
    if v: issues.append(("vage", f"{', '.join(sorted(set(v)))} - tausch es gegen eine Zahl, einen Namen oder ein Datum"))
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums: good.append(f"enthält eine konkrete Zahl ({', '.join(nums[:3])})")
    else: issues.append(("keine-zahl", "keine Zahl, kein Datum, kein Name - die zuverlässigste Einzelverbesserung"))
    if t.endswith("?"): good.append("offene Frage im Titel")
    front = [w for w in words(t)[:3] if w not in STOP]
    if not front: issues.append(("anfang", "die ersten drei Wörter sind alle Füllwörter - zieh das Thema nach vorn"))
    long_words = [w for w in t.split() if len(re.sub(r"\W", "", w)) > 16]
    if long_words: issues.append(("wortlänge", f"{', '.join(long_words)} - so lange Wörter brechen am Handy schlecht um"))
    if thumb:
        tw, hw = set(words(t)) - STOP, set(words(thumb)) - STOP
        shared = tw & hw
        if shared:
            issues.append(("doppelt", f"Thumbnail wiederholt den Titel bei {', '.join(sorted(shared))} - "
                                      "das Thumbnail sollte sagen, was der Titel nicht sagt"))
        else:
            good.append("Thumbnail und Titel nutzen verschiedene Wörter")
        if len(words(thumb)) > 4:
            issues.append(("thumb-länge", f"{len(words(thumb))} Wörter auf dem Thumbnail - drei sind die Grenze in Feed-Größe"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    return {"title": t, "chars": n, "score": score, "issues": issues, "good": good}

def show(r):
    print(f'\n  "{r["title"]}"')
    print(f"  {r['chars']} Zeichen   Punkte {r['score']}/100")
    for k, m in r["issues"]: print(f"    x  {k:<12} {m}")
    for m in r["good"]:      print(f"    ok              {m}")

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--title" in a:
        rows = [check(a[a.index("--title") + 1], thumb)]
    elif a and os.path.exists(a[0]):
        rows = [check(l, thumb) for l in open(a[0], encoding="utf-8").read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["score"])
    if as_json: print(json.dumps(rows, indent=1, ensure_ascii=False)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()
