> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Pointeri: accesarea unei variabile prin adresa ei

[00:00:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=5s) Această lecție construiește un pointer pornind de la citiri și scrieri obișnuite ale unei variabile. Mai întâi vei modifica un întreg folosindu-l pe nume, apoi îi vei obține adresa, iar la final vei citi și modifica același întreg prin acea adresă. Experimentul final explică de ce contează tipul țintei unui pointer: modificarea unui singur octet dintr-un întreg poate lăsa în urmă restul valorii vechi.

Termenii de care vei avea nevoie sunt:

- **Celulă de memorie, octet și bit:** o celulă din diagrame reprezintă un octet de memorie. Pe mașina din demonstrație, un octet conține opt biți, fiecare fiind 0 sau 1. **Reprezentarea binară** înseamnă modelul de biți folosit pentru a codifica o valoare.
- **Variabilă, valoare și atribuire:** o variabilă dă un nume unui obiect cu memorie; valoarea ei este datele memorate acolo în acel moment. **Durata de viață** a sa este perioada în care acel obiect există. O atribuire înlocuiește datele respective. O **declarare** îi atribuie variabilei tipul și numele; **inițializarea** îi furnizează valoarea inițială.
- **Tip și `int`:** un tip stabilește cum sunt reprezentate datele și ce operații sunt permise. `int` este tipul întreg folosit aici, care ocupă patru octeți pe mașina din demonstrație.
- **Flux de ieșire:** `std::cout` primește valori pentru afișare prin `<<`. `std::endl` încheie linia și golisește fluxul de ieșire.
- **Adresă, pointer și obiect indicat (pointee):** o adresă identifică o locație din memorie; un pointer stochează o valoare de adresă; obiectul indicat este obiectul la care se ajunge prin el. `int*` înseamnă pointer către `int`.
- **Operatorul de adresare și dereferențiere:** operatorul unar `&` obține adresa unui obiect. Operatorul unar `*` urmărește un pointer și oferă acces la obiectul indicat.
- **Hexazecimal:** notație în baza 16, cu cifre 0–9 și A–F; `0x` marchează un număr hexazecimal în adresele afișate.
- **Memorie virtuală:** sistemul de operare mapează adresele programului pe memoria fizică de sub ea. **Randomizarea adreselor** poate schimba aceste adrese între două rulări ale programului.
- **Aliniere:** un tip poate impune ca memoria lui să înceapă la o adresă divizibilă în mod corespunzător. Spațiul care pare gol dintre obiecte nu face parte automat din valoarea vreunuia dintre ele.
- **Tip de octet și verificare de tipuri:** `uint8_t` este un tip întreg fără semn pe opt biți, dacă este disponibil, cu valori 0–255. **Compilatorul**, care transformă codul sursă într-un program executabil, respinge atribuirile obișnuite între tipuri de pointer incompatibile.
- **Conversie explicită și ordine little-endian:** o conversie explicită (*cast*) cere în mod explicit schimbarea tipului. Un **cast în stil C** scrie tipul destinație între paranteze înaintea operandului; **`reinterpret_cast`** este sintaxa C++ pentru o reinterpretare explicită. **`unsigned char`** este un tip de caracter fără semn, permis pentru accesul pe octeți. Un **alias** de tip este alt nume pentru același tip. Ordinea little-endian plasează octetul cel mai puțin semnificativ al unui întreg pe mai mulți octeți la adresa cea mai mică.
- **Comportament nedefinit:** o operație pentru care C++ nu specifică niciun rezultat obligatoriu; accesarea unui obiect printr-un tip nepotrivit sau în afara memoriei lui poate produce acest lucru.

Pentru exerciții conexe, folosește laboratorul [Pointeri](../../../en/labs/cpp/03_pointer.md) din repozitoriu. Acesta conține exerciții dincolo de această înregistrare; acelea sunt studiu suplimentar opțional.

