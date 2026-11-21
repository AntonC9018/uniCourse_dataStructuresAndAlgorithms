> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Instrucțiuni C++ și funcții simple

[00:00:00](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=0s) Această lecție face legătura între codul C++ lizibil și ordinea în care un program execută acțiuni. Vei porni de la un singur mesaj, îi vei modifica ieșirea pas cu pas, apoi vei organiza aceleași acțiuni în funcții care pot fi apelate o dată, de două ori sau din altă funcție.

Termenii de care ai nevoie sunt:

- **Codul de mașină** este limbajul de instrucțiuni de nivel scăut al procesorului. Un **limbaj de programare**, aici C++, îți permite să descrii acțiuni în cod sursă lizibil. **Abstrația** înseamnă exprimarea detaliilor de nivel scăut prin concepte mai simple.
- **Memoria** stochează valori. O **celulă de memorie** este o locație care ține date; o **adresă** identifică o locație. Un **registru al procesorului** este o locație mică de stocare din interiorul procesorului. O **variabilă** oferă unui program un nume prin care poate lucra cu o valoare.
- O **instrucțiune de program**, numită de obicei în engleză **statement**, exprimă o acțiune în cod sursă. **Sintaxa** înseamnă regulile pentru scrierea acelui cod.
- O **funcție** este o secvență de instrucțiuni cu nume, reutilizabilă. **Definiția** ei furnizează numele și instrucțiunile; **corpul** ei este codul delimitat de acolade, `{ }`. **main** este funcția specială în care începe execuția acestor exemple.
- Un **apel de funcție** pornește execuția corpului unei funcții. **Funcția apelantă** este funcția care face apelul, iar **locul apelului** este locul unde acesta este scris. **Revenirea** înseamnă reluarea funcției apelante după apel. **Fluxul de control** este ordinea în care execuția trece între instrucțiuni. Un **apel imbricat** are loc când o funcție apelată apelează la rândul ei altă funcție.
- O **consolă** afișează text; **terminalul** din înregistrare oferă această afișare și un loc unde poți rula comenzi. Un **literal șir** este text scris între ghilimele duble.
- **Biblioteca standard** oferă facilități uzuale. Un **header** face disponibile declarațiile bibliotecii; `#include <iostream>` include headerul folosit pentru ieșirea pe consolă. `std::cout` este fluxul de ieșire standard, iar `<<` trimite către el valoarea următoare.
- Un **sfârșit de linie** încheie linia de ieșire curentă. `std::endl` scrie un sfârșit de linie și golește fluxul, adică trimite mai departe ieșirea tamponată.
- Un **comentariu** este text sursă ignorat drept cod. `//` începe un comentariu care continuă până la sfârșitul liniei sursă respective.
- Un **fișier sursă** conține codul scris de tine. Un **compilator** traduce codul sursă; **compilarea** este acea traducere. Un **linker** combină codul compilat cu codul de bibliotecă necesar într-un **executabil**, un fișier care poate fi rulat. **Linkarea** este acel pas de combinare, iar un **flag** este o opțiune pasată unei comenzi de build.
- `int` este tipul de întreg al C++ și tipul de returnare folosit pentru `main`. `void` ca tip de returnare al unei funcții înseamnă că funcția nu returnează nicio valoare. Un **parametru** este o intrare cu nume a unei funcții; funcțiile simple de aici nu au parametri.
- Doar pentru clarificarea de mai jos privind corectitudinea, un **pointer** este o valoare care conține o adresă de memorie. Operațiile cu pointeri nu sunt predate în acest video.

Folosește [laboratorul de instalare a compilatorului](../../../en/labs/common/05_compiler_install.md) pentru configurare și [laboratorul despre instrucțiuni](../../../en/labs/cpp/01_instruction.md) pentru exerciții conexe. Instalarea este o sarcină separată, nu o procedură demonstrată aici.

**Domeniul lecției.** [00:00:16](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=16s) Abstrația este tratată mai pe larg în subiectul despre algoritmi. [00:00:28](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=28s) Instalarea compilatorului aparține unor video-uri separate și laboratorului de configurare. [00:01:46](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=106s) Explicația completă pentru `main` vine mai târziu. [00:02:22](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=142s) Sintaxa detaliată și mecanica de build sunt lăsate intenționat deoparte, ca să te poți concentra asupra ordinii de execuție.

