> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Cum sunt stocate numerele întregi în octeți

[00:00:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=0s) Obiectivul este să legăm un șir de celule pline și goale de un număr întreg: mai întâi numărăm valorile pe care le poate ține un octet, apoi combinăm octeți, le scrim biții în hexazecimal și, în final, interpretăm valorile negative și aritmetica care depășește lățimea disponibilă.

Vocabularul folosit pe tot parcursul lecției este:

- **Bit**: o cifră binară, fie 0, fie 1. Un **octet** este grupul de opt biți folosit în această lecție. Un bit **setat** conține 1; un bit **șters** (clear) conține 0.
- **Sistem de numerație pozițional**: o modalitate de a scrie numere în care fiecare cifră are o valoare determinată de poziția ei. **Baza**, sau radixul, este numărul de cifre posibile: binarul are baza 2, zecimalul baza 10, iar hexazecimalul baza 16.
- **Valoare de poziție**, sau pondere: înmulțitorul asociat unei poziții. Pozițiile se numerotează de la zero spre dreapta; poziția `k` în baza `r` are ponderea `r^k`. Aici `^` înseamnă exponențiere matematică, nu un operator de programare.
- **Număr întreg fără semn**: un număr întreg interpretat fără valori negative. Un **număr întreg cu semn** reprezintă și valori negative. **Lățimea** este numărul de biți disponibili. `int` este tipul de număr întreg C++ menționat în înregistrare; dimensiunea lui nu este fixată de acest desen.
- **Cifră hexazecimală**: una dintre `0–9, A–F`. **Nibble** înseamnă patru biți, așadar un octet are doi nibble-uri. Prefixul `0x` identifică notația hexazecimală și nu face parte din valoare.
- **Bit cel mai semnificativ**: bitul cu ponderea pozițională cea mai mare; **bitul cel mai puțin semnificativ** are ponderea cea mai mică. În **complement de doi**, bitul cel mai înalt are pondere negativă, iar toate celelalte ponderi rămân pozitive. Acest bit cel mai înalt este **bitul de semn**.
- **Inversarea biților**: schimbarea fiecărui 0 cu 1 și a fiecărui 1 cu 0. Inversarea modulului pozitiv și adunarea lui 1 produc reprezentarea sa negativă în complement de doi, la aceeași lățime.
- **Transport**: o cantitate transmisă poziției următoare, mai înalte, în timpul adunării. **Împrumut**: o cantitate preluată de la o poziție mai înaltă în timpul scăderii.
- **Trunchiere**: eliminarea pozițiilor din afara lățimii destinației. **Rebucle**: revenirea rezultatului la o altă valoare din intervalul de lățime fixă.
- **Depășire**: un rezultat matematic aflat în afara intervalului reprezentabil. Înregistarea folosește și termenul **subdepășire** pentru scăderea sub acel interval, cu unele variații de denumire în exemplele cu semn.

Pentru exerciții, folosește [laboratorul despre stocarea numerelor în octeți](../../../en/labs/common/03_numbers.md). Înregistrarea este o lecție bazată pe desene și aritmetică: nu construiește și nu rulează un program C++. Stările calculate sunt susținute de [transcrierea fixată la un commit](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6/videos/cpp/08_%D0%9A%D0%B0%D0%BA_%D1%86%D0%B5%D0%BB%D1%8B%D0%B5_%D1%87%D0%B8%D1%81%D0%BB%D0%B0_%D1%85%D1%80%D0%B0%D0%BD%D1%8F%D1%82%D1%81%D1%8F_%D0%B2_%D0%B1%D0%B0%D0%B9%D1%82%D0%B0%D1%85/internal/transcript.md), care înregistrează explicația, nu o stare de cod executabil.

[00:04:22](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=262s) Un exemplu aritmetic simplificat din acea explicație citește biții setați ai unui octet după ponderile lor poziționale:

```text
01010100 = 64 + 16 + 4 = 84
```

**Domeniu de aplicare:** exemplele presupun octeți de opt biți și o lățime fixă a destinației. Ele explică reprezentarea și aritmetica la nivel de mașină, nu evaluarea expresiilor C++, conversiile automate de tipuri și nici garanția că orice expresie C++ care depășește limitele se rebuclează. De asemenea, ordinea logică a grupurilor de octeți într-un număr scris nu stabilește ordinea lor fizică în memorie.

