#!/usr/bin/env python3
"""Baut die komplette Webseite aus daten.py und den Texten in inhalt/.

Aufruf (im Ordner der Webseite):  python3 bauen.py
Danach liegen alle fertigen Seiten (.html) direkt in diesem Ordner.
"""
import datetime
import html
import json
import os
import re

from daten import BUECHER, lokal

HIER = os.path.dirname(os.path.abspath(__file__))
JAHR = datetime.date.today().year
E = html.escape
MAIL = "sachsenstyle@t-online.de"
SITE = "Zwergenbibliothek"
UNTERTITEL = "Modern. Vielseitig. Selbst geschrieben."

# ---------------------------------------------------------------- Menü
MENUE = [
    ("Startseite", "index.html"),
    ("Ratgeber & Arbeitsbücher", "ratgeber-arbeitsbuecher.html"),
    ("Krimis & Romane", "krimis-romane.html"),
    ("Kinderbücher & Geschichten", "kinderbuecher-geschichten.html"),
    ("Notizbücher & Rezeptbücher", "notizbuecher-rezeptbuecher.html"),
    ("Gastautoren /-innen", "gastautoren.html"),
    ("Kontakt", "kontakt.html"),
    ("Über Mich", "ueber-mich.html"),
    ("Quiz-Seite", "quiz.html"),
]

KATEGORIEN = {
    "ratgeber": dict(
        datei="ratgeber-arbeitsbuecher.html", titel="Ratgeber & Arbeitsbücher",
        beschreibung="Ratgeber und Arbeitsbücher der Zwergenbibliothek: verständlich erklärt, praxisnah und zum eigenen Ausprobieren.",
        intro=["Hier findest du Ratgeber und Arbeitsbücher, die Wissen verständlich vermitteln und zum eigenen Ausprobieren einladen. Sie bieten Impulse, Orientierung und praktische Ansätze für verschiedene Themen des Alltags und der persönlichen Entwicklung."],
        abschnitte=[
            ("Ratgeber", "Verständlich aufbereitete Inhalte geben Orientierung, regen zum Nachdenken an und eröffnen neue Blickwinkel für Alltag und persönliche Entwicklung.", ""),
            ("Arbeitsbücher", "Mit Raum für eigene Gedanken und praktische Übungen entsteht die Möglichkeit, Themen aktiv zu vertiefen und Schritt für Schritt umzusetzen.", ""),
        ]),
    "krimis": dict(
        datei="krimis-romane.html", titel="Krimis & Romane",
        beschreibung="Krimis und Romane aus der Zwergenbibliothek: Geschichten über Menschen, Entscheidungen und unerwartete Wendungen.",
        intro=["Spannende Geschichten über Menschen, Entscheidungen und Wege, die nicht immer geradlinig verlaufen.",
               "Fälle und Erzählungen, in denen Geheimnisse, Begegnungen und unerwartete Wendungen im Mittelpunkt stehen."],
        abschnitte=[
            ("Krimis", "Spannende Ermittlungen, rätselhafte Fälle und menschliche Abgründe führen Schritt für Schritt zur Wahrheit …", ""),
            ("Romane (Coming Soon)", "Geschichten über Begegnungen, Gefühle und Lebenswege, die von besonderen Momenten und inneren Veränderungen erzählen …",
             "<p class=\"klein\">Eine neue Geschichte wächst im Hintergrund und wird bald ihre Türen öffnen …</p>"),
        ]),
    "kinder": dict(
        datei="kinderbuecher-geschichten.html", titel="Kinderbücher & Geschichten",
        beschreibung="Kinderbücher und Geschichten der Zwergenbibliothek: Fantasie, leise Abenteuer und besondere Momente zum Vorlesen und Selberlesen.",
        intro=["Geschichten voller Fantasie, leiser Abenteuer und besonderer Momente – mal für Kinder, mal für alle, die sich ein Stück Erzählliebe bewahrt haben.",
               "Erzählungen zum Vorlesen, Selberlesen und einfach zum Eintauchen, unabhängig vom Alter."],
        abschnitte=[
            ("Kinderbücher", "Fantasievolle Geschichten, die junge Leser begleiten und zum Staunen, Mitfühlen und Entdecken einladen …", ""),
            ("Geschichten", "Kleine Erzählungen über besondere Momente, Gedanken und Begegnungen, die zum Innehalten und Weiterlesen einladen …", ""),
        ]),
    "notiz": dict(
        datei="notizbuecher-rezeptbuecher.html", titel="Notizbücher & Rezeptbücher",
        beschreibung="Notizbücher und Rezeptbücher der Zwergenbibliothek: Raum für eigene Gedanken, Ideen und Lieblingsrezepte.",
        intro=["Seiten zum Festhalten eigener Gedanken, Ideen und Lieblingsrezepte laden dazu ein, Persönliches aufzuschreiben und zu bewahren.",
               "Bücher, die Raum geben für Kreativität, Erinnerungen und alles, was im Alltag einen festen Platz finden soll."],
        abschnitte=[
            ("Notizbücher", "Raum für Gedanken, Ideen und Notizen, die festgehalten und immer wieder neu entdeckt werden können …", ""),
            ("Rezeptbücher", "Platz für Lieblingsgerichte, Küchenwissen und kleine Entdeckungen rund um Kräuter und Gewürze …", ""),
        ]),
}

