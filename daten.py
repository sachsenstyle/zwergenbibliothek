# Zentrale Liste aller Bücher. Aus dieser Datei baut bauen.py die Seiten.
import re

WP = "https://zwergenbibliothek.wordpress.com"
UPLOADS = WP + "/wp-content/uploads/"


def lokal(pfad):
    """'2026/09/presentation.png' -> 'bilder/2026-09-presentation.webp'"""
    pfad = pfad.split("?")[0]
    pfad = re.sub(r"\.[A-Za-z0-9]+$", "", pfad)
    name = re.sub(r"[^a-z0-9]+", "-", pfad.lower()).strip("-")
    return "bilder/" + name + ".webp"


# abschnitt: Überschrift auf der Kategorie-Seite
BUECHER = [
    # --- Ratgeber & Arbeitsbücher ---
    dict(slug="ki-und-trading-fur-anfanger-das-ki-trading-arbeitsbuch-band-3", seite="ratgeber", abschnitt="Ratgeber",
         post="/2026/09/28/ki-und-trading-fur-anfanger-das-ki-trading-arbeitsbuch-band-3/",
         cover="2026/09/presentation.png", start_cover="2026/09/bild_27.09.26_um_13.44.jpeg",
         teaser="Eine verständliche Reise in die Welt von KI und Trading – mit Analysen, Risiken, Routinen und der Frage, wie Künstliche Intelligenz sinnvoll unterstützen kann, ohne die eigenen Entscheidungen zu übernehmen …"),
    dict(slug="mein-weg-in-die-kreativitat-wie-alles-begann", seite="ratgeber", abschnitt="Ratgeber",
         post="/2025/12/23/mein-weg-in-die-kreativitat-wie-alles-begann/", cover="2025/12/presentation-2.png",
         teaser="Eine persönliche Reise zu den ersten kreativen Ideen, Zweifeln, Erfahrungen und dem Mut, den eigenen Weg zu beginnen …"),
    dict(slug="borse-und-investieren-nachhaltig-geld-anlegen", seite="ratgeber", abschnitt="Ratgeber",
         post="/2025/11/03/borse-und-investieren-nachhaltig-geld-anlegen/", cover="2025/11/presentation-2.png",
         teaser="Ein verständlicher Einstieg in die Welt von Börse und Investieren mit Grundlagen, Strategien und ersten Schritten zum eigenen Vermögensaufbau …"),
    dict(slug="richtig-mahnen-rechtssicher-handeln", seite="ratgeber", abschnitt="Ratgeber",
         post="/2025/07/14/richtig-mahnen-rechtssicher-handeln/", cover="2025/07/richtig-mahnen.png",
         teaser="Ein praxisnaher Leitfaden zum korrekten Mahnen, der zeigt, wie Forderungen strukturiert, sachlich und rechtssicher durchgesetzt werden können …"),
    dict(slug="ki-als-partner-das-affiliate-arbeitsbuch", seite="ratgeber", abschnitt="Arbeitsbücher",
         post="/2026/07/20/ki-als-partner-das-affiliate-arbeitsbuch/", cover="2026/07/presentation.png",
         teaser="Ein praxisnahes Arbeitsbuch für Affiliate-Marketing mit KI, fertigen Prompts, klaren Aufgaben und einem konkreten 30-Tage-Plan für den Aufbau deines eigenen Online-Business …"),
    dict(slug="affiliate-marketing-2025-neu-gedacht-ki-smart", seite="ratgeber", abschnitt="Arbeitsbücher",
         post="/2025/08/04/affiliate-marketing-2025-neu-gedacht-ki-smart/", cover="2025/08/presentation-1.png",
         teaser="Ein moderner Blick auf Affiliate-Marketing mit neuen Strategien, digitalen Möglichkeiten und praxisnahen Ansätzen für den Aufbau nachhaltiger Einnahmen …"),
    dict(slug="trading-mit-ki-bots-fur-einsteiger", seite="ratgeber", abschnitt="Arbeitsbücher",
         post="/2025/07/14/trading-mit-ki-bots-fur-einsteiger/", cover="2025/07/ki-1.png",
         teaser="Ein verständlicher Einstieg in automatisiertes Trading mit KI-Bots, der Grundlagen erklärt und Schritt für Schritt an erste Strategien heranführt …"),
    dict(slug="affiliate-marketing-2025-26-warum-ein-arbeitsbuch-fur-6-monate-sinnvoll-ist", seite="ratgeber", abschnitt="Arbeitsbücher",
         post="/2025/09/22/affiliate-marketing-2025-26-warum-ein-arbeitsbuch-fur-6-monate-sinnvoll-ist/", cover="2025/09/presentation.png",
         teaser="Ein aktueller Leitfaden zu Affiliate-Marketing 2025/26 mit neuen Strategien, digitalen Trends und klaren Wegen zum nachhaltigen Online-Einkommen …"),
    dict(slug="trading-mit-ki-bots-band-2", seite="ratgeber", abschnitt="Arbeitsbücher",
         post="/2025/12/23/trading-mit-ki-bots-band-2/", cover="2025/12/presentation.png",
         teaser="Ein praxisorientierter Leitfaden, der zeigt, wie automatisiertes Trading mit KI-Bots auch mit kleinen Beträgen strukturiert und verständlich umgesetzt werden kann …"),
    # --- Krimis & Romane ---
    dict(slug="k17-erster-fall", seite="krimis", abschnitt="Krimis",
         post="/2026/06/01/k17-erster-fall/", cover="2025/11/whatsapp-image-2025-11-17-at-11.40.53.jpeg",
         teaser="Ein München-Ost-Krimi: Manche Krimis arbeiten mit großen Gesten und spektakulären Showdowns. „K17 – Erster Fall“ geht einen anderen Weg – Schichtdienst, Papierstapel, kleine Beobachtungen und ein Team, das sich aufeinander verlässt …"),
    # --- Kinderbücher & Geschichten ---
    dict(slug="willis-adventskalender-ausmalen-vorlesen-im-advent", seite="kinder", abschnitt="Kinderbücher",
         post="/2026/10/19/willis-adventskalender-ausmalen-vorlesen-im-advent/", cover="2026/10/presentation-1.png",
         start_cover="2026/10/img_01458b9e7b6a-1.jpeg",
         teaser="Ein liebevoll gestalteter Adventskalender mit 24 kleinen Geschichten und passenden Ausmalbildern, der Kinder gemeinsam mit Zwerg Willi durch die Weihnachtszeit begleitet und zum Zuhören, Malen und Träumen einlädt."),
    dict(slug="meine-fantasiewelt-zum-ausmalen", seite="kinder", abschnitt="Kinderbücher",
         post="/2026/06/29/meine-fantasiewelt-zum-ausmalen/",
         titel="Meine Fantasiewelt zum Ausmalen", cover="2026/06/presentation.png",
         teaser="Ein fantasievolles Ausmalbuch voller kleiner Geschichten, magischer Orte und bunter Abenteuer, die Kinder zum Träumen, Malen und Weitererzählen einladen."),
    dict(slug="lena-und-max-huter-der-weihnachtsmagie", seite="kinder", abschnitt="Geschichten",
         post="/2025/11/03/lena-und-max-huter-der-weihnachtsmagie/", cover="2025/11/presentation-1.png",
         teaser="Eine winterliche Geschichte über Freundschaft, Mut und die leise Magie, die in der Weihnachtszeit spürbar wird. Lena und Max begeben sich auf ein Abenteuer, das zeigt, dass Wunder oft dort beginnen, wo man sie am wenigsten erwartet."),
    # --- Notizbücher & Rezeptbücher ---
    dict(slug="ideenimperium-jeder-strich-ein-neuer-anfang", seite="notiz", abschnitt="Notizbücher",
         post="/2026/06/29/ideenimperium-jeder-strich-ein-neuer-anfang/", cover="2026/06/presentation-1.png",
         teaser="Für all die Gedanken, die bleiben sollen, braucht es manchmal nur eine freie Seite. In diesem Notizbuch finden Ideen, Pläne, Skizzen und kleine Einfälle ihren Platz. Jede Seite lädt dazu ein, loszuschreiben, weiterzudenken und aus einem einzelnen Strich vielleicht den Anfang von etwas Größerem zu machen."),
    dict(slug="ideenimperium-jeder-strich-ein-neuer-anfang-2", seite="notiz", abschnitt="Notizbücher",
         post="/2026/06/29/ideenimperium-jeder-strich-ein-neuer-anfang-2/", cover="2026/06/presentation-2.png",
         teaser="Einige Gedanken entstehen leise und entwickeln sich erst mit der Zeit. Dieses Notizbuch bietet den passenden Raum, um Gedanken festzuhalten, Pläne zu strukturieren, Skizzen auszuprobieren und Einfälle wachsen zu lassen – bis aus ersten Ansätzen etwas ganz Eigenes entsteht."),
    dict(slug="tiefsee-geheimnisse-ein-ort-fur-ihre-gedanken-und-traume", seite="notiz", abschnitt="Notizbücher",
         post="/2026/06/29/tiefsee-geheimnisse-ein-ort-fur-ihre-gedanken-und-traume/", cover="2026/06/presentation-3.png",
         teaser="Wie ein Blick unter die Wasseroberfläche öffnet dieses Notizbuch einen ruhigen Raum für alles, was festgehalten werden möchte. Träume, Erinnerungen, Ideen und kleine Einfälle finden hier ihren Platz. Jede Seite lädt dazu ein, abzutauchen, Gedanken zu sammeln und aus stillen Momenten etwas Eigenes entstehen zu lassen."),
    dict(slug="50-krauter-und-gewurze-und-alles-was-man-mit-ihnen-machen-kann", seite="notiz", abschnitt="Rezeptbücher",
         post="/2026/10/05/50-krauter-und-gewurze-und-alles-was-man-mit-ihnen-machen-kann/", cover="2026/10/presentation.png",
         start_cover="2026/10/c2cb6e49-7b33-4ee7-94b4-24ac943afdc8_4_5005_c.jpeg",
         teaser="Ich finde es spannend zu sehen, wie vielseitig Kräuter und Gewürze eigentlich sein können. Dieses Buch lädt dazu ein, 50 davon genauer kennenzulernen, neue Verwendungsmöglichkeiten zu entdecken und vielleicht auch das eine oder andere selbst auszuprobieren – egal ob in der Küche, beim Anbau oder mit einem der passenden Rezepte."),
    dict(slug="notiert-gewurzt-mein-personliches-rezeptbuch", seite="notiz", abschnitt="Rezeptbücher",
         post="/2025/03/31/notiert-gewurzt-mein-personliches-rezeptbuch/", cover="2025/07/cover-rezeptbuch.png",
         teaser="Dieses Rezeptbuch bietet Raum, eigene Lieblingsgerichte festzuhalten und persönliche Küchenerinnerungen zu bewahren. Jede Seite lädt dazu ein, Rezepte, Ideen und Erfahrungen dauerhaft aufzuschreiben und immer wieder neu zu entdecken."),
]

