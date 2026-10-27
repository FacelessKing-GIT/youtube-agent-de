---
name: yt-script
description: >-
  Schreibt aus einer rohen Idee ein YouTube-Skript - fünf Hooks nach 21
  Formeln, bewertet, dann das komplette Sprechskript mit markierten
  Retention-Beats. Nutzen bei "Skript", "schreib mein nächstes Video",
  "Hook", "erster Satz", "was soll ich sagen" oder wenn jemand gleich
  aufnimmt und die ersten 15 Sekunden noch fehlen.
---

# yt-script

Aus einer Idee ein Skript, das jemand bis zum Ende schaut.

In diesem Ordner liegen zwei Werkzeuge, die wirklich laufen. Nutze sie. Bewerte den Hook nicht nach Gefühl.

```bash
python3 hookscore.py hooks.txt              # mehrere Hooks (einer pro Zeile) ranken
python3 hookscore.py --hook "ein Satz"      # einen einzelnen bewerten
```

## Bevor du schreibst

1. Lies `~/.claude/youtube/voice.md`, falls vorhanden. Das ist das Stimmprofil: wie die Person vor der
   Kamera spricht, welche Wörter sie nie benutzt, mit wem sie redet, was sie nicht behauptet. Fehlt die
   Datei, frag nach **drei eigenen Videos**, lies oder transkribiere sie, leite die Stimme ab und schreib
   die Datei. Ein Skript in der falschen Stimme ist schlimmer als keins, weil es laut vorgelesen werden muss.
2. Erfinde nie eine Zahl, ein Ergebnis oder eine Quelle. Würde eine Zahl helfen und du hast keine,
   frag danach oder schreib den Satz ohne sie.
3. Schreib auf Deutsch, außer die Person will ausdrücklich eine andere Sprache.

## Der Aufbau

**Die ersten 15 Sekunden sind der ganze Job.** Sie erledigen drei Dinge, sonst verliert das Video
Zuschauer: Sie bestätigen, was der Titel versprochen hat, öffnen eine Frage, die der Zuschauer nicht
selbst schließen kann, und beweisen, dass die Auflösung existiert.

1. **Hook.** Schreib FÜNF nach [den 21 Formeln](hooks.json), lass sie durch `hookscore.py` laufen,
   behalte die besten zwei und zeig beide mit Bewertung. Gib nie nur einen Hook ab.
2. **Die Wende** (0:15-0:45). In einem Satz sagen, was das Video tun wird, und sofort damit anfangen.
   Kein Kanal-Intro, kein "bevor wir loslegen", kein Abo-Aufruf. Das ist die häufigste Ursache für den
   Absturz bei 0:30.
3. **Der Hauptteil.** Eine Idee pro Beat. Markiere bei jedem Beat, was IM BILD ist, nicht nur was
   gesagt wird. Ein sprechender Kopf ohne etwas zum Anschauen ist ein Podcast.
4. **Die Auflösung.** Liefere ausdrücklich, was der Hook versprochen hat, und sag, dass du es lieferst:
   "Das ist der Prompt, er steht in der Beschreibung."
5. **Der Abschluss.** Eine Bitte. Nicht drei.

## Was du zurückgibst

- die zwei besten Hooks mit ihrer Bewertung
- das Skript Beat für Beat, mit `[IM BILD: ...]` bei jedem Beat
- die geschätzte Länge bei 150 Wörtern pro Minute
- eine Zeile: welche Formel der Sieger-Hook nutzt und warum sie zur Idee passt

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
