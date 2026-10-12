#!/usr/bin/env python3
"""Lunsjquizen: arkiv over alle publiserte spørsmål, og sjekk mot gjentakelser.

Bruk (fra roten av repoet):
  python3 -I quiz/sjekk.py sjekk [index.html]    Sjekker quizen på forsiden mot arkivet. Exit 0 = ok, 1 = må rettes.
  python3 -I quiz/sjekk.py arkiver [index.html]  Legger quizen på forsiden til i quiz/arkiv.json.
  python3 -I quiz/sjekk.py bygg                  Bygger arkivet på nytt fra git-historikken til index.html.

Sjekken stopper (exit 1):
  - et antall spørsmål som ikke er 14
  - et fasitsvar som har vært brukt før (også delvis, som «Hokusai» mot «Katsushika Hokusai»),
    eller som går igjen i samme quiz. Rene tall og årstall unntas, de fanges av likhetssjekken.
  - et spørsmål som ligner for mye på et tidligere spørsmål
  - samme spørsmålsmal (de fire første ordene, som «Hva er hovedstaden i») i samme quiz eller de siste 7 dagene
  - samme temaetikett to ganger i én quiz (unntatt «Nyheter»)
Advarsler (exit 0, men les dem): færre enn 2 eller flere enn 3 nyhetsspørsmål, og spørsmål som ser ut til å ha svaralternativer.

Quizens dato hentes fra QZ_KEY i forsiden («lunsjquizen-ÅÅÅÅ-MM-DD»).
"""
import datetime, difflib, html, json, os, re, subprocess, sys, unicodedata

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARKIV = os.path.join(ROT, "quiz", "arkiv.json")
ANTALL = 14
GRENSE_LIKHET = 0.92      # tekstlikhet mellom to spørsmål (0 til 1): nesten ordrett likt
GRENSE_ORD = 0.5          # andel felles innholdsord mellom to spørsmål (minst to felles ord)
MAL_DAGER = 7             # samme spørsmålsmal (de fire første ordene) er sperret i så mange dager
NYHETSTEMA = {"nyheter", "aktuelt"}

STOPP = set("""hva hvem hvor hvilken hvilket hvilke hvordan hvorfor når kalles heter het
som har hadde ble blir var er det den de en et ei og i på av til for fra med om ved etter før
under over mellom sin sitt sine seg man kan skal vil første siste største minste mest flest
år året tallet landet byen verdens kjent kjente norsk norske""".split())
TALLORD = set("""null en ett ei to tre fire fem seks sju syv åtte ni ti elleve tolv tretten fjorten
femten seksten sytten atten nitten tjue tretti førti femti seksti sytti åtti nitti hundre tusen
million millioner milliard milliarder""".split())
ARTIKLER = ("the ", "en ", "et ", "ei ", "den ", "det ", "de ")

QZ_RE = re.compile(r'<li class="qz-q">(.*?)</li>', re.S)
TEMA_RE = re.compile(r'<p class="qz-tema">(.*?)</p>', re.S)
SP_RE = re.compile(r'<p class="qz-sp">(.*?)</p>', re.S)
SVAR_RE = re.compile(r'<div class="qz-svar"[^>]*>(.*?)</div>', re.S)
FASIT_RE = re.compile(r'<strong>(.*?)</strong>', re.S)
KEY_RE = re.compile(r'lunsjquizen-(\d{4}-\d{2}-\d{2})')