Programele intermediare din înregistrare prezentate mai jos sunt **reconstrucții simplificate**, nu afirmații despre sursă exactă din commit. Exemplul de funcție din commit-ul inspectat folosește aritmetică, nu aceste mesaje de salutare. Citarea sa imutabilă conexă apare lângă exemplul de apel imbricat.

## De la instrucțiunile mașinii la acțiuni lizibile

[00:00:00](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=0s) În acest curs scrii C++, nu scrii sau manipulezi direct instrucțiuni în cod de mașină. Codul de mașină este limbajul de nivel scăut al procesorului; C++ este limbajul de programare care oferă o abstracție lizibilă peste acel nivel.

[00:00:21](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=21s) **Abstrația** înseamnă simplificarea a ceva neclar prin exprimarea lui în termeni mai ușor de înțeles. În loc să explici instrucțiuni de nivel scăut, scrii cod sursă obișnuit care descrie acțiunea.

[00:00:37](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=37s) Lucrul cu **memoria**, stocarea valorilor, include operații precum adunarea numerelor și copierea unei valori dintr-o celulă de memorie în alta. O celulă de memorie este o locație care ține date. Ai nevoie și de un mod de a spune când trebuie să se producă aceste operații.

[00:00:54](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=54s) Înregistrarea explică faptul că aceste exemple pentru începători nu selectează direct un registru al procesorului și nu citesc o adresă fixă aleasă. Un **registru** este stocare în interiorul procesorului, iar o **adresă** identifică o locație de memorie. Ideea lecției este că accesul trece printr-o abstracție a limbajului, în loc să te obligi să alegi tu locații hardware.

Această afirmație are nevoie de o precizare: C++ permite într-adevăr accesul prin **pointeri**, valori care conțin adrese de memorie, atunci când accesul este valid. „Nu poți citi o adresă fixă” este, așadar, o simplificare a abordării acestei lecții, nu o limitare generală a C++. [Explicația conexă despre memorie din commit](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/e6a198dd9d5f56bde01e2f74f0d71bf253316d82/en/05_programming_fundamentals/doc.md#writing-to-a-memory-address) demonstrează această distincție. Acest exemplu scurt este o clarificare de corectitudine, **nu o operație predată în video**:

```cpp
int value = 0;
int* pointerToValue = &value; // Reține adresa lui value.
*pointerToValue = 10;        // Scrie în acea locație validă.
```

[00:01:10](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=70s) În această etapă lucrezi la nivelul **variabilelor**: nume prin care programul lucrează cu valorile stocate. [00:01:17](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=77s) Variabilele oferă mecanismul de interacțiune cu memoria fără să alegi tu însuși registrele și adresele.

[00:01:23](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=83s) Pentru a specifica ordinea acțiunilor, scrii **instrucțiuni de program**, adică **statement-uri**. Acestea sunt acțiuni exprimate în cod sursă, nu instrucțiunile de mașină discutate mai devreme. Lecția trece acum la această ordine.

## Pornește de la main și o singură instrucțiune de ieșire

[00:01:46](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=106s) Un program de bază are o **funcție main**. Pentru moment, trateaz-o ca punctul de pornire al execuției. **Corpul** ei este secvența de instrucțiuni dintre acoladele sale. Pornește cu un corp gol:

```cpp
int main()
{
}
```

Acoladele delimitează corpul; ele nu afișează nimic prin ele însele. Aici `int` este tipul de returnare întreg cerut pentru `main`. Sensul complet al acestei funcții speciale este amânat.

[00:01:59](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=119s) Adaugă o instrucțiune care scrie pe **consolă**, afișajul de text folosit pentru ieșirea vizibilă a programului. Exemplul minim afișează **literalul șir** `"Hello World"`, text cuprins între ghilimele duble:

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello World";
}
```

**Biblioteca standard** oferă facilități reutilizabile. **Headerul** `<iostream>` face disponibile declarațiile sale de ieșire prin `#include`. `std::cout` este fluxul de ieșire standard; `<<` trimite șirul către el. Punctul și virgulă încheie această instrucțiune. Acestea sunt suficiente detalii de sintaxă — regulile pentru scrierea codului — ca să urmărești exemplul; video-ul amână o explicație sistematică a sintaxei.

## Construiește și rulează primul program

