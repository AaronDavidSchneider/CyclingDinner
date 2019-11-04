# Cycling Dinner Optimizer

## Python Script zur numerischen bestimmung der idealen Konfiguration bei einem Cycling Dinner

### Spielprinzip:

Es bilden sich jeweils Teams aus zwei Personen. Jedes Team entscheidet sich für einen Gang (in der Regel entweder Vorspeise, Hauptgang oder Nachtisch), den das Team dann bei sich zu Hause vorbereitet.
Die Teams erhalten zu Beginn des CyclinDinners die Adressen zu denen sie für die anderen Gänge radeln müssen. Bei jedem Gang trifft das Team auf 2 weitere Teams (im Fall von drei Gängen).

_Rahmenbedingungen für die Verteilung:_
1. Es gibt gleich viele Teams für jeden Gang (die anzahl der teams muss z.b. durch drei teilbar sein)
2. Mindestens doppelt so viele Teams wie Gänge haben sich angemeldet

_Verteilprinzip:_
1. Zwei Teams dürfen sich höchstens einmal treffen
2. Bei jedem Gang treffen sich immer Leute die einen anderen Gang vorbereiten
3. Möglichst kurze Wege zwischen den einzelnen Gängen

### Funktionsweise:

Dieser Code versucht zufällige (unterschiedliche) Kombinationen nach dem oben erklärtem Verteilprinzip zu erstellen und dann mittels einer Maps API (im Moment google maps) herauszufinden, welche Kombination die kürzesten Wege benötigt.
Warum zufällige Kombinationen? Einfach weil die Anzahl an möglichen Kombinationen sehr schnell höher ist als ein Computer testen kann.

Als Input verwendet dieser Code eine normale `.csv`  Liste mit den Daten der Teams. Diese kann zum Beispiel mit Google Forms erstellt werden.

Siehe beispielsweise: <https://forms.gle/QGrag6b2T4T4HFYK9>

### Installation:

Die Benutzung dieses Scripts erfordert eine standard Python Installation mit Numpy, Pandas und itertools

Maps API installieren:

    pip install googlemaps

Google Maps API key auf <https://cloud.google.com/maps-platform/> beantragen.

### Konfiguration:

Im Ordner `source`die Datei `config.py` anpassen.

_Beispiel Konfiguration:_

    API_KEY = "blablub"  # google maps api key
    iterations = 1000  # Anzahl an Konfiguration die getestet werden sollen
    N_courses = 3
    max_api_calls = 0
    ANMELDUNGEN = "export.csv"
    EINLADUNGS_TEMPLATE = "einladung.txt"

    # TIME SETTINGS FOR TRANSIT MODE
    TIMEZONE = +1  # BERLIN TIME
    YEAR = "2019"
    MONTH = "11"
    DAY = "8"
    TIMES = ["17:30","20:30","22:00"] # times of courses

**Vorsicht:** Bei hohen `iterations` kann es sein, dass der Code sehr lange läuft!

**Falls eine andere Googleform verwendet wird (andere Formatierung), muss man `import_data.py` anpassen.**

### Anwendung:

`python main.py`

### Todo:

-   [x] `import_data.py` anpassen (noch unvollständig)
-   [x] some more testing
-   [x] Loss (ist quadratische Addition der Distanzen sinnvoll?) überdenken
-   [ ] Exceptions einbauen (aktuell keine Zeit)
-   [ ] Mit Einzelanmeldungen umgehen lernen... (nicht sinnvoll, besser per Hand)
-   [ ] funktionen in der Main aufräumen

### Anmerkung:

Der Code wurde getestet und funktioniert. Jedoch ist er nicht allgemein genug:

-   Funktioniert bisher nur mit 3 Gängen
    Falls bei der Verwendung Probleme auftauchen, gerne melden