**Domeniul de aplicare.** Lecția acoperă adresele, `int*`, `&`, citirea și scrierea prin `*`, compatibilitatea tipurilor de pointeri și un experiment explicit de conversie către un pointer pe octet. Memoria virtuală și alinierea sunt doar amintite pe scurt. Codificarea detaliată a numerelor este amânată la un videoclip separat. Experimentul de scriere pe octeți servește înțelegerii reprezentării, nu este o metodă recomandată de a atribui valori obișnuite unor întregi.

Exemplele de mai jos reconstruesc în formă simplificată stările de cod din înregistrare. Linkurile cu timp identifică aceste stări. [Exemplul conex de memorie din repozitoriu](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/eb8f41e0402f4552beec72bc0953b86251d16cf4/en/05_programming_fundamentals/memory_example_1/example.cpp) demonstrează și el adresarea și dereferențierea, dar folosește alte valori și operații suplimentare; nu este o versiune salvată exact a acestui videoclip. Fragmentul său relevant este:

```cpp
int i = 69;
int* iPointer = &i;
std::cout << *iPointer << std::endl;
```

## Citirea variabilelor inițiale

[00:00:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=5s) Pornim de la două **variabile**, obiecte cu nume a căror memorie conține **valorile** curente. Fiecare **declarare** furnizează un tip și un nume, iar inițializatorul său furnizează valoarea inițială:

```cpp
#include <iostream>

int main()
{
    int i = 10;
    int a = 5;

    std::cout << i << std::endl;
    std::cout << a << std::endl;
}
```

[00:00:14](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=14s) Instrucțiunile de afișare afișează `10` și `5` pe linii separate. **Fluxul de ieșire** `std::cout` acceptă fiecare valoare prin `<<`; `std::endl` inserează un sfârșit de linie și golește fluxul. Un punct și virgulă încheie fiecare instrucțiune, iar acoladele delimitează corpul funcției `main`.

[00:00:29](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=29s) Folosirea lui `i` în această expresie de afișare citește valoarea memorată în el, deci la ieșire ajunge `10`. Folosirea lui `a` furnizează în mod similar `5`. Ea nu furnizează identitatea sau adresa variabilei. Explicația din înregistrare despre înlocuirea valorilor se referă la `i = 10`; `a` rămâne `5`.

## Suprascrierea unei valori

[00:00:52](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=52s) O **atribuire** schimbă valoarea păstrată în memoria existentă. Inserează `i = 15;` înaintea afișării:

```cpp
int i = 10;
int a = 5;
i = 15;
std::cout << i << std::endl;
std::cout << a << std::endl;
```

Urmește schimbarea în ordine:

1. Inițializarea memorează `10` în `i` și `5` în `a`.
2. Atribuirea suprascrie `i` cu `15`; nu creează un al doilea `i`.
3. Afișarea citește conținutul curent, deci primește `15` pentru `i` și `5` pentru `a`.

[00:01:08](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=68s) Compilarea folosește compilatorul pentru a traduce sursa într-un program executabil. Rularea programului modificat produce `15`, apoi `5`, ceea ce confirmă suprascrierea. [00:01:17](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=77s) Aceste instrucțiuni se execută în ordinea în care sunt scrise. Mutarea afișării înaintea atribuirii ar citi valoarea veche.

<details>
<summary>De ce modificarea lui i îl lasă pe a neschimbat?</summary>

Sunt variabile distincte, cu memorie distinctă. Atribuirea vizează doar obiectul numit `i`.

</details>

## Memorarea unei adrese

[00:01:22](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=82s) Memoria poate păstra și o **adresă**, o valoare care identifică locația altui obiect. [00:01:29](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=89s) Diagrama introduce o celulă nouă și scrie în ea adresa ilustrativă `32`. Aceasta este o operație din diagramă, nu o instrucțiune C++ validă de obținere a unui pointer din literalul întreg `32`.

[00:01:45](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=105s) Un **pointer** este o valoare folosită pentru a se referi la un obiect prin adresa lui. În diagramă, noua variabilă memorează adresa lui `i`, ceea ce îl face pe `i` obiectul **indicat** (*pointee*), obiectul la care se ajunge prin pointer.