[00:02:18](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=138s) Scrierea sursei nu este același lucru cu rularea ei. Un **fișier sursă** conține codul tău. Un **compilator** îl traduce, iar **compilarea** este acea traducere. **Linkerul** efectuează **linkarea**, combinând codul compilat cu codul de bibliotecă necesar într-un **executabil**, un fișier care poate fi rulat.

Urmează secvența de build și rulare:

1. Compilează și linkează fișierul sursă folosind uneltele tale C++ configurate. Lecțiile de configurare separate explică comenzile.
2. [00:02:28](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=148s) **Flag-uri** suplimentare, adică opțiuni pasate comenzii de build, pot fi furnizate pentru linkare. Sunt menționate aici, nu explicate ca procedură nouă de configurare.
3. [00:02:37](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=157s) Rulează executabilul rezultat. În mediul Linux prezentat, acesta se numește `a.out`. Rezultatul înregistrat este `Hello World`.

După fiecare modificare ulterioară a sursei, repetă build-ul înainte de rulare. Rularea singură a unui executabil existent nu include o modificare a fișierului său sursă.

## Adaugă instrucțiuni și observă ordinea lor

[00:02:46](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=166s) Instrucțiunea `std::cout` produce șirul vizibil. [00:02:48](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=168s) Extinde corpul astfel încât după mesaj să urmeze un **sfârșit de linie**, care încheie linia de ieșire curentă, apoi un nume:

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello World";
    std::cout << std::endl;
    std::cout << "Anton";
    std::cout << std::endl;
}
```

`std::endl` scrie un sfârșit de linie și golește fluxul de ieșire, trimițând mai departe orice ieșire tamponată. Aici sunt patru instrucțiuni: două scriu text și două încheie linii. O linie nouă în fișierul sursă nu creează automat o linie nouă în ieșire.

[00:03:08](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=188s) După rebuild și rerulare, ieșirea înregistrată este:

```text
Hello World
Anton
```

Instrucțiunile au rulat una după alta, de sus în jos: salutare, sfârșit de linie, nume, sfârșit de linie. Acesta este primul exemplu concret de **flux de control**, ordinea în care programul execută acțiunile.

## Comentează un sfârșit de linie

[00:03:19](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=199s) Un **comentariu** este text ignorat ca cod de program. Punând `//` înaintea unei instrucțiuni, restul acelei linii sursă devine comentariu. Mai întâi elimină astfel ultimul sfârșit de linie:

```cpp
std::cout << "Hello World";
std::cout << std::endl;
std::cout << "Anton";
// std::cout << std::endl;
```

[00:03:29](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=209s) După rebuild și rerulare, terminalul afișează la sfârșitul ieșirii un marcaj cu semnul procent. În terminalul prezentat, acel marcaj indică faptul că programul s-a încheiat fără un sfârșit de linie final. Este un marcaj de afișare al terminalului, nu un semn procent tipărit de acest program C++. Salutarea și numele sunt în continuare pe linii separate, deoarece sfârșitul de linie din mijloc rămâne.

[00:03:37](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=217s) Apoi omite sfârșitul de linie **dintre** cele două instrucțiuni de text. Asta izolează un alt efect:

```cpp
std::cout << "Hello World";
// std::cout << std::endl;
std::cout << "Anton";
std::cout << std::endl;
```

Demonstrația înregistrată arată că textul continuă pe aceeași linie. În această reconstrucție ieșirea este `Hello WorldAnton`, urmată de un sfârșit de linie. A doua instrucțiune de text rulează direct după prima; nu se inserează niciun separator automat.

<details>
<summary>De ce împărțirea celor două instrucțiuni de text pe linii sursă diferite nu împarte ieșirea lor pe linii de consolă?</summary>

Formatarea sursei și ieșirea sunt lucruri diferite. Un sfârșit de linie în sursă separă codul scris; ieșirea își schimbă linia doar când o instrucțiune executată scrie un sfârșit de linie. Dacă comentezi sfârșitul de linie din mijloc, cele două șiruri rămân alăturate.

</details>

## Definește o funcție fără a o apela

[00:03:50](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=230s) O **funcție** este o secvență de instrucțiuni cu nume, pe care o poți reutiliza. **Definiția** unei funcții furnizează acel nume și **corpul** ei, instrucțiunile delimitate de acolade. Mută instrucțiunile de salutare într-o funcție numită `f` și lasă un mesaj separat în `main`:

