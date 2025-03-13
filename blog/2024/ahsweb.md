# Überblick Webdesign und Webseiten-Entwicklung für AHS Schüler:innen

Ein Lehrer der AHS Akademisches Gymnasium Innsbruck (Angerzellgasse) hat mich gefragt, ob ich eine Übersicht über Webdesign und Webseiten-Entwicklung für Schüler:innen eines Wahlpflichtfaches Informatik erstellen kann.
In einer Stunde kann ich nicht viel mehr als einen Überblick geben.
Hier ist der Inhalt, den ich in einer Stunde präsentieren würde:

## HTML und CSS (und Javascript)?

In Lehrer:innen-Kreisen kursiert oft noch die Idee für Webdesign solle man den Schüler:innen HTML und CSS beibringen. Das ist nicht ganz falsch, hilft aber ansich nicht wirklich weiter. HTML und CSS sind die Grundlagen für einen sehr kleinen Teil des Berufsbildes: für die Darstellung von Webseiten im Webbrowser bzw. einer Webview.

Also ganz kurz: HTML ist die Struktur einer Webseite, CSS ist das Aussehen einer Webseite.
In HTML werden Elemente wie Überschriften, Absätze, Bilder, Links, Tabellen, Formulare, etc. definiert. In CSS werden diese Elemente gestaltet.

Beispiel:

```html
<article class="content">
    <h1>Das ist eine Überschrift</h1>
    <p>Das ist ein <strong>fetter</strong> Absatz</p>
    <img src="bild.jpg" />
</article>
```

```css
article.content {
    background-color: #f0f0f0;
    padding: 10px;
    border: 1px solid #ccc;
}
```

Wer da mehr wissen will, kann sich das [HTML und CSS Tutorial von SelfHTML](https://wiki.selfhtml.org/wiki/HTML/Tutorials) ansehen.

Dazu muss noch gesagt werden, dass alle komplexeren Webseiten inzwischen mit Frameworks arbeiten, die das Schreiben von HTML und CSS vereinfachen.

HTML wird per programmierbaren Templates aus verschiedenen Dateien zusammengesetzt.

CSS wird in SCSS oder LESS geschrieben und dann in CSS umgewandelt. SCSS und LESS sind CSS-Präprozessoren, die mehr Flexibilität und Programmierung ermöglichen.

Und jetzt kommt sicher die frage nach JavaScript!

Javascript ist die Programmiersprache, die im Webbrowser ausgeführt wird. Da im Webbrowser (ausser mit Tricks) keine andere Programmiersprache ausgeführt werden kann, ist Javascript die einzige Möglichkeit, um Webseiten im Browser zu programmieren.

Javascript wird für Interaktionen auf Webseiten verwendet. Das können einfache Dinge wie das Ein- und Ausblenden von Elementen sein, aber auch komplexe Anwendungen wie Google Maps, MS Teams, Instagram, Tiktok, Mastodon, etc. sind in Javascript geschrieben.

Javascript kann auch auf dem Server ausgeführt werden. Das ist aber ein anderes Thema.

## Wenn das nicht so wichtig ist. Was denn dann?

**Ja wie funkltioniert denn so eine Webseite?**

**Oder wie kommt man zu einer Webseite?**

Gut, da muss ich mal was an die Tafel Pinseln...

Mal die Stichworte aufschreiben:


### Das Design

Stichworte

- Informationsdesign
    - Was will ich mitteilen?
    - Wie strukturiere ich Informationen?
    - Wie präsentiere ich Informationen?
        - Medien (Text, Bild, Grafiken, Video, Audio)
        - Reihenfolge
        - Textaufbereitung (Überschriften, Absätze, Listen, Tabellen)
        - Textstil: Akademisch, Jugendlich, Technisch, etc.
    - ...
- Interaktionsdesign (Navigation, Buttons, etc.)
    - Wie bewegt sich der Benutzer durch die Webseite?
    - Wie interagiert der Benutzer mit der Webseite?
    - Wie reagiert die Webseite auf Benutzerinteraktionen?
    - Wie reagiert die Webseite auf Benutzerfehler?
    - Wie verhält sich die Webseite auf verschiedenen Geräten?
    - Welche Plattformen werden verknüpft?
    - ...
- Grafikdesign
    - Welche Stimmung soll die Webseite vermitteln?
    - Welche Farben, Schriften, Formen, Bilder, Videos, etc. passen dazu?
    - Wie ist das Layout der Webseite?
    - Wie ist die Typografie der Webseite?
    - Wie wird die Webseite auf verschiedenen Geräten dargestellt?
    - ...

Prozess:
- Moodboard erstellen
- Wireframes erstellen
- Prototypen mit klickbaren Verläufen erstellen
- Detailausarbeitung von Seiten oder Komponenten der Webseite
- Styleguide/ Designsystem
- ...
-
-
### Die Technik

- Webbrowser / Webview
- Webserver / Webhosting
    - Static Site Hosting
    - Dynamic Site Hosting
    - "Cloud" Hosting
        - Platform (Kubernetes; Anbieter z.b. AWS, Google, Azure, etc.)
        - SaaS (Software as a Service)
    - Domain/ DNS
    - Anfrage / Antwort (Request/Response)
- Webapplikationen
    - Basis
        - Frontend
        - Backend
        - Datenbank
        - API
    - Content Management Systeme
        - Wordpress
        - Plone
        - Joomla
        - Drupal
        - Typo3
        - 1000 andere
- Static Site Generators
    - Basics erklären
    - Hugo
    - Jekyll
    - Gatsby
    - Sphinx
    - 1000 andere

- Spezialitäten zum Verwirren:
    - Caching-Server: Varnish, Hosted Solutions (Cloudflare, Cloudfront)
    - Firewalls
    - WAF (Web Application Firewall)

Das reicht mal ;-)


### Das Projekt

Stichworte

Kommunikation ist das A und O. Projekte scheitern fast nie an der Technik, am Projektteam aber schon.

Projektmanagement

Grundfrage
- Resourcen
- Kosten
- Zeit

Agil oder Klassisch?

Heutzutage eher Agil, da bessere Ergebnisse und zufriedenere Kunden.

Plannings, Standups. Sprints. Retrospektiven.

Beispiel an aktuellem Projekt erklären.

## Berufsbilder

- IT-Projekt-Manager:in
- Backend-Entwickler:in
- Frontend-Entwickler:in
- Fullstack-Entwickler:in
- Webdesigner:in
- UX-Designer:in
- DevOps-Engineer:in
- Systemadministrator:in


ITOnboard https://www.itonboard.eu/students

ITOnboard Interessentest: https://interesttest.itonboard.eu/


