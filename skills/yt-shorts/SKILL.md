---
name: yt-shorts
description: >-
  Findet die Shorts, die in einem langen Video stecken, und schreibt sie -
  anhand des Transkripts werden Momente gewählt, die allein funktionieren.
  Nutzen bei "mach Shorts daraus", "schneid Clips", "verwerte das Video
  weiter", "was soll ich ausschneiden".
---

# yt-shorts

Ein Short aus einem langen Video ist nicht der Clip vom besten Moment. Es ist ein Moment, der **ohne
das Video drumherum funktioniert**, und davon gibt es viel weniger.

## Auswählen

Lies das Transkript und finde Abschnitte von 20 bis 55 Sekunden, auf die alle drei Punkte zutreffen:

1. Er beginnt mit einem vollständigen Gedanken. Braucht der erste Satz die Minute davor, ist es kein Short.
2. Es gibt eine Wendung: eine Behauptung, dann etwas, das sie verkompliziert oder beweist.
3. Er endet mit einem klaren Satz, nicht mit einem Auslaufen.

Ranke die Kandidaten und zeig die Top 5 mit Timecodes und erstem Satz, damit die Person einen ablehnen
kann, ohne das ganze Transkript zu lesen.

## Jeden einzelnen schreiben

- **Einen NEUEN ersten Satz.** Der Satz aus dem langen Video setzt Wissen voraus, das dieser Zuschauer
  nicht hat. Schreib den Ersatz und lass ihn durch `../yt-script/hookscore.py` laufen.
- **Text im Bild für die ersten zwei Sekunden**, andere Wörter als der gesprochene Satz.
- **Einen Loop-Punkt**: Was der letzte Satz aufbaut, damit der erste Satz es beantwortet.
- Hinweis zum Hochformat: Was aus einem 16:9-Bild herausgeschnitten wird und ob das wichtig ist.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
