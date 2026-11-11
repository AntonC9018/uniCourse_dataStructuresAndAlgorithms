> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Aritmetica între baze: numărare, transport, înmulțire și conversie

[00:00:02](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2s) Lecția construiește o singură idee în trei procedee: fiecare cifră numără unități ale unei anumite ponderi. Numărarea explică acele ponderi; adunarea ponderilor egale explică adunarea în coloane; distribuirea produselor pe ponderi explică înmulțirea lungă. Exercițiul final folosește aceeași structură pentru a converti `5FE₁₆` în baza șase.

Păstrează la îndemână aceste noțiuni pe parcurs:

- **Cifră, număr și bază (radix):** o cifră este un simbol care reprezintă o valoare permisă; un număr (numeral) este o succesiune de cifre care reprezintă o valoare. Baza specifică numărul de valori posibile ale cifrelor. **Ternarul** este baza trei (0–2), baza patru folosește 0–3, baza șase folosește 0–5, iar **zecimalul** este baza zece (0–9). **Hexazecimalul** este baza șaisprezece: 0–9 urmate de A, B, C, D, E, F, ale căror valori zecimale sunt 10, 11, 12, 13, 14, 15.
- **Sistem de numerație pozițional, valoare de poziție, coeficient și dezvoltare pozițională:** poziția atribuie unei cifre o pondere, adică o valoare de poziție. Cifra este coeficientul acelei ponderi. O dezvoltare pozițională adună contribuțiile de forma cifră înmulțită cu ponderea.
- **Putere și exponent:** o putere este un produs repetat; exponentul precizează câți factori apar. Ponderile succesive ale pozițiilor în baza `b` sunt `1, b, b², b³, …`.
- **Poziția cea mai puțin semnificativă:** poziția din dreapta, a unităților, a cărei pondere este unu.
- **Ciclu, revărsare, transport și rest:** un ciclu parcurge cifrele disponibile ale unei poziții. Revărsarea readuce acea poziție la zero; un grup complet al bazei devine transport către poziția următoare. Restul este ceea ce rămâne după eliminarea grupurilor complete.
- **Zero inițial și zero substituent:** un zero inițial precedă cifrele semnificative și nu schimbă valoarea. Un zero substituent păstrează vizibilă o poziție goală; un zero final la un număr întreg păstrează o pondere mai mare și îi schimbă valoarea.
- **Adunare în coloane:** aliniază ponderile egale, apoi adună de la coloana unităților spre stânga, inclusiv transporturile care vin din dreapta.
- **Comutativitate și asociativitate:** adunarea permite schimbarea ordinii și a grupării termenilor fără a modifica totalul.
- **Distributivitate, dezvoltare și factorizare:** `a × (x + y) = a × x + a × y`. Dezvoltarea separă produsele; factorizarea reunește un factor comun.
- **Produs parțial, înmulțire lungă și deplasare pozițională:** un produs parțial este o contribuție la un produs. Înmulțirea lungă formează rânduri pe baza cifrelor, le așază la ponderile cerute și le adună. O deplasare pozițională înmulțește ponderea fiecărei cifre cu baza; adăugarea unui zero implementează o deplasare spre stânga.
- **Adunare repetată, tabel de înmulțire și calculator în mod programator:** adunarea repetată obține un produs adunând copii ale unei valori. Un tabel de înmulțire consemnează produsele cifrelor pentru o bază aleasă. Un calculator în mod programator poate primi și afișa direct valori hexazecimale.
- **Împrumut și complement față de bază:** împrumutul schimbă o unitate de pe o poziție mai înaltă cu un grup complet de unități mai mici. Complementul este cantitatea necesară pentru a completa un asemenea grup; în hexazecimal, `B + 5 = 10₁₆`.
- **Conversie de bază:** schimbă reprezentarea păstrând valoarea numărului. Convertește coeficienții și valoarea bazei inițiale, apoi evaluează dezvoltarea lor pozițională în baza țintă.

Un indice scris dedesubt indică baza: `12₃` înseamnă un trei și două unități; `12₁₀` înseamnă un zece și două unități. Fiecare bloc de calcul de mai jos precizează baza tuturor numerelor din el. Semnele de înmulțire deosebesc produsele precum `2 × D` de numerele precum `2D₁₆`.

Laboratorul [Sisteme numerice](../../../en/labs/common/02_number_systems.md) oferă exerciții conexe, inclusiv aritmetică fără a converti integral operanzii în zecimal și conversie prin coeficienți și valori de poziție. [Transcrierea fixată la un commit](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6/videos/cpp/02_Сложение,_умножение_в_других_системах_счисления_Перевод_из_одной_системы_в_другую_%28сырой%29/internal/transcript.md) consemnează șirul de calcule; ea conține erori de transcriere, așa că numerele rostite prescurtat sunt verificate față de contribuțiile lor poziționale complete. De exemplu:

```text
12₃ = 1 × 3 + 2 × 1 = 5₁₀
```

**Domeniul de aplicare:** înregistrarea dezvoltă aritmetica numerelor întregi pe hârtie. Nu conține nicio implementare de program, modificări de sintaxă a limbajelor, pași de instalare sau teste software. Adunarea se încheie la [00:11:22](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=682s), apoi urmează înmulțirea, iar conversia începe la [00:35:39](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2139s). Dezvoltarea inițială a înmulțirii amână produsele cifrelor și transporturile până la evaluarea lor numerică. Verificările aritmetice de mai jos confirmă valorile reconstruite; nu sunt rezultate de teste software din înregistrare.

## Numărarea cu trei cifre

[00:00:02](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2s) **Baza** determină ce **cifre**, adică simboluri individuale, pot apărea. Un **număr (numeral)** combină acele simboluri într-un număr scris. Ternarul are doar 0, 1 și 2, așa că șirul său de numărare începe astfel:

```text
All numerals base three:
0, 1, 2, 10, 11, 12, 20, 21, 22, 100
```

[00:00:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=24s) Poziția unităților pornește de la 0 și trece prin 1 și 2. În acel moment alegerile sale de cifre sunt epuizate. Continuarea nu poate însemna scrierea cifrei 3, pentru că în ternar nu există o asemenea cifră.

[00:00:31](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=31s) Fă poziția următoare vizibilă cu un **zero inițial**, un zero înaintea cifrelor semnificative: `2₃ = 02₃`. Adăugarea unu completează un grup de trei. Poziția unităților devine 0, iar poziția din stânga ei devine 1: `10₃`. Cuvintele rostite „1.0” se referă la aceste două cifre întregi, nu la un număr fracționar.