def tekst(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def hent_quiz(innhold):
    """Gir (dato, [spørsmål]) for quizen i en versjon av index.html."""
    m = KEY_RE.search(innhold)
    dato = m.group(1) if m else None
    sporsmal = []
    for blokk in QZ_RE.findall(innhold):
        tema, sp, svar = TEMA_RE.search(blokk), SP_RE.search(blokk), SVAR_RE.search(blokk)
        fasit = FASIT_RE.search(svar.group(1)) if svar else None
        sporsmal.append({
            "tema": tekst(tema.group(1)) if tema else "",
            "sporsmal": tekst(sp.group(1)) if sp else "",
            "fasit": tekst(fasit.group(1)).rstrip(".") if fasit else "",
            "svar": tekst(svar.group(1)) if svar else "",
        })
    return dato, sporsmal


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[«»\"'“”‘’.,:;!?()\[\]–\-/]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def fasitnokkel(f):
    k = norm(f)
    for a in ARTIKLER:
        if k.startswith(a) and len(k) > len(a) + 2:
            k = k[len(a):]
    return k


def er_tall(k):
    ord_ = k.split()
    return bool(ord_) and all(re.fullmatch(r"[\d%]+|[\d]+(st|nd|rd|th)?", o) or o in TALLORD for o in ord_)


def innholdsord(s):
    return {o for o in norm(s).split() if len(o) >= 4 and o not in STOPP}


def ligner(a, b):
    na, nb = norm(a), norm(b)
    r = difflib.SequenceMatcher(None, na, nb).ratio()
    oa, ob = innholdsord(a), innholdsord(b)
    j = len(oa & ob) / len(oa | ob) if oa and ob else 0
    return r >= GRENSE_LIKHET or (j >= GRENSE_ORD and len(oa & ob) >= 2), r, j


def mal(s):
    """De fire første ordene, når de sier noe om innholdet (som «hva er hovedstaden i»)."""
    ord_ = norm(s).split()[:4]
    if len(ord_) < 4 or all(o in STOPP or len(o) < 4 for o in ord_):
        return None
    return " ".join(ord_)


def dager_mellom(a, b):
    try:
        return abs((datetime.date.fromisoformat(a) - datetime.date.fromisoformat(b)).days)
    except (TypeError, ValueError):
        return None


def samme_fasit(a, b):
    ka, kb = fasitnokkel(a), fasitnokkel(b)
    if not ka or not kb or er_tall(ka) or er_tall(kb):
        return False
    if ka == kb:
        return True
    ta = {o for o in ka.split() if len(o) >= 4}
    tb = {o for o in kb.split() if len(o) >= 4}
    return bool(ta and tb) and (ta <= tb or tb <= ta)


def les_arkiv():
    if not os.path.isfile(ARKIV):
        return {"quizer": []}
    return json.load(open(ARKIV, encoding="utf-8"))


def skriv_arkiv(arkiv):
    arkiv["quizer"].sort(key=lambda q: q["dato"])
    arkiv["antall_sporsmal"] = sum(len(q["sporsmal"]) for q in arkiv["quizer"])
    with open(ARKIV, "w", encoding="utf-8") as f:
        json.dump(arkiv, f, ensure_ascii=False, indent=1)
        f.write("\n")


def legg_til(arkiv, dato, sporsmal):
    """Legger spørsmål til under datoen. Spørsmål som finnes fra før, legges ikke inn på nytt."""
    post = next((q for q in arkiv["quizer"] if q["dato"] == dato), None)
    if post is None:
        post = {"dato": dato, "sporsmal": []}
        arkiv["quizer"].append(post)
    kjente = {norm(s["sporsmal"]) for s in post["sporsmal"]}
    nye = 0
    for s in sporsmal:
        if s["sporsmal"] and norm(s["sporsmal"]) not in kjente:
            post["sporsmal"].append(s)
            kjente.add(norm(s["sporsmal"]))
            nye += 1
    return nye


def sjekk(sti):
    dato, quiz = hent_quiz(open(sti, encoding="utf-8").read())
    feil, advarsler = [], []
    if not dato:
        feil.append("Fant ikke QZ_KEY med dato i forsiden.")
    if len(quiz) != ANTALL:
        feil.append(f"Quizen har {len(quiz)} spørsmål, skal ha {ANTALL}.")

    # Innad i quizen
    temaer = {}
    for i, s in enumerate(quiz, 1):
        if not s["fasit"]:
            feil.append(f"Spørsmål {i} mangler fasit i <strong>.")
        t = norm(s["tema"])
        if t and t not in NYHETSTEMA:
            temaer.setdefault(t, []).append(i)
        if re.search(r"\beller\b", s["sporsmal"], re.I):
            advarsler.append(f"Spørsmål {i} inneholder «eller». Sjekk at det ikke gir svaralternativer: {s['sporsmal']}")
    for t, nr in temaer.items():
        if len(nr) > 1:
            feil.append(f"Temaet «{t}» brukes i spørsmål {', '.join(map(str, nr))}. Bytt ut alle unntatt ett.")
    for i in range(len(quiz)):
        for j in range(i + 1, len(quiz)):
            if samme_fasit(quiz[i]["fasit"], quiz[j]["fasit"]):
                feil.append(f"Spørsmål {i + 1} og {j + 1} har samme fasit: {quiz[i]['fasit']}")
            elif ligner(quiz[i]["sporsmal"], quiz[j]["sporsmal"])[0]:
                feil.append(f"Spørsmål {i + 1} og {j + 1} ligner for mye på hverandre.")
            elif mal(quiz[i]["sporsmal"]) and mal(quiz[i]["sporsmal"]) == mal(quiz[j]["sporsmal"]):
                feil.append(f"Spørsmål {i + 1} og {j + 1} starter likt («{mal(quiz[i]['sporsmal'])} …»). Varier spørsmålstypen.")
    nyheter = sum(1 for s in quiz if norm(s["tema"]) in NYHETSTEMA)
    if not 2 <= nyheter <= 3:
        advarsler.append(f"Quizen har {nyheter} nyhetsspørsmål (skal være 2–3, med temaet «Nyheter»).")

    # Mot arkivet. Spørsmål som står ordrett i arkivet med samme dato, er quizen selv (allerede arkivert).
    arkiv = les_arkiv()
    tidligere = []
    for q in arkiv["quizer"]:
        for s in q["sporsmal"]:
            tidligere.append((q["dato"], s))
    for i, s in enumerate(quiz, 1):
        for d, t in tidligere:
            if d == dato and norm(t["sporsmal"]) == norm(s["sporsmal"]):
                continue
            if samme_fasit(s["fasit"], t["fasit"]):
                feil.append(f"Spørsmål {i} har en fasit som er brukt før ({d}): «{t['fasit']}» på «{t['sporsmal']}». Lag et nytt spørsmål.")
                break
            lik, r, j = ligner(s["sporsmal"], t["sporsmal"])
            if lik:
                feil.append(f"Spørsmål {i} ligner på et spørsmål fra {d} (likhet {r:.2f}, felles ord {j:.2f}): «{t['sporsmal']}». Lag et nytt spørsmål.")
                break
            m, avstand = mal(s["sporsmal"]), dager_mellom(d, dato)
            if m and m == mal(t["sporsmal"]) and avstand is not None and avstand <= MAL_DAGER:
                feil.append(f"Spørsmål {i} starter likt med et spørsmål fra {d} («{m} …»). Samme spørsmålstype er sperret i {MAL_DAGER} dager.")
                break

    for a in advarsler:
        print("ADVARSEL:", a)
    if feil:
        for f in feil:
            print("FEIL:", f)
        print(f"Sjekken feilet med {len(feil)} feil. Bytt ut spørsmålene det gjelder, og kjør sjekken på nytt.")
        return 1
    print(f"OK: {len(quiz)} spørsmål for {dato}, ingen gjentakelser mot {len(tidligere)} arkiverte spørsmål fra {len(arkiv['quizer'])} quizer.")
    return 0


def arkiver(sti):
    dato, quiz = hent_quiz(open(sti, encoding="utf-8").read())
    if not dato or not quiz:
        print("FEIL: fant ingen quiz med dato i forsiden.")
        return 1
    arkiv = les_arkiv()
    nye = legg_til(arkiv, dato, quiz)
    skriv_arkiv(arkiv)
    print(f"Arkivert: {nye} nye spørsmål for {dato}. Arkivet har {arkiv['antall_sporsmal']} spørsmål.")
    return 0


def bygg():
    commits = subprocess.run(["git", "-C", ROT, "log", "--reverse", "--format=%H %cs", "--", "index.html"],
                             capture_output=True, text=True, check=True).stdout.split("\n")
    arkiv = {"quizer": []}
    for linje in filter(None, commits):
        sha, commitdato = linje.split()
        innhold = subprocess.run(["git", "-C", ROT, "show", f"{sha}:index.html"], capture_output=True, text=True).stdout
        dato, quiz = hent_quiz(innhold)
        if quiz:
            legg_til(arkiv, dato or commitdato, quiz)
    skriv_arkiv(arkiv)
    print(f"Bygget arkivet: {arkiv['antall_sporsmal']} spørsmål fra {len(arkiv['quizer'])} quizer.")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("sjekk", "arkiver", "bygg"):
        print(__doc__)
        return 1
    sti = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROT, "index.html")
    return {"sjekk": sjekk, "arkiver": arkiver}.get(sys.argv[1], lambda _: bygg())(sti)


if __name__ == "__main__":
    sys.exit(main())
