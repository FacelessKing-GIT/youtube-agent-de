---
name: yt-retention
description: >-
  Liest den Export der Zuschauerbindung aus YouTube Studio, findet die
  Stellen, an denen Zuschauer wirklich abspringen, und sagt, was zu ändern
  ist. Nutzen bei "warum schauen die Leute nicht zu Ende", "meine Retention
  ist schlecht", einer eingefügten Retention-Kurve oder CSV, "Tempo verbessern".
---

# yt-retention

Die Retention-Kurve ist das einzige ehrliche Feedback, das YouTube dir gibt. Fast niemand exportiert sie.

```bash
python3 retention.py retention.csv --duration 600
python3 retention.py retention.csv --transcript transkript.srt
```

So kommst du an die Datei: Studio -> Video -> Analytics -> Interaktion -> Diagramm
"Zuschauerbindung" -> Download-Symbol -> "Zuschauerbindung".

## Drei verschiedene Probleme

- **HOOK-VERLUST** - was in den ersten 30 Sekunden verloren geht. Unter 25 % ist gesund. Das wird
  immer zuerst behoben, und es liegt immer an den ersten fünfzehn Sekunden Skript, nie am Schnitt.
- **ABSTÜRZE** - einzelne steile Einbrüche. Ein Absturz ist ein Moment: ein Themenwechsel ohne
  Ankündigung, eine Werbeeinblendung, eine lange Vorbereitung. Mit `--transcript` zeigt das Werkzeug,
  was an der Stelle gesagt wurde. Erst das macht den Bericht umsetzbar statt nur interessant.
- **RUTSCHEN** - der gleichmäßige Verlust im Mittelteil. Ein flaches Rutschen ist ein Tempo-Problem.
  Die Lösung ist kürzen, nicht umschreiben.

## Was du zurückgibst

Nenne den einen größten Verlust und eine Änderung dafür. Keine Liste mit fünf. Den Rest nur auf
Nachfrage. Ist der Hook-Verlust gesund und das Rutschen flach, sag ehrlich, dass das Video in Ordnung
ist und das Problem beim Packaging liegt, und verweise auf `/yt-package`.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