[00:00:57](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=57s) Acesta este un **ciclu** urmat de **revărsare**: readuce o poziție epuizată la cifra sa de început și mărește poziția următoare. Un **transport** mută grupul completat pe acea poziție superioară.

[00:01:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=76s) Imaginează discurile care se roteau ale unui contor mecanic de apă. Un disc care își parcurge toate marcajele avansează următorul disc. [00:01:42](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=102s) Într-un contor ternar, primul disc înregistrează unitățile, iar următorul înregistrează ciclurile complete ale primului. Al doilea avansează după trei incrementări de unitate; al treilea avansează după trei avansări ale celui de-al doilea, ceea ce necesită nouă incrementări de unitate. Distinge un pas individual al discului de o rotație completă.

[00:02:08](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=128s) Cifra „trei” numără deci grupuri complete de câte trei, schimbându-se o dată la trei numărări. [00:02:25](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=145s) Un ciclu completat lasă zero în poziția inferioară, pentru că grupul acumulat acolo a fost mutat spre stânga.

[00:02:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=158s) Un transport poate repeta acest proces:

1. Pornește de la `22₃` și adaugă unu.
2. Cifra unităților 2 se revarsă în 0; transportă un grup de trei.
3. Cifra următoare 2 se revarsă și ea în 0; transportă către poziția următoare.
4. Noua cifră inițială este 1, ceea ce dă `100₃`.

<details>
<summary>Precizează numărul care urmează după 12₃ și explică zero-ul său.</summary>

Este 20₃. Cifra unităților a epuizat 0, 1 și 2, așa că se resetează la 0. Transportul mărește cifra „trei” de la 1 la 2.

</details>

## Dând fiecărei poziții o pondere

[00:03:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=195s) Într-un **sistem de numerație pozițional**, poziția unei cifre îi furnizează ponderea. **Valoarea de poziție** este acea pondere numărată după poziție. Mișcarea contorului oferă o rațiune pentru fiecare pondere:

1. [00:03:29](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=209s) Unitățile au ponderea unu: acea poziție se schimbă la fiecare numărare.
2. [00:03:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=218s) Poziția următoare are ponderea trei: se schimbă după trei incrementări de unitate.
3. [00:03:46](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=226s) Următoarea are ponderea nouă: se schimbă după trei incrementări ale poziției „trei”.

Ponderile continuă cu 1, 3, 9, 27. Fiecare este de trei ori precedenta. Referirea la zecimal privește aici exprimarea acestor ponderi în zecimal; nu face din nouă și nouăzeci valori de poziție zecimale succesive. Valorile de poziție zecimale sunt 1, 10, 100.

[00:03:55](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=235s) Construiește un tabel de corespondență pentru a vedea ce contribuie o poziție ocupată:

| Număr ternar | Contribuții exprimate în zecimal | Valoare zecimală |
|---|---|---:|
| 1₃ | 1 × 1 | 1 |
| 10₃ | 1 × 3 + 0 × 1 | 3 |
| 100₃ | 1 × 9 + 0 × 3 + 0 × 1 | 9 |
| 12₃ | 1 × 3 + 2 × 1 | 5 |

[00:04:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=250s) În `100₃`, o poziție „nouă” ocupată contribuie cu nouă; pozițiile „trei” și a unităților, egale cu zero, nu contribuie cu nimic. [00:04:22](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=262s) În `10₃`, un 1 în poziția „trei” contribuie cu trei, chiar dacă cifra unităților este zero. Contribuția „trei” nu înseamnă așezarea cifrei 3 într-un număr ternar.

[00:04:31](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=271s) Un **coeficient** este cifra care înmulțește ponderea poziției sale. O **dezvoltare pozițională** prezintă acele produse ca o sumă: `12₃ = 1 × 3 + 2 × 1 = 5₁₀`. Fiecare poziție contribuie independent; totalul le reunește.

## Derivarea adunării zecimale în coloane

[00:04:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=288s) Folosește acum ponderile pentru a deriva adunarea. [00:04:58](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=298s) În **zecimal**, adică în baza zece, descompune `123₁₀` în `100 + 20 + 3`, și descompune la fel și celălalt adunând.

[00:05:14](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=314s) **Comutativitatea** permite reordonarea bucăților, iar **asociativitatea** permite regruparea lor. Reunește ponderile egale:

```text
All numerals decimal:
123 + 466
= (100 + 20 + 3) + (400 + 60 + 6)
= (100 + 400) + (20 + 60) + (3 + 6)
= 500 + 80 + 9
= 589
```

[00:05:32](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=332s) Prescurtarea rostită „100 + 4” trebuie să păstreze ponderea sutelor: a doua contribuție este 400. [00:05:47](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=347s) Ponderile egale pot fi reunite în orice sistem pozițional; baza zecimală nu este esențială pentru această rearanjare.

[00:05:55](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=355s) **Adunarea în coloane** aranjează compact acea sumă ponderată. Aliniază unitățile cu unitățile, zecile cu zecile și sutele cu sutele. Pentru numere de lungimi diferite, aliniază marginile din dreapta. Cifrele cele mai din stânga se potrivesc doar când ponderile pozițiilor lor sunt egale.

[00:06:08](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=368s) Un **zero substituent** păstrează prezentă o poziție goală. Un zero inițial oferă spațiu de afișare pentru un transport care depășește cea mai înaltă cifră inițială. Un zero în dreapta unei contribuții îi consemnează deplasarea: 70 aparține poziției zecilor, pe când 7 aparține unităților.

Înregistrarea menționează 466, dar discută și o cifră a zecilor egală cu 5. Urmează separat cele două variante:

1. [00:06:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=376s) Unități: atât `123 + 466`, cât și `123 + 456` folosesc `3 + 6 = 9`.
2. [00:06:25](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=385s) Pentru explicația zecilor, `2 + 5 = 7`, ceea ce dă o contribuție de 70 și suma 579. Dacă al doilea adunând este 466, folosește în schimb `2 + 6 = 8`, ceea ce dă 80 și suma 589.
3. Sute: `1 + 4 = 5`, contribuind cu 500 în oricare dintre variante.