## Biți și octeți

[00:00:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=0s) Pornește de la opt celule. Fiecare celulă este un **bit**, o cifră binară cu două stări posibile; împreună, acești opt biți formează un **octet**. Celulele goale și cele pline sunt un model pentru aceste stări.

[00:00:10](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=10s) O celulă goală, adică ștearsă, înseamnă 0; o celulă plină, adică setată, înseamnă 1. Astfel, **binarul**, sistemul de numerație cu baza 2, este o notație naturală pentru tipar:

```text
eight clear cells:  00000000
a different pattern: 01010100
```

[00:00:18](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=18s) Opt poziții nu pot exprima numere arbitrar de mari. Pentru a determina limita, separă mai întâi două întrebări: câte tipare sunt disponibile și care este cea mai mare valoare dintre ele?

## Numărarea valorilor în orice bază

[00:00:33](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=33s) Un **sistem de numerație pozițional** atribuie o pondere fiecărei poziții a cifrelor. **Baza** sa `r` precizează ce cifre pot ocupa o poziție: de la `0` la `r − 1`.

[00:00:39](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=39s) În **zecimal**, cu baza 10, trei poziții conțin cifre de la 0 la 9. Cel mai mare număr este 999. [00:00:51](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=51s) Fiecare poziție are o pondere fixă, așadar plasarea cifrei maxime permise în fiecare poziție maximizează totalul.

[00:01:09](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=69s) Numără tiparele în ordine:

1. Pornește de la `000`.
2. Crește cifra din dreapta: `001, 002, …, 009`.
3. Continuă în poziția următoare: `010, 011, …`.
4. Se termină la `999`.

Fiecare număr întreg din interval apare, fără goluri. [00:01:32](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=92s) Există **1.000 de valori**, incluzând zero, deși cea mai mare valoare este 999.

[00:01:43](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=103s) Fiecare dintre cele `N` poziții are `r` posibilități, independent de celelalte. Prin urmare:

```text
number of patterns = r^N
unsigned range     = 0 through r^N − 1

three decimal positions: 10^3 = 1000 patterns
largest value:            10^3 − 1 = 999
```

De ce maximul este cu unu mai mic decât numărul tiparelor?

<details>
<summary>Răspuns</summary>

Valorile pornesc de la zero. O succesiune de 1.000 de valori care începe de la zero se termină la 999, nu la 1.000.

</details>

## Intervalul unui octet fără semn

[00:02:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=120s) Un octet **fără semn** interpretează toate cele opt poziții cu ponderi binare pozitive. Înlocuiește baza 2 și lățimea 8 în regula de numărare:

```text
2^8 = 256 distinct patterns
```

[00:02:23](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=143s) Intervalul este **de la 0 la 255**, inclusiv. Zero nu are niciun bit setat; 255 are toți biții setați.

```text
00000000 → 0
11111111 → 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255
```

[00:02:39](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=159s) Problema devine acum concretă: 256 nu are niciun tipar disponibil într-un singur octet fără semn. Stocarea lui, sau a oricărui număr întreg mai mare, necesită mai multe poziții.

## Construirea unui număr zecimal mai mare

[00:02:47](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=167s) În zecimal, ajungerea la 10, 100 sau 1.000 necesită adăugarea unei poziții superioare. **Valoarea de poziție** este înmulțitorul atașat acelei poziții. Scris în mod convențional, poziția din dreapta are ponderea 1, apoi 10, apoi 100.

[00:03:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=180s) Puterile 10, 100 și 1.000 ilustrează ponderi succesiv mai mari; nu sunt ponderile tuturor celor trei cifre dintr-un număr întreg de trei cifre. Un al doilea grup de trei cifre asigură ponderile 1.000, 10.000 și 100.000:

```text
positions:  hundred-thousands ten-thousands thousands | hundreds tens ones
weights:         100000           10000       1000    |   100     10    1
```

[00:03:17](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=197s) Păstrează grupurile în celule separate, dar atribuindu-le poziții diferite. Astfel, ele pot fi interpretate ca un singur număr mai mare.

[00:03:43](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=223s) Cu 999 în fiecare grup, valoarea combinată este **999.999**:

```text
high group | low group
    999    |    999

999 × 1000 + 999 = 999999
```

