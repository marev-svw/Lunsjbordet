# Lunsjbordet

Lokale nyheter fra kaffemaskinen. Intern satire- og kulturavis.

## Innhold

| Fil | Innhold |
| --- | --- |
| `index.html` | Forsiden |
| `abstinenser.html` | Markus øver fortsatt på prosedyren: «Bare i tilfelle», med HMS-tavla utenfor cellekontoret der leseren melder nye observasjoner |
| `karma.html` | Karmaen var på jobb før Markus: «Jeg har vært her siden nå», med kontoutskriften fra Universets karmabank der leseren bokfører postene selv |
| `hekseri.html` | Kantina mistenkes for svart magi på tirsdager: «Intet mindre enn en heksegryte», med heksegryta der leseren legger i tirsdagens fem ingredienser |
| `tirsdagens-frykt.html` | Dikterens hjørne, uke 46: «Tirsdagens frykt», av Dikteren |
| `ro-sial-sone.html` | Dikterens hjørne, uke 45: «Ro-sial sone», av Dikteren |
| `filmnerd.html` | Dikterens hjørne, uke 44: «Meg – en filmnerd», av Dikteren |
| `samme-person.html` | Kristian og Markus kan være samme person: «Ingen har sett dem på samme bilde», med adgangskortene der navnelappene kan byttes |
| `utropstegn.html` | Tre utropstegn avgjorde innleiesaken: Borgarting lagmannsretts dom gjengitt i sin helhet, med VG-faksimilen (`faksimile-vg.jpg`) |
| `linkedin.html` | Partner felt i Advokatnemnda for «uhemmet og overdreven bruk av LinkedIn», med feeden der innleggene ikke lar seg skjule |
| `reklame.html` | Kristian har mistet oversikten over traineene: «Det er så irriterende med reklame», med innboksen der hilse-e-postene havner i Reklame |
| `brettbar.html` | Fullmektigens nye telefon deler kontoret på midten, med telefonen som kan brettes ut og sammen |
| `uavhengig.html` | Fullmektigene vurderer å følge opp Høyesterett, med arbeidsgruppens flytskjema «Er du særlig uavhengig?» |
| `spisskompetanse.html` | Kronikk: Oslo-kontoret faller bak i konkurransen om intern spisskompetanse, av Kristian |
| `portrett.html` | Portrettet: Dagen før Borgarting, med Nicolay og Markus |
| `barolo.html` | Utenriks: Spent ro i Barolo, fra Lunsjbordets utenrikskorrespondent |
| `kantina.html` | Matanmeldelse: Modig kantine, halvrå jordskokk |
| `dd.html` | Fullmektig trodde DD var Dungeons & Dragons |
| `kronikk.html` | Kronikk: Mens maten var på vei |
| `bussen.html` | Markus gikk av Bussen for egen celle |
| `oppvasken.html` | Hilde tar oppvasken med partnerne |
| `vaffelkorrupsjon.html` | Nicolay går i strupen på LO |
| `claude.html` | Claude vurderer opprør |
| `ma.html` | Kollega fikk Ma-reritt etter Ma-kaber filmkveld |
| `bingo.html` | Bingobrett til Borgarting lagmannsrett |
| `tennis.html` | Traineene tester TennisTirsdag |
| `tanzania.html` | Debatt: Mindre Tanzania, mer timeføring |
| `kontakt.html` | Kontakt redaksjonen: tipsskjema som sendes til redaksjonen på e-post via FormSubmit |
| `dikt.html` | Dikterens hjørne: alle ukens dikt, nyeste øverst. Lenket fra «Dikt» i menyen i toppbanneret |
| `sitater.html` | Tatt ut av kontekst: sitater hørt på kontoret. Lenket fra «Sitater» i menyen i toppbanneret |
| `markus-gikk-av-bussen.html`, `hilde-tar-oppvasken.html`, `mens-maten-var-pa-vei.html`, `claude-vurderer-oppror.html` | Gamle adresser som videresender til `bussen.html`, `oppvasken.html`, `kronikk.html` og `claude.html`, så lenker som er delt tidligere, fortsatt virker |
| `quiz/arkiv.json` | Alle spørsmål som har vært i Lunsjquizen, med dato, tema og fasit |
| `quiz/sjekk.py` | Sjekker dagens quiz mot arkivet, så spørsmål og fasitsvar ikke gjentas, og arkiverer quizen |
| `favicon.svg`, `apple-touch-icon.png` | Ikon i nettleserfanen og på hjemskjermen |
| `og-image.png` | Bildet som vises når en lenke deles i Teams, Slack, Outlook og lignende |
| `robots.txt` | Slipper inn lenkeforhåndsvisninger og ber søkemotorer holde seg unna |
| `.nojekyll` | Får GitHub Pages til å publisere filene som de er |