[00:06:40](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=400s) Schimbă cifra unităților 6 în 9. Acum `3 + 9 = 12`, prea mult pentru o singură cifră zecimală. [00:07:34](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=454s) Descompune 12 în două unități și un grup de zece. Scrie 2 la unități; mută grupul ca transport de 1 în zeci.

```text
All numerals decimal:
123 + 459
units:    3 + 9     = 12 → write 2, carry 1
tens:     2 + 5 + 1 = 8  → write 8
hundreds: 1 + 4     = 5  → write 5
result: 582
```

Poziția superioară a transportului poate fi deja ocupată. O cifră inițială suplimentară este necesară doar dacă un transport depășește cea mai înaltă poziție existentă. Zerourile substitutive fac explicit aceste destinații.

## Schimbarea pragului de transport în baza patru

[00:08:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=480s) Baza patru permite cifrele 0–3. [00:08:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=496s) Descompunerea pozițională și alinierea în coloane rămân aceleași; grupul complet care declanșează un transport conține acum patru unități.

[00:08:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=506s) Numărul scris `10` înseamnă o unitate a poziției următoare. [00:08:53](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=533s) Așadar `10₄` are valoarea zecimală patru, iar `10₁₀` are valoarea zecimală zece. Ambele sunt grupuri complete în propriile sisteme. În baza patru, elimină patru unități inferioare și adaugă o unitate superioară; nu muta zecimalul zece.

[00:09:07](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=547s) Pornește de la **poziția cea mai puțin semnificativă**, coloana unităților din dreapta, pentru ca fiecare transport ieșit să fie disponibil la calcularea coloanei următoare. [00:09:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=556s) Instructorul observă o nepotrivire de tabel: tabelul anterior era ternar, dar acest calcul este în baza patru. Înlocuiește-l cu un tabel în baza patru, unde cifra 3 este validă.

[00:09:29](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=569s) Prima sumă mică este `3 + 3 = 12₄`: o unitate din al doilea 3 completează patrul împreună cu primul 3, lăsând 2. Scrie acel **rest**, adică unitățile rămase după eliminarea grupurilor complete, și transportă 1.

[00:09:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=578s) Dacă cifrele inițiale se termină în timp ce mai rămâne un transport, scrie acel transport ca o nouă cifră inițială. [00:09:58](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=598s) Comutativitatea explică de ce grupul transportat se alătură poziției următoare: este încă o contribuție cu ponderea acelei poziții.

[00:10:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=615s) Adăugarea unui 1 transportat la cifra 3 dă `10₄`. Aceasta produce un transport nou: scrie 0 și mută 1 spre stânga. Expresia „și atât” încheie acest calcul mic; nu anulează transportul ieșit. [00:10:30](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=630s) Aceeași regulă se aplică ori de câte ori o cifră maximă primește o unitate transportată.

[00:10:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=638s) Cu contribuția proprie a coloanei următoare inclusă, un termen ponderat precum `20₄` poate rămâne pe loc în timp ce alt grup complet se mută spre stânga. Numărul întreg 20 nu este o singură cifră; cifra sa 2 ocupă poziția „patru”.

```text
All numerals base four:
  123
+ 333
-----
 1122

units:     3 + 3     = 12 → write 2, carry 1
fours:     2 + 3 + 1 = 12 → write 2, carry 1
sixteens:  1 + 3 + 1 = 11 → write 1, carry 1
new leading digit: 1
```

[00:10:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=648s) Contribuțiile inițiale `300₄ + 100₄` singure dau `1000₄`. Păstrează și transportul care sosește atunci când calculezi totalul complet al coloanei inițiale. [00:11:07](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=667s) Odată stabilite transporturile, răspunsul este un singur număr valid, `1122₄`. Adunarea în coloane folosește aceeași succesiune cunoscută de operații, cu altă cifră maximă.

<details>
<summary>Încap 33₄ + 1₄ în două cifre?</summary>

Nu. Ambele cifre 3 se revarsă pe măsură ce transportul se mută spre stânga. Rezultatul este 100₄.

</details>

## Dezvoltarea unui produs după poziții

[00:11:22](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=682s) Adunarea este completă; următoarea construcție este înmulțirea. [00:11:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=684s) Pornește în zecimal cu `123 × 345`:

```text
All numerals decimal:
123 × 345 = (100 + 20 + 3) × (300 + 40 + 5)
```

[00:11:51](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=711s) **Distributivitatea** spune că înmulțirea unei sume înmulțește fiecare termen al ei. Dezvoltă primul operand, lăsând cealaltă sumă neatinsă:

```text
All numerals decimal:
100 × (300 + 40 + 5)
+ 20 × (300 + 40 + 5)
+  3 × (300 + 40 + 5)
```

[00:11:59](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=719s) Fiecare contribuție a lui 123 se înmulțește cu tot 345. [00:12:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=726s) **Factorizarea** inversează dezvoltarea reunind multiplicatorul comun. Doar primul și ultimul termen se factorizează ca `(100 + 3) × (300 + 40 + 5)`. Aceasta ilustrează regula pe doi termeni; produsul inițial complet include și contribuția din mijloc, 20.

[00:12:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=758s) Separă o cifră de factorul său pozițional: `100 = 1 × 100`, `20 = 2 × 10` și `3 = 3 × 1`. Produsele rămân neschimbate, dar construcția lor deosebește acum aritmetica mică între cifre de așezare.

## Separarea deplasărilor de aritmetica între cifre

[00:12:49](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=769s) O **deplasare pozițională** mărește ponderea fiecărei cifre cu un factor egal cu baza. Pentru un număr întreg, înmulțirea cu `10_b` adaugă un zero; înmulțirea cu `100_b` adaugă două. Înmulțirea cu 1 nu deplasează nimic.

```text
In any base b, for a valid whole-number numeral N:
N × 1_b   = N
N × 10_b  = N0
N × 100_b = N00

Base-six illustration:
24₆ × 100₆ = 2400₆
```

Exemplul rostit din jurul lui „84” și al numelui bazei este neclar. Un număr care conține 6 sau 8 este invalid în baza șase. Ecuația `84 × 100 = 8400` necesită o bază care permite cifra 8; nu poate stabili acel exemplu în baza șase.

[00:13:09](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=789s) Adăugarea zerourilor funcționează pentru că fiecare pondere `bᵏ` devine `bᵏ⁺¹` după înmulțirea cu baza. Regula se aplică indiferent de simbolurile folosite pentru cifre în bază. Aceste zerouri finale afectează valoarea, spre deosebire de zerourile inițiale.