# Kleine Korrekturen an Buchtiteln gegenüber WordPress
TITEL_FIX = {
    "k17-erster-fall": "K17 – Erster Fall",
    "ki-und-trading-fur-anfanger-das-ki-trading-arbeitsbuch-band-3": "KI und Trading für Anfänger – Das KI-Trading-Arbeitsbuch, Band 3",
    "ideenimperium-jeder-strich-ein-neuer-anfang-2": "Ideenimperium: Jeder Strich ein neuer Anfang (Ausgabe 2)",
    "notiert-gewurzt-mein-personliches-rezeptbuch": "Notiert & Gewürzt – Mein persönliches Rezeptbuch",
}


def lade_inhalt(name):
    pfad = os.path.join(HIER, "inhalt", name)
    if not os.path.exists(pfad):
        return None
    with open(pfad, encoding="utf-8") as f:
        return f.read()


for b in BUECHER:
    meta = lade_inhalt(b["slug"] + ".json")
    gescrapt = json.loads(meta)["titel"] if meta else ""
    b["titel"] = TITEL_FIX.get(b["slug"]) or b.get("titel") or gescrapt or b["slug"]
    b["kurz"] = re.sub(r"\s*…$", "", b["teaser"])

BUCH = {b["slug"]: b for b in BUECHER}


def buch_link(b, r):
    return f"{r}buecher/{b['slug']}.html" if b["post"] else None


# ---------------------------------------------------------------- Bausteine
def kachel(href, bild, titel, text, r, eng=False, buchbild=False):
    klasse = ' class="buchbild"' if buchbild else ""
    absatz = "<p>" + E(text) + "</p>" if text else ""
    img = f'<img src="{r}{bild}" alt="" loading="lazy"{klasse}>'
    inner = f'{img}<div class="kachel-text"><h3>{E(titel)}</h3>{absatz}'
    if href:
        inner += '<span class="mehr">Mehr erfahren →</span>'
    inner += "</div>"
    if href:
        return f'<a class="kachel" href="{href}">{inner}</a>'
    return f'<div class="kachel">{inner}</div>'


def buch_kachel(b, r, start=False):
    bild = lokal(b["start_cover"]) if start and b.get("start_cover") else lokal(b["cover"])
    return kachel(buch_link(b, r), bild, b["titel"], "" if start else b["kurz"], r, buchbild=True)


def buecher_grid(liste, r, start=False, eng=False):
    klasse = "kacheln eng" if eng else "kacheln"
    return f'<div class="{klasse}">' + "".join(buch_kachel(b, r, start) for b in liste) + "</div>"


def ersetze_root(text, r):
    return text.replace("@ROOT@", r)


