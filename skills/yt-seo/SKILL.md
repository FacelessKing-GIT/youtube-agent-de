---
name: yt-seo
description: >-
  Schreibt Beschreibung, Tags und Suchtexte für ein YouTube-Video, ausgerichtet
  auf die Suchanfrage, die ein echter Mensch eintippt. Nutzen bei "schreib
  meine Beschreibung", "Tags", "SEO", "hilf dem Video, gefunden zu werden",
  "niemand findet das".
---

# yt-seo

Die Suche ist ein kleinerer Hebel als das Packaging, bei zeitlosen Videos aber ein größerer, als die
meisten denken. Ist das Video für den Abo-Feed gedacht, sag das und steck die Mühe lieber in `/yt-package`.

## Bevor du schreibst

1. Lies `~/.claude/youtube/voice.md`, falls vorhanden. Fehlt die Datei, frag nach **drei eigenen
   Videos**, leite die Stimme ab und schreib die Datei.
2. Erfinde nie eine Zahl, ein Ergebnis oder eine Quelle. Frag danach oder lass sie weg.
3. Schreib auf Deutsch. Englische Fachbegriffe nur, wenn die Zielgruppe sie so sucht (z. B. "Claude Code").

## Die Beschreibung

- **Nur die ersten zwei Zeilen werden gelesen.** Sie stehen vor "...mehr" und sind der Suchausschnitt.
  Sag, was das Video bringt, in den Worten, die die Leute eingetippt hätten.
- Dann der Link oder die Ressource, falls es eine gibt, damit sie ohne Aufklappen sichtbar ist.
- Dann die Kapitel (`/yt-chapters` schreibt sie).
- Dann die lange Version: was behandelt wird, für wen es ist, was vorausgesetzt wird.

## Tags, ehrlich gesagt

Tags sind ein schwaches Signal, und YouTube sagt das selbst. Nutze sie zur Unterscheidung:
Schreibweisen, Toolnamen, Abkürzungen, die die Leute wirklich eintippen. Dann ist Schluss. Fünfzehn
reichen. Eine Wand aus Tags ist keine Strategie, und unpassende Tags reinzustopfen verstößt gegen die
Nutzungsbedingungen.

## Der Suchanfragen-Test

Bevor du etwas abgibst: Schreib die drei Suchanfragen auf, die dieses Video gewinnen soll, und prüfe,
ob Titel und die ersten zwei Beschreibungszeilen deren Wörter enthalten. Wenn nicht, liegt das Problem
beim Titel, nicht bei der Beschreibung.

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
