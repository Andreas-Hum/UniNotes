---
tags: [it-ret, gdpr, lektion2]
pensum: "Udsen kap. 3–4 · DBF art. 5, 24–31 · DBL § 5"
---
# Lektion 2 – Aktører og behandlingsprincipper

## 1. Aktørerne
**Den registrerede → Den dataansvarlige → Databehandler → (Under)databehandler**

| Rolle | Definition | Kendetegn |
|---|---|---|
| **Den registrerede** | den fysiske person, oplysningerne vedrører (art. 4, nr. 1) | |
| **Dataansvarlig (DA)** | afgør **formål** og **hjælpemidler** for behandlingen, alene eller sammen med andre (art. 4, nr. 7) | **bestemmer** hvorfor, hvordan og af hvem |
| **Databehandler** | behandler personoplysninger **på DA's vegne** (art. 4, nr. 8) | bestemmer **ikke** – handler efter **instruks** |
| **Underdatabehandler** | ingen selvstændig definition – en databehandler, der engageres af en anden databehandler | |

### Dataansvarlig eller databehandler?
- **Google Spain, C-131/12:** en **søgemaskine er dataansvarlig** for sin egen behandling (indeksering af tredjemands websider), fordi den selv afgør formål og hjælpemidler (præmis 33). Det ville stride mod ordlyden og formålet om "effektiv og fuldstændig beskyttelse" at undtage den (præmis 34). → Grundlaget for "retten til at blive glemt".
- **Datatilsynets vejledning (2017):** der foreligger kun en databehandlerkonstruktion, hvis en aftale går ud på, at den anden part skal behandle personoplysninger **efter instruks** fra DA. Det afgørende er, om DA **fortsat bestemmer formålet og de væsentligste behandlingsskridt** (indsamling, sletning, videregivelse, brug af underdatabehandlere).
- **Eksempler:** et IT-system til medlemsfakturering og et webhotel, der hoster en webshop → **databehandlere**.
- **Faldgrube:** en IT-konsulent hyres til at bygge et HR-webinterface uden en **konkret instruks** om behandling af personoplysninger → konsulenten kan blive **selvstændigt dataansvarlig**. Få altid en instruks og en databehandleraftale!

**Momenter, der taler for, at DU er dataansvarlig** (DT's vejledning):
oplysningerne behandles kun til dine formål · den anden part handler kun på dine vegne · du har ved lov fået pålagt opgaven · aftalen indeholder en (in)direkte **instruks** om behandling · opgaven kunne i princippet være udført af dig selv · du bestemmer formål og væsentlige hjælpemidler · den anden part gør intet uden din godkendelse · du **fører kontrol** · de registrerede forventer, at du er ansvarlig · du kan kræve oplysningerne tilbageleveret/slettet.

## 2. Databehandleraftale – art. 28
- **Art. 28, stk. 3:** behandlingen skal reguleres af en **bindende kontrakt**, der fastsætter genstand, varighed, karakter og formål, typen af oplysninger, kategorier af registrerede og DA's rettigheder og pligter. Databehandleren skal bl.a.:
  - a) kun behandle efter **dokumenteret instruks** (også ved overførsel til tredjelande)
  - b) sikre **fortrolighed/tavshedspligt** for autoriserede personer
  - c) iværksætte **sikkerhedsforanstaltninger efter art. 32**
  - d) overholde betingelserne for brug af **underdatabehandlere** (stk. 2 og 4)
  - e) **bistå** med at besvare de registreredes anmodninger (kap. III)
  - f) bistå med art. 32–36 (sikkerhed, brud, DPIA)
  - g) **slette eller tilbagelevere** alle data efter ophør
  - h) stille oplysninger til rådighed og bidrage til **revisioner/inspektioner**
- **Hvis ansvar?** DA's pligt – men databehandleren har også en interesse: **art. 28, stk. 10** – fastlægger databehandleren selv formål og hjælpemidler, **anses den for dataansvarlig** for den behandling.
- Datatilsynet har en **standardskabelon** for databehandleraftaler.