Înregistrarea scrie `999.999` drept notație de grupare; nu înseamnă o fracție zecimală. [00:03:59](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=239s) Cea mai joasă poziție a grupului din stânga este poziția miilor. Contribuția sa vine din locul unde aparține grupul, nu doar din câte cifre conține. Adăugarea unui grup superior extinde numărul spre stânga în notația scrisă convențională.

## Combinarea a doi octeți

[00:04:06](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=246s) Aplică aceeași construcție octeților. Pune alături două grupe de câte opt biți, tratând una ca grup superior și cealaltă ca grup inferior.

[00:04:22](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=262s) În interiorul unui octet, un bit setat își contribuie ponderea, iar un bit șters contribuie cu zero. De la dreapta la stânga, ponderile sunt `1, 2, 4, 8, 16, 32, 64, 128`. **Bitul cel mai puțin semnificativ** este bitul din dreapta, cu ponderea 1; **bitul cel mai semnificativ** este poziția cea mai înaltă.

Primul exemplu are valoarea 84:

```text
01010100 = 64 + 16 + 4 = 84
```

[00:04:48](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=288s) Octețului vecin i se atribuie valoarea 85. [00:04:52](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=292s) Pentru a-i combina, ține cont de cele opt poziții inferioare deja ocupate de al doilea octet:

1. Citește octetul superior ca 84.
2. Înmulțește-l cu `2^8 = 256`, deoarece primul său bit începe cu opt locuri deasupra primului bit al octețului inferior.
3. Adună valoarea octețului inferior, 85.

[00:05:44](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=344s) Rezultatul calculat este:

```text
high byte | low byte
01010100  | 01010101

84 × 256 + 85 = 21589
```

Aceasta este o interpretare pozițională a două grupuri. Ea nu precizează pe care dintre grupuri calculatorul îl stochează la adresa de memorie mai mică.

## Cele șaisprezece cifre hexazecimale

[00:05:49](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=349s) **Hexazecimalul** este un sistem de numerație pozițional cu baza 16, folosit frecvent pentru a scrie compact tiparele binare.

[00:05:59](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=359s) Cele șaisprezece cifre ale sale sunt:

| Simbol | Valoare |
| --- | --- |
| 0–9 | 0–9 |
| A | 10 |
| B | 11 |
| C | 12 |
| D | 13 |
| E | 14 |
| F | 15 |

[00:06:20](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=380s) O literă precum F este o singură cifră a cărei valoare este cincisprezece. [00:06:30](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=390s) Numele hexazecimal se referă la aceste șaisprezece cifre posibile.

## O cifră hexazecimală la fiecare patru biți

[00:06:39](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=399s) Împarte un octet în două **nibble-uri**, adică grupuri de patru biți. Fiecare nibble are `2^4 = 16` tipare posibile, ceea ce corespunde exact celor șaisprezece cifre hexazecimale.

[00:06:59](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=419s) Așadar, orice tipar de patru biți corespunde exact unei cifre hex. Citește fiecare grup folosind ponderile sale locale `8, 4, 2, 1`:

- [00:07:14](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=434s) `0101` dă `4 + 1 = 5`, deci scrii 5.
- [00:07:22](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=442s) `0100` dă 4, deci scrii 4.
- [00:07:23](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=443s) `1111` dă `8 + 4 + 2 + 1 = 15`, deci scrii F.

[00:07:43](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=463s) Unește nibble-ul superior F cu nibble-ul inferior 5:

```text
1111 0101 → F 5 → 0xF5
```

**Prefixul 0x** marchează notația hexazecimală. Nu adaugă biți și nu schimbă valoarea.

[00:07:52](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=472s) Șirurile lungi de zerouri și de unu sunt greu de citit. [00:08:05](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=485s) Hexazecimalul înlocuiește fiecare grup de patru biți cu un singur simbol, așa că opt biți necesită doar două cifre hex.

Prezice forma hexazecimală a lui `0101 1111`.

<details>
<summary>Răspuns</summary>

Nibble-ul superior este 5, iar nibble-ul inferior este F, deci octetul este 0x5F. Inversarea cifrelor ar schimba valoarea.

</details>

## De ce valorile de poziție hexazecimale coincid cu cele binare