def seite(datei, titel, beschreibung, inhalt, h1=None, aktiv=None, gross=False, kopf_extra="", fuss_extra="", r_override=None):
    """Setzt eine komplette HTML-Seite zusammen. datei = Pfad relativ zum Hauptordner."""
    tiefe = datei.count("/")
    r = r_override if r_override is not None else "../" * tiefe
    aktiv = aktiv or datei
    punkte = []
    for name, ziel in MENUE:
        aktuell = ' aria-current="page"' if ziel == aktiv else ""
        punkte.append(f'<li><a href="{r}{ziel}"{aktuell}>{E(name)}</a></li>')
    menue = "".join(punkte)
    ist_start = datei == "index.html"
    seitentitel = f"{SITE} – {UNTERTITEL}" if ist_start else f"{titel} – {SITE}"
    titelblock = ""
    if h1:
        gross_klasse = " gross" if gross else ""
        titelblock = f'<div class="seitentitel{gross_klasse}"><h1>{E(h1)}</h1></div>'
    out = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(seitentitel)}</title>
<meta name="description" content="{E(beschreibung)}">
<meta property="og:title" content="{E(seitentitel)}">
<meta property="og:description" content="{E(beschreibung)}">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%93%9A%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{r}style.css">
<script>document.documentElement.className += ' js';</script>
{kopf_extra}</head>
<body>
<a class="sprung" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf">
  <a class="kopf-titel" href="{r}index.html">{SITE}</a>
  <p class="kopf-untertitel">{UNTERTITEL}</p>
</header>
<nav class="menue" aria-label="Hauptmenü">
  <div class="menue-innen">
    <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="menueliste"><span class="balken" aria-hidden="true"><i></i><i></i><i></i></span>Menü</button>
    <ul id="menueliste">{menue}</ul>
  </div>
</nav>
<main class="hauptteil" id="inhalt">
  <div class="karte">
    {titelblock}
    <div class="inhalt">
{ersetze_root(inhalt, r)}
    </div>
  </div>
</main>
<footer class="fuss">
  <p><a href="{r}impressum.html">Impressum</a><a href="{r}datenschutz.html">Datenschutz</a><a href="{r}kontakt.html">Kontakt</a></p>
  <p>© {JAHR} {SITE} · Nivora Graufeder</p>
  <p class="affiliate">Diese Seite enthält Affiliate-Links (Amazon-Partnerprogramm) – siehe Impressum.</p>
</footer>
<script>
(function () {{
  var m = document.querySelector('.menue'), b = document.querySelector('.menue-knopf');
  if (!m || !b) return;
  b.addEventListener('click', function () {{
    var offen = m.classList.toggle('offen');
    b.setAttribute('aria-expanded', offen ? 'true' : 'false');
  }});
}})();
</script>
{fuss_extra}</body>
</html>
"""
    pfad = os.path.join(HIER, datei)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(out)


# ---------------------------------------------------------------- Startseite
def baue_startseite():
    aktuell = [BUCH[s] for s in (
        "willis-adventskalender-ausmalen-vorlesen-im-advent",
        "50-krauter-und-gewurze-und-alles-was-man-mit-ihnen-machen-kann",
        "ki-und-trading-fur-anfanger-das-ki-trading-arbeitsbuch-band-3")]
    wege = [
        ("Ratgeber & Arbeitsbücher", "Impulse, Wissen und praktische Begleiter für eigene Wege", "ratgeber-arbeitsbuecher.html", "bilder/2026-02-70dfc647-aa38-4ed1-a8e4-b9f828e9d7eb.webp"),
        ("Krimis & Romane", "Spannung, Geschichten und Begegnungen voller Wendungen", "krimis-romane.html", "bilder/2026-02-1f86e0ce-32e9-4a55-ba1a-c99151a235d9.webp"),
        ("Kinderbücher & Geschichten", "Fantasievolle Erzählungen für kleine und große Leser", "kinderbuecher-geschichten.html", "bilder/2026-02-233bd521-6b30-4d90-9115-2976ab0a47ea.webp"),
    ]
    mehr = [
        ("Gastautorin & Gastautor", "Neue Stimmen und kleine Geschichten entdecken", "gastautoren.html", "bilder/2026-02-9dd0f408-b2a8-4e77-9b89-f146c7803384-edited-1.webp"),
        ("Notizbücher & Rezeptbücher", "Raum für eigene Gedanken und Lieblingsrezepte", "notizbuecher-rezeptbuecher.html", "bilder/2026-02-0dc21a28-bc77-4799-beb6-d861e27a851e-edited.webp"),
        ("Kontakt", "Fragen, Austausch oder Zusammenarbeit", "kontakt.html", "bilder/2026-02-8d120158-3eaa-425b-962f-79ff18faff08-edited.webp"),
    ]
    k = lambda liste: '<div class="kacheln">' + "".join(kachel("@ROOT@" + h, bild, t, x, "@ROOT@") for t, x, h, bild in liste) + "</div>"
    inhalt = f"""<p class="lead">Zwischen Büchern entstehen Welten – mal spannend, mal inspirierend, mal voller Fantasie. Die Zwergenbibliothek vereint Geschichten, Ratgeber und kreative Werke, die mit Herz geschrieben und mit Ruhe entdeckt werden möchten. Wähle deinen Weg durch die verschiedenen Buchbereiche und finde genau das, was dich gerade begleitet, inspiriert oder einfach zum Lesen einlädt.</p>