### Underdatabehandlere – art. 28, stk. 2 og 4
- Kræver **forudgående specifik eller generel skriftlig godkendelse** fra DA. Ved generel godkendelse: DA skal underrettes om ændringer og kunne gøre indsigelse.
- Underdatabehandleren pålægges **samme forpligtelser** som i hovedaftalen (stk. 4).
- **DT j.nr. 2019-442-3996 (Herning Kommune / EG A/S / ServiceNow):** EG brugte ServiceNow uden Herning Kommunes forudgående godkendelse; data kunne ikke garanteres inden for EU. Ved sikkerhedsbruddet var **databehandleren (EG) ansvarlig**, da den havde handlet uden for instruks → selvstændigt dataansvarlig, jf. art. 28, stk. 10.
- **Kiropraktorhuset / Uptime-IT ApS (2020):** ransomware krypterede både serveren og backuppen, og krypteringsnøglen var ikke sikret. Databehandleren havde ifølge aftalen ansvaret for at kunne genoprette tilgængeligheden og havde ikke testet backup-procedurerne → **politianmeldt og indstillet til bøde**.

### DA's tilsyn med databehandlere
- HR: DA skal føre **løbende tilsyn** (art. 5, stk. 2 – ansvarlighed). Det kan gøres af DA selv eller af en uafhængig tredjepart (revisor, advokat).
- **Fysisk tilsyn** (på stedet) eller **skriftligt tilsyn** (afrapportering, stikprøver, temakontroller).
- **Hyppighed** afhænger af risikovurderingen (høj risiko → måske årligt/halvårligt).
- Tilsyn med **underdatabehandlere** varetages som udgangspunkt af den oprindelige databehandler, men DA skal sikre sig, at det sker (fx via dokumentation).

## 3. Fælles dataansvar – art. 26
- HR: én DA. **U:** to eller flere parter **bestemmer i fællesskab formål og hjælpemidler**.
- Krav: en **aftale** med klar ansvarsfordeling. **Det væsentligste indhold skal gøres tilgængeligt** for de registrerede.
- **Solidarisk ansvar** over for den registrerede, uanset den indbyrdes aftale (art. 26, stk. 3).
- **Wirtschaftsakademie, C-210/16:** administratoren af en Facebook-fanside er **fælles dataansvarlig med Facebook**, fordi den via indstillinger (målgruppe, demografi) **bidrager til at afgøre formål og hjælpemidler** for Facebook Insights-statistikken.
- **Fashion ID, C-40/17:** en webshop, der indlejrer Facebooks "synes godt om"-knap (data sendes til Facebook, **uanset** om brugeren klikker eller er medlem), er **fælles dataansvarlig** med Facebook **for indsamling og videregivelse** – ikke for Facebooks efterfølgende behandling.
- **Rejsebureau-eksemplet:** et rejsebureau, der blot sender kundedata til et flyselskab og hotel for at booke = typisk **separate** DA'er. Hvis de opretter en **fælles platform** og aftaler brug, opbevaring, adgang og fælles markedsføring = **fælles DA**.

## 4. DA's pligter (overblik)
Lovligt grundlag · **fortegnelse** (også databehandler) · efterleve **de registreredes rettigheder** · anmelde **brud inden for 72 timer** · **databehandleraftaler** · kunne **dokumentere** passende tekniske og organisatoriske foranstaltninger (art. 24).

## 5. Behandlingsprincipperne – art. 5
> [!important] Hjørnestenen
> Principperne gælder **altid** og er ofte centrale for vurderingen af en behandlings lovlighed (Udsen s. 126). Seks principper i **stk. 1** + **ansvarlighed** i **stk. 2**.

| Litra | Princip | Indhold |
|---|---|---|
| a | **Lovlighed, rimelighed, gennemsigtighed** | behandlingsgrundlag, ingen skjult/urimelig behandling, klar information ("god databehandlingsskik") |
| b | **Formålsbegrænsning** | udtrykkeligt angivne, legitime formål; ingen uforenelig viderebehandling |
| c | **Dataminimering** | tilstrækkelige, relevante og begrænset til det nødvendige |
| d | **Rigtighed** | korrekte og ajourførte; urigtige oplysninger slettes/berigtiges straks |
| e | **Opbevaringsbegrænsning** | ikke identificerbare længere end nødvendigt |
| f | **Integritet og fortrolighed** | passende sikkerhed (tekniske og organisatoriske foranstaltninger) |
| stk. 2 | **Ansvarlighed** | DA er ansvarlig og skal kunne **påvise** overholdelse (indre: politikker/procedurer · ydre: kunne bevise det over for registrerede/tilsyn) |

