---
tags: [it-ret, gdpr, lektion1]
pensum: "Udsen kap. 1–2 · DBF art. 1–4 · DBL §§ 1–4"
---
# Lektion 1 – GDPR: baggrund, anvendelsesområde og begreber

## 1. Hvorfor databeskyttelse?
Personoplysninger kan misbruges. **TIM-sagen (Italien):** teleselskabet TIM brugte callcentre til "kold kanvas" – nogle blev ringet op 155 gange om måneden, over 200.000 ikke-kunder blev kontaktet, og folk, der bad om at blive fjernet fra listen, kom på den igen. **Bøde: € 27,8 mio.** for ugyldigt samtykke, at de registrerede ikke kunne udøve deres rettigheder, og en ulovlig opbevaringsperiode på 10 år.

## 2. Formål – art. 1
GDPR har **to formål**:
1. **Beskyttelse af fysiske personer** ved behandling af personoplysninger (grundlæggende rettigheder, særligt retten til beskyttelse af personoplysninger), art. 1, stk. 2.
2. **Fri udveksling af personoplysninger** i EU, art. 1, stk. 3.

**Samspil:** GDPR er en forordning og gælder umiddelbart. **DBL** supplerer og gennemfører den, fx med danske særregler om CPR-nr. (§ 11), strafbare forhold (§ 8) og straf (§ 41).

## 3. Anvendelsesområdet – overblik
| | GDPR | DBL |
|---|---|---|
| **Materielt** (hvilken behandling?) | art. 2 | §§ 1–3 |
| **Territorialt** (hvor?) | art. 3 | § 4 |

> [!important] Hovedregel
> GDPR gælder, hvis der sker **1) behandling** af **2) personoplysninger**, jf. art. 2, stk. 1 – helt eller delvis **automatisk**, eller **manuelt**, hvis oplysningerne er/skal indgå i et **register**.

### 3.1 Behandling – art. 4, nr. 2
"Enhver aktivitet eller række af aktiviteter … f.eks. indsamling, registrering, organisering, systematisering, opbevaring, tilpasning eller ændring, genfinding, søgning, brug, videregivelse …, sammenstilling eller samkøring, begrænsning, sletning eller tilintetgørelse."
- Begrebet er **meget bredt**. Allerede **indsamling** er behandling – også sletning er behandling.
- Eksempler: lønadministration, opslag i en kontaktdatabase, reklamemails, makulering, billede på en hjemmeside, **lagring af IP-/MAC-adresser**, videoovervågning.
- **Automatisk** = digital/computer. **Ikke-automatisk** = manuel ("papir og pen") – kun omfattet ved et **register** (struktureret samling tilgængelig efter bestemte kriterier, art. 4, nr. 6).
- **Mundtlige oplysninger:** HR ikke omfattet. **U:** omfattet, hvis oplysningen også behandles elektronisk – **U.2011.2343 H** (en kommune videregav telefonisk en reference om mistanke om alkoholmisbrug; oplysningen fandtes også i et elektronisk sagsregister → omfattet).

### 3.2 Personoplysning – art. 4, nr. 1
"Enhver form for information om en identificeret eller identificerbar fysisk person." Fire elementer:
1. **Enhver form for information** (også urigtige oplysninger og vurderinger)
2. **om**
3. en **identificeret eller identificerbar**
4. **fysisk person**

- **Identificeret:** du ved, hvem personen er (fx banken).
- **Identificerbar:** personen kan identificeres **direkte eller indirekte** (navn, id-nr., lokaliseringsdata, online-identifikator …) – af den dataansvarlige **eller en hvilken som helst anden**.
- **PR 26:** alle midler, der **med rimelighed** kan tænkes bragt i anvendelse af den dataansvarlige eller en anden person.
- **Anonymiserede** oplysninger er **ikke** omfattet (pseudonymiserede er!).
- **Breyer, C-582/14:** en **dynamisk IP-adresse** var en personoplysning for en udbyder af online-medietjenester, fordi udbyderen havde **lovlige midler** (via myndigheden og internetudbyderen ved fx angreb) til at få personen identificeret.

### 3.3 Fysisk person
| Beskyttet | Ikke beskyttet |
|---|---|
| Levende personer | Kapitalselskaber (IVS, ApS, A/S) |
| **Afdøde i 10 år**, jf. **DBL § 2, stk. 5** | Fonde, selvejende institutioner |
| Enkeltmandsvirksomheder, I/S (fordi de er knyttet til personer) | Offentlige myndigheder |

### 3.4 Undtagelser – art. 2, stk. 2
GDPR gælder **ikke** for behandling
- a) uden for EU-retten,
- b) af medlemsstaterne under den fælles udenrigs- og sikkerhedspolitik (TEU afsnit V kap. 2),
- c) **af en fysisk person som led i rent personlige eller familiemæssige aktiviteter** (husholdningsundtagelsen),
- d) af kompetente myndigheder til at forebygge/efterforske/retsforfølge strafbare handlinger (→ retshåndhævelsesdirektivet/-loven).