<h2>Wähle deinen Weg durch die Bibliothek</h2>
{k(wege)}
<h2 id="aktuelle-buecher">Aktuelle Bücher</h2>
{buecher_grid(aktuell, "@ROOT@", start=True)}
<h2>Die Idee hinter der Zwergenbibliothek</h2>
<p>Die Zwergenbibliothek ist aus der Freude am Schreiben und Erzählen entstanden – aus Ideen, die mit der Zeit zu Geschichten und Büchern gewachsen sind.</p>
<p>Jedes Werk trägt ein Stück dieser Reise in sich und lädt dazu ein, für einen Moment einzutauchen und Neues zu entdecken.</p>
<h2>Mehr aus der Zwergenbibliothek</h2>
{k(mehr)}
<p class="schluss">Zwischen den Seiten setzt sich die Reise leise fort,<br>während die Bibliothek ihre Türen offen hält.</p>"""
    seite("index.html", "Startseite",
          "Die Zwergenbibliothek: Krimis, Ratgeber, Arbeitsbücher, Kinderbücher, Notizbücher und Rezeptbücher von Nivora Graufeder – mit Herz geschrieben.",
          inhalt, h1="Ein Ort zwischen Geschichten, Gedanken und Magie", gross=True)


# ---------------------------------------------------------------- Kategorien
def baue_kategorien():
    for key, kat in KATEGORIEN.items():
        teile = ["".join(f"<p>{E(p)}</p>" for p in kat["intro"]).replace("<p>", '<p class="lead">', 1)]
        for name, text, extra in kat["abschnitte"]:
            liste = [b for b in BUECHER if b["seite"] == key and b["abschnitt"] == name]
            teile.append(f"<h2>{E(name)}</h2><p>{E(text)}</p>")
            if liste:
                teile.append(buecher_grid(liste, "@ROOT@"))
            teile.append(extra)
        seite(kat["datei"], kat["titel"], kat["beschreibung"], "\n".join(teile), h1=kat["titel"])


# ---------------------------------------------------------------- Buch-Detailseiten
KAUF_BESCHRIFTUNG = {
    "50-krauter-und-gewurze-und-alles-was-man-mit-ihnen-machen-kann": ["Taschenbuch bei Amazon", "Hartcover bei Amazon"],
    "notiert-gewurzt-mein-personliches-rezeptbuch": ["Taschenbuch bei Amazon", "Hartcover bei Amazon"],
}


def kauf_knoepfe(slug, text):
    """Kauf-Knöpfe unter dem Cover: übernimmt die Links der Knöpfe aus dem Buchtext."""
    links = re.findall(r'<a href="([^"]+)" class="button"', text)
    namen = KAUF_BESCHRIFTUNG.get(slug, [])
    html_knoepfe = []
    for i, href in enumerate(links):
        if i < len(namen):
            name = namen[i]
        else:
            name = "Bei Amazon ansehen" if "amazon." in href else "Zum Buch"
        html_knoepfe.append(f'<a class="button buch-kaufen" href="{href}" target="_blank" rel="noopener sponsored">{E(name)}</a>')
    return "".join(html_knoepfe)


def baue_buchseiten():
    for b in BUECHER:
        if not b["post"]:
            continue
        kat = KATEGORIEN[b["seite"]]
        text = lade_inhalt(b["slug"] + ".html") or ""
        kauf = kauf_knoepfe(b["slug"], text)
        inhalt = f"""<article class="buch">
  <div class="buch-bild"><img src="@ROOT@{lokal(b['cover'])}" alt="Buchcover: {E(b['titel'])}">{kauf}</div>
  <div class="buch-text">
{text}
  </div>
