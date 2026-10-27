---
name: yt-chapters
description: >-
  Schreibt YouTube-Kapitel aus einem Transkript und prüft sie gegen
  YouTubes eigene Regeln, damit sie wirklich angezeigt werden. Nutzen bei
  "Kapitel", "Zeitstempel", "teil das Video in Abschnitte".
---

# yt-chapters

```bash
python3 chapters.py transkript.srt --target 8
```

## Die Regeln, ohne Ausnahme

Verletzt eine Kapitelliste eine dieser Regeln, werden daraus stillschweigend keine Kapitel. Der Block
steht dann nutzlos in der Beschreibung:

- Der erste Eintrag muss **00:00** sein.
- Es braucht **mindestens drei**.
- Jedes Kapitel muss **mindestens 10 Sekunden** lang sein.

Das Werkzeug prüft alle drei und sagt dir, wenn eine Liste ungültig ist, statt sie dich einfügen zu lassen.

## Jede Zeile neu betiteln

`chapters.py` findet die GRENZEN gut: Es bewertet deine echten Pausen danach, wie stark sich der
Wortschatz davor und danach ändert. Die ausgegebenen Titel sind nur Themenwörter, also ein Entwurf.
Ein Kapitel namens "Thumbnails Titel Packaging" ist ein Platzhalter. Schreib jedes als Versprechen
dieses Abschnitts um, in der Stimme der Person, drei bis fünf Wörter.

Kapitel sind auch ein Retention-Test: Lässt sich ein Abschnitt nicht in fünf Wörtern benennen, sind es
zwei Abschnitte oder er ist Füllmaterial.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