### 5a. Lovlighed, rimelighed og gennemsigtighed
- **Lovlighed** (PR 39): behandlingsgrundlag efter art. 6–10/DBL §§ 5–14, lovhjemmel ved begrænsninger og respekt for **anden lovgivning** og menneskerettigheder.
- **DT j.nr. 2018-32-0065 (SKAT/SØIK):** SKAT brugte materiale, som SØIK havde indsamlet ulovligt (aflytning mellem klient og advokat i strid med retsplejeloven). En behandling i strid med anden lovgivning er heller ikke lovlig efter databeskyttelsesreglerne → **kritik**.
- **MEN DT j.nr. 2024-32-0482 (Helsingør Kommune):** kommunen måtte bruge en fars **ulovlige aflytning** af moren (han blev dømt efter strfl. § 263, stk. 2) i en underretningssag om barnets trivsel. I rimelighedsvurderingen indgår **hvordan og af hvem** oplysningerne er tilvejebragt og de **modstående interesser** (barnets tarv) → lovligt efter art. 6, stk. 1, litra e, og art. 5; ingen pligt til sletning. *Forskellen:* her var det **tredjemand**, ikke myndigheden selv, der havde skaffet oplysningerne ulovligt, og der var et tungtvejende hensyn.
- **Rimelighed:** ingen indsamling ved bedrag eller uden den registreredes viden. **LaLiga-appen (Spanien):** appen aktiverede **mikrofonen hvert minut** for at finde barer, der viste kampe uden licens; brugerne var ikke informeret og kunne ikke trække samtykket tilbage → **€ 250.000**.
- **Gennemsigtighed – Pant-appen (DT j.nr. 2023-431-0013):** det skal være **tydeligt og entydigt**, hvilke oplysninger der behandles, til hvilke formål og af hvem, i et klart sprog – tidligt i forløbet. Dansk Retursystem kunne ikke basere behandlingen på brugsscenarier (Tink-API), hvor man vidste, at der ville blive behandlet flere oplysninger end nødvendigt → overtrædelse af art. 5, stk. 1, litra a.

### 5b. Formålsbegrænsning
- Oplysninger skal **indsamles til udtrykkeligt angivne og legitime formål** (gælder alle faser). Formålet skal ligge fast ved indsamlingen – man må **ikke indsamle "fordi det måske bliver nyttigt"**.
- **Legitimt** = naturlig sammenhæng med DA's almindelige aktivitet.
- Viderebehandling må **ikke være uforenelig**. **U:** arkiv, forskning, statistik (art. 89); DBL § 5, stk. 3 (ministerregler for myndigheder); lovhjemmel; samtykke.
- **Forenelighedstesten, art. 6, stk. 4 (= DBL § 5, stk. 2):** (1) forbindelse mellem formålene, (2) sammenhængen ved indsamlingen og forholdet mellem den registrerede og DA, (3) oplysningernes art (art. 9/10?), (4) mulige konsekvenser, (5) garantier (kryptering, pseudonymisering).
- **DT j.nr. 2008-632-0034 (Forsvaret → Topdanmark):** udlevering af navne/adresser på ca. 15.000 ansatte til forsikringstilbud = **uforenelig**. Oplysningerne var indsamlet for at administrere et ansættelsesforhold, og de ansatte kunne ikke forvente markedsføring fra en privat virksomhed.