[00:08:13](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=493s) Gruparea funcționează pentru că valorile de poziție hexazecimale coincid cu fiecare a patra valoare de poziție binară:

```text
16^0 = 2^0 = 1
16^1 = 2^4 = 16
16^2 = 2^8 = 256
16^k = 2^(4k)
```

Mutarea cu o poziție hex spre stânga mută patru poziții binare spre stânga. Ponderea se modifică cu un factor de 16.

[00:08:29](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=509s) Zecimalul nu oferă aceeași înlocuire cu un singur simbol pentru un nibble. Înlocuirea lui F cu cele două caractere `15` ar introduce două poziții zecimale. De exemplu, `F5` înseamnă `15 × 16 + 5 = 245`; șirul zecimal `155` înseamnă alt număr.

[00:08:49](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=529s) Ai putea scrie valorile nibble-urilor separat, ca `[15, 5]`, dar aceasta este o listă de valori de grup, nu notația zecimală obișnuită a întregului număr. Zecimalul nu are o singură cifră pentru cincisprezece.

## Citirea unui număr care se întinde pe patru octeți

[00:09:02](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=542s) Gruparea hexazecimală funcționează la orice lățime. Patru octeți de câte opt biți conțin 32 de biți, deci opt cifre hexazecimale.

[00:09:18](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=558s) Înregistrarea menționează **int**, tipul de număr întreg C++, ca ocupând în mod obișnuit patru octeți și menționează și cazuri de opt octeți. [00:09:27](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=567s) Folosește patru octeți pentru acest exemplu; nu transforma acea dimensiune frecventă într-o garanție universală de dimensiune. Cele opt cifre hex din desen rezultă din lățimea aleasă pentru el.

[00:09:37](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=577s) Pozițiile hex individuale au ponderile `16^k = 2^(4k)`. Un octet întreg conține două asemenea cifre, deci grupurile succesive de octeți au ponderile `2^0, 2^8, 2^16, 2^24`.

[00:09:50](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=590s) Pentru a obține valoarea zecimală, înmulțește fiecare cifră sau grup cu ponderea poziției sale și adună contribuțiile.

[00:10:04](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=604s) Pentru exemplul cu octeți repetați, fiecare octet este citit ca 135. **135 este valoarea unui octet întreg, nu o cifră hexazecimală**: este `0x87`. Dezvoltarea corespunzătoare fără semn este:

```text
byte groups:  87 87 87 87
hex notation: 0x87878787

135 × 2^24 + 135 × 2^16 + 135 × 2^8 + 135 × 2^0
```

[00:10:23](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=623s) Dezvoltarea grupurilor reconstruiește același număr întreg fără semn. Ultimul termen este pur și simplu 135, deoarece `2^0 = 1`. Ca verificare aritmetică a acelei dezvoltări scrise:

```text
2264924160 + 8847360 + 34560 + 135 = 2273806215
```

Această sumă zecimală este o verificare a formulei, nu rezultatul unei rulări de program. [00:10:44](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=644s) Înmulțirea fiecărui grup este anevoioasă; păstrarea reprezentării hexazecimale este de obicei mai simplă atunci când scopul este inspectarea biților.

## Scrierea biților în formă compactă

[00:11:38](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=698s) Pentru a scrie în hexazecimal un tipar binar mai lung:

1. Împarte-l în grupuri de patru biți, pornind din dreapta.
2. Citește fiecare grup ca o valoare de la 0 la 15.
3. Înlocuiește-l cu cifra hex corespunzătoare.
4. Păstrează grupurile în ordinea lor inițială.

[00:11:54](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=714s) O succesiune ilustrată mai lungă se scrie în formă compactă precum:

```text
… 1111 0100 1111 0100 1111 0100 0101 0010 1111 0101
…    F    4    F    4    F    4    5    2    F    5
```

Punctele indică grupuri precedente, nu cifre hexazecimale. [00:12:09](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=729s) Notația mai scurtă păstrează tiparul; nu comprimă și nu modifică biții stocați.

## Citirea numerelor negative în complement de doi

[00:12:14](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=734s) Un **număr întreg cu semn** trebuie să distingă valorile negative de cele nenegative. În **complement de doi**, se schimbă doar ponderea pozițională cea mai înaltă: pentru o valoare pe opt biți aceasta este `−2^7 = −128`, în timp ce ponderile inferioare rămân pozitive.