</article>
<p class="zurueck"><a href="@ROOT@{kat['datei']}">← Zurück zu „{E(kat['titel'])}“</a></p>"""
        seite(f"buecher/{b['slug']}.html", b["titel"], b["kurz"][:300], inhalt, h1=b["titel"], aktiv=kat["datei"])


# ---------------------------------------------------------------- Einzelseiten
def baue_gastautoren():
    inhalt = """<p class="lead">Dieser Bereich öffnet Raum für Gastautorinnen und Gastautoren, die ihre Geschichten, Gedanken und Texte mit anderen teilen möchten.</p>
<p>Unterschiedliche Stimmen, neue Perspektiven und kleine Erzählungen laden dazu ein, zu lesen, zu entdecken und einen Moment zu verweilen.</p>
<div class="gast">
  <a href="https://seriesmagicx.wordpress.com/mira-soren-blackstar/" target="_blank" rel="noopener"><img src="@ROOT@bilder/2026-02-storie-highlights-cover-mira-soren-1.webp" alt="Mira Soren Blackstar – Geschichten im Zwielicht" loading="lazy"></a>
  <div>
    <h2>Mira Soren Blackstar</h2>
    <p><strong>Geschichten im Zwielicht</strong><br>Romance, Cozy Crime &amp; ein Hauch Magie – erzählt von <a href="https://seriesmagicx.wordpress.com/mira-soren-blackstar/" target="_blank" rel="noopener">Mira Soren Blackstar by Series-Magic</a>.</p>
    <p class="trenner" aria-hidden="true">• • • ✶ • • •</p>
    <p>Geschichten, die zwischen Wirklichkeit und Magie wandern – leise, warm und ein wenig geheimnisvoll.</p>
  </div>
</div>"""
    seite("gastautoren.html", "Gastautoren /-innen",
          "Gastautorinnen und Gastautoren in der Zwergenbibliothek: neue Stimmen und kleine Geschichten.", inhalt, h1="Gastautoren /-innen")


def baue_kontakt():
    inhalt = f"""<p class="lead">Ich freue mich darauf, von dir zu hören! Nutze einfach das Kontaktformular unten, um mir eine Nachricht zu schicken – ob Frage, Feedback oder Buchanfrage.</p>
<h2>📬 Schreib mir direkt</h2>
<form class="formular" id="kontaktformular">
  <label for="k-name">Name <span class="pflicht">(erforderlich)</span>
    <input id="k-name" type="text" autocomplete="name" required></label>
  <label for="k-mail">E-Mail <span class="pflicht">(erforderlich)</span>
    <input id="k-mail" type="email" autocomplete="email" required></label>
  <label for="k-text">Nachricht
    <textarea id="k-text" rows="7" required></textarea></label>
  <button class="button" type="submit">Nachricht vorbereiten</button>
  <p class="klein">Der Knopf öffnet dein E-Mail-Programm mit einer fertig ausgefüllten Nachricht an <strong>{MAIL}</strong>, die du dort nur noch abschicken musst. Alternativ kannst du direkt an diese Adresse schreiben.</p>
  <div class="meldung" id="k-hinweis" role="status" hidden>Dein E-Mail-Programm sollte sich jetzt geöffnet haben. Falls nicht, schreib mir bitte direkt an <a href="mailto:{MAIL}">{MAIL}</a>.</div>