```cpp
#include <iostream>

void f()
{
    std::cout << "Hello World";
    std::cout << std::endl;
    std::cout << "Anton";
    std::cout << std::endl;
}

int main()
{
    std::cout << "main";
    std::cout << std::endl;
}
```

`void` înseamnă că această funcție nu returnează nicio valoare. `()` gol înseamnă că nu are **parametri**, adică intrări cu nume ale funcției. Definiția creează secvența cu nume; ea nu cere executarea acelei secvențe.

[00:04:05](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=245s) Execuția acestor programe începe în `main`, nu în funcția care apare prima în fișierul sursă. [00:04:18](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=258s) Rularea înregistrată afișează doar:

```text
main
```

[00:04:31](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=271s) Acest rezultat explică diferența dintre a defini o listă de instrucțiuni și a o activa. Nimic din `main` nu apelează încă `f`, deci instrucțiunile sale de salutare nu rulează niciodată.

<details>
<summary>Ar punea definiția lui f înainte de main ca salutarea să ruleze prima?</summary>

Nu. Poziția ei face definiția disponibilă, dar nu o apelează. În acest program execuția începe în main, iar main conține doar propriile instrucțiuni de ieșire.

</details>

## Apelează funcția din main

[00:04:43](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=283s) Păstrează definiția lui `f` și adaugă o instrucțiune după sfârșitul de linie din `main`:

```cpp
int main()
{
    std::cout << "main";
    std::cout << std::endl;
    f();
}
```

`f();` este un **apel de funcție**: pornește execuția corpului lui `f`. `main` este **funcția apelantă**, funcția care face apelul. Locația lui `f();` este **locul apelului**.

[00:04:51](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=291s) În modelul de procesor al lecției, apelul transferă execuția către prima instrucțiune a lui `f`. Corpul rulează instrucțiune cu instrucțiune. **Revenirea** înseamnă reluarea funcției apelante după acel apel. Acest model explică comportamentul programului; nu promite că fiecare instrucțiune sursă devine exact o instrucțiune de mașină.

[00:05:08](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=308s) Rularea completă înregistrată produce mai întâi `main` și sfârșitul său de linie, urmate de salutarea și numele din `f`. Reconstrucția produce deci:

```text
main
Hello World
Anton
```

Cuvântul „Hello” din explicația vorbită se referă la instrucțiunea de salutare; recapitularea ulterioară o identifică explicit ca „Hello World”.

## Apelează aceeași funcție de două ori

[00:05:23](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=323s) O funcție reutilizabilă poate fi apelată de mai multe ori. Păstrează o singură definiție a lui `f` și adaugă un al doilea apel:

```cpp
int main()
{
    std::cout << "main";
    std::cout << std::endl;
    f();
    f();
}
```

Urmează execuția în loc să tratezi cele două apeluri ca simultane:

1. [00:05:27](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=327s) `main` afișează mesajul și sfârșitul de linie.
2. [00:05:39](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=339s) Primul apel transferă execuția către începutul lui `f`. Acesta afișează `Hello World`, un sfârșit de linie, `Anton` și încă un sfârșit de linie.
3. [00:05:56](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=356s) Când `f` nu mai are instrucțiuni, revine la **locul apelului**, locul din `main` care a făcut acest apel concret. Execuția continuă cu instrucțiunea următoare, al doilea apel.
4. [00:06:12](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=372s) Al doilea apel pornește din nou `f` de la prima sa instrucțiune. Întregul corp rulează din nou, apoi revine după acest al doilea apel. În `main` nu mai există instrucțiuni, deci programul se încheie.

Ieșirea sugerată de această urmărire este:

```text
main
Hello World
Anton
Hello World
Anton
```

Expresia „ultimul loc al apelului” („last call site“) înseamnă apelul care se finalizează. Prima invocare revine după primul apel; a doua revine după al doilea. Fiecare invocare rulează același corp de funcție.

<details>
<summary>Dacă adaugi un al treilea f(); după al doilea, ce se repetă?</summary>

Salutarea, sfârșitul ei de linie, numele și sfârșitul său de linie se repetă încă o dată. Mesajul din main nu se repetă, deoarece instrucțiunile sale de ieșire sunt în afara lui f și nu sunt apelate din nou.