[00:12:29](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=749s) Ponderile cu semn, de la stânga la dreapta, sunt:

```text
bit position:    7   6   5   4   3   2   1   0
signed weight: −128 64  32  16   8   4   2   1
```

[00:12:44](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=764s) Așadar, un tipar cu bitul cel mai înalt setat este negativ. De exemplu, citește tiparul denumit E1 după regulă:

```text
0xE1 = 11100001
signed value = −128 + 64 + 32 + 1 = −31
```

Narațiunea din jurul acestui exemplu menționează și −18, apoi calculează `−128 + 64 + 32 + 4 = −28` la [00:13:13](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=793s). Acestea sunt tipare diferite: suma din urmă descrie `0xE4`, nu `0xE1`. Verifică tiparul folosind ponderile, în loc să preiei în continuare o valoare rostită inconsistentă.

[00:13:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=780s) Când bitul cel mai înalt este șters, contribuția sa negativă dispare. Setarea doar a pozițiilor 16 și 4 dă `00010100 = 20`. Un tipar format numai din zerouri dă zero, așadar „bitul cel mai înalt este șters” înseamnă **nenegativ**, zero fiind inclus.

[00:13:04](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=784s) Pentru a construi un tipar negativ, **inversează** biții modulului său pozitiv — schimbă 0 cu 1 și 1 cu 0 — și adaugă apoi unu la aceeași lățime. O derivare clară pentru −18 este:

1. Scrie +18 ca `00010010`.
2. Inversează toți cei opt biți: `11101101`.
3. Adună unu: `11101110`.
4. Verifică ponderile cu semn: `−128 + 64 + 32 + 8 + 4 + 2 = −18`.

Această derivare clarifică reprezentarea; contribuțiile intermediare rostite în acest punct nu se adună în mod consecvent la −18.

[00:13:23](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=803s) Bitul cel mai înalt se numește **bit de semn** pentru că starea sa distinge valorile negative de cele nenegative. El rămâne parte din numărul ponderat; nu este un simbol de minus separat atașat unei mărimi altfel fără semn.

## Corectarea limitelor octetului cu semn

[00:13:37](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=817s) Discuția despre „toți biții setați”, −1 și 127 necesită o distincție precisă. Tiparul format numai din unu-uri nu este nici cel mai negativ octet cu semn, nici cel mai mare octet pozitiv cu semn:

```text
11111111 = −128 + 127 = −1
01111111 =    0 + 127 = 127
10000000 = −128 +   0 = −128
```

[00:14:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=840s) **127 este cea mai mare valoare pozitivă cu semn pe opt biți.** Cei șapte biți inferiori sunt toți setați, iar bitul de semn este șters. Setarea tuturor celor opt biți produce în schimb −1. Maximul fără semn rămâne 255.

[00:14:12](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=852s) Ștergerea bitului de semn din `11111111` dă `01111111`, adică 127. Acea observație explică cele șapte poziții cu pondere pozitivă, dar nu face din 127 cea mai mare mărime negativă. Intervalul cu semn este **de la −128 la 127**, iar `10000000` reprezintă −128. Faptul că alegi să stochezi doar numere negative nu schimbă aceste ponderi de complement de doi.

De ce există o valoare negativă în plus față de cele pozitive?

<details>
<summary>Răspuns</summary>

Bitul înalt contribuie cu −128. Cu el șters, cei șapte biți inferiori dau valori de la 0 la 127. Cu el setat, aceleași combinații de biți inferiori dau valori de la −128 la −1. Zero aparține jumătății nenegative.

</details>

## Scăderea unuia dintr-un octet format numai din zerouri

[00:14:29](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=869s) Un alt mod de a înțelege reprezentarea lui −1 ca șir de unu-uri este să pornești de la `00000000` și să scăzi unu. Un **împrumut** transferă valoare de la o poziție mai înaltă, astfel încât scăderea să poată continua la poziția curentă.

[00:14:46](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=886s) Urmează scăderea de la poziția cea mai joasă:

1. Zero-ul cel mai jos nu poate furniza unul care se scade, deci ceri un împrumut de la poziția următoare.
2. [00:15:05](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=905s) Acea poziție este tot zero, deci trimite cererea de împrumut mai sus.
3. Repetă prin fiecare poziție cu zero.
4. [00:15:31](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=931s) Imaginează o poziție mai înaltă, din afara octetului, care furnizează împrumutul. Păstrează doar cele opt poziții care aparțin într-adevăr valorii stocate.