[00:01:58](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=118s) Diagrama reprezintă atât întregii obișnuiți, cât și adrese prin numere; interpretarea lor intenționată diferă. [00:02:07](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=127s) Memoria reală păstrează modeluri de biți, nu o locație sau o variabilă în miniatură în interiorul altei celule. [00:02:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=135s) Modelul de biți memorat de pointer este interpretat drept adresă. Acest model numeric explică relația, însă pointerii C++ sunt un tip distinct, nu valori întregi obișnuite `int` interschimbabile.

[00:02:22](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=142s) Ținta de aici este, în mod specific, un obiect `int`. [00:02:30](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=150s) Luarea adresei sale produce un pointer către acel întreg, nu un pointer către o colecție de octeți nespecificată.

[00:02:45](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=165s) Adresa memorată furnizează poziția de început. Programul are nevoie și de tipul țintei pentru a ști ce obiect desemnează un acces. [00:02:52](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=172s) În această demonstrație, un `int` ocupă patru celule de octet, care împreună reprezintă un singur întreg. [00:03:00](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=180s) Așadar, valoarea `32` din diagramă indică începutul lui `i`, ai cărui patru octeți se află la adresele 32–35.

Pentru sintaxa corespunzătoare, vezi [exemplul conex din repozitoriu](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/eb8f41e0402f4552beec72bc0953b86251d16cf4/en/05_programming_fundamentals/memory_example_1/example.cpp); această reconstrucție simplificată folosește valoarea din videoclip:

```cpp
int i = 15;
int* iad = &i; // obține adresa reală; nu înlocui cu literalul 32
```

Pointerul memorează adresa. Tipul țintei este cunoscut din declarare; nu este o informație suplimentară despre dimensiune stocată alături de acea adresă.

## Declararea unui pointer către int

[00:03:21](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=201s) O declarare obișnuită de `int` ar spune că noua variabilă conține o valoare întreagă. Ca să declari un pointer către un întreg, adaugă steluța:

```cpp
int* iad; // doar declarație; inițializarea lipsește în continuare
```

[00:03:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=224s) **`int*`** înseamnă „pointer către `int`”: o adresă prin care poate fi accesat un obiect întreg. [00:04:03](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=243s) `*` furnizează partea de pointer; `int` furnizează tipul obiectului indicat. [00:04:10](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=250s) Pe mașina din demonstrație, un acces la un întreg tratează patru octeți ca pe un singur întreg.

