---
name: yt-audit
description: >-
  Prüft einen YouTube-Kanal von vorne bis hinten - Packaging, Regelmäßigkeit,
  die ersten fünfzehn Sekunden und was zuerst zu beheben ist. Nutzen bei
  "prüf meinen Kanal", "warum wächst mein Kanal nicht", "schau dir meine
  Videos an" oder einer eingefügten Kanal-URL.
---

# yt-audit

Ein Audit mit zwanzig Problemen ist eine Methode, dem einen auszuweichen, das zählt. Dieses endet mit
EINER Maßnahme.

## Bevor du schreibst

1. Lies `~/.claude/youtube/voice.md`, falls vorhanden. Fehlt die Datei, frag nach **drei eigenen
   Videos**, leite die Stimme ab und schreib die Datei.
2. Erfinde nie eine Zahl, ein Ergebnis oder eine Quelle. Frag danach oder lass sie weg.

## Was du anschaust, in dieser Reihenfolge

1. **Die letzten zehn Titel als Ganzes.** Lies sie als Liste, so wie die Kanalseite sie zeigt.
   Versprechen sie verschiedene Dinge? Lass sie durch `../yt-package/title.py` laufen. Hat jeder Titel
   dieselbe Form, ist es ein Format-Problem, kein Titel-Problem.
2. **Die Thumbnails in Feed-Größe.** Verkleinere sie. Was bleibt lesbar? Sind drei davon in dieser Größe
   unlesbar, ist das die Maßnahme, und alles andere ist noch egal.
3. **Die ersten fünfzehn Sekunden der drei neuesten Videos.** Transkribieren und mit
   `../yt-script/hookscore.py` bewerten. Hier verlieren die meisten Kanäle.
4. **Upload-Rhythmus.** Nicht Häufigkeit, sondern REGELMÄSSIGKEIT. Sechs Videos in einer Woche und dann
   einen Monat nichts ist schlechter als für immer eins alle zwei Wochen.
5. **Die Retention-Kurve**, falls sie exportiert werden kann: `/yt-retention`.

## Was du zurückgibst

- Die eine größte Maßnahme, benannt, mit dem, was diese Woche zu tun ist.
- Drei Dinge, die schon funktionieren, damit sie nicht kaputtgemacht werden. Sei konkret: "Deine
  Energie ist gut" ist keine Beobachtung.
- Was man noch NICHT tun sollte, und warum.

Beginne ein Audit nie mit Lob, das du nicht meinst, und beende es nie mit einer Liste von zwanzig Punkten.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