</form>
<p class="klein">Hinweis: Die übermittelten Daten werden nur zur Bearbeitung deiner Anfrage verwendet. Weitere Informationen findest du in meiner <a href="@ROOT@datenschutz.html">Datenschutzerklärung</a>.</p>"""
    skript = f"""<script>
document.getElementById('kontaktformular').addEventListener('submit', function (e) {{
  e.preventDefault();
  var text = 'Name: ' + document.getElementById('k-name').value + '\\n' +
             'E-Mail: ' + document.getElementById('k-mail').value + '\\n\\n' +
             document.getElementById('k-text').value;
  document.getElementById('k-hinweis').hidden = false;
  window.location.href = 'mailto:{MAIL}?subject=' + encodeURIComponent('Nachricht über die Zwergenbibliothek') +
                         '&body=' + encodeURIComponent(text);
}});
</script>
"""
    seite("kontakt.html", "Kontakt", "Kontakt zur Zwergenbibliothek: Fragen, Feedback oder Buchanfragen.", inhalt, h1="Kontakt", fuss_extra=skript)


def baue_ueber_mich():
    inhalt = """<div class="portrait"><img src="@ROOT@bilder/2025-07-whatsapp-image-2025-07-14-at-10-39-17.webp" alt="Nivora, Autorin der Zwergenbibliothek"></div>
<p class="lead">Schön, dass du hier bist! Ich bin die Autorin hinter der Zwergenbibliothek und freue mich, dir ein wenig mehr über mich zu erzählen.</p>
<h2>Wer ich bin</h2>
<p>Hallo, ich bin Nivora – leidenschaftliche Autorin, kreative Macherin und Kopf hinter der Zwergenbibliothek.</p>
<p>Ich schreibe, weil ich es liebe. Mal entstehen Krimis mit Tiefgang, mal moderne Märchen oder ehrliche Ratgeber, die aus dem echten Leben kommen. Alles, was ich veröffentliche, ist selbst erdacht, erlebt oder gründlich recherchiert – je nachdem, was gerade in mir brennt.</p>
<p>Ich bin im Ruhestand, aber Stillstand ist das für mich nicht. Im Gegenteil: Schreiben, gestalten, ausprobieren – das alles ist mein Ausgleich, meine Freude und mein kreatives Zuhause. Ich arbeite mit 3D-Avataren, entwickle Social-Media-Kampagnen, tauche in Themen wie Kryptowährungen oder KI-Trading ein und lasse diese Erfahrungen in meine Projekte einfließen.</p>
<p>Ich mache alles selbst – vom ersten Satz bis zum fertigen Buch.</p>
<p>Und genau das ist mein Antrieb: Etwas schaffen, das bleibt. Bücher, die berühren. Inhalte, die weiterhelfen. Geschichten, die zum Träumen oder Nachdenken anregen.</p>
<p>Das ist kein Beruf, das ist Herzblut.</p>
<h2>Was ich schreibe</h2>
<p>In der Zwergenbibliothek findest du eine bunte Mischung aus Genres: spannende Krimis, fantasievolle Kindergeschichten und hilfreiche Ratgeber für den Alltag. Jedes Buch ist mit viel Herzblut selbst geschrieben.</p>
<h2>Was mir wichtig ist</h2>
<p>Mir liegt am Herzen, Leser*innen mit meinen Büchern zu unterhalten, zum Nachdenken anzuregen oder einfach den Alltag ein bisschen schöner zu machen. Ich möchte Geschichten schaffen, die im Gedächtnis bleiben und Menschen verbinden.</p>
<h2>Neugierig geworden?</h2>
<p>Stöbere gern durch meine Bücher oder schreib mir direkt über das Kontaktformular – ich freue mich auf den Austausch!</p>
<p><a class="button" href="@ROOT@index.html#aktuelle-buecher">Meine Bücher</a></p>"""
    seite("ueber-mich.html", "Über Mich", "Über Nivora, die Autorin hinter der Zwergenbibliothek: Krimis, Kindergeschichten und Ratgeber mit Herzblut.", inhalt, h1="Über Mich")


# ---------------------------------------------------------------- Recht
def datenschutz_anpassen(text):
    teile = re.split(r"(?=<h2>)", text)
    neu = {
        "3.": """<h2><strong>3. Hosting</strong></h2>