Dimensiunea de patru octeți este o presupunere a acestui exemplu, nu o cerință universală a C++. [Specificația tipurilor întregi din C++](https://eel.is/c++draft/basic.fundamental) permite lățimi dependente de implementare. Și dimensiunea proprie a variabilei pointer este distinctă de dimensiunea obiectului indicat: `int*` nu înseamnă „un pointer de patru octeți”.

[00:04:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=255s) Declarația se termină cu numele `iad`. [00:04:20](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=260s) Inițializarea sa este amânată intenționat pentru mai târziu. Declarația singură nu furnizează o adresă țintă utilizabilă; nu citi și nu dereferenția acest pointer neinițializat.

[00:04:22](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=262s) O **declarare** combină tipul cu numele variabilei; un **inițializator** poate furniza în plus valoarea inițială. [00:04:37](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=277s) În `int i`, tipul descrie un obiect întreg, reprezentat ca o singură valoare răspândită pe octeții săi. [00:04:54](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=294s) În `int* iad`, tipul descrie o adresă a cărei țintă este un obiect întreg. [00:05:07](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=307s) Numele `iad` a fost ales pentru a sugera „adresa lui i”; orice nume potrivit de variabilă ar funcționa.

## Luarea adresei lui i

[00:05:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=315s) Acum inițializează pointerul cu **operatorul de adresare**, operatorul unar `&`, care obține adresa obiectului numit:

```cpp
int i = 15;
int* iad = &i;
```

[Exemplul conex din repozitoriu](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/eb8f41e0402f4552beec72bc0953b86251d16cf4/en/05_programming_fundamentals/memory_example_1/example.cpp) folosește aceeași operație `&i`, cu alt nume de pointer și altă valoare inițială a întregului.

[00:05:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=315s) Compară cele două utilizări ale numelui:

1. Într-o expresie care are nevoie de valoarea sa, `i` furnizează numărul memorat în acel moment, `15`.
2. În `&i`, operatorul cere locația obiectului `i`.
3. Inițializarea memorează acea adresă în `iad`.

[00:05:32](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=332s) Aceasta este adresa variabilei în sine, nu adresa „numărului 15”. Atribuirea unui număr nou lui `i` nu schimbă obiectul la care se referă `iad`. [00:05:55](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=355s) Citește `&i` ca „dă-mi adresa memoriei acestui obiect”. Dacă diagrama plasează `i` la adresa 32, scrie 32 în `iad`; programul în execuție obține adresa reală a lui `i`.

<details>
<summary>După i = 40, trebuie inițializat din nou iad?</summary>

Nu. Adresa se referă în continuare la același `i`. S-au schimbat doar conținuturile acelui obiect.

</details>

## Afișarea adresei reale

[00:06:08](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=368s) Adaugă afișarea pointerului însuși, compilează și rulează:

```cpp
int i = 15;
int* iad = &i;
std::cout << iad << std::endl;
```

[00:06:22](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=382s) Ieșirea din înregistrare începe cu `0x`. Aceasta este notație **hexazecimală**, adică în baza 16. [00:06:30](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=390s) Cifrele de după prefix pot include A–F, deci litere precum F și B sunt cifre obișnuite ale adresei afișate.

[00:06:38](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=398s) Adresa afișată este adresa reală folosită pentru `i` în acea rulare. Valoarea 32 din diagramă a fost inventată pentru explicație. [00:06:53](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=413s) Convertirea cifrelor hexazecimale în zecimal schimbă doar notația, nu adresa pe care o reprezintă; de exemplu, hexazecimalul `0x20` reprezintă zecimalul 32.

[00:07:02](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=422s) Rulările repetate din demonstrație arată adrese diferite. **Randomizarea adreselor** poate schimba locul unde sunt plasate obiectele între rulări, deci nu presupune o adresă fixă și nici faptul că fiecare rulare diferă obligatoriu. În interiorul duratei de viață a obiectului — perioada în care există — schimbarea valorii memorate nu îl mută.

[00:07:21](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=441s) **Memoria virtuală** înseamnă că acestea sunt adrese în spațiul de adrese al programului. Sistemul de operare le mapează pe memoria fizică; un număr afișat nu trebuie să identifice un octet fizic cu același număr. Înregistrarea menționează această mapare și lasă mecanismul ei detaliat în afara lecției.

## Scrierea prin pointer

[00:07:37](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=457s) O variabilă poate fi citită, scrisă sau i se poate lua adresa. Demonstrația elimină `a`, acum inutilă, și folosește adresa lui `i` pentru a-i schimba conținutul.

[00:07:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=464s) Ca să scrii printr-o adresă, folosește **operatorul de dereferențiere**, operatorul unar `*`. Acesta urmărește pointerul și oferă acces la obiectul indicat. [00:07:53](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=473s) Schimbarea este:

```cpp
int i = 10;
i = 15;
int* iad = &i;
*iad = 40;
std::cout << i << std::endl; // 40
```

[00:08:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=485s) Citește `*iad` ca „obiectul aflat la adresa păstrată în iad”. Steluța de aici este un operator de expresie; steluța din declarația `int* iad` formează tipul pointer.

[00:08:17](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=497s) Urmărește atribuirea:

1. Citește adresa memorată în `iad`.
2. Urmește-o până la obiectul `i`.
3. Folosește acel obiect ca țintă a atribuirii.
4. Memorează acolo `40`.

[00:08:29](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=509s) Ținta conținea `15`; scrierea o înlocuiește cu `40`. Pointerul conține în continuare aceeași adresă. [00:08:42](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=522s) În partea stângă a unei atribuiri, atât `i`, cât și `*iad` identifică același obiect țintă. Prin urmare, `*iad = 40` are aici același efect ca `i = 40`.

## Citirea prin pointer

[00:09:02](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=542s) Dereferențierea oferă acces la obiectul țintă fie pentru citire, fie pentru scriere. [00:09:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=555s) Înlocuiește afișarea directă a lui `i` cu afișarea lui `*iad`:

```cpp
int i = 15;
int* iad = &i;
*iad = 40;
std::cout << iad << std::endl;  // adresa
std::cout << *iad << std::endl; // 40
```

[Exemplul conex din repozitoriu](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/eb8f41e0402f4552beec72bc0953b86251d16cf4/en/05_programming_fundamentals/memory_example_1/example.cpp) afișează și el un pointer către întreg dereferențiat; este cod conex, nu această stare exactă.

[00:09:37](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=577s) O variabilă pointer folosită într-o expresie de valoare furnizează propria valoare memorată: adresa. Dacă un exemplu schematic arată 100 memorat în acea celulă de pointer, citirea pointerului furnizează acea adresă schematică, nu conținutul întregului. Aceasta nu trebuie confundată cu ieșirea `40` obținută prin dereferențiere.

[00:09:57](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=597s) Expresia `*iad` oferă mai întâi acces la obiectul țintă; într-o expresie de afișare valoarea sa este apoi citită. [00:10:10](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=610s) Cu adresa 32 din diagramă, pașii conceptuali sunt:

1. Citește 32 din `iad`.
2. Urmește adresa 32 până la `i`.
3. Citește conținutul lui `i`, în prezent 40.
4. Transmite 40 către fluxul de ieșire.

[00:10:17](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=617s) Luarea lui `&i` a memorat o adresă în memoria proprie a pointerului. Citirea acelui pointer și citirea obiectului său indicat sunt operații diferite. [00:10:27](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=627s) Așadar, citirea prin `*iad` furnizează `40` către ieșire.

<details>
<summary>Dereferențierea scrie întotdeauna ceva?</summary>

Nu. `*iad = 40` scrie pentru că este o atribuire. `std::cout << *iad` citește pentru că ieșirea are nevoie de valoarea curentă a țintei. Dereferențierea însăși oferă acces la obiect.

</details>

## De ce un pointer pe octet este un alt tip

[00:10:47](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=647s) **Tipul obiectului indicat** spune programului ce fel de obiect se așteaptă un acces. Lecția compară un `int` de patru octeți cu **`uint8_t`**, un întreg fără semn pe opt biți, cu intervalul 0–255. Pe mașina din demonstrație ocupă un singur octet.

Schimbarea care motivează totul încearcă să dea unui pointer către întreg adresa unui obiect pe octet:

```cpp
#include <cstdint>

std::uint8_t a = 5;
int* iad = &a; // eroare de compilare: tipuri de pointer incompatibile
```

Aceasta este starea respinsă discutată în înregistrare. Tipul sursă al lui `&a` este `std::uint8_t*`, iar destinația este `int*`.

[00:11:07](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=667s) Imaginează că ignorăm nepotrivirea. O citire de întreg ar încerca să acceseze un întreg întreg acolo unde există doar un obiect de un octet. Octeții suplimentari nu aparțin acelei variabile. [00:11:33](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=693s) Conținutul lor nu poate fi presupus a fi zero sau semnificativ. În C++ real, un asemenea acces nepotrivit este **comportament nedefinit**: limbajul nu promite nici măcar un anumit „număr-gunoi”.

## Înțelegerea diagramei memoriei

[00:11:40](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=700s) Diagrama folosește **alinierea**, o cerință privind locul unde poate începe memoria unui obiect, pentru a explica golurile dintre obiecte. Ea modelează memoria în sloturi de patru octeți, lăsând spațiu nefolosit după o variabilă de un octet.

Aceasta este o dispunere didactică, nu o regulă conform căreia un alocator așază fiecare variabilă într-un bloc de patru octeți sau nu folosește niciodată octeții vecini pentru alt obiect. [Specificația alinierii din C++](https://eel.is/c++draft/basic.align) definește cerințe în funcție de tip; plasarea efectivă poate diferi.

[00:11:54](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=714s) Dispunerea ilustrativă este:

| Obiectul din diagramă | Adresa de început | Octeții care aparțin obiectului |
| --- | --- | --- |
| Întreg de patru octeți | 32 | 32–35 |
| Întreg de un octet într-un slot de patru octeți | 36 | doar 36 |
| Valoare de opt octeți | 40 | 40–47 |

Intervalul de opt octeți se termină chiar înainte de 48; nu include octetul 48. Spațiul de la 37 la 39 în această ilustrare nu devine parte din variabila de un octet.

[00:12:14](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=734s) O adresă are și o **reprezentare binară**, un model de biți memorat chiar în octeții proprii ai pointerului. Diagrama distribuie o adresă mică precum 32 în interiorul unui slot mai mare. Pentru această reprezentare numerică mică este suficient ca un singur octet să aibă biți nenuli. [00:12:54](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=774s) Aceeași simplificare este folosită și pentru un întreg mic precum 15.

„Gol” aici înseamnă octeți cu reprezentare nulă în desenul simplificat, nu memorie inexistentă sau octeți pe care o atribuire obișnuită de întreg i-ar lăsa nescrise. Ordinea stânga/dreapta din desen nu trebuie tratată ca o garanție a ordinii în memorie. Experimentul ulterior care poate fi rulat folosește ordinea little-endian. Înregistrarea menționează și că pointerii de pe mașina sa ocupă opt octeți, chiar dacă desenul este simplificat la sloturi de patru octeți.

[00:13:02](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=782s) Codificarea detaliată pe octeți este amânată la un alt videoclip. Ideea esențială aici este să deosebim octeții care reprezintă o adresă de octeții care aparțin obiectului la care acea adresă ajunge.

## Potrivirea pointerului cu obiectul

[00:13:26](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=806s) Presupunem că pointerul către întreg ar putea memora adresa 36 din diagramă. Un acces ca `int` ar aștepta patru octeți, deși variabila care începe acolo deține doar primul ei octet. [00:13:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=824s) Octeții din afara obiectului nu sunt disponibili ca parte din valoarea lui. [00:13:53](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=833s) Tipul țintă `int` declarat al pointerului este motivul pentru care accesul așteaptă un întreg întreg. [00:14:14](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=854s) În acest exemplu înseamnă toți cei patru octeți împreună, nu primul octet care s-ar întâmpla să fie util.

[00:14:37](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=877s) Ca să accesezi variabila de un octet ca atare, potrivește pointerul cu tipul ei:

```cpp
std::uint8_t a = 5;
std::uint8_t* ap = &a; // tip potrivit
*ap = 15;             // scrie în variabila de un octet
```

[00:14:52](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=892s) **Verificarea de tipuri** este controlul compilatorului asupra faptului că operațiile și atribuirile corespund tipurilor declarate. Ea respinge și nepotrivirea inversă:

```cpp
int i = 15;
std::uint8_t* ap = &i; // eroare de compilare fără o conversie explicită
```

[00:15:12](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=912s) Diagrama ilustrează două pericole distincte. Scrierea printr-un pointer pe octet în interiorul unui întreg ar modifica un singur octet și ar păstra ceilalți octeți ai acestuia. Accesarea memoriei unui obiect pe octet ca pe un întreg ar încerca un acces mai larg, dincolo de memoria acelui obiect. Niciunul nu trebuie înțeles ca o conversie implicită sigură.

[00:15:24](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=924s) Discuția despre „coruperea întregului număr” înseamnă că o scriere parțială schimbă valoarea interpretată a întregului. O scriere autentică pe un singur octet **nu** suprascrie fizic patru octeți. La fel, un acces invalid mai larg nu are niciun comportament de deplasare garantat și niciun rezultat predictibil.

[00:15:32](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=932s) Atribuirea obișnuită între pointeri incompatibili este respinsă de compilator înainte de execuție. Problema ține de tipuri și de acces valid la obiecte, nu doar de dimensiune: două tipuri fără legătură nu devin compatibile doar pentru că au aceeași dimensiune.

## Conversia către un pointer pe octet

[00:15:35](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=935s) Lecția ocolește acum intenționat verificarea obișnuită la atribuirea de pointeri printr-o **conversie explicită** (*cast*), adică o cerere explicită de a converti o valoare la alt tip. [00:15:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=944s) Aceasta interpretează adresa unui întreg drept un pointer pe octet, astfel încât accesul prin acel pointer atinge un singur octet în loc de un întreg întreg.

O reconstrucție simplificată a experimentului cu conversie este:

```cpp
int i = 15;
int* iad = &i;
std::uint8_t* byte = (std::uint8_t*)iad;
*byte = 8;
std::cout << i << std::endl;
```

Tipul dintre paranteze din `(std::uint8_t*)iad` este castul în stil C arătat de această reconstrucție. El schimbă interpretarea pointerului; nu transformă întregul memorat într-un nou obiect de un octet.

[00:16:06](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=966s) După scrierea pe octet, experimentul cu valoare mică din înregistrare citește înapoi `8`. [00:16:16](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=976s) Explicația se bazează pe **ordinea little-endian**: octetul cel mai puțin semnificativ se află la adresa cea mai mică, adică primul octet întâlnit. Pornind de la valoarea mică 15, ceilalți octeți ai întregului sunt zero, deci înlocuirea octetului mic cu 8 face ca întregul să fie citit ca 8.

O conversie explicită nu face singură să fie valid accesul arbitrar la memoria prin prisma unui tip nepotrivit. C++ permite în mod specific accesul la reprezentarea unui obiect prin `unsigned char`; abordarea cu `uint8_t` din videoclip se bazează pe faptul că acest tip este un alias, adică un alt nume pentru același tip, al lui `unsigned char` pe implementarea respectivă. Această distincție urmează [regulile C++ de acces la obiecte](https://eel.is/c++draft/basic.lval#11) și [regulile de reinterpretare](https://eel.is/c++draft/expr.reinterpret.cast). Pentru o variantă a aceleiași reconstrucții, orientată explicit spre octeți:

```cpp
unsigned char* byte = reinterpret_cast<unsigned char*>(iad);
*byte = 8; // modifică un singur octet de reprezentare, nu un întreg complet
```

Aici `unsigned char` este tipul pentru accesul pe octeți, iar `reinterpret_cast` este sintaxa explicită de reinterpretare a pointerului. Această scriere clarifică chestiunea; nu se pretinde că este exact scrierea din înregistrare.

## De ce 500 devine 264

[00:16:33](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=993s) Un întreg mai mare decât 255 are nevoie de mai mult de un octet pe opt biți. Demonstrația schimbă întregul inițial în 500, lăsând un octet superior nenul înainte de a scrie octetul mic:

```cpp
int i = 500;
unsigned char* byte = reinterpret_cast<unsigned char*>(&i);
*byte = 8;
std::cout << i << std::endl; // 264 pe dispunerea din demonstrație
```

Acest exemplu reconstruiește experimentul din înregistrare folosind tipul explicit pentru acces pe octeți descris mai sus. [00:16:49](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1009s) Ieșirea este `264`, nu `8`.

Pe dispunerea demonstrată, de patru octeți, little-endian, urmărește octeții în ordinea crescătoare a adreselor:

1. `500 = 1 × 256 + 244`, deci octeții săi sunt `244, 1, 0, 0`.
2. Pointerul pe octet ajunge doar la primul octet.
3. Scrierea lui 8 îi schimbă în `8, 1, 0, 0`.
4. Citirea întregului `int` complet dă `1 × 256 + 8 = 264`.

Octetul superior a păstrat o parte din valoarea inițială 500. Scrierea nu l-a golit. „Depășirea în octetul următor” descrie modul în care întregul `int` pe mai mulți octeți reprezintă o valoare mai mare; atribuirea unei valori prea mari unui întreg fără semn de un octet nu scrie dincolo de acel octet, în vecinul său.

<details>
<summary>După ce scrierea anterioară a produs 8, de ce aceasta produce 264?</summary>

Întregul anterior avea zero în toți octeții superiori. Întregul 500 avea 1 în octetul următor, iar scrierea pe un octet l-a lăsat pe acel 1 neschimbat.

</details>

## De ce următorul rezultat este 257

[00:17:45](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1065s) Discuția folosește 256 pentru a face limita foarte vizibilă. Este cel mai mic întreg nenegativ care are nevoie de mai mult de un octet pe opt biți. Reprezentarea sa little-endian începe cu `0, 1`.

[00:18:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1085s) O reconstrucție mai clară a ultimei modificări a octetului mic este:

```cpp
int i = 256;
unsigned char* byte = reinterpret_cast<unsigned char*>(&i);
*byte = 1;
std::cout << i << std::endl; // 257 pe dispunerea din demonstrație
```

Același rezultat se obține dacă octetul superior din exemplul anterior cu 500 rămâne 1, iar scrierea octetului mic devine 1. [00:18:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1085s) Rezultatul demonstrat este `257 = 256 + 1`. Chiar înaintea acestui moment, la [00:18:02](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1082s), instructorul observă că programul modificat nu fusese recompilat. Rezultatul corect apare după recompilare: rularea executabilului vechi nu testează o modificare a codului sursă.

[00:18:11](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1091s) Scrierea pe octet modifică doar primul dintre cei patru octeți ai întregului. [00:18:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1095s) Ceilalți octeți rămân cum erau. Înlocuirea unui octet nu se propagă în vecini, nu îi incrementează și nu îi resetează; aceasta este altceva decât efectuarea unei operații aritmetice asupra întregului complet.

<details>
<summary>Dacă octetul superior rămâne 1, iar cel mic devine 15, ce număr întreg rezultă?</summary>

Pe această dispunere, `256 + 15 = 271`. Octetul superior păstrat contribuie cu 256 indiferent de noua valoare a octetului mic.

</details>

## Revenirea la scrieri de întregi complete

[00:18:23](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1103s) Experimentul cu conversia către un octet servește înțelegerii reprezentării, nu este ceva ce lecția recomandă pentru atribuirile obișnuite de întregi. Lucrează cu întregul prin tipul său întreg propriu.

[00:18:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1124s) Elimină reinterpretarea pe octet și revino la un `int*`:

```cpp
int i = 500;
int* iad = &i;
*iad = 8;
std::cout << i << std::endl; // 8
```

[00:19:01](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1141s) Deoarece `iad` este un pointer către `int`, atribuirea înlocuiește întreaga valoare întreagă. Pe mașina din demonstrație, aceasta scrie întregul pe toți cei patru octeți; nu lasă nicio parte superioară păstrată din 500. Adresa din `iad` identifică în continuare același `i`.

Distincția centrală a lecției este acum vizibilă: `iad` furnizează o adresă, iar `*iad` oferă acces la întregul de la acea adresă. Tipul obiectului indicat stabilește ce fel de obiect așteaptă acel acces.

## Istoricul modificărilor de cod

Acestea sunt stări de cod succesive din înregistrare, nu afirmații că un commit din repozitoriu conține exact demonstrația:

- [00:00:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=5s) — Inițializează `i = 10` și `a = 5`, apoi afișează valorile lor.
- [00:00:52](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=52s) — Inserează `i = 15`; rularea compilată afișează 15 și 5.
- [00:03:21](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=201s) — Introduce declarația `int* iad`, amânând inițializarea.
- [00:05:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=315s) — Inițializează `iad` din `&i`; afișează adresa sa reală la [00:06:08](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=368s).
- [00:07:37](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=457s) — Elimină `a`, apoi scrie 40 prin `*iad`.
- [00:09:15](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=555s) — Citește prin `*iad` în loc să afișeze doar adresa.
- [00:10:47](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=647s) — Compară `int*` cu adresa incompatibilă a unei variabile de un octet.
- [00:15:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=944s) — Convertește către un pointer pe octet; testul cu valoare mică citește înapoi 8.
- [00:16:49](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1009s) — Porneste de la 500 și scrie octetul mic cu 8; întregul se citește 264.
- [00:18:05](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1085s) — După recompilare, scrie octetul mic cu 1, iar octetul superior rămâne 1; rezultatul este 257.
- [00:18:44](https://www.youtube.com/watch?v=859Y0Q8pyLg&t=1124s) — Revine la o atribuire obișnuită prin `int*` care înlocuiește întregul complet.