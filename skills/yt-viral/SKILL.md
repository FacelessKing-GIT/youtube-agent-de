---
name: yt-viral
description: >-
  Findet, was in der eigenen Nische auf YouTube gerade wirklich
  funktioniert, rankt es danach, wie weit jedes Video seinen eigenen Kanal
  übertroffen hat, und benennt die Formel. Nutzen bei "was läuft gerade",
  "finde virale Videos in meiner Nische", "warum ist das durch die Decke
  gegangen", Konkurrenz-Recherche oder einer Ideensammlung (Swipe-File).
---

# yt-viral

Reine Aufrufzahlen messen die Kanalgröße, nicht die Idee. Hier wird nach dem **Vielfachen des
Kanal-eigenen Medians** gerankt. Nur so geht es wirklich um das Video.

```bash
python3 swipe.py gesammelt.json --min 2.0
```

## Die Eingabe sammeln

Du brauchst **mindestens vier Videos pro Kanal**, sonst ist ein Median bedeutungslos. Das Werkzeug
überspringt solche Kanäle und sagt es dir. Sammle so, wie es der Person passt: `yt-dlp --flat-playlist -J`
auf eine Kanal-URL ist am schnellsten, die öffentliche Seite geht, eine Liste von Hand geht auch.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Lesen, nicht scrapen.** Nur öffentliche Listen, nie eine eingeloggte Sitzung, nie die Zugangsdaten
der Person.

## Die Ausgabe lesen

Das Vielfache ist das Signal. Die Formel-Zeile ist eine Einschätzung des TITELS, abgeglichen mit
[den 21 Formeln](../yt-script/hooks.json). Sie behauptet nicht, warum das Video funktioniert hat, und
das sagst du auch so, wenn du sie präsentierst.

Was du zurückgibst: die Top 5 mit ihrem Vielfachen, die jeweilige Formel und die EINE Gemeinsamkeit im
Aufbau. Dann die ehrlichere Zeile: Welches davon könnte die Person diese Woche selbst machen, in ihrer
Stimme, mit dem, was sie hat?

## Die Freigabe

Hier wird nichts veröffentlicht. Der Skill schreibt, du lädst hoch. Jede Ausgabe endet mit einem Block
zum Kopieren, und die letzte Zeile jedes Durchlaufs ist die Frage: **Veröffentlichen oder ändern?**
