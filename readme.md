|                                                                                                                                            |                  |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- |
| Universitatea Tehnică Gheorghe Asachi din Iași<br />Facultatea de Automatică și Calculatoare<br />Departamentul de Automatică și Informatică Aplicată  | **Proiect SBC**  |

@authors: Taradaciuc\_Nicolae, Vicol\_Șerban-Ilie, Butacu\_Ionel-Cătălin

***

Taradaciuc_Nicolae, Vicol_Șerban-Ilie, Butacu_Ionel-Cătălin

\<Dezvoltarea unui Sistem Expert bazat pe cazuri pentru jocul
Battleship\>

**Rezumat**

În acest proiect s-a dorit realizarea unui sistem expert bazat pe cazuri
pentru jocul Battleship. Soluția cu care echipa noastră a venit este un
sistem ce este capabil să își schimbe comportamentul în funcție de
dificultatea aleasă dar și de situația în care se află jocul. Dacă trec
prea multe runde în care acesta nu poate găsi o navă pe tabla de joc
folosindu-se de atacul cu bombă atunci va trece la utilizarea atacurilor
de linie sau a atacului de scanare în dorința de a grăbi procesul de
localizare al unei nave. Pentru a face posibil aceste funcționalități
s-a utilizat atât limbajul de programare bazat pe reguli pentru a
descrie terenurile jucătorului și a sistemul expert, tipurile de atac și
mecanismele prin care se actualizează cele două terenuri, cât și
limbajul de programare python pentru realizarea unei interfețe grafice
intuitive pentru utilizator.

**1. Enunțul problemei. Obiective**

Problema propusă spre rezolvare este realizarea unui sistem expert bazat
pe cazuri capabil să ia decizii privind o nouă mutare cu scopul de a
doborî toate navele inamicului (utilizatorul uman) și a câștiga meciul.

Scopul principal al sistemului este să doboare navele oponentului prin
utilizarea unei singure abilități pe runda. În cazul unei lovituri cu
succes, sistemul are posibilitatea de a lua o nouă decizie și a ataca
din nou, bazând-se pe cunoștințele sale din mediul prezent.

Elementele de interes sunt navele ce pot avea două stări (atacată sau
nu), bombă și abilitați (scanare, etc). Bombele pot fi plasate pe o
singură porțiune din harta, o singură dată pe runda.

In final, utilizatorul uman va fi capabil să joace împotriva sistemului,
acesta din urmă schimbându-și comportamentul și strategiile de atac în
funcție de numărul de nave distruse de utilizator.

Exemplu de ipoteza:

-   Se poate lovi până în momentul în care lovitura este fară succes;

-   Ambii jucători au posibilitatea de a ataca(cu o bombă) cel puțin o
    dată în fiecare rundă;

-   Se poate folosi o singură abilitate(scanare) de către fiecare
    jucător, per rundă;

-   Dacă ai atacat o locație, nu o vei putea ataca din nou.

**2. Descrierea universul de discurs**

La începutul jocului, mediul de lucru va conține doar "nave" și
"poziție_neatacată". Pe parcursul jocului, utilizatorii "player" și
"sistem_expert" se vor ataca reciproc utilizând "bombă" sau "abilitate".
Un atac cu succes asupra unei nave va rezulta în schimbarea poziției
unei "nave" în "poziție_nava_distrusă", iar un atac eșuat asupra unei
"poziții_neatacate" o va transforma într-o "poziție_atacată". După ce
fiecare porțiune dintr-o "navă" este în întregime transformată în
"pozitie_nava_atacata", aceasta va deveni "nava_distrusa", iar
porțiunile vor trece in starea „poziție_navă_distrusă".

**a. Concepte**

Conceptele utilizate sunt: poziție_liberă, poziție_atacată, navă,
poziție_navă_atacată, navă_distrusă, bombă, abilitate, player,
sistem_expert

**b. Proprietăți**

Teren T1 poziția (rând, coloana) este liberă.

Teren T1 poziția (rând, coloana) este atacată.

Teren T1 poziția (rând, coloana) este ocupată de nava N2 și este
atacată.

