/* Quiz: "Welches Buch passt heute zu dir?" – läuft komplett im Browser, nichts wird gespeichert oder gesendet.
   Fragen und Antworten stehen hier unten in "fragen"; k = Bereich, dem die Antwort einen Punkt gibt. */
(function () {
  'use strict';

  var wurzel = document.getElementById('quiz');
  var ERG = window.QUIZ_ERGEBNISSE;
  if (!wurzel || !ERG) return;

  var BEREICHE = ['krimi', 'ratgeber', 'kinder', 'notiz'];

  var fragen = [
    { text: 'Wie soll sich dein nächster Lesemoment anfühlen?', antworten: [
      { t: 'Spannend – ich will unbedingt wissen, wie es ausgeht', k: 'krimi' },
      { t: 'Lehrreich – ich möchte etwas mitnehmen', k: 'ratgeber' },
      { t: 'Märchenhaft und gemütlich', k: 'kinder' },
      { t: 'Ruhig – ich möchte eigene Gedanken festhalten', k: 'notiz' }
    ] },
    { text: 'Wo tauchst du am liebsten in ein Buch ein?', antworten: [
      { t: 'Im Sessel, mit Tee und Licht – gern bis spät in die Nacht', k: 'krimi' },
      { t: 'Am Schreibtisch, mit Stift und Kaffee', k: 'ratgeber' },
      { t: 'Auf dem Sofa, mit Decke und jemandem zum Vorlesen', k: 'kinder' },
      { t: 'In der Küche oder am Fenster, das Notizbuch griffbereit', k: 'notiz' }
    ] },
    { text: 'Welches Wort spricht dich gerade am meisten an?', antworten: [
      { t: 'Rätsel', k: 'krimi' },
      { t: 'Plan', k: 'ratgeber' },
      { t: 'Zauber', k: 'kinder' },
      { t: 'Idee', k: 'notiz' }
    ] },
    { text: 'Wie sieht dein ideales freies Wochenende aus?', antworten: [
      { t: 'Einem kniffligen Rätsel auf der Spur sein', k: 'krimi' },
      { t: 'Etwas Neues lernen und gleich ausprobieren', k: 'ratgeber' },
      { t: 'Basteln, Malen oder Geschichten erzählen', k: 'kinder' },
      { t: 'Lieblingsrezepte kochen und aufschreiben', k: 'notiz' }
    ] },
    { text: 'Was würdest du heute Abend am liebsten tun?', antworten: [
      { t: 'Herausfinden, wer es war', k: 'krimi' },
      { t: 'Meinen Plan endlich Schritt für Schritt angehen', k: 'ratgeber' },
      { t: 'Jemandem eine Geschichte vorlesen', k: 'kinder' },
      { t: 'Die Gedanken des Tages aufschreiben', k: 'notiz' }
    ] }
  ];

  var schritt, punkte, letzte;

  function el(tag, klasse, text) {
    var e = document.createElement(tag);
    if (klasse) e.className = klasse;
    if (text != null) e.textContent = text;
    return e;
  }

  function leeren() {
    while (wurzel.firstChild) wurzel.removeChild(wurzel.firstChild);
  }

  function start(mitFokus) {
    schritt = 0;
    punkte = { krimi: 0, ratgeber: 0, kinder: 0, notiz: 0 };
    letzte = null;
    zeigeFrage(mitFokus);
  }

  function zeigeFrage(mitFokus) {
    var f = fragen[schritt];
    leeren();

    var balken = el('div', 'quiz-fortschritt');
    balken.setAttribute('role', 'progressbar');
    balken.setAttribute('aria-valuemin', '0');
    balken.setAttribute('aria-valuemax', String(fragen.length));
    balken.setAttribute('aria-valuenow', String(schritt));
    balken.setAttribute('aria-label', 'Fortschritt im Quiz');
    var fuellung = el('span');
    fuellung.style.width = (schritt / fragen.length * 100) + '%';
    balken.appendChild(fuellung);
    wurzel.appendChild(balken);

    wurzel.appendChild(el('p', 'quiz-zaehler', 'Frage ' + (schritt + 1) + ' von ' + fragen.length));

    var titel = el('h2', 'quiz-frage', f.text);
    titel.tabIndex = -1;
    wurzel.appendChild(titel);

    var liste = el('ul', 'quiz-antworten');
    f.antworten.forEach(function (a) {
      var li = document.createElement('li');
      var knopf = el('button', 'quiz-antwort', a.t);
      knopf.type = 'button';
      knopf.addEventListener('click', function () { antwort(a.k); });
      li.appendChild(knopf);
      liste.appendChild(li);
    });
    wurzel.appendChild(liste);

    if (mitFokus) titel.focus();
  }

  function antwort(bereich) {
    punkte[bereich] += 1;
    letzte = bereich;
    schritt += 1;
    if (schritt < fragen.length) {
      zeigeFrage(true);
    } else {
      zeigeErgebnis();
    }
  }

  function gewinner() {
    var max = Math.max.apply(null, BEREICHE.map(function (b) { return punkte[b]; }));
    var vorn = BEREICHE.filter(function (b) { return punkte[b] === max; });
    if (vorn.length === 1) return vorn[0];
    return vorn.indexOf(letzte) !== -1 ? letzte : vorn[0];
  }

  function zeigeErgebnis() {
    var e = ERG[gewinner()];
    leeren();

    var box = el('div', 'quiz-ergebnis');
    box.appendChild(el('p', 'quiz-zaehler', 'Dein Ergebnis'));
    var titel = el('h2', null, e.titel);
    titel.tabIndex = -1;
    box.appendChild(titel);
    box.appendChild(el('p', 'lead', e.text));

    var liste = el('div', 'kacheln quiz-liste');
    e.buecher.forEach(function (b) {
      var karte = el(b.link ? 'a' : 'div', 'kachel');
      if (b.link) karte.href = b.link;
      var bild = document.createElement('img');
      bild.src = b.cover;
      bild.alt = '';
      bild.className = 'buchbild';
      var text = el('div', 'kachel-text');
      text.appendChild(el('h3', null, b.titel));
      if (b.link) text.appendChild(el('span', 'mehr', 'Mehr erfahren →'));
      karte.appendChild(bild);
      karte.appendChild(text);
      liste.appendChild(karte);
    });
    box.appendChild(liste);

    var aktionen = el('div', 'quiz-aktionen');
    var mehr = el('a', 'button', e.mehr.label);
    mehr.href = e.mehr.link;
    aktionen.appendChild(mehr);
    var neu = el('button', 'quiz-neu', 'Quiz noch einmal spielen');
    neu.type = 'button';
    neu.addEventListener('click', function () { start(true); });
    aktionen.appendChild(neu);
    box.appendChild(aktionen);

    wurzel.appendChild(box);
    titel.focus();
  }

  start(false);
})();