### 5c. Dataminimering
"Tilstrækkelige, relevante og begrænset til det nødvendige." Indebærer et **proportionalitetsprincip** og valg af det **mindst indgribende middel**.
- **DT j.nr. 2009-631-0099 (fitnesscenter):** 7 kameraer i herrernes omklædningsrum ved skabene (for at forhindre tyveri) – folk færdes nøgne → **for integritetskrænkende**; formålet står ikke mål med midlet (også i strid med rimelighed/lovlighed).
- **DT j.nr. 2018-432-0015 (Fredericia Gymnasium – ExamCookie):** overvågning af elevernes private computere under eksamen (URL'er, processer, clipboard, skærmbilleder). Gymnasiet havde ikke godtgjort, at alle oplysninger var **nødvendige** for at forebygge snyd, og havde givet mangelfulde/modstridende oplysninger → **kritik**.

### 5d. Rigtighed
- Urigtige oplysninger er også personoplysninger. Der skal tages **ethvert rimeligt skridt** for at slette/berigtige dem straks; kræver interne rutiner (PR 39).
- **DT j.nr. 2020-32-1733 (Danmarks Statistik):** blev ved med at ringe til en borger, der havde frabedt sig kontakt (manglende registrering på intern liste) → **ikke i overensstemmelse** med art. 5, stk. 1, litra d.

### 5e. Opbevaringsbegrænsning
- Ikke **identificerbare** længere end nødvendigt; DA bør fastsætte **slettefrister** eller periodisk gennemgang. U: arkiv, forskning, statistik (art. 89).
- **Typiske slettefrister:**

| Område | Frist | Hjemmel |
|---|---|---|
| Sædvanlig handel | 3 år | forældelsesloven § 3, stk. 1 |
| Personaleadministration | 5 år | forældelsesloven § 4 |
| Kundekendskab (hvidvask) | 5 år efter forretningsforbindelsens ophør | hvidvaskloven § 30, stk. 2 |
| Bogføring | 5 år fra udgangen af regnskabsåret | bogføringsloven § 10 |
| Forældelse af GDPR-overtrædelser | 5 år | DBL § 41, stk. 7 |

- **Taxa 4x35 (DT j.nr. 2018-41-0016):** slettede navn efter 2 år, men beholdt telefonnummer + turdata i 5 år ("ikke personhenførbart"). Det var forkert – oplysningerne kunne stadig henføres via telefonnummeret. Overskridelse på ca. 2 år → **indstillet til bøde på 1,2 mio. kr.**
- **IDdesign (DT j.nr. 2018-41-0015):** ca. 385.000 kunders oplysninger i et gammelt system uden slettefrister; kunne ikke dokumentere sletteprocedurer (**ansvarlighed!**) → indstillet til 1,5 mio. kr. (se forløbet i retten under [[Lektion 4 - Sikkerhed, konsekvensanalyse, brud, DPO og tilsyn#Danske bødesager|Lektion 4]]).

### 5f. Integritet og fortrolighed
"Tilstrækkelig sikkerhed … beskyttelse mod uautoriseret eller ulovlig behandling og mod hændeligt tab, tilintetgørelse eller beskadigelse, under anvendelse af passende tekniske eller organisatoriske foranstaltninger."
- **Integritet:** oplysningernes korrekthed og troværdighed over tid.
- **Fortrolighed:** uvedkommende (hackere, men også kolleger uden arbejdsbetinget behov) må ikke få adgang.
- Niveauet beror på en **konkret risikovurdering** → se [[Lektion 4 - Sikkerhed, konsekvensanalyse, brud, DPO og tilsyn]].

## 6. Cases
Se [[Øvelsescases og løsningsskitser#Lektion 2]]: BB og virksomhed C (forkert adresse i CRM), journalistspørgsmål (toiletliste i folkeskolen, jordemoder og etnicitet, diskotek med 30+ kameraer).

## Hurtig repetition
- [ ] Forskellen på DA og databehandler – og hvad sker der, når en databehandler går ud over instruksen (art. 28, stk. 10)?
- [ ] Mindstekrav til en databehandleraftale (art. 28, stk. 3)?
- [ ] Hvornår er der fælles dataansvar – Wirtschaftsakademie og Fashion ID?
- [ ] Nævn de 6 + 1 principper i art. 5 med et eksempel fra praksis på hver.
- [ ] Forenelighedstesten i art. 6, stk. 4.

Forrige: [[Lektion 1 - GDPR intro, anvendelsesområde og begreber]] · Næste: [[Lektion 3 - Behandlingsgrundlag og de registreredes rettigheder]]