<p><strong>Cloudflare Pages</strong></p>
<p>Diese Website wird bei Cloudflare Pages gehostet, einem Angebot der Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA.</p>
<p>Beim Aufruf der Seite verarbeitet Cloudflare automatisch Server-Logfiles (z. B. IP-Adresse, Browsertyp, Datum/Uhrzeit des Zugriffs), um die Website technisch bereitzustellen und die Sicherheit zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer funktionsfähigen, sicheren Website).</p>
<p>Da Cloudflare in den USA sitzt, kann es zu einer Datenübermittlung in ein Drittland kommen. Cloudflare ist unter dem EU-US Data Privacy Framework zertifiziert; zusätzlich gelten EU-Standardvertragsklauseln. Details findest du in der Datenschutzerklärung von Cloudflare: <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">https://www.cloudflare.com/privacypolicy/</a></p>""",
        "4.": """<h2><strong>4. Cookies, Schriften und Quiz</strong></h2>
<p>Diese Website setzt selbst keine Cookies und verwendet keine Analyse- oder Tracking-Dienste.</p>
<p>Die verwendeten Schriften werden von dieser Website selbst ausgeliefert. Es werden dafür keine Daten an Schriftanbieter wie Google übertragen.</p>
<p>Das Quiz läuft vollständig in deinem Browser. Deine Antworten werden weder gespeichert noch an mich oder Dritte übertragen.</p>""",
        "5.": f"""<h2><strong>5. Kontaktaufnahme</strong></h2>
<p>Wenn du mich per E-Mail kontaktierst, werden deine Angaben (E-Mail-Adresse, ggf. Name und Nachricht) zur Bearbeitung deiner Anfrage gespeichert. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche/vertragliche Maßnahmen) bzw. lit. f DSGVO (berechtigtes Interesse an der Beantwortung). Die Daten werden gelöscht, sobald sie für die Bearbeitung nicht mehr erforderlich sind.</p>
<p>Das Kontaktformular auf dieser Website versendet selbst nichts: Es öffnet dein E-Mail-Programm mit einer vorbereiteten Nachricht, die du selbst abschickst. Bis dahin werden keine Daten an mich oder einen Server übertragen.</p>""",
    }
    ergebnis = []
    for t in teile:
        m = re.match(r"<h2><strong>(\d)\.", t)
        if m and (m.group(1) + ".") in neu:
            ergebnis.append(neu[m.group(1) + "."] + "\n")
        else:
            ergebnis.append(t)
    out = "".join(ergebnis)
    out = out.replace("Der eigentliche Buchkauf",
                      "Einige dieser Links laufen zunächst über einen Kurzlink-Dienst (TinyURL) und leiten dann zu Amazon weiter. Der eigentliche Buchkauf", 1)
    out = re.sub(r"Stand: \w+ \d{4}\.", "Stand: November 2026.", out)
    return out


def baue_recht():
    imp = lade_inhalt("impressum.html") or "<p>Impressum fehlt.</p>"
    seite("impressum.html", "Impressum", "Impressum der Zwergenbibliothek.", imp, h1="Impressum", aktiv="__keins__")
    ds = datenschutz_anpassen(lade_inhalt("datenschutz.html") or "<p>Datenschutzerklärung fehlt.</p>")
    seite("datenschutz.html", "Datenschutz", "Datenschutzerklärung der Zwergenbibliothek.", ds, h1="Datenschutzerklärung", aktiv="__keins__")


def baue_404():
    inhalt = """<p class="lead">Diese Seite gibt es leider nicht (mehr). Vielleicht findest du in der Bibliothek etwas anderes, das dich begleitet.</p>
<p><a class="button" href="@ROOT@index.html">Zur Startseite</a></p>"""
    seite("404.html", "Seite nicht gefunden", "Diese Seite wurde nicht gefunden.", inhalt, h1="Seite nicht gefunden",
          aktiv="__keins__", r_override="/")


