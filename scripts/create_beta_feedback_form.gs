/**
 * Creates the Task Z' beta feedback form from Appendix A of the beta test protocol.
 *
 * Protocol: findings/no_db_universal_skill/2026-08-08-beta-test-protocol.md
 *
 * The German question wording below is verbatim from Appendix A and must not be
 * edited here — if a question needs to change, change the protocol first, and only
 * before the protocol is frozen (§7).
 *
 * How to run:
 *   1. Open https://script.google.com and create a new project.
 *   2. Replace the contents of Code.gs with this file.
 *   3. Run createBetaFeedbackForm(). Google will ask for permission to manage forms.
 *   4. The published URL is printed to the execution log (View > Logs).
 *
 * The form collects no email address (§6: anonymous).
 */

function createBetaFeedbackForm() {
  var form = FormApp.create('thesis-finder — Beta-Feedback')
    .setDescription(
      'Danke, dass du thesis-finder ausprobiert hast. Dieser Fragebogen ist anonym und ' +
      'dauert ca. 3 Minuten. Ehrliches Feedback ist deutlich hilfreicher als freundliches — ' +
      'wenn etwas nicht funktioniert hat, ist genau das die interessante Antwort.\n\n' +
      'Nicht-kommerzielles StudyOS-Kursprojekt, kein offizielles Angebot der Universität ' +
      'Tübingen.'
    )
    .setCollectEmail(false)
    .setProgressBar(true)
    .setAllowResponseEdits(false);

  // 1 — installability
  form.addMultipleChoiceItem()
    .setTitle('Hat die Installation funktioniert?')
    .setChoiceValues(['Ja, problemlos', 'Ja, aber mit Mühe', 'Nein'])
    .setRequired(true);

  // 2 — where they got stuck (§2: getting stuck is a measurement, not a failure)
  form.addParagraphTextItem()
    .setTitle('Falls „mit Mühe“ oder „nein“ — wo bist du hängen geblieben?')
    .setRequired(false);

  // 3 — human setup time (§5: never anchored against the 48 s agent lower bound)
  var minutes = form.addTextItem()
    .setTitle('Wie lange hat das Setup ungefähr gedauert (in Minuten)?')
    .setRequired(true);
  minutes.setValidation(
    FormApp.createTextValidation()
      .setHelpText('Bitte eine Zahl eintragen, z. B. 12')
      .requireNumber()
      .build()
  );

  // 4 — relevance
  form.addScaleItem()
    .setTitle('Wie relevant waren die vorgeschlagenen Optionen für dich?')
    .setBounds(1, 5)
    .setLabels('gar nicht', 'sehr')
    .setRequired(true);

  // 5 — source trust
  form.addScaleItem()
    .setTitle('Wie vertrauenswürdig fandest du die genannten Quellen und Belege?')
    .setBounds(1, 5)
    .setLabels('gar nicht', 'sehr')
    .setRequired(true);

  // 6 — would contact
  form.addMultipleChoiceItem()
    .setTitle('Würdest du eine der vorgeschlagenen Personen oder Firmen tatsächlich kontaktieren?')
    .setChoiceValues(['Ja', 'Vielleicht', 'Nein'])
    .setRequired(true);

  // 7 — confusion
  form.addParagraphTextItem()
    .setTitle('Was war verwirrend oder unklar?')
    .setRequired(false);

  // 8 — study programme, optional
  form.addTextItem()
    .setTitle('Studiengang (freiwillig)')
    .setRequired(false);

  // 9 — the reflection question, shared with the interview protocol (§3)
  form.addParagraphTextItem()
    .setTitle(
      'In ein bis zwei Sätzen: Was für eine Abschlussarbeit suchst du jetzt — ' +
      'und hat sich das durch den Durchlauf verändert?'
    )
    .setRequired(true);

  Logger.log('Ausfüll-Link (dieser gehört in INSTALL.md und die Release-Notes):');
  Logger.log(form.getPublishedUrl());
  Logger.log('Bearbeiten-Link (nicht weitergeben):');
  Logger.log(form.getEditUrl());

  return form.getPublishedUrl();
}
