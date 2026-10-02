---
tags: [it-ret, gdpr, lektion4]
pensum: "Udsen kap. 7–8, 10–11 · DBF art. 30, 32–35, 37–39, 51–67, 77–84 · DBL §§ 24, 26–43"
---
# Lektion 4 – Fortegnelse, privacy by design, sikkerhed, DPIA, brud, DPO, tilsyn og sanktioner

## 1. Fortegnelse over behandlingsaktiviteter – art. 30
**Formål:** dokumentere overholdelse (**ansvarlighed**), give internt overblik og være grundlag for videre compliancearbejde.
**Form:** skriftlig, også elektronisk (skema/Word), **løbende opdateret**, udleveres til Datatilsynet på anmodning.

| DA's fortegnelse (stk. 1) | Databehandlerens fortegnelse (stk. 2) |
|---|---|
| navn og kontaktoplysninger på DA (+ fælles DA, repræsentant, DPO) | navn og kontaktoplysninger på databehandleren og **hver DA** |
| formål | kategorier af behandling for hver DA |
| kategorier af registrerede og personoplysninger | evt. tredjelandsoverførsler |
| kategorier af modtagere | generel beskrivelse af sikkerhedsforanstaltninger |
| evt. tredjelandsoverførsler | |
| **slettefrister** pr. kategori | |
| generel beskrivelse af sikkerhedsforanstaltninger | |

**Hvem?** HR: alle virksomheder og myndigheder. **U:** private virksomheder med **under 250 ansatte**. **UU:** pligten gælder alligevel, hvis behandlingen 1) indebærer en risiko for de registrerede, 2) **ikke er lejlighedsvis**, eller 3) omfatter **følsomme oplysninger** eller **strafbare forhold** (art. 30, stk. 5). → I praksis har næsten alle pligten (fx løn er ikke lejlighedsvis).

## 2. Databeskyttelse gennem design og standardindstillinger – art. 25
- **Stk. 1 (design):** under hensyn til **det aktuelle tekniske niveau**, **implementeringsomkostninger**, behandlingens karakter, omfang, sammenhæng og formål og **risiciene** skal DA – **både når midlerne fastlægges og under behandlingen** – gennemføre passende tekniske og organisatoriske foranstaltninger (fx **pseudonymisering**), der effektivt implementerer principperne (fx dataminimering).
- **Stk. 2 (default):** standardindstillinger skal sikre, at kun de **nødvendige** oplysninger behandles – mht. **mængde, omfang af behandlingen, opbevaringsperiode og tilgængelighed**. Oplysninger må ikke uden personens indgriben gøres tilgængelige for et **ubegrænset antal personer**.
- **Stk. 3:** certificering (art. 42) kan bruges som et element i dokumentationen.
- **Privacy by default** præciserer **dataminimering** (art. 5(1)(c)).
- **"Aktuelt teknisk niveau"** er ikke et fast niveau: følg udviklingen, omkostninger er en faktor, men **ikke en grund til at undlade** foranstaltninger, og vurder løbende igen. Brug anerkendte standarder og certificeringer som pejlemærker.

**Cavoukians 7 principper for privacy by design:** 1) proaktiv, ikke reaktiv · 2) privatliv som standard · 3) indlejret i designet · 4) fuld funktionalitet (positiv sum, ikke nulsum) · 5) end-to-end-sikkerhed gennem hele livscyklussen · 6) synlighed og gennemsigtighed · 7) respekt for brugerens privatliv.

**Praksis:** Pant-appen (DT 2024 – alvorlig kritik, påbud og advarsel), se afsnit 3.4 i afgørelsen.

## 3. Behandlingssikkerhed – art. 32
> [!note] Bemærk
> Slides nævner art. 25 i denne sammenhæng, men **sikkerhedskravet står i art. 32** (DA **og** databehandler).

- **Passende sikkerhedsniveau** ud fra en **konkret risikovurdering**, hvor **de registrerede er i centrum** (risikoen for *dem*, ikke for virksomheden).
- Art. 32, stk. 1 nævner bl.a.: pseudonymisering og **kryptering**; fortrolighed, integritet, tilgængelighed og robusthed; evne til **rettidigt at genoprette** tilgængeligheden efter en hændelse (backup!); procedurer til regelmæssig **test og evaluering**.
- **Hvornår risikovurdering?** Nye behandlinger, nyt system/app, ny leverandør, kontrol af databehandler, ved DPIA, ved overførsel til tredjelande (TIA).
- **Datatilsynets tilgang:** identificér relevante **trusler** → vurdér **konsekvens** pr. trussel → vurdér **sårbarhed** ud fra eksisterende foranstaltninger → **risiko** (sandsynlighed × konsekvens).