[00:15:56](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=956s) Tiparul păstrat este:

```text
00000000 − 1 → 11111111   (keeping eight bits)

unsigned interpretation: 255
signed interpretation:   −1
```

[00:16:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=960s) Toată aritmetica păstrată rămâne în interiorul octetului. Citirea fără semn trebuie, așadar, să fie tot între 0 și 255. Același tipar stocat are o citire cu semn diferită pentru că se schimbă ponderea cea mai înaltă.

## Transporturi și rebucle fără semn

[00:16:17](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=977s) **Depășirea** apare atunci când rezultatul matematic depășește intervalul disponibil. [00:16:24](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=984s) În modelul de mașină cu lățime fixă, pozițiile din afara octetului sunt eliminate, iar hardware-ul poate semnaliza eșecul de interval. Biții păstrați singuri nu garantează că rezultatul matematic inițial încape.

[00:16:39](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=999s) Un **transport** transmite o cantitate în poziția următoare, mai înaltă. La o poziție binară individuală, `1 + 1 = 10`: scrii 0 în acea poziție și transporti 1 în sus. Cu un transport de intrare, `1 + 1 + 1 = 11`: scrii 1 și transporti 1.

Un exemplu simplificat face explicit lanțul transporturilor:

1. Adună 1 la octetul format numai din unu-uri.
2. La bitul cel mai jos, `1 + 1` scrie 0 și transportă 1.
3. Fiecare bit setat rămas, împreună cu acel transport, scrie tot 0 și transportă 1.
4. [00:17:09](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1029s) Transportul final ajunge la poziția de deasupra celui mai înalt bit stocat.

[00:17:15](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1035s) **Trunchierea** elimină acea a noua poziție:

```text
  11111111
+ 00000001
-----------
1 00000000    full mathematical sum: 256
  00000000    retained eight-bit result: 0
```

[00:17:25](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1045s) Porțiunea din afara octetului dispare. Aceasta este **rebucla**: tiparul păstrat revine la o valoare din interval. Un obișnuit `1 + 1` pe un octet întreg este 2 și nu depășește; pașii repetiți de `1 + 1` de aici privesc poziții biților individuale dintr-un lanț de transport.

[00:17:30](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1050s) Scăderea are cazul corespunzător al împrumutului. Dacă scăzutul este mai mare decât valoarea de pornire fără semn, rezultatul matematic este sub zero. Un împrumut ajunge dincolo de destinație și rămân doar cei opt biți inferiori.

[00:17:40](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1060s) Astfel, tiparul `0 − 1` de mai devreme este citit ca 255 când este tratat fără semn. [00:17:53](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1073s) Înregistrarea numește acest eșec de interval în jos **subdepășire**. „Rebucle fără semn sub zero” descrie comportamentul fără ambiguități.

## Depășirea cu semn și suma corectată

[00:17:59](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1079s) Eșecurile de interval apar și pentru valori cu semn. [00:18:01](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1081s) **Depășirea cu semn** înseamnă că rezultatul nu poate reprezenta suma matematică în intervalul cu semn, aici de la −128 la 127.

[00:18:05](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1085s) Adunarea este construită bit cu bit, folosind aceleași reguli de transport. Un `1 + 1` la o poziție de bit este un pas local de adunare; nu înseamnă că adunarea numerelor întregi 1 și 1 produce o depășire cu semn. Operanzii reali sunt identificați mai târziu ca fiind 106 și 96.

[00:19:02](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1142s) Ambii operanzi sunt pozitivi, iar suma lor matematică este 202:

```text
  01101010    106
+ 01100000     96
-----------
  11001010    unsigned reading: 202
```

[00:19:11](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1151s) Nu există eșec de interval fără semn: 202 încape între 0 și 255. Există însă un eșec de interval cu semn, pentru că 202 depășește 127. Citirea aceluiași rezultat în complement de doi dă bitului cel mai înalt ponderea −128, nu +128.

[00:19:29](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1169s) Narațiunea numește inițial −18, apoi corectează rezultatul. Biții inferiori setați contribuie cu 64, 8 și 2:

```text
11001010 → −128 + 64 + 8 + 2
         → −128 + 74
         → −54
```

[00:19:37](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1177s) **−54 este rezultatul corectat cu semn**, nu −18 și nici 106. Operandul 106 nu trebuie confundat cu rezultatul. Nici nu este adevărata sumă matematică, 202.

[00:19:41](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1181s) Doi operanzi pozitivi care produc un rezultat negativ la lățime fixă indică o depășire cu semn. [00:19:58](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1198s) Cazul opus este doi operanzi negativi care produc un rezultat păstrat nenegativ, pentru că suma lor adevărată este sub minim.

[00:20:02](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1202s) Înregistrarea alternează între termenii depășire și subdepășire pentru aceste cazuri cu semn. Ambele sunt eșecuri de interval cu semn. Descrie suma matematică și intervalul permis, în loc să te bazezi doar pe denumire.

[00:20:09](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1209s) Aici contează o distincție: depășirea fără semn poate pierde un transport dincolo de bitul 7, dar **depășirea cu semn nu necesită un transport pe al nouălea bit**. În `106 + 96`, toți cei opt biți ai rezultatului fără semn încap; interpretarea de semn schimbată face rezultatul invalid ca sumă matematică cu semn.

[00:20:31](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1231s) Exemplul este reluat ca o sumă care nu a încăput în destinația sa cu semn și a devenit negativă. [00:20:34](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1234s) Numirea aceluiasi eveniment subdepășire sau depășire nu schimbă diagnosticul: 202 este în afara intervalului de la −128 la 127.

Ar permite mărirea destinației la șaisprezece biți cu semn această sumă matematică?

<details>
<summary>Răspuns</summary>

Da. 202 este în intervalul cu semn pe șaisprezece biți. Tiparul său are bitul cel mai înalt șters la acea lățime. Aceasta răspunde întrebării despre reprezentare; nu precizează regulile de conversie sau de evaluare a expresiilor în C++.

</details>

## Un singur bit de semn pentru întregul număr

[00:20:42](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1242s) O valoare cu semn pe doi octeți are șaisprezece poziții, dar doar **un bit de semn**, bitul cel mai înalt al întregii valori. Bitul cel mai înalt al octețului inferior este o poziție obișnuită cu pondere pozitivă.

[00:20:49](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1249s) Corectarea finală este ponderea acelei singure poziții celei mai înalte:

```text
eight-bit signed value:    highest weight = −2^7  = −128
sixteen-bit signed value:  highest weight = −2^15 = −32768

sixteen-bit value =
    −b15 × 32768 + b14 × 16384 + … + b1 × 2 + b0 × 1
```

Fiecare `b` este 0 sau 1. Toate pozițiile inferioare își păstrează ponderile binare pozitive obișnuite. Lecția se încheie cu același principiu pozițional de la care a pornit: tiparul, lățimea lui și interpretarea sa cu sau fără semn determină împreună valoarea.

## Istoricul modificărilor de cod

În această înregistrare nu apar revizii de cod sursă executabil și nici teste de program. Stările relevante din videoclip, în ordine cronologică, sunt:

- [00:00:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=0s): pornire de la opt celule binare pline sau goale.
- [00:02:00](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=120s): stabilirea a 256 tipare și a intervalului fără semn 0–255.
- [00:04:52](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=292s): combinarea valorilor de octeți 84 și 85 folosind ponderea 256 a grupului superior.
- [00:07:43](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=463s): înlocuirea a două grupuri de patru biți cu F și 5.
- [00:10:04](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=604s): dezvoltarea a patru grupuri de octeți cu ponderi la distanță de câte opt poziții binare.
- [00:12:14](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=734s): schimbarea ponderii maxime în −128 pentru interpretarea cu semn pe opt biți.
- [00:14:29](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=869s): derivarea tiparului format numai din unu-uri prin împrumut la zero minus unu.
- [00:16:17](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=977s): păstrarea doar a lățimii destinației în timpul aritmeticii.
- [00:19:37](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1177s): corectarea citirii cu semn a sumei 106 + 96 la −54.
- [00:20:49](https://www.youtube.com/watch?v=3HnvK8WrK4M&t=1249s): extinderea la șaisprezece biți, cu o singură pondere maximă de −32768.