Teren T1 poziția (rând, coloana) este ocupată de nava N3 și este
distrusă.

Sistemul decide.

Sistemul așteaptă.

**c. Relații**

Teren T1 nava N2 se află pe pozițiile ( x1, y1), (x2, y1), (x3, y1).

Teren T1 poziția (rând, coloana) este atacată cu B.

**d. Acțiuni**

Acțiunea de a ataca cu B poziția (x, y) din Terenul T1. Aceasta este
aplicabilă doar daca poziția nu a fost atacata anterior.

Acțiunea de a scana cu S poziția (x, y) din Terenul T2. Aceasta este
aplicabila oricând, dar abilitatea nu mai poate fi refolosita timp de 5
runde.

**3. Scenarii considerate**

Instanța 1: Distrugerea unei poziții de pe tabla de joc

Sistemul expert primește comanda de a ataca o poziție de pe tabla de joc
cu un atac de tip bombă.

Instanța 2 : Distrugerea unei linii de pe tabla de joc

Sistemul expert primește comanda de a ataca o poziție de pe tabla de joc
cu un atac de tip linie.

**4. Strategii de rezolvare**

Pentru instanța 1: Distrugerea unei poziții de pe tabla de joc

Pentru rezolvarea acestui scenariu, sistemul expert are nevoie să ia în
considerare două aspecte:

-   Dacă poziția este deja distrusă

-   Dacă poziția este ocupată de o porțiune de navă sau nu

În funcție de tipul poziției, sistemul expert o va considera poziție
liberă atacată sau poziție cu porțiune de navă atacată.

Pentru instanța 2: Distrugerea unei linii de pe tabla de joc

Pentru rezolvarea acestui scenariu, sistemul expert se va folosi de
poziția pe care o primește pentru a-și da seama care linie de pe tabla
de joc trebuie distrusă. Acesta va planifica o serie de atacuri de tip
bombă asupra tuturor pozițiilor de pe acea linie după care va intra
scenariul de mai sus.

**5. Definirea bazei de fapte**

a\. Tipare de fapte

(Teren \<ID_Teren\> poziția \<rând\> \<coloana\> este \<stare\>)

(Teren \<ID_Teren\> poziția \<rând\> \<coloana\> este ocupată de nava
\<ID_Navă\> si este \<stare_poziție_navă\>)

(Nava \<ID_Navă\> din poziția \<rând\> \<coloana\> este atacată cu
\<tip_atac\>)

(Sistem ataca poziția \<rând\> \<coloana\> din terenul \<ID_Teren\> cu
\<tip_atac\>)

(Jucător ataca poziția \<rând\> \<coloana\> din terenul \<ID_Teren\> cu
\<tip_atac\>)

(Nava orizontala \<ID_Navă\> rând \<ID_rând\> pe coloanele \<\<\<
indici_coloane\>\>\>)

(Nava verticala \<ID_Navă\> coloana \<ID_coloana\> pe rândurile \<\<\<
indici_rânduri\>\>\>)

(Nava \<ID_Navă\> în terenul \<ID_Teren\>)

(dificultate \<Nivel_dificultate\>)

(update_map \<Stare\>)

(calcul_frontiera \< rând \> \<coloana\>)

(frontiera \<rând_colt_stanga_sus\> \<coloana_colt_stanga_sus\>
\<rând_colt_dreapta_jos\> \<coloana_colt_dreapta_jos\>)

b\. Descriere prin fapte nestructurate

Faptele nestructurate din instanța 1:

-   Cazul pentru atacul unei poziții libere

> (Teren T1 poziția 6 7 este liber)
>
> (Sistem ataca poziția 6 7 din terenul T1 cu B)

-   Cazul pentru atacul unei porțiuni de navă

> (Teren T1 poziția 6 7 este ocupata de nava N1 și este neatacata)
>
> (Sistem ataca poziția 6 7 din terenul T1 cu B)

**6. Definirea bazei de reguli**

În situația în care se alege atacarea cu B (bombă) a unei poziții din
Terenul adversarului, iar poziția nu este atacată anterior atunci
această acțiune este realizabilă. Rezolvarea acestei situații este
concretizată în următoarea regulă denumita Actualizare_Teren_atacat_B:

Dacă sistemul sau jucătorul atacă poziția dată prin ?rand și ?coloana
din terenul ?Teren și poziția este liberă, atunci aceasta devine
atacată.

În situația în care regula Actualizare_Teren_atacata_B a dus la atacarea
unei nave vom prevedea o regulă pentru a-i actualiza starea. Rezolvarea
acestei situații este concretizată în următoarea regulă denumita
Actualizare_Nava_atacata_B:

Dacă sistemul sau jucătorul atacă poziția dată prin ?rand și ?coloana
din terenul ?Teren, poziția este ocupată de nava ?nava și este
neatacată, atunci starea navei devine atacată.

În situația în care se alege atacarea unei linii din Terenul
adversarului, fiecare poziție de pe acea linie va fi atacata cu o bombă,
cu condiția ca poziția să nu fi fost atacată anterior. Rezolvarea
acestei situații este concretizată în următoarele reguli denumite
Atac_linie_jucator și Atac_linie_sistem:

Dacă sistemul sau jucătorul atacă linia dată prin ?rand din terenul
?Teren, pozițiile libere neatacate/libere for deveni atacate.

În situația în care se alege scanarea unei porțiuni din Terenul
adversarului, fiecare poziție din acea porțiune va fi scanată pentru a
se detecta prezența a cel puțin unei nave fără a se oferi exact poziția
acesteia. Rezolvarea acestei situații este concretizată în următoarele
reguli denumite Atac_scanare_jucator și Atac_scanare_sistem:

Dacă sistemul sau jucătorul selectează o poziție pentru scanare,
porțiunea de scanat va fi o matrice de 3x3 cu centrul în poziția
selectată (?rand, ?coloana) din terenul ?Teren, atunci se va trimite
mesajul „Există o navă în zona scanată".

**7. Rezolvarea conflictelor**

**7.1 Cazuri conflictuale**

Conflict 1:

Un conflict ce a fost identificat în cadrul aplicației este închiderea,
deschiderea, scrierea si citirea din fișier într-o ordine incorectă,
ceea ce a dus la diferite erori precum "scrierea de informații într-un
fisier deja închis" și "citirea dintr-un fișier ce încă nu a fost
deschis".

Conflict 2:

Un alt conflict identificat a fost activarea reguli
Actualizare_Teren_atacat_B în timpul rulării regulilor Atac_linie_sistem
/ Atac_linie_jucator ceea ce a dus la diferite erori precum actualizarea
unei poziții înainte ca atacul liniei să fie finalizat.

**7.2 Strategii de rezolvare conflicte**

Rezolvare conflict 1:

Strategia utilizată pentru a rezolva acest conflict a fost utilizarea
priorităților, oferind regulilor urmatoarele priorități:
Rule_Opening_File_Read (100), Rule_Reading_Map (99),
Rule_Closing_File_Read (98), Rule_Opening_File_Write (97),
Rule_Writing_In_Map (96), Update_Map_Command (96) și
Rule_Closing_File_Write (95).

Rezolvare conflict 2:

Strategia utilizată pentru a rezolva acest conflict a fost utilizarea
priorităților, mărind prioritarea atacului de linie pentru a fi mai mare
decât regula de actualizare a poziției: Actualizare_Teren_atacat_B (1),
Atac_linie_sistem (10), Atac_linie_jucator (10).

**8. Schema (logică) de funcționare. Arbore decizional**

![A diagram of a company Description automatically
generated](.doc/image1.jpeg)

**9. Utilizare Clips în altă aplicație**

Limbajul utilizat: Python

Biblioteci utilizate: clipspy \[2\], NumPy \[3\], PyQt5 \[4\]

Funcții utilizate:

-   clipspy \[2\] : clear, load, reset, eval, run, facts, activations

-   NumPy \[3\] : zeros, random

-   PyQt5 \[4\] : connect, emit, blockSignals, move, show, exec, exit,
    parentWidget, addWidget, addLayout, setCursor, moveCursor,
    updateGeometry setObjectName, setStyleSheet, setProperty,
    setAlignment, setCheckable, setEnabled, setText, setFont,
    setCentralWidget, setWindowTitle, setFixedSize, setReadOnly,
    currentDateTime