[00:13:44](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=824s) Distribuie fiecare multiplicator de cifră pe contribuțiile lui 345. [00:14:05](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=845s) Cele trei rânduri arată astfel:

```text
100 × [1 × (300 + 40 + 5)]
 10 × [2 × (300 + 40 + 5)]
  1 × [3 × (300 + 40 + 5)]
```

[00:14:50](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=890s) Această algebră este valabilă în orice bază pozițională. [00:15:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=900s) Până aici nu a fost necesar niciun transport: termenii doar au fost despărțiți și regrupați. [00:15:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=915s) Cifra maximă, 9 în zecimal, devine relevantă atunci când produsele mici sunt efectiv evaluate și scrise ca cifre. Dezvoltarea algebrică nu elimină această cerință ulterioară.

## Obținerea primului produs de cifre în baza șase

[00:15:23](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=923s) Produsele zecimale ale cifrelor cu 1, 2 și 3 ar transforma 5 în 5, 10 și 15. Pentru a face vizibilă limita cifrelor într-un alt sistem, lecția interpretează acum numerele 123 și 345 în baza șase. Valorile lor numerice se schimbă, dar dezvoltarea lor în contribuții de forma cifră înmulțită cu ponderea funcționează în continuare.

[00:15:31](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=931s) Înmulțirea cu 1 lasă numărul neatins: `1₆ × 345₆ = 345₆`. Deoarece acel 1 vine din poziția cea mai înaltă a lui 123, rândul va primi mai târziu deplasarea cu două poziții asociată lui `100₆`.

[00:16:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=984s) **Adunarea repetată** înseamnă obținerea unui produs prin adunarea numărului necesar de copii ale unei valori. Pentru două copii ale lui 5, descompune a doua copie în 1 și 4:

```text
All numerals base six:
2 × 5 = 5 + 5
      = 5 + 1 + 4
      = 10 + 4
      = 14
```

[00:16:43](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1003s) Suma 5 + 1 completează șase, scris `10₆`. Acel grup complet devine cifra superioară 1, cu restul 4 la unități. Așadar `2 × 5 = 14₆`, a cărui valoare zecimală este zece.

## Alegerea unei metode pentru obținerea produselor de cifre

[00:17:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1026s) Ce se întâmplă cu valori de cifre mai mari, precum D și E hexazecimale? [00:17:11](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1031s) Adunând E de treisprezece ori am obține produsul lor, dar repetarea acestei munci pentru fiecare pereche de cifre este anevoioasă.

[00:17:17](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1037s) Un **tabel de înmulțire** consemnează produsele mici în baza aleasă. Intrarea zecimală familiară `8 × 8 = 64₁₀` ilustrează un tabel; în hexazecimal, aceeași valoare se scrie `40₁₆`. Un tabel trebuie să folosească aceeași bază ca calculul.

Lecția oferă trei trasee:

1. Construiește sau consultă tabelul de înmulțire pentru baza curentă.
2. [00:17:40](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1060s) Obține produsul cu un calculator care acceptă cifrele bazei și întoarce un rezultat în acea bază.
3. [00:18:14](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1094s) Convertește în zecimal doar cele două valori individuale de cifră, înmulțește-le și convertește înapoi acel mic rezultat.

[00:18:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1090s) Un **calculator în mod programator** este un mod de calculator care acceptă și afișează direct numere hexazecimale. [00:18:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1118s) Folosirea lui pentru un produs de cifre nu impune conversia întregii expresii cu mai multe cifre în zecimal. Așezarea din jur și lucrul cu transporturile pot rămâne în baza atribuită.

[00:18:54](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1134s) Introducerea hexazecimalului D înmulțit cu E produce:

```text
D₁₆ × E₁₆ = B6₁₆
Decimal value check: 13 × 14 = 182 = 11 × 16 + 6
```

[00:19:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1155s) Convertirea celor două cifre și a produsului lor dă același răspuns. Aceste trasee schimbă modul în care se obține un produs mic, nu locul unde îi aparține contribuția.

## Calcularea lui D înmulțit cu E prin complemente

[00:19:27](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1167s) **Complementul față de bază** măsoară distanța până la un grup complet. E este cu doi mai puțin decât hexazecimalul `10`, deci scrie `E = 10₁₆ − 2`.

[00:20:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1200s) Dezvoltă factorul mai ușor prin distributivitate:

```text
All numerals hexadecimal:
D × E = D × (10 − 2)
      = D0 − 2 × D
      = D0 − D − D
```

`10` este hexazecimalul șaisprezece, nu binarul doi. Deosebește și `2 × D`, o înmulțire, de `2D`, un număr cu două cifre.

[00:20:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1226s) Scade D de două ori din D0. [00:20:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1248s) Instructorul dă inițial cifrelor-litră valori cu unu prea mari, apoi le corectează: A = 10, B = 11, C = 12, D = 13 în zecimal. Cu corecția, D este cu trei mai puțin decât șaisprezece: `D = 10₁₆ − 3`.

[00:21:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1266s) **Împrumutul** schimbă o unitate de pe o poziție superioară cu un grup complet de unități mai mici. Aici scăderea `10 − 3` poate fi tratată eliminând un grup complet și restituind 3:

```text
All numerals hexadecimal:
D0 − (10 − 3) − (10 − 3)
= D0 − 10 − 10 + 3 + 3
= B0 + 6
= B6
```

[00:21:25](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1285s) Cifra superioară scade D → C → B. Fiecare scădere a unui minus 3 restituie trei unități, în total șase. [00:21:38](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1298s) Rezultatul manual B6 coincide cu cel al calculatorului. Rearanjarea în jurul unui grup complet apropiat evită treisprezece adunări separate.

<details>
<summary>De ce ajută identitatea E = 10₁₆ − 2?</summary>

Înmulțirea cu 10₁₆ este o deplasare cu o poziție. După ce ai scris D0, mai rămân doar două copii ale lui D de scăzut. Însuși D este aproape de bază, așa că D = 10₁₆ − 3 simplifică acele scăderi.

</details>

## Construirea rândului în baza șase pentru cifra 2

[00:21:51](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1311s) Reia `123₆ × 345₆`. „14” amintit aparține lui `2 × 5` în baza șase; nu este o valoare atribuită hexazecimalului D.

Un **produs parțial** este o contribuție formată înainte de totalul final. Pentru cifra din mijloc, 2, calculează mai întâi `2 × 345₆`, apoi deplasează o dată rândul complet, pentru poziția acelei cifre.

