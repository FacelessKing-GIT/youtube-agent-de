#!/usr/bin/env python3
"""hookscore.py - bewertet einen YouTube-Hook, bevor du einen Take dafür verschwendest.

Fünf Eigenschaften, je 0-100, und ein Urteil aus 60 % Mittelwert und 40 % schwächster Eigenschaft.
Die Gewichtung auf das schwächste Glied ist Absicht: Ein Hook mit vier starken und einer toten
Eigenschaft verliert die Leute genau an der toten Stelle, und ein Mittelwert versteckt das.

    python3 hookscore.py hooks.txt            # ein Hook pro Zeile, gerankt
    python3 hookscore.py --hook "ein Satz"    # einen einzelnen bewerten
    python3 hookscore.py --json hooks.txt     # maschinenlesbar

WAS DAS KANN UND WAS NICHT. Das englische Original wurde an 74 echten Kurzvideo-Hooks kalibriert:
Es trennt absichtlich schlechte Hooks gut von echten, die Hits eines Creators von dessen eigenen
Flops aber kaum. Die deutschen Wortlisten hier sind eine Übertragung und nicht neu kalibriert.
Ein niedriger Wert ist ein Grund, nochmal hinzuschauen, ein hoher ist kein Versprechen.

Basiert auf youtube-agent-skill von Jake Schincariol (MIT).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json"), encoding="utf-8"))["hooks"]

FILLER = {"eigentlich","quasi","halt","einfach","wirklich","sehr","also","irgendwie","sozusagen",
          "ja","leute","hallo","hey","willkommen","heute","video","abonniert","abonnieren","kanal","mal"}
VAGUE = {"krass","unglaublich","wahnsinn","wahnsinnig","verrückt","riesig","mega","geheimnis","geheim",
         "mächtig","ultimativ","ultimative","beste","besten","revolutionär","gamechanger","unfassbar","genial"}
CONCRETE = re.compile(r"\b(\d[\d.,]*\s?(%|k|x|€)?|€\s?\d|\d+\s?(sekunde|sekunden|minute|minuten|stunde|stunden|tag|tage|tagen|woche|wochen|monat|monate|monaten|jahr|jahre|jahren))\b", re.I)
YOU = re.compile(r"\b(du|dich|dir|dein|deine|deinen|deinem|deiner|deins)\b", re.I)
STAKE = re.compile(r"\b(verlier\w*|verschwend\w*|aufhören|hörst|scheiter\w*|pleite|kostet|kosten|risiko|bevor|stopp|nie|niemals|tot|stirbt)\b", re.I)
CURIOSITY = re.compile(r"\b(warum|wieso|wie|was|welche[rs]?|bis|bevor|aber|niemand|fast|außer|grund|eigentlich)\b", re.I)
WORD = re.compile(r"[a-zäöüß0-9'%€.]+")

def words(t): return WORD.findall(t.lower())

def specificity(t):
    w = words(t)
    if not w: return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # Im Deutschen sind alle Nomen großgeschrieben, Großschreibung sagt also nichts über Eigennamen.
    # Stattdessen zählen Wörter mit Großbuchstaben im Inneren (YouTube, ChatGPT) oder ganz in Versalien.
    s += min(18, 6 * sum(1 for x in t.split() if re.search(r".[A-Z]", x) or (len(x) > 1 and x.isupper())))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # ein Hook, der sich selbst beantwortet, hat keine offene Frage mehr
    closed = -18 if re.search(r"\b(weil|damit|das heißt|deshalb)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 8-22 Wörter: so lang ist ein gesprochener deutscher Hook, der in 10 Sekunden passt
    if 8 <= n <= 22: return 100
    if n < 8:  return max(30, 100 - (8 - n) * 11)
    return max(10, 100 - (n - 22) * 7)

PROPS = [("KONKRET", specificity), ("ANSPRACHE", address), ("EINSATZ", stakes),
         ("NEUGIER", curiosity), ("KÜRZE", brevity)]

def classify(t):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Keine Formel"), hits

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t)
    return parts, verdict, name, hits

def band(v): return "STARK" if v >= 72 else "BRAUCHBAR" if v >= 55 else "SCHWACH"

FIX = {
 "KONKRET": "tausch ein Adjektiv gegen eine Zahl, einen Namen oder ein Datum",
 "ANSPRACHE": "sag 'du' oder 'dein' in den ersten sechs Wörtern",
 "EINSATZ": "sag, was es kostet, so weiterzumachen wie bisher",
 "NEUGIER": "streich die Satzhälfte, die sich selbst beantwortet",
 "KÜRZE": "8 bis 22 Wörter. Lies es laut und hör auf, wo dir die Luft ausgeht",
}

def report(t, parts, verdict, name, hits):
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'URTEIL':<12} {verdict:3d}  {band(verdict)}")
    print(f"    Formel       {name}" + (f"  ({hits} Muster erkannt)" if hits else "  (keine Formel erkannt - meist ist das eine Zusammenfassung, kein Hook)"))
    low = min(parts, key=parts.get)
    print(f"    schwächste   {low} - {FIX[low]}")

def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0], encoding="utf-8").read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    out = []
    for t in lines:
        parts, verdict, name, hits = score(t)
        out.append({"hook": t.strip(), "properties": parts, "verdict": verdict,
                    "band": band(verdict), "formula": name, "matched": hits})
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([{k: v for k, v in r.items() if k != "matched"} for r in out], indent=1, ensure_ascii=False)); return
    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched"])
    if len(out) > 1:
        print(f"\n  Sieger: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n")

if __name__ == "__main__":
    main()