Descriere interfață GUI:

Înainte de a începe jocul, suntem întâmpinați de o interfață simplă unde
trebuie sa ne introducem numele și să selectăm nivelul de dificultate.
Alegerea nivelului de dificultate influențează agresivitatea atacurilor
sistemului, realizând astfel o experiență de joc personalizată.

![A screenshot of a computer Description automatically
generated](.doc/image2.png)

Interfața va prezenta un teritoriu de luptă împărțit în două terenuri
distincte, unul pentru navele jucătorului (stânga) și celălalt pentru
navele sistemului (dreapta). În primul stadiu al jocului, atât sistemul
cât si jucătorul își vor amplasa navele aleator în propriile terenuri.
Navele pe care jucătorul și le va amplasa se află sub terenul acestuia.

![A screenshot of a computer game Description automatically
generated](.doc/image3.png)

Pe măsură ce jocul avansează, jucătorul va putea lansa o serie de
atacuri împotriva inamicului, atacuri precum bombe, scanare, atac în
linie, acestea fiind vizibile sub terenul inamicului. Pe parcursul
jocului, în ambele terenuri, fiecare stare („Poziție liberă/neatacată",
„Poziție atacată", „Nava atacată", „Navă găsită dar neatacată", "Navă
scanată și liberă") va fi reprezentată printr-o serie de simboluri
precum:

-   Pătrat albastru= Poziție liberă/neatacată

-   Pătrat albastru deschis cu simbolul "X" gri = Poziție atacată ( fără
    navă )

-   Pătrat albastru deschis cu simbolul "X" roșu = Nava atacată

-   Pătrat albastru cu simbolul "?" gri = Poziție scanată și liberă

-   Pătrat albastru cu simbolul "?"galben = Navă scanată, dar neatacată

**Concluzii**

Elemente pozitive:

-   interfața ce este simpla si intuitiva, permițând jucătorilor sa
    înceapă jocul rapid, fără a parcurge alte etape complicate

-   Personalizarea stilului de joc prin selectarea nivelului de
    dificultate.

-   Feedback-ul interactiv ce se află în partea de sus a interfeței si
    ne oferă date despre ce se acțiuni au loc pe parcursul jocului.

Elemente negative:

-   Nivelul de dificultate ar putea fi extins prin a afecta stilul de
    joc si prin alte modalități și nu doar atacurile sistemului.

-   În momentul scanării, jucătorul știe exact poziția navelor de pe
    hartă, nu doar un detaliu precum existența sau absența lor.

Posibilități de îmbunătățire:

-   Rezolvarea unei erori întâmpinate în integrarea clips-ului \[5\] cu
    interfața python.

-   Îmbunătățirea algoritmului de căutare și atac al sistemului
    (Actualmente, incomplet).

```{=html}
<!-- -->
```
-   Adăugarea unui ghid explicativ cu o scurtă descriere a fiecărui
    nivel de dificultate și a diferențelor dintre acestea.

-   Îmbunătățiri vizuale pentru a face interfața mai atrăgătoare și
    captivantă.

-   Modificarea atacului de scanare pentru a oferi detalii precum
    existența sau absența de nave în zona respective, nu exact sterile
    tuturor pozițiilor scanate.

-   Adăugarea unei bombe ca obiect de amplasat pe hartă, pentru a crea o
    experiență de joc mai detaliată.

**Bibliografie**

\[1\] Panescu D., Pascal C., Programare bazată pe reguli, Îndrumar de
laborator, Editura Conspress, București, 2013, ISBN 978-973-100-258-3.\
\[2\] Documentație, librăria clipspy, <https://clipspy.readthedocs.io>\
\[3\] Documentație, librăria NumPy, <https://numpy.org/>

\[4\] Documentație, librăria PyQt5,
<https://www.riverbankcomputing.com/static/Docs/PyQt5/>

\[5\] Manual Clips, CLIPS Reference Manual Volume I Basic Programming
Guide, Version 6.30 March 17th 2015