**Husholdningsundtagelsen fortolkes strengt:**
- **Ryneš, C-212/13:** et privat kamera, der også filmede offentlig vej og genboens indgang → **ikke** rent personligt; GDPR gælder.
- **Lindqvist, C-101/01:** offentliggørelse af oplysninger om kolleger (inkl. en skadet fod = helbredsoplysning) på en hjemmeside, tilgængelig for **et ubestemt antal personer** → **ikke** rent personligt.
- **Bestemt antal personer?** HR: undtagelsen kan gælde. **U:** stor gruppe → omfattet. **U.2018.1675 Ø:** en mor delte billeder fra overvågningsvideo af en mand, der blottede sig, i en Facebook-gruppe med **>9.000 medlemmer** + på sin åbne profil → omfattet. Den nedre grænse er en **konkret vurdering**.

## 4. Territorialt anvendelsesområde – art. 3 (DBL § 4)
- **Art. 3, stk. 1 – etableringskriteriet:** GDPR gælder for behandling som led i aktiviteter i en **etablering** af en DA/databehandler i EU, **uanset hvor behandlingen sker**. *PR 22:* etablering = effektiv og faktisk udøvelse af aktivitet gennem en mere permanent struktur; retlig form (filial/datterselskab) er ikke afgørende.
- **Art. 3, stk. 2 – målretningskriteriet:** DA uden for EU er omfattet, hvis behandlingen vedrører registrerede **i EU** og angår
  - **a) udbud af varer/tjenester** (også gratis) – *PR 23:* momenter som lokalt sprog, valuta, mulighed for bestilling, omtale af kunder i EU; det er **ikke nok**, at hjemmesiden blot er tilgængelig.
  - **b) overvågning af adfærd** i EU – *PR 24:* sporing på nettet, profilering.
- **Repræsentant (art. 27):** gælder art. 3, stk. 2, skal der skriftligt udpeges en repræsentant i EU. Det **ændrer ikke ansvaret** (art. 27, stk. 5).

| Etablering | GDPR? | DBL? | Repræsentant? |
|---|---|---|---|
| I EU, ikke i DK | Ja, art. 3(1) | Nej | Nej |
| I DK | Ja | Ja | Nej |
| Uden for EU | HR nej. **U1:** ja ved udbud af varer/tjenester til personer i EU (art. 3(2)(a)). **U2:** ja ved overvågning (art. 3(2)(b)) | Tilsvarende for personer i DK, DBL § 4, stk. 3, nr. 1–2 | **Ja**, art. 27(1) |

## 5. Legaldefinitioner – art. 4 (de vigtigste)
| Nr. | Begreb | Kerne |
|---|---|---|
| 1 | Personoplysning | info om identificeret/identificerbar fysisk person ("den registrerede") |
| 2 | Behandling | enhver aktivitet med personoplysninger |
| 4 | Profilering | automatisk behandling til at evaluere/forudsige personlige forhold |
| 5 | Pseudonymisering | kan ikke henføres uden supplerende oplysninger, der opbevares separat – **stadig personoplysning** |
| 6 | Register | struktureret samling tilgængelig efter bestemte kriterier |
| 7 | Dataansvarlig | afgør **formål og hjælpemidler** (alene eller sammen med andre) |
| 8 | Databehandler | behandler **på vegne af** den dataansvarlige |
| 9 | Modtager | den, oplysningerne videregives til |
| 10 | Tredjemand | andre end den registrerede, DA, databehandler og personer under deres myndighed |
| 11 | Samtykke | **frivillig, specifik, informeret og utvetydig** viljestilkendegivelse |
| 12 | Brud på persondatasikkerheden | brud, der fører til hændelig/ulovlig tilintetgørelse, tab, ændring, uautoriseret videregivelse/adgang |

Art. 4 bruges til at (1) afgrænse anvendelsesområdet, (2) fastlægge roller og ansvar, (3) danne grundlag for juridiske vurderinger og (4) skabe et fælles sprog.

## 6. Cases fra lektionen
Se løsningsskitser i [[Øvelsescases og løsningsskitser#Lektion 1]]:
- Pædagogen i metroen (Facebook-opslag til 1.200 venner + deling af to kendisser med 550.000 og 125.000 følgere)
- BIG IDEAS Corp. (amerikansk betting-site, .de-domæne, tysk annoncering)
- Bloggeren med amerikansk cloudhosting

## Hurtig repetition
- [ ] Hvilke to formål har GDPR?
- [ ] Hvad skal der til, for at GDPR finder anvendelse (materielt)?
- [ ] De fire elementer i "personoplysning"?
- [ ] Hvornår er en IP-adresse en personoplysning (Breyer)?
- [ ] Hvornår gælder husholdningsundtagelsen ikke (Ryneš, Lindqvist)?
- [ ] Art. 3, stk. 1 vs. stk. 2 – og hvornår kræves en repræsentant?

Oversigt: [[00 - IT-ret Oversigt]] · Næste: [[Lektion 2 - Aktører og behandlingsprincipper]]