1. [00:22:02](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1322s) Unități: `2 × 5 = 14₆ = 10₆ + 4`. Scrie 4 și transportă 1. Aceasta înlocuiește produsul 2 × 5, nu factorul 5, cu 10 + 4.
2. [00:22:09](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1329s) Calculează `2 × 4` înainte de a atașa ponderea „șase”.
3. [00:22:30](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1350s) Baza șase folosește doar cifrele 0–5: șase, șapte și opt zecimal sunt `10₆`, `11₆` și `12₆`. Așadar `2 × 4 = 12₆`.
4. [00:22:43](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1363s) Adaugă transportul de la unități: `12₆ + 1 = 13₆`. Scrie 3 și transportă 1.
5. [00:22:56](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1376s) Continuă cu cifra 3. Produsul `2 × 3 = 10₆`, iar transportul care sosește îl face `11₆`. Scrie 1, apoi transportul final 1.

[00:23:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1386s) Produsul de cifre 2 × 3 are restul zero și transportul unu. Restul său devine 1 doar după includerea transportului care sosește. [00:23:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1406s) Grupul transportat contribuie cu o unitate a următoarei ponderi.

[00:23:37](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1417s) Rândul poate fi asamblat și din bucățile sale ponderate independent:

```text
All numerals base six:
2 × 300 = 1000
2 ×  40 =  120
2 ×   5 =   14
sum      = 1134
```

[00:23:54](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1434s) Restabilește factorul pozițional al cifrei din mijloc: `1134₆ × 10₆ = 11340₆`. Această deplasare a întregului rând este separată de transporturile din interiorul rândului.

[00:24:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1440s) Repetă procedeul de produs de cifre pentru următorul termen. [00:24:12](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1452s) Odată stabilite cifrele și transporturile interne ale unui rând, consemnează-l ca contribuție intermediară. El mai trebuie combinat cu celelalte rânduri.

## Construirea celorlalte rânduri în baza șase

[00:24:19](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1459s) Contribuția inițială `100₆` deplasează rândul său parțial cu două poziții, dând `34500₆`. Un factor pozițional cu trei cifre care se termină în două zerouri specifică două deplasări, nu trei.

[00:24:27](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1467s) Pentru cifra unităților 3 a lui 123, dezvoltă contribuția care implică `300₆` ca `3 × 3 × 100₆`. [00:24:32](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1472s) Aceasta așază produsul mic în poziția sutelor bazei curente. [00:24:40](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1480s) Produsul mic este `3 × 3 = 13₆`: cifra sa inferioară este 3, iar cea superioară este 1.

[00:24:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1488s) Înmulțirea lui 13 cu `100₆` adaugă două zerouri, deci acea contribuție este `1300₆`. [00:24:58](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1498s) La fel, `40₆ = 4 × 10₆`; `3 × 4 = 20₆`, urmat de o deplasare, dă `200₆`. [00:25:09](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1509s) Zero-ul final consemnează așezarea. Este adăugat produsului, nu tratat ca o altă înmulțire cu o cifră semnificativă.

Contribuția unităților este `3 × 5 = 23₆`. Asamblează rândul rămas:

```text
All numerals base six:
3 × 345 = 1300 + 200 + 23 = 1523

Placed rows for 123 × 345:
1 × 345 × 100 = 34500
2 × 345 ×  10 = 11340
3 × 345 ×   1 =  1523
```

[00:25:32](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1532s) Înmulțirea unei contribuții cu 1 o lasă neschimbată. [00:25:36](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1536s) După ce toate produsele de cifre și factorii poziționali au fost luați în calcul, nu mai rămâne decât adunarea lor.

## Adunarea rândurilor în baza șase

[00:25:39](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1539s) **Înmulțirea lungă** formează și așază produsele parțiale, apoi le adună. Ultima ei etapă este exact adunarea în coloane deja derivată:

```text
All numerals base six:
  34500
  11340
+ 01523
-------
  52203
```

Zero-ul inițial aliniază ponderile egale. Adună de la dreapta spre stânga:

1. Unități: `0 + 0 + 3 = 3`; scrie 3.
2. [00:26:01](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1561s) Șase: `0 + 4 + 2 = 10₆`; scrie 0 și transportă 1.
3. [00:26:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1566s) Treizecișase: include transportul care sosește în `5 + 3 + 5 + 1 = 22₆`; scrie 2 și transportă **2**.
4. [00:26:12](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1572s) Mai multe grupuri complete pot părăsi o coloană atunci când se adună mai multe rânduri. Păstrează ambele grupuri transportate în acest exemplu.
5. [00:26:18](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1578s) Următoarea coloană: `4 + 1 + 1 + 2 = 12₆`; scrie 2 și transportă 1.
6. [00:27:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1653s) Coloana cea mai înaltă: `3 + 1 + 0 + 1 = 5`; scrie 5.

[00:26:35](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1595s) Calculul revine la cifrele inferioare în timp ce reunește termenii dezvoltați. [00:26:42](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1602s) Un grup complet lasă un zero scris în coloana sa; grupul transportat trebuie totuși inclus în stânga.

[00:27:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1630s) Citește întreaga contribuție acumulată a coloanei din mijloc. Expresia izolată „1 + 3 + 5 = 12” omite un 5 deja acumulat; totalul complet este `22₆`, cu restul 2 și transportul 2. [00:27:17](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1637s) Următorul `2 + 4 = 10₆` formează și el un grup, dar celelalte contribuții determină în continuare restul final al acelei coloane. [00:27:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1653s) Citind toate coloanele stabilite obținem `52203₆`, cu cifra inițială 5 și cifra unităților 3.

O verificare independentă a valorii confirmă: `123₆ = 51₁₀`, `345₆ = 137₁₀` și `51 × 137 = 6987`. Dezvoltarea `5 × 1296 + 2 × 216 + 2 × 36 + 0 × 6 + 3` este tot 6987.

<details>
<summary>Trebuie ca fiecare transport să fie egal cu unu?</summary>

Nu. O coloană cu totalul 22₆ conține două grupuri complete de câte șase și două unități. Restul ei este 2, iar transportul este 2. Adunarea mai multor rânduri parțiale poate produce mai mult de un grup complet.

</details>

## Dezvoltarea produsului hexazecimal

