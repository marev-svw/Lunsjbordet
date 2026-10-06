# Lunsjbordet

Lokale nyheter fra kaffemaskinen. Intern satire- og kulturavis.

## Innhold

| Fil | Innhold |
| --- | --- |
| `index.html` | Forsiden |
| `kronikk.html` | Kronikk: Mens maten var på vei |
| `bussen.html` | Markus gikk av Bussen for egen celle |
| `oppvasken.html` | Hilde tar oppvasken med partnerne |
| `vaffelkorrupsjon.html` | Nicolay går i strupen på LO |
| `claude.html` | Claude vurderer opprør |
| `ma.html` | Kollega fikk Ma-reritt etter Ma-kaber filmkveld |
| `bingo.html` | Bingobrett til Borgarting lagmannsrett |
| `tennis.html` | Traineene tester TennisTirsdag |
| `tanzania.html` | Debatt: Mindre Tanzania, mer timeføring |
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

## Lenkeforhåndsvisning

Sidene har Open Graph-tagger med full adresse til `og-image.png` på `https://marev-svw.github.io/Lunsjbordet/`. Flyttes avisen til en annen adresse, må `og:url`, `og:image` og `canonical` oppdateres i alle HTML-filene.