| Tekniske foranstaltninger | Organisatoriske foranstaltninger |
|---|---|
| adgangskontrol, anonymisering, antispam/phishing-filtre, antivirus, asset management, **backup og reetablering**, kryptering, logning | beredskabsplan, fortegnelse, HR-instruks, IT-sikkerhedspolitik, privatlivspolitik, procedurer for brud, **træning af medarbejdere** |

## 4. Konsekvensanalyse (DPIA) – art. 35–36
**Først risikovurdering → så konsekvensanalyse, hvis risikoen er høj.**
- **HR:** DPIA, når en behandling **sandsynligvis indebærer en høj risiko** for fysiske personers rettigheder. Den skal laves **før behandlingen starter**.
- **Art. 35, stk. 3:** altid ved systematisk og omfattende **profilering med retsvirkning**, **følsomme/strafbare oplysninger i stor skala** og systematisk **overvågning af offentligt tilgængelige områder i stor skala**.
- **Datatilsynets liste** (godkendt af EDPB) – DPIA altid ved:
  1. biometriske data til entydig identifikation + mindst ét yderligere kriterium (WP248)
  2. genetiske data + ét kriterium
  3. lokationsdata + ét kriterium
  4. nye teknologier + ét kriterium
  5. automatiserede afgørelser (inkl. profilering) om rettigheder til produkter/ydelser/muligheder
  6. profilering i stor skala
  7. sårbare personer eller følsomme oplysninger **kombineret med** profilering/automatiserede afgørelser
  8. hvor et brud kan påvirke en persons **fysiske helbred eller sikkerhed** direkte
- **Indhold (art. 35, stk. 7):** 1) systematisk beskrivelse (ansvar, formål, retsgrundlag, omfang, dataflows), 2) vurdering af **nødvendighed og proportionalitet** (art. 5), 3) **risikovurdering** for de registrerede, 4) **afhjælpende foranstaltninger**.
- **Art. 36 – forudgående høring:** viser DPIA'en en høj restrisiko, som DA ikke kan nedbringe → **hør Datatilsynet** før behandlingen.
- **Case:** Superligaens ansigtsgenkendelse (DT-tilladelse juli 2025) – biometri = art. 9 (væsentlig samfundsinteresse, art. 9(2)(g) / DBL § 7, stk. 4) → betingelser og DPIA.
- Datatilsynet har [skabeloner til konsekvensanalyser (2024)](https://www.datatilsynet.dk/presse-og-nyheder/nyhedsarkiv/2024/maj/nye-skabeloner-til-gennemfoerelse-af-konsekvensanalyser).

## 5. Sikkerhedsbrud – art. 33–34
**Definition (art. 4, nr. 12):** brud på sikkerheden, der fører til hændelig eller ulovlig **tilintetgørelse, tab, ændring, uautoriseret videregivelse eller adgang** (fortrolighed, integritet eller tilgængelighed).

| | **Anmeldelse til Datatilsynet – art. 33** | **Underretning af de registrerede – art. 34** |
|---|---|---|
| HR | **skal anmeldes** | når bruddet sandsynligvis indebærer **høj risiko** |
| U | **usandsynligt**, at bruddet indebærer en risiko | usandsynligt med **høj** risiko (fx pga. **kryptering**), eller **uforholdsmæssig indsats** → i stedet offentlig meddelelse |
| Frist | uden unødig forsinkelse og **om muligt senest 72 timer** efter, at DA er **blevet bekendt** med bruddet | uden unødig forsinkelse |
| Bevisbyrde | DA | DA |

- **Databehandleren** skal underrette DA uden unødig forsinkelse (art. 33, stk. 2).
- **Alle brud skal dokumenteres i en intern log** (art. 33, stk. 5) – også dem, der ikke anmeldes: faktiske omstændigheder, karakter, antal berørte, typer af oplysninger, varighed, konsekvenser, afhjælpende foranstaltninger, om der er anmeldt/underrettet.
- **DT j.nr. 2020-442-8866 (Datatilsynet selv!):** en beholder til makulering var ved en fejl markeret forkert under en flytning, så fortrolige papirer endte i almindeligt affald. Tilsynet blev bekendt med det **5. august** og anmeldte **10. august** → **for sent** (72 timer). Datatilsynet behandlede sagen om sig selv, fordi kompetencen ved lov ligger hos tilsynet.
- **DT j.nr. 2020-32-1390 (Randers Kommune):** en påtænkt opsigelse med fagforenings- og helbredsoplysninger blev sendt til en forkert kollega 15. nov. 2019. Kommunen bad samme dag om sletning, men anmeldte ikke. Medarbejderen klagede i februar 2020 → **ikke anmeldt rettidigt**.
- Typiske brud: e-mails sendt til den forkerte, tabte/stjålne enheder, hacking/ransomware, forkert adgangsstyring.

## 6. Databeskyttelsesrådgiver (DPO) – art. 37–39
- **Funktion:** rådgive og understøtte DA – men **DA har ansvaret**.
- **Pligt til at udpege (art. 37, stk. 1):**
  - **a) offentlige myndigheder/organer** (forvaltningslovens § 1, stk. 1–2) – uanset om de er DA eller databehandler (domstole undtaget, når de handler som domstol);
  - **b–c) private**, når **kerneaktiviteten** består i behandling, der i **stort omfang** indebærer **regelmæssig og systematisk overvågning**, **eller** behandling i stort omfang af **følsomme/strafbare** oplysninger (kumulative betingelser).