[00:27:52](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1672s) Treci la `FD₁₆ × B5₁₆`. **Hexazecimalul** oferă șaisprezece valori de cifre, inclusiv A–F, așa că poziția următoare după unități are ponderea șaisprezece.

[00:28:01](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1681s) Descompune FD ca `F × 10 + D`. [00:28:08](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1688s) Descompune B5 ca `B × 10 + 5`, cu fiecare număr din aceste descompuneri fiind hexazecimal.

[00:28:19](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1699s) Distribuie cele două sume:

```text
All numerals hexadecimal:
(F × 10 + D) × (B × 10 + 5)
= (F × B) × 100
+ (F × 5) × 10
+ (D × B) × 10
+  D × 5
```

Termenul „mare × mare” are **doi** factori ai bazei. `F0 × B0` deplasează deci produsul F × B cu două poziții. Omisiunea oricăreia dintre deplasări îi schimbă ponderea.

[00:28:35](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1715s) Factorizarea lui `F0 = F × 10` separă produsul său de cifre de multiplicatorul său pozițional; distribuirea lui D pe B0 + 5 face același lucru pentru termenii lui D. [00:28:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1728s) Aceasta folosește aceeași construcție pe cifre ca exemplul în baza șase.

[00:28:56](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1736s) În particular, `F × B0 = (F × B) × 10`. [00:29:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1740s) Cifra maximă F satisface `F + 1 = 10₁₆`, așa că poate fi înlocuită cu `10 − 1`.

[00:29:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1746s) Pune provizoriu deoparte multiplicatorii poziționali cât timp calculezi produsele de cifre, apoi restaurează-i. Factorul amânat este `10₁₆`, nu un simplu 1: doar primul adaugă un zero.

## Simplificarea produselor hexazecimale cu F

[00:29:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1764s) Folosind `F = 10 − 1`, produsul mic F × B devine B0 − B. [00:30:04](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1804s) Această scurtătură aparține lui **F × B**, în timp ce D × B rămâne un termen separat.

[00:30:19](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1819s) Împrumută un grup de șaisprezece din B0:

```text
All numerals hexadecimal:
F × B = (10 − 1) × B
      = B0 − B
      = A0 + (10 − B)
```

[00:30:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1826s) Numără în sus de la B pentru a găsi complementul `10 − B`: B → C → D → E → F → 10. [00:30:37](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1837s) Sunt necesare cinci incrementări, deci `10 − B = 5` și `F × B = A5`.

[00:30:50](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1850s) Înmulțirea cu 1 lasă A5 neschimbat; restaurarea unui factor pozițional produce A50. Termenul „mare × mare” are nevoie și de al doilea factor, așa contribuția sa completă este A500.

[00:31:03](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1863s) Aplică aceeași scurtătură la F × 5:

```text
All numerals hexadecimal:
F × 5 = (10 − 1) × 5
      = 50 − 5
      = 40 + (10 − 5)
      = 40 + B
      = 4B
```

[00:31:14](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1874s) Complementele sunt împerecheate: B + 5 face `10₁₆`. [00:31:56](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1916s) Deoarece B desemnează unsprezece, numărul `40 + B` este 4B. [00:32:12](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1932s) Scăderea `10₁₆ − 5` are valoarea zecimală `16 − 5 = 11`, scrisă B. Nu este egală cu cifra 5. Amestecarea sensurilor zecimal și hexazecimal ale lui 10 ar strica calculul.

Restaurează factorul 10 din poziția inițială a lui F pentru a obține contribuția `4B0₁₆`.

## Finalizarea înmulțirii hexazecimale

[00:32:41](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1961s) Următorul termen neevaluat este D × B0. [00:32:45](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1965s) Instructorul alege să calculeze direct produsul său mic, în loc să derive o altă scurtătură prin complement.

[00:33:11](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1991s) Produsul `D₁₆ × B₁₆ = 8F₁₆` devine `8F0₁₆` după deplasarea cu o poziție cerută. Operanzii cu o singură cifră nu provoacă ei înșiși acea deplasare; o face poziția lui B în B5.

[00:33:23](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2003s) Ultimul produs mic este `D₁₆ × 5 = 41₁₆`. Verificările valorilor cifrelor dau `13 × 11 = 143 = 8 × 16 + 15` și `13 × 5 = 65 = 4 × 16 + 1`.

[00:33:31](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2011s) Reunește produsele parțiale, incluzând toți multiplicatorii poziționali. [00:33:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2013s) Suma completă are patru termeni:

```text
All numerals hexadecimal:
(F × B) × 100 = A500
(F × 5) ×  10 =  4B0
(D × B) ×  10 =  8F0
 D × 5        =   41
```

[00:33:54](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2034s) Așază acești termeni în coloane. [00:33:59](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2039s) Zerourile inițiale fac alinierea vizibilă fără a schimba valorile:

```text
All numerals hexadecimal:
  A500
  04B0
  08F0
+ 0041
------
  B2E1
```

1. [00:34:17](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2057s) Unități: rândurile deplasate se termină în zero, iar ultimul rând se termină în 1. Scrie 1; niciun transport nu părăsește această coloană.
2. [00:34:25](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2065s) Șaispreze: `B + 4 = F`, atingând cifra maximă fără a o depăși.
3. [00:34:35](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2075s) Adaugă F rămas: `F + F = 1E₁₆`. Scrie E și transportă 1. Dezvoltarea `(10 − 1) + F = 10 + E` explică apariția lui E. Un 1 suplimentar care s-ar fi primit ar fi dat `1F₁₆`; nu există un asemenea transport de la unități.
4. [00:34:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2088s) Include transportul 1 în următoarea coloană.
5. [00:35:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2110s) Calculează `5 + 4 = 9`, apoi `9 + 1 = A`, apoi `A + 8 = 12₁₆`. Scrie 2 și transportă 1.
6. [00:35:20](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2120s) A-ul inițial primește acel transport: `A + 1 = B`. Scrie B.

Produsul finit este `B2E1₁₆`. Valoarea sa este 45793 în zecimal, în acord cu `253 × 181`, valorile zecimale ale lui FD și B5. Procedura cunoscută de așezare a rândurilor și de transport a supraviețuit și altei schimbări de bază.

## Punerea în scenă a conversiei prin dezvoltare pozițională

[00:35:39](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2139s) Sarcina următoare este conversia lui `5FE₁₆` în baza șase. **Conversia de bază** păstrează valoarea numerică schimbând cifrele și ponderile folosite pentru a o reprezenta.