</details>

## Imbrică un apel de funcție în altul

[00:06:34](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=394s) Un **apel imbricat** are loc când o funcție apelată apelează la rândul ei altă funcție. [00:06:38](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=398s) Adaugă `B`, fă-l să afișeze `B` și un sfârșit de linie, apoi să apeleze `f`. Schimbă `main` să apeleze `B` în loc să apeleze direct `f`.

Această reconstrucție simplificată a înregistrării are aceeași formă de apel și revenire ca [exemplul de funcție din commitul conex](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/83e6302c9a3af2c28f3a17539cbdff6d63159ec8/en/05_programming_fundamentals/function_example_1/main.cpp). Acea sursă folosește `main → b → a` și aritmetică, deci este **dovadă conexă, nu exact programul de salutare**:

```cpp
#include <iostream>

void f()
{
    std::cout << "Hello World";
    std::cout << std::endl;
    std::cout << "Anton";
    std::cout << std::endl;
}

void B()
{
    std::cout << "B";
    std::cout << std::endl;
    f();
}

int main()
{
    std::cout << "main";
    std::cout << std::endl;
    B();
}
```

Funcțiile sunt definite înaintea utilizărilor lor în acest exemplu. `B` are trei instrucțiuni: scrie text, scrie un sfârșit de linie și apelează `f`. Un apel este o instrucțiune de program obișnuită, deci participă la aceeași secvență ordonată ca ieșirea.

Urmează fluxul de control complet:

1. [00:06:49](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=409s) Pornește în `main`. Execută instrucțiunile sale de ieșire, apoi ajunge la `B();`.
2. [00:07:03](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=423s) Acel apel transferă execuția către prima instrucțiune a lui `B`. Afișează `B`, apoi sfârșitul său de linie.
3. [00:07:14](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=434s) A treia instrucțiune a lui `B`, `f();`, transferă execuția către prima instrucțiune a lui `f`. Rulează toate instrucțiunile de ieșire ale lui `f`.
4. [00:07:23](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=443s) Când corpul lui `f` se încheie, execuția revine la funcția apelantă, `B`, după apelul către `f`. Acel apel era ultima instrucțiune a lui `B`, deci și `B` se încheie acum.
5. Revine în `main` după `B();`. Nu există instrucțiune următoare, deci programul se termină.

Ieșirea prezisă de reconstrucție este:

```text
main
B
Hello World
Anton
```

Înregistrarea explică acest ultim exemplu urmărind execuția. Execuțiile anterioare și urmărirea finală stabilesc împreună regula centrală: execută instrucțiunile în ordine în corpul curent, urmărește un apel într-alt corp și reia funcția apelantă când acel corp se termină.

<details>
<summary>Când f se termină, de ce revine execuția la B înainte de a reveni la main?</summary>

B a făcut apelul activ către f, deci B este funcția apelantă a lui f. Terminarea lui f reia execuția în B după acel apel. Abia după ce și B se termină, execuția reia main după apelul său către B.

</details>

## Istoricul modificărilor de cod

Niciun commit inspectat nu păstrează toate programele intermediare de salutare din înregistrare. Aceste linkuri cu timestamp identifică stările video în ordinea în care au fost construite; sursele conexe imutabile sunt etichetate lângă exemplele lor de mai sus.

- [00:01:59 — prima ieșire](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=119s): adaugă ieșirea pe consolă pentru `Hello World` în interiorul lui `main`.
- [00:02:48 — ieșire ordonată](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=168s): adaugă un sfârșit de linie, numele și un sfârșit de linie final.
- [00:03:19 — comentarii](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=199s): comentează un sfârșit de linie, apoi examinează efectul eliminării celui din mijloc.
- [00:03:50 — doar definiția](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=230s): mută secvența de salutare în `f`, în timp ce `main` afișează propriul mesaj.
- [00:04:43 — un singur apel](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=283s): adaugă `f();` după ieșirea lui `main`.
- [00:05:23 — apeluri repetate](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=323s): apelează aceeași funcție a doua oară.
- [00:06:38 — apeluri imbricate](https://www.youtube.com/watch?v=Z8AFpeE7hOo&t=398s): adaugă ieșirea lui `B` și apelul către `f`, apoi face ca `main` să apeleze `B`.