---
name: yt-package
description: >-
  Schreibt und prüft Titel und Thumbnail eines YouTube-Videos als ein Paar -
  Abschneiden, Wiederholungen und vage Wörter, vor dem Veröffentlichen.
  Nutzen bei "Titel-Ideen", "wie soll ich das nennen", "Thumbnail-Text",
  "meine CTR ist schlecht", Packaging oder beim Umbenennen eines Videos.
---

# yt-package

Titel und Thumbnail sind EINE Einheit. Wer sie getrennt schreibt, landet fast immer beim selben Fehler:
Das Thumbnail wiederholt den Titel, und die halbe Klickfläche sagt zweimal dasselbe.

```bash
python3 title.py --title "..." --thumb "KI MACHT ES"
python3 title.py titles.txt            # einer pro Zeile, gerankt
```

## Bevor du schreibst

1. Lies `~/.claude/youtube/voice.md`, falls vorhanden. Fehlt die Datei, frag nach **drei eigenen
   Videos**, leite die Stimme ab und schreib die Datei.
2. Erfinde nie eine Zahl, ein Ergebnis oder eine Quelle. Frag danach oder lass sie weg.
3. Schreib auf Deutsch, außer die Person will etwas anderes.

## Regeln, die das Werkzeug prüft, und warum

- **60 Zeichen** schneidet die Desktop-Suche ab, **40** der Startseiten-Feed am Handy. Beides wird
  gemeldet, weil es verschieden scheitert: Am Desktop geht das Ende verloren, am Handy womöglich das Thema.
- **Das Thumbnail wiederholt den Titel nicht.** Andere Wörter, gleiches Versprechen.
- **Höchstens drei Wörter aufs Thumbnail.** In Feed-Größe ist ein viertes Wort ein grauer Fleck.
- **Eine Zahl, ein Name oder ein Datum** schlägt jedes Adjektiv.
- **Zwei Wörter in Großbuchstaben** sind die Obergrenze, danach wirkt der Titel wie Spam.
- Deutsche Wörter sind lang: Lieber ein kurzes Wort mehr als ein Kompositum, das abgeschnitten wird.

## Zehn schreiben, zwei behalten

Schreib zehn Titel, lass alle durch `title.py` laufen und zeig die besten drei mit Punktzahl und dem
konkreten Problem bei jedem. Für den Sieger das Thumbnail-Briefing: Gesichtsausdruck, Bildausschnitt,
die drei Wörter und was der Hintergrund tun muss, damit der Kontrast in Feed-Größe hält.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