# ---------------------------------------------------------------- Quiz
def baue_quiz():
    def pick(slug):
        b = BUCH[slug]
        return {"titel": b["titel"], "link": buch_link(b, ""), "cover": lokal(b["cover"])}

    ergebnisse = {
        "krimi": {
            "titel": "Dich zieht es zur Spannung",
            "text": "Du willst Spuren folgen, Widersprüche entdecken und am Ende wissen, was wirklich passiert ist. Ein Krimi mit viel Menschlichkeit und realistischer Polizeiarbeit passt gerade genau zu dir.",
            "buecher": [pick("k17-erster-fall")],
            "mehr": {"label": "Alle Krimis & Romane ansehen", "link": "krimis-romane.html"}},
        "ratgeber": {
            "titel": "Du willst etwas mitnehmen und ausprobieren",
            "text": "Du liest am liebsten Bücher, die dich weiterbringen: verständlich erklärt, mit klaren Schritten und Raum für eigene Gedanken. Diese Ratgeber und Arbeitsbücher sind ein guter Start.",
            "buecher": [pick("mein-weg-in-die-kreativitat-wie-alles-begann"), pick("ki-als-partner-das-affiliate-arbeitsbuch")],
            "mehr": {"label": "Alle Ratgeber & Arbeitsbücher ansehen", "link": "ratgeber-arbeitsbuecher.html"}},
        "kinder": {
            "titel": "Dir ist nach Zauber und Gemütlichkeit",
            "text": "Du magst Geschichten, die leise berühren, zum Vorlesen einladen und ein bisschen Magie in den Tag bringen – für Kinder und für alle, die sich ihre Erzählliebe bewahrt haben.",
            "buecher": [pick("willis-adventskalender-ausmalen-vorlesen-im-advent"), pick("lena-und-max-huter-der-weihnachtsmagie")],
            "mehr": {"label": "Alle Kinderbücher & Geschichten ansehen", "link": "kinderbuecher-geschichten.html"}},
        "notiz": {
            "titel": "Du hältst gern Eigenes fest",
            "text": "Gedanken, Ideen, Lieblingsrezepte: Du bist eher der Typ, der Dinge aufschreibt, sammelt und ausprobiert. Diese Bücher geben dir den Platz dafür.",
            "buecher": [pick("ideenimperium-jeder-strich-ein-neuer-anfang"), pick("50-krauter-und-gewurze-und-alles-was-man-mit-ihnen-machen-kann"), pick("notiert-gewurzt-mein-personliches-rezeptbuch")],
            "mehr": {"label": "Alle Notizbücher & Rezeptbücher ansehen", "link": "notizbuecher-rezeptbuecher.html"}},
    }
    daten = json.dumps(ergebnisse, ensure_ascii=False).replace("</", "<\\/")
    inhalt = """<p class="lead">Fünf kurze Fragen – und die Zwergenbibliothek verrät dir, welches Buch gerade zu dir passt.</p>
<div class="quiz" id="quiz" aria-live="polite">
  <noscript><p class="meldung">Für das Quiz wird JavaScript benötigt. Du kannst stattdessen direkt in der Bibliothek stöbern: <a href="index.html">zur Startseite</a>.</p></noscript>
</div>"""
    skript = f'<script>window.QUIZ_ERGEBNISSE = {daten};</script>\n<script src="quiz.js"></script>\n'
    seite("quiz.html", "Quiz-Seite", "Welches Buch passt heute zu dir? Fünf kurze Fragen, ein Buchtipp aus der Zwergenbibliothek.",
          inhalt, h1="Welches Buch passt heute zu dir?", fuss_extra=skript)


if __name__ == "__main__":
    baue_startseite()
    baue_kategorien()
    baue_buchseiten()
    baue_gastautoren()
    baue_kontakt()
    baue_ueber_mich()
    baue_recht()
    baue_quiz()
    baue_404()
    print("Fertig – Seiten gebaut.")