[00:36:07](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2167s) Folosește o **dezvoltare pozițională**, o sumă de coeficienți de cifre înmulțiți cu valorile lor de poziție:

```text
5FE₁₆ = 5 × (10₁₆)² + F × 10₁₆ + E × 1
```

[00:37:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2220s) O **putere** este un produs repetat; **exponentul** îi numără factorii. Ridicarea la ptrat înseamnă folosirea a două copii. Deși `100_b = (10_b)²` în fiecare bază, aceste numere au valori diferite în baze diferite. Cea mai înaltă pondere inițială este șaisprezece la pătrat, `100₁₆ = 256₁₀`, nu șase la pătrat, `100₆ = 36₁₀`.

[00:37:05](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2225s) Conversia poate deci avea loc fără a exprima mai întâi întregul număr în zecimal. Convertește fiecare coeficient și valoarea bazei inițiale în baza șase, apoi înmulțește și adună termenii convertiți acolo. Păstrarea valorilor ponderilor vechi este esențială.

## Convertirea coeficienților și a bazei inițiale

Urmează substituțiile în ordinea construcției din lecție:

1. [00:37:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2235s) Coeficientul 5 rămâne `5₆`.
2. [00:37:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2244s) F desemnează cincisprezece. Două grupuri de șase și trei unități dau `F₁₆ = 23₆`.
3. [00:37:35](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2255s) Multiplicatorul `10₁₆` desemnează șaisprezece. Două grupuri de șase și patru unități dau `10₁₆ = 24₆`. Aceasta convertește valoarea bazei, nu doar cifra 1.
4. [00:38:27](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2307s) E desemnează paisprezece. Două grupuri de șase și două unități dau `E₁₆ = 22₆`.
5. [00:38:36](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2316s) Termenul lui E este în continuare înmulțit cu ponderea unităților 1. Descompunerea „șase + șase + doi” descrie valoarea lui E, nu un transport care intră în termen.

Noua expresie este:

```text
All numerals base six:
5 × (24)² + 23 × 24 + 22
```

[00:38:41](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2321s) Ponderea ridicată la pătrat este pusă ca întrebare următoare; ea nu a fost încă calculată. [00:38:44](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2324s) Obține-o înmulțind valoarea bazei inițiale convertite, `24₆`, cu ea însăși. Ridicarea la pătrat a lui `10₆` ar ridica la pătrat șase și ar furniza ponderea greșită.

<details>
<summary>Ai putea înlocui 5, F și E cu 5, 23 și 22 și să le alipești?</summary>

Nu. Pozițiile inițiale au ponderi care sunt puteri ale lui șaisprezece. După conversia coeficienților, păstrează acele ponderi calculând 5 × 24² + 23 × 24 + 22 în baza șase. Alipirea ar da poziții diferite și o valoare diferită.

</details>

## Ridicarea lui 24 la pătrat și corectarea primului rând

[00:39:01](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2341s) Calculează `24₆ × 24₆` înainte de a înmulți ponderea ridicată la pătrat cu coeficientul 5. Pornește cu rândul pentru cifra unităților 4.

[00:39:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2356s) Produsul mic `4 × 4` poate fi găsit dublând suma 4 + 4. [00:39:35](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2375s) Acea sumă este `12₆ = 10₆ + 2`. Dublarea trebuie aplicată ambelor părți:

```text
All numerals base six:
4 × 4 = 2 × (4 + 4)
      = 2 × (10 + 2)
      = 20 + 4
      = 24
```

[00:40:00](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2400s) Grupul complet șase se scrie 10 în această bază. Ultimul termen dezvoltat trebuie să fie 4, nu 2: ambii termeni inițiali sunt dublați. [00:40:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2426s) Dezvoltarea alternativă confirmă `4 × 4 = 24₆`. Acest 24 este produsul de cifre, nu întregul pătrat al numărului 24 cu două cifre.

Construiește primul rând parțial:

1. Din `4 × 4 = 24₆`, scrie cifra unităților 4 și transportă 2.
2. [00:40:39](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2439s) Calculează `4 × 2 = 12₆`, a cărui valoare zecimală este opt.
3. [00:40:47](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2447s) Include transportul: `12₆ + 2 = 14₆`. Scrie 4 și transportă 1 într-o poziție inițială nouă.
4. [00:40:57](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2457s) Instructorul observă o cifră scrisă greșit și o înlocuiește cu 1. Păstrează acel 1 inițial corectat, așa că rândul este `144₆`.

Starea intermediară este un rând complet: `24₆ × 4 = 144₆`. Cifra de pe poziția superioară, 2, își are încă nevoie de rândul propriu.

## Deplasarea celui de-al doilea rând și completarea pătratului

[00:41:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2470s) Următorul rând vine din înmulțirea lui 24 cu cifra 2 și deplasarea o dată, pentru a compensa poziția superioară a acelei cifre. [00:41:12](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2472s) Atât dezvoltarea algebrică, cât și înmulțirea în coloane sunt modalități acceptabile de a-l obține; oricare trebuie să păstreze această pondere.

1. [00:41:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2493s) Unități: `2 × 4 = 12₆`. Scrie 2 și transportă 1.
2. [00:41:36](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2496s) Următoarea coloană: `2 × 2 + 1 = 5`. Valoarea 5 încape într-o cifră a bazei șase, așa că această coloană nu are transport ieșit.
3. Rândul fără deplasare este `52₆`; deplasarea sa cu o poziție îl face `520₆`.
4. [00:41:49](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2509s) Adună acest rând deplasat la 144, incluzând fiecare transport.

```text
All numerals base six:
   24
×  24
-----
  144
+ 520
-----
 1104
```

Unitățile dau 4. Coloana șaselor dă `4 + 2 = 10₆`: scrie 0 și transportă 1. Următoarea coloană dă `1 + 5 + 1 = 11₆`: scrie 1 și transportă 1. Transportul rămas creează al doilea 1 inițial.

[00:42:04](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2524s) Transcrierea abreviază pătratul ca „104”. [00:42:11](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2531s) Păstrează rezultatul complet **1104₆** înainte de a continua. O verificare a valorii face clară cifra lipsă: `24₆ = 16₁₀`, deci pătratul său este `256₁₀ = 1104₆`. În schimb, `104₆` este doar patruzeci. Cele repetate cifre 1 inițiale sunt semnificative.

## Înmulțirea ponderii ridicate la pătrat cu cinci

