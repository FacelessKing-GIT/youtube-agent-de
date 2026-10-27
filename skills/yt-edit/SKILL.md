---
name: yt-edit
description: >-
  Macht aus dem Transkript einer Rohaufnahme eine Schnittliste - Leerlauf,
  Füllwörter und Neuansätze, mit Timecodes. Nutzen bei "schneid das",
  "Pausen raus", "mach das Video kürzer", "ich hab rumgelabert" oder wenn
  Material anhand eines Transkripts gekürzt werden soll.
---

# yt-edit

Eine Schnittliste aus einem Transkript mit Zeitstempeln. Das Werkzeug listet die Schnitte, du setzt sie um.

```bash
python3 deadair.py transkript.srt              # srt, vtt oder Whisper-JSON
python3 deadair.py transkript.srt --floor 0.35 --json
```

Noch kein Transkript? Frag danach oder erzeug zuerst eins: `whisper`, `faster-whisper` oder die
Untertitel, die YouTube bei einem nicht gelisteten Upload erstellt, funktionieren alle. Rate keine Zeiten.

## Was es findet

- **LEER** - Pausen länger als die Schwelle, aus der MITTE geschnitten, damit beide Seiten einen Atemzug
  behalten. Wer direkt an der Sprache schneidet, bekommt eine gehetzte, atemlose Aufnahme.
- **FÜLL** - Abschnitte, die nur aus "äh", "also ja", "quasi" bestehen.
- **NEU** - ein neu angefangener Satz. Verglichen mit dem letzten Abschnitt, der wirklich Sprache war,
  nicht mit dem direkt davor, weil zwischen zwei Versuchen meistens ein "äh" liegt.

## Was es nicht tut

Es fasst keine Mediendatei an und hat keine Meinung zu deinem B-Roll. 40 % Kürzung im Bericht heißt
40 % der SPRACHE. Enthält das Video eine lange stille Demo, stimmt die Zahl nicht. Vergleich den Bericht
mit dem Material, bevor du der Laufzeit unten traust.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
