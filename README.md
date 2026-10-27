# YouTube-Agent für Claude - deutsche Fassung

Elf Claude-Skills, die dir beim Führen eines YouTube-Kanals helfen. Kostenlos, MIT-Lizenz, keine
Anmeldung, kein API-Key, nichts zu verbinden.

> Deutsche Übertragung von [youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
> von Jake Schincariol (MIT). Alle Skills, Werkzeuge und Hook-Formeln wurden ins Deutsche übertragen;
> die Werkzeuge erkennen deutsche Füllwörter, Stoppwörter und deutsche CSV-Exporte.

**Veröffentlicht wird nichts, bevor du es tust.** Die Skills schreiben, du lädst hoch.

## Installation

In Claude Code einfügen:

```
https://github.com/DEIN-NAME/youtube-agent-de

Installiere diesen Skill und prüfe dann, ob /yt-script funktioniert.
```

Oder selbst im Terminal:

```bash
git clone https://github.com/DEIN-NAME/youtube-agent-de.git youtube-agent-de
cp -r youtube-agent-de/skills/yt-* ~/.claude/skills/
```

Nur für ein Projekt: dieselben Ordner nach `.claude/skills/` im Projekt kopieren. Ohne Claude Code:
Eine einzelne `SKILL.md` an den Anfang eines normalen Claude-Chats kopieren, dann läuft sie als Modus,
allerdings ohne die sechs Python-Werkzeuge.

Danach zehn Minuten in [`templates/voice.md`](templates/voice.md) stecken: nach
`~/.claude/youtube/voice.md` kopieren und ausfüllen, oder Claude drei eigene Videos schicken und sagen
"Schreib meine voice.md aus diesen Videos". Jeder Skill liest diese Datei.

## Die elf Skills

| Befehl | Was er tut |
| --- | --- |
| `/yt-script` | Aus einer Idee ein Skript. Fünf Hooks nach [21 Formeln](skills/yt-script/hooks.json), bewertet, dann das Sprechskript mit markierten Retention-Beats. |
| `/yt-package` | Titel und Thumbnail als ein Paar, geprüft auf Abschneiden, Wiederholung und vage Wörter. |
| `/yt-edit` | Aus einem Transkript eine Schnittliste: Pausen, Füllwörter, Neuansätze, mit Timecodes. |
| `/yt-comment` | Kommentare in vier Stapel sortiert, Antworten in deiner Stimme, Empfehlung zum Anpinnen. |
| `/yt-plan` | Eine Woche, die zu deiner echten Zeit passt. Ein Hauptvideo, ein schnelles, drei Shorts. |
| `/yt-viral` | Was in deiner Nische läuft, gerankt nach dem Vielfachen des Kanal-eigenen Medians. |
| `/yt-retention` | Dein Retention-Export richtig gelesen: Hook-Verlust, Abstürze, Rutschen, und was zu ändern ist. |
| `/yt-shorts` | Die Shorts, die schon in einem langen Video stecken, mit neuem ersten Satz für jeden. |
| `/yt-seo` | Beschreibung, sinnvolle Tags und die drei Suchanfragen, die das Video gewinnen soll. |
| `/yt-chapters` | Kapitel aus dem Transkript, geprüft gegen YouTubes Regeln, damit sie angezeigt werden. |
| `/yt-audit` | Der ganze Kanal, mit EINER Maßnahme am Ende statt zwanzig. |

## Die sechs Werkzeuge

Alle laufen mit normalem Python 3 ohne Zusatzpakete.

```bash
python3 skills/yt-script/hookscore.py --hook "ein Satz"          # Hook-Bewertung, 5 Eigenschaften
python3 skills/yt-package/title.py --title "..." --thumb "..."   # Titel + Thumbnail prüfen
python3 skills/yt-edit/deadair.py transkript.srt                 # Schnittliste
python3 skills/yt-chapters/chapters.py transkript.srt            # geprüfte Kapitel
python3 skills/yt-retention/retention.py retention.csv           # wo die Leute gehen, und warum
python3 skills/yt-viral/swipe.py gesammelt.json --min 2.0        # Ausreißer nach Kanal-Vielfachem
```

Unter Windows heißt der Befehl oft `python` statt `python3`.

## Das Kleingedruckte

**Es veröffentlicht nichts.** Jeder Skill endet mit einem Block zum Kopieren und der Frage
"Veröffentlichen oder ändern?".

**`hookscore.py` ist eine Faustregel, keine Vorhersage.** Das Original wurde an englischen Hooks
kalibriert; die deutschen Wortlisten sind übertragen und nicht neu kalibriert. Ein niedriger Wert ist
ein Grund, nochmal hinzuschauen, ein hoher ist kein Versprechen auf Aufrufe.

**Die Formel beschreibt den Titel, nicht den Erfolg.** Wenn `/yt-viral` eine Formel nennt, ist das eine
Einschätzung der Wörter, keine Erklärung, warum das Video lief.

**`/yt-viral` liest nur öffentliche Daten.** Es loggt sich nie ein und fasst nie dein Konto an.

**Tags sind fast egal**, und das Paket sagt das, statt dir einen Tag-Generator zu verkaufen.

**Keine erfundenen Zahlen.** Fehlt einem Skill eine Zahl, fragt er nach oder schreibt den Satz ohne sie.

## Lizenz

MIT, siehe [LICENSE](LICENSE). Original © 2026 Jake Schincariol.