[00:42:22](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2542s) Prima contribuție are încă nevoie de coeficientul 5: calculează `5 × 1104₆`.

[00:42:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2544s) O scurtătură de factorizare apropiată folosește `23₆ = 24₆ − 1`. Ea aparține celei de-a **doua** contribuții:

```text
All numerals base six:
23 × 24 = (24 − 1) × 24 = 1104 − 24
```

Expresia 24 − 1 reprezintă 23, nu 5. Păstrează această scurtătură separată de înmulțirea ponderii ridicate la pătrat cu cinci.

[00:43:03](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2583s) Revino la acea înmulțire. [00:43:06](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2586s) Produsele sale de cifre nenule sunt 5 × 1 și 5 × 4; poziția zero rămâne pe loc.

[00:43:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2590s) Reutilizează produsul de cifre deja obținut:

```text
All numerals base six:
5 × 4 = 4 × 4 + 4 = 24 + 4 = 32

1104 × 5:
units:        4 × 5     = 32 → write 2, carry 3
sixes:        0 × 5 + 3 = 3  → write 3
thirty-sixes: 1 × 5     = 5  → write 5
next:         1 × 5     = 5  → write 5
result: 5532
```

Transportul de la unități alimentează poziția șaselor, altfel goală. Ambele cifre 1 inițiale ale pătratului furnizează cifre de 5. Prima contribuție a conversiei este acum `5532₆`.

## Combinarea tuturor contribuțiilor conversiei

[00:43:57](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2637s) Reunește cei trei termeni ai conversiei: primul este 5532, al doilea este 1104 − 24, iar al treilea este 22, toți în baza șase.

[00:44:04](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2644s) Simplifică mica corecție înainte de a aduna rândurile mari:

```text
All numerals base six:
−24 + 22 = −2
1104 − 24 + 22 = 1104 − 2 = 1102
```

[00:44:12](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2652s) Expresia completă este deci `5532₆ + 1102₆`. Referirile abreviate la „32” și „102” omit poziții superioare; păstrează numerele complete când faci conversia.

[00:44:22](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2662s) Aliniază cele două rânduri:

```text
All numerals base six:
   5532
+  1102
-------
  11034
```

1. Unități: `2 + 2 = 4`; scrie 4.
2. Șase: `3 + 0 = 3`; scrie 3.
3. [00:44:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2673s) Treizecișase: `5 + 1 = 10₆`; scrie 0 și transportă 1.
4. [00:44:45](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2685s) Include acel transport 1 în următoarea coloană.
5. [00:44:52](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2692s) Următoarea sumă este `5 + 1 + 1 = 11₆`. Prima pereche formează 10, iar transportul care sosește adaugă încă o unitate. Scrie 1 și transportă din nou 1.
6. Scrie transportul final 1 ca o nouă cifră inițială.

[00:45:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2710s) „1034” final din transcriere pierde un 1 inițial repetat. Rezultatul complet este **5FE₁₆ = 11034₆**.

Verifică valoarea păstrată:

```text
5FE₁₆  = 5 × 256 + 15 × 16 + 14 = 1534₁₀
11034₆ = 1 × 1296 + 1 × 216 + 0 × 36 + 3 × 6 + 4 = 1534₁₀
 1034₆ = 1 × 216 + 0 × 36 + 3 × 6 + 4 = 238₁₀
```

Verificarea zecimală confirmă reconstrucția. Procedura de conversie însăși a evaluat coeficienții și ponderile inițiale în baza șase.

<details>
<summary>Care sunt cele două distincții care previn greșelile principale din această conversie?</summary>

Convertește valoarea bazei inițiale, șaisprezece, în 24₆ înainte de a o ridica la pătrat și păstrează ambele cifre 1 inițiale din 1104₆. Păstrează, de asemenea, scurtătura 23₆ = 24₆ − 1 atașată contribuției lui F, în loc să o tratezi drept coeficientul 5.

</details>

## Ce stabilește aritmetica aceasta

[00:45:26](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2726s) Exercițiul oferă un sens concret reprezentării: un număr (numeral) este o colecție de coeficienți, fiecare atașat propriei ponderi poziționale.

[00:45:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2733s) Aceleași legi aritmetice se aplică în orice bază. Adunarea reunește ponderi egale; înmulțirea se distribuie pe contribuțiile poziționale; conversia reexprimă atât coeficienții, cât și valoarea bazei inițiale, apoi îi înmulțește și îi adună în baza țintă.

[00:45:59](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2759s) Calculul pe hârtie urmărește să stabilească acest principiu. Un calculator poate furniza valoarea unui produs de cifre, dar înțelegerea reprezentării îți spune unde să-l așezi, ce zerouri să păstrezi și unde trebuie să ajungă un transport.

## Istoricul modificărilor de cod

În această lecție nu se construiește niciun cod de program. Traseul relevant constă în aceste stări de calcul din video, cu marcaje de timp, în ordinea construcției, cel mai recent la final:

- [00:00:02](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2s) — Începe numărarea ternară cu cifrele 0–2 și derivă revărsarea.
- [00:03:15](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=195s) — Atribuie ponderile 1, 3 și 9 și citește numerele ca sume ponderate.
- [00:04:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=288s) — Reunește ponderile egale pentru a deriva adunarea în coloane.
- [00:09:16](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=556s) — Corectează nepotrivirea tabel/bază și finalizează transportul în baza patru.
- [00:11:24](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=684s) — Dezvoltă 123 × 345 în contribuții poziționale.
- [00:15:31](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=931s) — Evaluează aceeași construcție pe cifre în baza șase.
- [00:20:48](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1248s) — Corectează valorile literelor hexazecimale și derivă D × E = B6.
- [00:27:33](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1653s) — Combină rândurile parțiale din baza șase în 52203.
- [00:27:52](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=1672s) — Dezvoltă FD × B5 în patru termeni hexazecimali.
- [00:35:20](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2120s) — Finalizează suma hexazecimală B2E1.
- [00:37:05](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2225s) — Reexprimă coeficienții și baza inițială ale lui 5FE în baza șase.
- [00:42:04](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2524s) — Finalizează ponderea ridicată la pătrat 24₆ × 24₆ = 1104₆, păstrând ambele cifre 1 inițiale.
- [00:45:10](https://www.youtube.com/watch?v=cPKhqBM0gIc&t=2710s) — Combină contribuțiile conversiei în 11034₆.