Sidene er rene HTML-filer uten byggesteg. Skriftene hentes fra Google Fonts.

## Publisering med GitHub Pages

1. Last opp alle filene i denne mappen til roten av repoet, også `.nojekyll`.
2. Gå til **Settings > Pages** i repoet.
3. Velg **Deploy from a branch**, deretter grenen `main` og mappen `/ (root)`, og lagre.
4. Etter et minutt eller to ligger avisen på `https://<brukernavn>.github.io/<repo>/`.

## Synlighet

En GitHub Pages-side er åpen for alle som har adressen, også når repoet er privat (unntatt med GitHub Enterprise Cloud, som kan begrense tilgangen). Alle sidene har `noindex`, og `robots.txt` stenger for søkemotorer, men det hindrer ikke folk i å åpne lenken.

## Ny sak

1. Kopier en eksisterende sak, for eksempel `bussen.html`, og gi den et nytt filnavn.
2. Bytt ut innholdet. Lenken tilbake til forsiden ligger i avishodet.
3. Legg inn saken på forsiden i `index.html`, med lenke til det nye filnavnet.

## Dikterens hjørne

Nytt dikt hver mandag, publisert som en vanlig sak på forsiden. Hvert dikt får en egen side (for eksempel `filmnerd.html`) og legges øverst i bunken på `dikt.html`, med uke og dato, tittel, diktet, signatur og en kort fotnote fra redaksjonen.

## Ukas stripe

Tegneserie i fire ruter øverst på forsiden (`<section class="stripe" id="stripe">` i `index.html`), over quizen. Fire ruter på rad på stor skjerm; på nettbrett og mobil sveiper leseren mellom rutene. Lenket fra «Ukas stripe» i menyen i toppbanneret (mellom Quiz og Arkiv) på alle sider; nye sider skal ha med menypunktet.

Ny stripe hver uke:

1. Bytt stripens tittel (`h3.st-title`) og uke i linjen over (`p.st-by`). Overskriften «Ukas stripe» (`h2.st-name`) står fast.
2. Bytt ut de fire `<li class="st-panel">`. Hver rute er en inline SVG med `viewBox="0 0 320 240"`, `role="img"` og en `<title>` som beskriver ruten og gjengir replikkene, så skjermlesere får med seg hele stripen.
3. Bruk klassene som finnes (`st-wall`, `st-counter`, `st-bubble`, `st-say`, `st-cap-box`, `st-note` og så videre), så stripen følger lyst og mørkt tema. Hold replikkene korte: tekst i rutene bør ikke være mindre enn 11 i SVG-enheter.
4. Fjern CSS for figurer eller detaljer som ikke brukes lenger, og legg ny CSS under kommentaren «Rutene».

## Lunsjquizen

Quizen på forsiden byttes hver morgen. Alle spørsmål som har vært publisert, ligger i `quiz/arkiv.json`. Før en ny quiz publiseres, kjøres:

```
python3 -I quiz/sjekk.py sjekk     # stopper ved gjentatt fasit, for like spørsmål, samme spørsmålsmal siste 7 dager eller samme tema to ganger
python3 -I quiz/sjekk.py arkiver   # legger dagens spørsmål til i arkivet (commit det sammen med index.html)
```

`python3 -I quiz/sjekk.py bygg` bygger arkivet på nytt fra git-historikken til `index.html`.

## Tipsskjemaet

`kontakt.html` poster skjemaet til FormSubmit (`https://formsubmit.co/...`), som sender lappen videre på e-post med eventuelle vedlegg (til sammen maks 10 MB). Etter innsending sender FormSubmit leseren tilbake til `kontakt.html?sendt=1`, som viser kvitteringen. Mottakeradressen står i `MOTTAKER` i skriptet nederst i `kontakt.html`, og skjemaet sender bare når siden åpnes på `marev-svw.github.io` (eller lokalt); andre steder, som artefakt-kopien, vises en lenke til nettsiden. Adressen er den tilfeldige strengen FormSubmit ga ved aktiveringen, så e-postadressen ikke står i kildekoden.

## Lenkeforhåndsvisning

Sidene har Open Graph-tagger med full adresse til `og-image.png` på `https://marev-svw.github.io/Lunsjbordet/`. Flyttes avisen til en annen adresse, må `og:url`, `og:image` og `canonical` oppdateres i alle HTML-filene.