- **Frivillig eller fejlagtig udpegelse:** art. 37–39 gælder **fuldt ud**.
- **Krav:** ekspertviden (37(5)) · **offentliggør** kontaktoplysninger og meddel dem til tilsynet (37(7)) · inddrages rettidigt · **ressourcer** (38(2)) · **uafhængighed** – ingen instrukser, må ikke afskediges for at udføre sine opgaver, **rapporterer direkte til øverste ledelse** (38(3)) · tilgængelig for de registrerede (38(4)) · **tavshedspligt** (38(5)) · ingen interessekonflikter (38(6)).
- **Opgaver (art. 39):** underrette/rådgive, overvåge overholdelse, rådgive om DPIA, samarbejde med og være kontaktpunkt for tilsynet.

## 7. Tilsynsmyndigheden – Datatilsynet (art. 51–59, DBL kap. 10)
- **Art. 51:** hver medlemsstat har mindst én uafhængig tilsynsmyndighed (Tyskland: 16 regionale for den private sektor). I DK: **Datatilsynet** + **Domstolsstyrelsen** for domstolenes administrative funktioner (DBL § 37, stk. 2; art. 55, stk. 3).
- **Art. 52 – fuld uafhængighed:** ingen instrukser, ingen uforenelig virksomhed, tilstrækkelige ressourcer, eget personale, separat offentligt budget.
- **Art. 54:** oprettes ved lov; medlemmer og personale har tavshedspligt.
- **Opgaver (art. 57, DBL § 27):** tilsyn og håndhævelse, oplysning af offentligheden, rådgivning af Folketing/regering, information til registrerede, **klagebehandling (gratis, art. 57, stk. 3)**, samarbejde med andre tilsyn, overvågning af teknologisk udvikling, liste over DPIA-krav.
- **Beføjelser (art. 58):**
  - stk. 1 **undersøgelse** (oplysninger, inspektion, adgang – DBL § 29, stk. 2)
  - stk. 2 **korrigerende**: advarsler, **kritik** (litra b), **påbud**, begrænsning/forbud, sletning, suspension af overførsler – og bøder (i DK via domstolene)
  - stk. 3 godkendelse og rådgivning
  - stk. 5 indbringelse for domstolene (DBL § 30, stk. 2)
- Tilsynets afgørelser kan ikke indbringes for anden administrativ myndighed (DBL § 30), men kan prøves ved **domstolene** (GRL § 63).
- **EDPB (art. 68–76):** Det Europæiske Databeskyttelsesråd (afløste Artikel 29-gruppen); repræsentanter fra de nationale tilsyn; udsteder **retningslinjer**, træffer afgørelser om generelle spørgsmål og **bindende afgørelser** ved uenighed mellem tilsyn.

## 8. Retsmidler og sanktioner
| Retsmiddel | Hjemmel |
|---|---|
| Klage til tilsynsmyndigheden | art. 77 |
| Retsmiddel mod tilsynets afgørelse | art. 78 (domstolene) |
| Søgsmål mod DA/databehandler | art. 79 |
| **Erstatning** for materiel og **immateriel** skade | art. 82 (jf. også erstatningsansvarsloven § 26 om tort) |
| **Bøder** | art. 83 · DBL § 41 |
| **Fængsel indtil 6 måneder** | **DBL § 41** |

**Klage til Datatilsynet vs. retssag – den registreredes valg:**