# Weitere Bilder (Kopfbild, Kategorie-Kacheln, Autorinnen-Foto …): (Pfad, maximale Breite)
SONSTIGE_BILDER = [
    ("2025/07/cropped-chatgpt-image-14.-juli-2025-10_53_52.png", 1800),  # Kopfbild (Bücherregal)
    ("2026/02/70dfc647-aa38-4ed1-a8e4-b9f828e9d7eb.png", 700),            # Kachel Ratgeber
    ("2026/02/1f86e0ce-32e9-4a55-ba1a-c99151a235d9.png", 700),            # Kachel Krimis
    ("2026/02/233bd521-6b30-4d90-9115-2976ab0a47ea.png", 700),            # Kachel Kinder
    ("2026/02/9dd0f408-b2a8-4e77-9b89-f146c7803384-edited-1.png", 700),   # Kachel Gastautoren
    ("2026/02/0dc21a28-bc77-4799-beb6-d861e27a851e-edited.png", 700),     # Kachel Notizbücher
    ("2026/02/8d120158-3eaa-425b-962f-79ff18faff08-edited.png", 700),     # Kachel Kontakt
    ("2025/07/whatsapp-image-2025-07-14-at-10.39.17.jpeg", 700),          # Foto Über mich
    ("2026/02/storie-highlights-cover-mira-soren-1.png", 700),            # Gastautorin
]
