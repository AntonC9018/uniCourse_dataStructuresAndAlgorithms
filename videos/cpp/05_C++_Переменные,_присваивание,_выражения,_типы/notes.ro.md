> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Variabile, atribuire, expresii și tipuri

[00:00:00](https://www.youtube.com/watch?v=6ML34OuwZrc&t=0s) Această lecție construiește un program mic pornind de la stocare cu nume: creezi o variabilă, scrii în ea un număr, copiezi acel număr, calculezi o valoare nouă și alegi un tip care determină modul de stocare și de afișare.

Termenii de care vei avea nevoie sunt:

- **Celulă de memorie, adresă și variabilă:** o celulă este o locație de dimensiunea unui octet în desenul de memorie al lecției; adresa ei îi identifică poziția. O variabilă oferă codului programului un nume pentru un obiect care stochează o valoare.
- **Abstrație:** o modalitate mai simplă de a folosi ceva fără a-i gestiona detaliile interne. Numele unei variabile ascunde detaliile găsirii stocării.
- **Declarare și definiție:** o declarație introduce un nume și tipul său; declarațiile locale de aici sunt tot definiții, care creează variabilele. **Inițializarea** furnizează o valoare în momentul în care variabila este creată.
- **Valoare, citire, scriere și atribuire:** o valoare este numărul stocat în aceste exemple. Citirea îl obține; scrierea îl înlocuiește. Atribuirea, scrisă cu `=`, scrie rezultatul din dreapta într-o destinație existentă din stânga.
- **Expresie, evaluare, operator și operand:** o expresie produce o valoare când este evaluată. Un operator precum `+` efectuează o operație asupra operandelor sale, expresiile pe care le combină. Parantezele grupează o expresie.
- **Tip, alias și întreg:** un tip determină valorile permise, cerințele de stocare și comportamentul susținut. Un alias este alt nume pentru același tip. Un întreg este un număr întreg; `int` este tipul întreg folosit primul.
- **Bit, octet și lățime:** un bit reține 0 sau 1. Aici un octet conține opt biți, iar lățimea unui tip își numără biții de valoare. Întregii **cu semn** includ valori negative; întregii **fără semn** pornesc de la zero. `uint8_t` este un tip de întreg fără semn cu exact opt biți, acolo unde este disponibil.
- **Antet și compilator:** un antet furnizează declarațiile folosite de un program; `#include` face disponibil conținutul său. Compilatorul traduce codul sursă și emite diagnostice, inclusiv avertismente și erori.
- **Conversie și depășire:** conversia schimbă o valoare în alt tip. Înregistrarea numește „depășire” o conversie a unui octet în afara intervalului; aici numărul stocat este înfășurat în intervalul octetului.
- **Ieșire, cod de caracter și suprasarcină:** ieșirea trimite date către o destinație precum terminalul. `std::cout` este fluxul standard de ieșire al C++-ului, iar `<<` inserează o valoare în el. Un cod de caracter este un număr care reprezintă un caracter; ASCII este tabelul de coduri folosit în exemple. Suprasarcina oferă comportamente diferite sub același nume de operație, selectate folosind tipurile.
- **Funcție și corp:** o funcție grupează instrucțiuni; corpul ei este codul dintre acolade. Exemplele rulează în interiorul funcției de intrare numită `main`.
- **Stivă:** modelul de stocare menționat pentru aceste variabile locale; aspectul său este lăsat pentru mai târziu.

Pentru exerciții, folosește laboratorul [Variabile și tipuri](../../../en/labs/cpp/02_variables.md). Acoperă material suplimentar față de această înregistrare.

Lecția rămâne la variabile locale, valori întregi, aritmetică simplă și ieșire. Ea lasă pentru mai târziu aspectul stivei, obținerea adresei dintr-un nume, definiția completă a expresiilor, reprezentarea pe mai mulți octeți, detaliile codificării caracterelor și mecanismele suprasarcării. `int`-ul de patru octeți și octetul de opt biți descriu mediul ilustrat aici, nu orice implementare posibilă a C++-ului.

## Stocare cu nume

[00:00:09](https://www.youtube.com/watch?v=6ML34OuwZrc&t=9s) O **variabilă** este o abstracție peste stocare: folosește numele ei pentru a lucra cu valoarea sa. Problema care motivează exemplul este că programul nu ar trebui să cunoască o adresă numerică fixă precum 32. Acest număr aparține aspectului stocării; numele este ceea ce folosește codul sursă.

[00:00:14](https://www.youtube.com/watch?v=6ML34OuwZrc&t=14s) Înregistrarea menționează **stiva**, modelul de stocare folosit pentru aceste variabile locale, apoi lasă aspectul ei pentru mai târziu. Aceasta nu stabilește că fiecare variabilă din fiecare program C++ se află pe o stivă.

[00:00:17](https://www.youtube.com/watch?v=6ML34OuwZrc&t=17s) Începe declarând o variabilă. O **declarație** introduce numele și tipul ei; această declarație locală este și o **definiție**, care creează variabila:

```cpp
int i;
```

Aici `int` furnizează tipul, `i` furnizează numele, iar punct-virgula încheie declarația. Fragmentele scurte merg în interiorul lui `main`, funcția de intrare a programului; acoladele delimitează corpul său în exemplele complete. Încă nu s-a scris intenționat niciun număr util în `i`; nu o citi înainte de a-i atribui o valoare. Mostrele din această notă reconstruesc stările succesive din înregistrare. Nu a fost identificat niciun fișier sursă potrivit în commit-uri; legăturile către stările din videoclip sunt dovezile acestei construcții. [Transcrierea fixată la commit](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6/videos/cpp/05_C%2B%2B_Переменные,_присваивание,_выражения,_типы/internal/transcript.md) păstrează narațiunea, nu o copie a codului sursă.

[00:00:24](https://www.youtube.com/watch?v=6ML34OuwZrc&t=24s) Imaginează-ți memoria ca un șir de celule cu adrese consecutive: 32, 33, 34 și așa mai departe. O **celulă de memorie** este o locație de dimensiunea unui octet în acest desen; o **adresă** îi identifică poziția. Denumirea stocării permite codului să scrie `i` în loc să precizeze locația.

[00:00:33](https://www.youtube.com/watch?v=6ML34OuwZrc&t=33s) Sensul lui `int` este amânat temporar, ca ideea denumirii să poată sta în sine. [00:00:39](https://www.youtube.com/watch?v=6ML34OuwZrc&t=39s) Variabila cu nume are totuși o stocare la o adresă; numele ei este modul programului de a ajunge la ea.

[00:00:58](https://www.youtube.com/watch?v=6ML34OuwZrc&t=58s) Nu scrie 32 în cod ca să însemne „variabila mea”. [00:01:05](https://www.youtube.com/watch?v=6ML34OuwZrc&t=65s) Accesul se face prin nume; obținerea adresei sale este un subiect ulterior. [00:01:22](https://www.youtube.com/watch?v=6ML34OuwZrc&t=82s) Pentru operațiile predate aici, folosește numele declarat. Afirmația din înregistrare că acesta este „singurul mod” se limitează la această introducere și nu interzice mecanismele ulterioare ale C++-ului bazate pe adrese.

## Scrierea și copierea valorilor

[00:01:31](https://www.youtube.com/watch?v=6ML34OuwZrc&t=91s) Stocarea permite **scrierea**, care pune o valoare în ea, și **citirea**, care obține valoarea stocată. Adaugă o **atribuire** la declarația existentă:

```cpp
int i;   // creează variabila
i = 5;   // scrie 5 în ea
```

[00:01:40](https://www.youtube.com/watch?v=6ML34OuwZrc&t=100s) Păstrează separate aceste acțiuni: definiția creează `i`; atribuirea scrie în ea. Atribuirea singură nu declară o variabilă nouă. În `int i = 5;`, dimpotrivă, crearea și **inițializarea**, care furnizează prima valoare, se întâmplă împreună.

[00:01:54](https://www.youtube.com/watch?v=6ML34OuwZrc&t=114s) Pentru a muta o valoare între locații cu nume, creează mai întâi destinația. [00:02:01](https://www.youtube.com/watch?v=6ML34OuwZrc&t=121s) Extinde programul:

```cpp
int i;
i = 5;
int a;
a = i;
```

[00:02:08](https://www.youtube.com/watch?v=6ML34OuwZrc&t=128s) Partea dreaptă este o **expresie**, ceva evaluat pentru a produce o valoare. Definiția sa formală este amânată; începe cu un nume de variabilă. [00:02:13](https://www.youtube.com/watch?v=6ML34OuwZrc&t=133s) Citirea lui `i` în dreapta obține numărul stocat în acel moment.

[00:02:27](https://www.youtube.com/watch?v=6ML34OuwZrc&t=147s) O **valoare**, aici, înseamnă numărul stocat: atribuirea anterioară a pus 5 în `i`. [00:02:32](https://www.youtube.com/watch?v=6ML34OuwZrc&t=152s) Așadar `a = i;` citește 5 din `i` și scrie o copie în `a`. Ambele conțin acum 5. Se copiază valoarea, nu se stabilește o legătură permanentă între variabile.

<details>
<summary>După copiere, dacă modificăm i, se modifică automat și a?</summary>

Nu. Atribuirea a copiat deja numărul 5. Fiecare variabilă are propria valoare stocată.

</details>

## Evaluarea aritmeticii înainte de atribuire

[00:02:37](https://www.youtube.com/watch?v=6ML34OuwZrc&t=157s) Copierea este utilă, dar calculul are nevoie de operații asupra valorilor. Extinde starea anterioară adăugând cele două numere stocate și scriind rezultatul înapoi în `i`:

```cpp
// Înaintea acestei linii: i este 5 și a este 5.
i = i + a;
```

[00:02:47](https://www.youtube.com/watch?v=6ML34OuwZrc&t=167s) Semnul egal împarte atribuirea într-o destinație în stânga și o expresie în dreapta. [00:02:56](https://www.youtube.com/watch?v=6ML34OuwZrc&t=176s) **Evaluarea** calculează valoarea acelei expresii înainte ca atribuirea să memoreze rezultatul. Valoarea veche a lui `i` este încă disponibilă în timp ce partea dreaptă este evaluată.

[00:03:15](https://www.youtube.com/watch?v=6ML34OuwZrc&t=195s) Această expresie este mai complexă decât un simplu nume, deoarece include un **operator**, `+`. **Operandele** sale sunt expresiile de o parte și de alta, `i` și `a`.

[00:03:19](https://www.youtube.com/watch?v=6ML34OuwZrc&t=199s) Parantezele fac gruparea explicită:

```cpp
i = (i + a);
```

[00:03:32](https://www.youtube.com/watch?v=6ML34OuwZrc&t=212s) Urmărește fluxul valorilor:

1. Evaluează fiecare operand pentru a-i obține valoarea.
2. [00:03:51](https://www.youtube.com/watch?v=6ML34OuwZrc&t=231s) Citește numerele stocate, nu aduna numele sau adresele lor.
3. [00:04:03](https://www.youtube.com/watch?v=6ML34OuwZrc&t=243s) Înlocuiește conceptual valorile cunoscute: `i + a` devine `5 + 5`, producând 10.
4. [00:04:19](https://www.youtube.com/watch?v=6ML34OuwZrc&t=259s) Scrie 10 în destinația din stânga, `i`. Valoarea din `a` rămâne 5.

Aceasta descrie sensul calculului, nu o succesiune obligatorie de instrucțiuni pentru procesor și nici o ordine garantată de citire a celor doi operanzi. Starea finală este vizibilă și la [00:06:00](https://www.youtube.com/watch?v=6ML34OuwZrc&t=360s).

<details>
<summary>De ce poate apărea i în ambele părți fără a-și pierde prematur valoarea veche?</summary>

Partea dreaptă folosește valoarea veche pentru a calcula rezultatul. Abia apoi atribuirea înlocuiește valoarea destinației.

</details>

## Tipurile stabilesc dimensiunea stocării

[00:04:25](https://www.youtube.com/watch?v=6ML34OuwZrc&t=265s) Revino la `int`. Un **tip** determină valorile pe care o variabilă le poate reprezenta și stocarea necesară pentru ele. Aici `int` reprezintă numere întregi pe patru octeți. Un **octet** este o celulă adresabilă din desen, deci un întreg ocupă patru celule consecutive.

[00:04:33](https://www.youtube.com/watch?v=6ML34OuwZrc&t=273s) Modul în care un număr este reprezentat pe mai mulți octeți aparține unui alt videoclip; această lecție are nevoie doar de dimensiunea stocării. [00:04:38](https://www.youtube.com/watch?v=6ML34OuwZrc&t=278s) Înlocuiește schița inițială „o variabilă, o celulă” cu patru celule de dimensiunea unui octet pentru fiecare `int`.

[00:04:54](https://www.youtube.com/watch?v=6ML34OuwZrc&t=294s) Desenul plasează `i` la adresele 32 până la 35. Adresa finală 36 este **exclusivă**: este granița de după ultimul octet. [00:05:06](https://www.youtube.com/watch?v=6ML34OuwZrc&t=306s) O a doua variabilă de patru octeți, `a`, este desenată imediat după ea:

| Variabilă | Tip | Adrese incluse | Sfârșit exclusiv |
| --- | --- | --- | --- |
| `i` | `int` | 32, 33, 34, 35 | 36 |
| `a` | `int` | 36, 37, 38, 39 | 40 |

Declarațiile corespunzătoare, păstrate în [starea înregistrată la 00:06:00](https://www.youtube.com/watch?v=6ML34OuwZrc&t=360s), sunt:

```cpp
int i;
int a;
```

Aceste adrese și vecinătatea lor sunt ilustrative. Două variabile locale distincte nu sunt garantat să fie vecine. De asemenea, patru octeți reprezintă dimensiunea lui `int` în mediul înregistrat; C++ permite și alte lățimi. Vezi [cerințele pentru tipurile întregi din proiectul C++](https://eel.is/c++draft/basic.fundamental).

## Alegerea unui singur octet

[00:05:18](https://www.youtube.com/watch?v=6ML34OuwZrc&t=318s) Acum cerința care motivează exemplul se schimbă: rezervă doar un octet și memorează numere de la 0 la 255. Un `int` de patru octeți este mai mare decât este necesar.

[00:05:24](https://www.youtube.com/watch?v=6ML34OuwZrc&t=324s) **Corectare a intervalului rostit:** un întreg semnat pe 32 de biți cuprinde valori de la −2,147,483,648 la 2,147,483,647, nu aproximativ de la minus patru miliarde la plus patru miliarde. Intervalul corespunzător fără semn este de la 0 la 4,294,967,295. Acestea rezultă din [regulile de interval pentru tipurile cu și fără semn](https://eel.is/c++draft/basic.fundamental).

[00:05:53](https://www.youtube.com/watch?v=6ML34OuwZrc&t=353s) Include un **antet** pentru numere întregi, un fișier care furnizează declarațiile de tip necesare, apoi schimbă tipul înainte de `i`. [Starea înregistrată la 00:06:05](https://www.youtube.com/watch?v=6ML34OuwZrc&t=365s) arată `<stdint.h>` și `uint8_t`:

```cpp
#include <stdint.h>

int main()
{
    uint8_t i;
    i = 5;
    int a;
    a = i;
    i = (i + a);
}
```

Antetul C++ corespunzător este `<cstdint>`, care furnizează `std::uint8_t`. Tipurile de lățime exactă sunt disponibile atunci când implementarea le acceptă; vezi [specificația antetului pentru întregii din C++](https://eel.is/c++draft/cstdint.syn). Desenul este rămas de la variabilele anterioare de patru octeți; după schimbarea tipului, nu folosi vechea dimensiune a cutiei sale pentru a deduce dimensiunea lui `i`.

[00:06:07](https://www.youtube.com/watch?v=6ML34OuwZrc&t=367s) **Fără semn** înseamnă că intervalul nu are numere negative: toți cei opt biți de valoare contribuie la intervalul de la 0 la 255. Un întreg semnat pe opt biți acoperă în schimb intervalul de la −128 la 127.

[00:06:19](https://www.youtube.com/watch?v=6ML34OuwZrc&t=379s) Citește numele în bucăți: `u` înseamnă fără semn, `int` înseamnă întreg, `8` înseamnă opt biți, iar sufixul `_t` marchează un nume de tip. Un **bit** memorează 0 sau 1; opt biți formează un octet în acest mediu.

## O atribuire în afara intervalului

[00:06:33](https://www.youtube.com/watch?v=6ML34OuwZrc&t=393s) Valoarea maximă este 255. Ce se întâmplă dacă atribuirea încearcă 256? Înregistrarea numește aceasta **depășire**: numărul încercat nu încape în intervalul destinației.

[00:06:47](https://www.youtube.com/watch?v=6ML34OuwZrc&t=407s) Schimbă atribuirea anterioară și compilează. Diagnosticul vizibil la [00:06:51](https://www.youtube.com/watch?v=6ML34OuwZrc&t=411s) spune **warning**, identifică `uint8_t` drept `unsigned char` pe acest sistem și spune că conversia schimbă 256 în 0:

```cpp
uint8_t i;
i = 256;  // avertisment înregistrat: conversia schimbă 256 în 0
```

Comanda înregistrată este `g++ main.cpp`. Deși vorbitorul numește diagnosticul o eroare, această compilare anume emite un avertisment și continuă. **Conversia**, schimbarea unei valori în tipul destinației, memorează 0; nu memorează niciodată 256 în octet. Aceasta este în acord cu [regula conversiei întregi din C++](https://eel.is/c++draft/conv.integral).

<!-- Decizie privind dovezile: TP-043 numește acest lucru o eroare, însă cadrul inspectat la 411.233333 s efectiv arată vizibil „warning” și schimbă 256 în 0. Cadrul inspection-47b63a4a7a508cc94a38c298-7f1730c676387315da46243a-6b39db2a1f7ebd63.png; sha256 95eede0df8a838dac8e61d8bb80ca1acefd2db1484336c3e8539548d01678956. Diagnosticul înregistrat are prioritate față de formularea din registru. -->

## Afișarea expresiilor și a valorilor convertite

[00:07:04](https://www.youtube.com/watch?v=6ML34OuwZrc&t=424s) O variabilă poate fi folosită ca expresie și la ieșire. **Ieșirea** trimite o valoare către terminal; `std::cout << expression;` evaluează expresia și inserează rezultatul ei în fluxul standard de ieșire. [Starea de la 00:07:15](https://www.youtube.com/watch?v=6ML34OuwZrc&t=435s) schimbă temporar expresia de ieșire într-o adunare:

```cpp
// i conține deja 0 după atribuirea în afara intervalului.
std::cout << (i + 5);
```

Aceasta arată că argumentul poate fi un calcul, nu doar un nume. Starea captată este o editare în curs; terminalul ei arată în continuare rularea anterioară, deci nu stabilește un rezultat de ieșire pentru această expresie nouă.

[00:07:21](https://www.youtube.com/watch?v=6ML34OuwZrc&t=441s) Demonstrația separă apoi afișarea numerică de afișarea de caractere, convertind valoarea octetului la `int`. La [00:07:27](https://www.youtube.com/watch?v=6ML34OuwZrc&t=447s), programul vizibil este:

```cpp
#include <iostream>
#include <stdint.h>

int main()
{
    uint8_t i;
    i = 256;
    int a = i;
    std::cout << a;
}
```

Terminalul arată încă un avertisment de compilare, urmat de o rulare care afișează `0`. **Conversia** la `int` păstrează valoarea care se află deja în octet — zero. Ea schimbă modul în care acea valoare este afișată; nu poate recupera valoarea 256 pierdută.

[00:07:28](https://www.youtube.com/watch?v=6ML34OuwZrc&t=448s) Există două probleme distincte: conversia octetului a pierdut numărul încercat, în timp ce operația de ieșire folosește tipul expresiei pentru a alege o reprezentare.

[00:07:34](https://www.youtube.com/watch?v=6ML34OuwZrc&t=454s) Explicația „adaugă unu la maxim” descrie înfășurarea atunci când un rezultat este memorat înapoi în octet. O ilustrare simplificată a acelei explicații este:

```cpp
uint8_t i;
i = 255;
i = i + 1;  // memorarea rezultatului în uint8_t produce 0
int a = i;
std::cout << a; // afișează numeric 0
```

Aceasta este o mostră didactică, nu un test înregistrat suplimentar. Conversia la stocare este pasul care produce înfășurarea; calcularea unui rezultat mai larg nu înseamnă singură că acel rezultat a devenit deja zero. Vezi [regula conversiei întregi](https://eel.is/c++draft/conv.integral).

[00:07:44](https://www.youtube.com/watch?v=6ML34OuwZrc&t=464s) Corectarea este să folosești înainte de afișare o altă variabilă, mai largă. Pentru a păstra însuși numărul 256, acea destinație mai largă trebuie să primească numărul înainte de a fi restrânsă la un octet. Copierea unui octet deja înfășurat într-o variabilă mai largă păstrează doar zero.

[00:07:47](https://www.youtube.com/watch?v=6ML34OuwZrc&t=467s) **Suprasarcina** înseamnă că pentru aceeași operație există comportamente diferite, iar tipurile determină care este selectat. Mecanismul său complet este amânat. [00:07:53](https://www.youtube.com/watch?v=6ML34OuwZrc&t=473s) Pe acest sistem, ieșirea unui `int` formatează un număr; ieșirea unui `uint8_t`, aici alias (alt nume) al lui `unsigned char`, inserează un caracter. [Specificația inseratorului de caractere](https://eel.is/c++draft/ostream.inserters.character) descrie acest comportament.

<details>
<summary>De ce copierea octetului în int repară afișarea numerică, dar nu recuperează 256?</summary>

Octetul conține deja 0. Copia păstrează acea valoare într-un alt tip. Ieșirea formatează acum numărul 0 în loc să insereze caracterul cu codul 0.

</details>

<!-- Decizie privind dovezile: la 447.0 s efectiv, cadrul inspection-26bbfa0092700db2c8258f44-5c2fdc7a55da85c34b3975f9-fd488c2914170e2b.png (sha256 a84ab112ea703551feae6d8dd6196a480fea3c93f50e088675978e43956fbb28) arată int a = i, std::cout << a, avertismentul de conversie și ieșirea numerică 0. Aceasta separă corectarea afișării din TP-045 de conversia la stocare din TP-046. -->

## Codurile caracterelor

[00:08:14](https://www.youtube.com/watch?v=6ML34OuwZrc&t=494s) Un **cod de caracter** este un număr asociat unui caracter într-un tabel de coduri. În tabelul ASCII folosit pentru această explicație, codul 0 este caracterul nul și în mod normal nu are un glif vizibil; 32 este un spațiu, iar 33 este `!`. [Tabelul ASCII din RFC 20](https://www.rfc-editor.org/rfc/rfc20) confirmă aceste asocieri.

Subtitrarea confundă litera A cu exemplul spațiului. **32 nu este A**; A din ASCII este 65. Nu trata subtitrarea fuzionată ca pe un tabel de coduri corect. [Editarea inspectată de la 00:08:20](https://www.youtube.com/watch?v=6ML34OuwZrc&t=500s) arată exemplul cu codul spațiului:

```cpp
uint8_t i;
i = 32;
std::cout << i; // afișare de caracter: un spațiu pe acest sistem
```

Terminalul din acel cadru conține în continuare avertismentul anterior și rularea cu zero numeric; nu este o dovadă a unei rulări noi a exemplului cu 32. [00:08:24](https://www.youtube.com/watch?v=6ML34OuwZrc&t=504s) Detaliile codificării caracterelor și sensul mai larg al tipurilor sunt lăsate pentru mai târziu.

<!-- Decizie privind dovezile: TP-051 incorect unește A și spațiul sub codul 32. La 500.0 s efectiv, cadrul inspection-caed93988299bde9424ce766-7974fc2b132f533ac9af606d-d1574e77336e8bf8.png (sha256 21efee1cebefecee283ad120ce00656ce881508e44fc8d0acf8b3f0193f33347) confirmă i = 32 și afișarea directă a caracterului în editor, dar nu o nouă execuție și nici ce s-a spus despre A. RFC 20 stabilește asocierea factuală; eroarea exactă rostită rămâne nerezolvată. -->

## Citirea unei declarații

[00:08:27](https://www.youtube.com/watch?v=6ML34OuwZrc&t=507s) Un **tip** descrie valorile și comportamentul unei variabile; proprietatea evidențiată aici este dimensiunea stocării. El apare înaintea numelui în aceste declarații. [00:08:35](https://www.youtube.com/watch?v=6ML34OuwZrc&t=515s) Compară declarațiile din [programul înregistrat](https://www.youtube.com/watch?v=6ML34OuwZrc&t=365s):

```cpp
int a;       // patru octeți în mediul înregistrat
uint8_t i;   // un octet de opt biți în acel mediu
```

[00:08:44](https://www.youtube.com/watch?v=6ML34OuwZrc&t=524s) `int` este un **tip întreg**: reprezintă valori întregi numărice. De aceea se numește „întreg”. [00:09:00](https://www.youtube.com/watch?v=6ML34OuwZrc&t=540s) Alte tipuri nu trebuie să reprezinte deloc numere; acestea sunt în afara acestei lecții.

[00:09:05](https://www.youtube.com/watch?v=6ML34OuwZrc&t=545s) Scrierea lui `int` înaintea lui `a` selectează tipul care aici necesită patru celule de dimensiunea unui octet. Selectarea tipului fără semn de un octet pentru `i` îi dă o singură celulă și un interval mai mic. Numele identifică variabila; tipul ei determină modul în care valoarea stocată poate fi reprezentată și folosită.

<!-- Decizie privind cronologia: transcrierea inspectată la d6b06478df12bc7fb0e14a9c58ecddcbb18c92a6 plasează editarea parantezelor la 199 s, memorarea rezultatului la 259 s, introducerea lui int la 265 s, explicația tipului întreg la 524 s, amânarea tipurilor nenumerice la 540 s și recapitularea declarațiilor la 545 s. Mai multe intervale furnizate încep mai devreme sau mai târziu; legăturile din notă urmează subiectul efectiv, iar acoperirea păstrează fiecare ID furnizat. Exemplele candidate memory_example_1/example.cpp la eb8f41e0402f4552beec72bc0953b86251d16cf4 și memory_example_2/example.cpp actual predau exemple diferite cu pointeri/tablouri/structuri, deci commit-urile lor nu sunt citite ca starea main.cpp înregistrată. -->

## Istoricul modificărilor de cod

Acestea sunt stări înregistrate succesive, nu o succesiune pretinsă de commit-uri din repository; nu a fost identificat niciun fișier sursă al lecției potrivit în commit-uri.

- [00:00:17](https://www.youtube.com/watch?v=6ML34OuwZrc&t=17s) — introducerea definiției locale `int i;`.
- [00:01:31](https://www.youtube.com/watch?v=6ML34OuwZrc&t=91s) — atribuirea valorii 5 variabilei existente.
- [00:02:01](https://www.youtube.com/watch?v=6ML34OuwZrc&t=121s) — definirea lui `a` și copierea lui `i` în el.
- [00:03:19](https://www.youtube.com/watch?v=6ML34OuwZrc&t=199s) — gruparea adunării în `i = (i + a);`.
- [00:06:00](https://www.youtube.com/watch?v=6ML34OuwZrc&t=360s) — adăugarea lui `<stdint.h>`; programul întreg anterior și desenul de memorie rămân vizibile.
- [00:06:05](https://www.youtube.com/watch?v=6ML34OuwZrc&t=365s) — schimbarea lui `i` în `uint8_t`.
- [00:06:51](https://www.youtube.com/watch?v=6ML34OuwZrc&t=411s) — compilarea atribuirii cu 256; avertismentul spune că devine 0.
- [00:07:15](https://www.youtube.com/watch?v=6ML34OuwZrc&t=435s) — editarea temporară a ieșirii pentru a folosi `i + 5`; acest cadru nu stabilește niciun rezultat nou.
- [00:07:27](https://www.youtube.com/watch?v=6ML34OuwZrc&t=447s) — copierea octetului într-un `int`, afișarea lui și observarea lui 0 numeric.
- [00:08:20](https://www.youtube.com/watch?v=6ML34OuwZrc&t=500s) — editarea la `i = 32;` și afișarea directă a octetului pentru explicația codurilor de caractere.