| Klage til DT | Retssag |
|---|---|
| + kræver kun den registreredes egen opfattelse af en krænkelse | − krav om forudgående dialog om forlig (RPL § 336 a) |
| + officialprincippet (DT oplyser sagen) | − forhandlingsprincippet (parterne oplyser) |
| + gratis (art. 57, stk. 3), relativt hurtigt, én instans | − risiko for sagsomkostninger, lang tid, to instanser |
| + kan føre til sanktion (via anklagemyndigheden) | − ingen bøde |
| − **ingen erstatning** eller godtgørelse | + **erstatning/godtgørelse** mulig |
| − dyr advokat, ingen omkostningsdækning | + retshjælp/fri proces, bevisførelse (partsforklaring, syn og skøn) |

### Bøder – art. 83
- **Stk. 4:** op til **€ 10 mio. eller 2 %** af den globale årlige omsætning (fx art. 8, 11, 25–39 – DA/databehandlers forpligtelser).
- **Stk. 5:** op til **€ 20 mio. eller 4 %** (principperne art. 5–7 og 9, de registreredes rettigheder art. 12–22, tredjelandsoverførsler art. 44–49, påbud).
- Det **højeste** beløb gælder. Bøder skal være **effektive, forholdsmæssige og have afskrækkende virkning** (stk. 1).
- **Udmålingsmomenter (stk. 2, a–k):** overtrædelsens karakter, alvor og varighed, antal registrerede, **forsæt eller uagtsomhed**, skadebegrænsning, ansvar efter art. 25/32, tidligere overtrædelser, samarbejde, typer af oplysninger, hvordan tilsynet fik kendskab, adfærdskodeks/certificering, øvrige skærpende/formildende forhold.
- **Offentlige myndigheder** kan straffes for virksomhed, der svarer til privates (DBL § 41, stk. 6). Forelæsningen angav lofter på 2 %/4 % af myndighedens driftsbevilling, maks. 8/16 mio. kr. – tjek den gældende lovtekst.

### Bøder i Danmark
- Danmark har **ikke administrative bøder** – **bøder er altid strafferetlige** og pålægges af **domstolene** (PR 151). Datatilsynet **politianmelder og indstiller** et bødeniveau.
- **DBL § 42:** Datatilsynet kan udstede et **bødeforelæg**, hvis overtrædelsen ikke ville medføre højere straf end bøde, og den pågældende vedtager det.
- **Forældelse: 5 år** (DBL § 41, stk. 7).

### Danske bødesager
- **IDdesign:** ca. 385.000 kunders data lå i et gammelt ERP-system (AX 2.5), var mere end 5 år gamle, og der var ingen sletning eller slettepolitik. DT indstillede **1,5 mio. kr.** **Byretten i Aarhus** nedsatte til **100.000 kr.** (ikke koncernomsætning + formildende omstændigheder). **Vestre Landsret** udsatte sagen og forelagde spørgsmålet om "virksomhed" for **EU-Domstolen** (2022). **2. sep. 2025: Vestre Landsret – 1,5 mio. kr.**
- **Arp-Hansen Hotel Group:** ca. 500.000 kundeprofiler; den aftalte automatiske sletning hos leverandøren virkede ikke. DT indstillede 1,1 mio. kr. (senere 350.000 kr.). **Retten i Lyngby:** flertallet gav en advarsel (formildende: sagsbehandlingstid på over 3 år). **Vestre Landsret 20. sep. 2023: 1 mio. kr.**
- Taxa 4x35: 1,2 mio. kr. indstillet (se [[Lektion 2 - Aktører og behandlingsprincipper#5e. Opbevaringsbegrænsning|Lektion 2]]).
- Alle bødesager: [datatilsynet.dk/afgoerelser/boedesager](https://www.datatilsynet.dk/afgoerelser/boedesager)

## 9. Cases
Se [[Øvelsescases og løsningsskitser#Lektion 4]]: advokatfirma X (nedlagt DPO-funktion og mangelfuld fortegnelse), **BorgerPuls** (kommunal app – alle lektionens emner i én case).

## Hurtig repetition
- [ ] Hvem skal føre fortegnelse – og hvorfor rammer undtagelsen for under 250 ansatte sjældent?
- [ ] Forskellen på privacy by design og privacy by default?
- [ ] Hvornår er en DPIA obligatorisk – nævn tre tilfælde fra DT's liste.
- [ ] Art. 33 vs. art. 34: tærskel, frist, undtagelser.
- [ ] De tre kumulative betingelser for privates DPO-pligt.
- [ ] Bøderammer i art. 83, stk. 4 og 5 – og hvorfor pålægger Datatilsynet ikke selv bøder?

Forrige: [[Lektion 3 - Behandlingsgrundlag og de registreredes rettigheder]] · Oversigt: [[00 - IT-ret Oversigt]] · Næste: [[Lektion 5 - Cybercrime]]
