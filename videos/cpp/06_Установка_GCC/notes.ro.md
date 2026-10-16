> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Instalarea GCC și verificarea unui program C++

[00:00:00](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=0s) Obiectivul este să instalăm același compilator C++ GCC folosit în curs, să transformăm un fișier text mic într-un program care poate fi executat și să facem compilatorul disponibil după nume într-o consolă Windows. Folosirea unui compilator și a unei versiuni aproximativ identice reduce diferențele dintre build-urile studenților; nu garantează însă că fiecare program funcționează pe fiecare mașină. Instalarea demonstrată se poate face fără parola de administrator dacă locul de instalare ales și permisiunile contului permit acest lucru.

Termenii folosiți pe parcurs sunt:

- **Compilator C++, GCC și g++:** un compilator traduce codul sursă într-un program pe care computerul îl poate rula. GCC este GNU Compiler Collection; `gcc` și `g++` sunt programe care conduc uneltele sale de compilare. `g++` oferă valori implicite potrivite pentru C++. **Linkarea** combină codul compilat cu codul de bibliotecă de care are nevoie.
- **Standardul C++ și toolchain-ul:** un standard specifică o versiune a limbajului C++ și a bibliotecii sale, cum ar fi C++17. Un toolchain este colecția de unelte folosite pentru a construi programe. Un toolchain **preconfigurat** (prebuilt) a fost deja compilat pentru tine.
- **Arhitectură:** platforma de procesor pe care uneltele descărcate trebuie să o suporte, de exemplu x86-64 pentru un PC Windows tipic pe 64 de biți.
- **MSYS2, MinGW și UCRT64:** MSYS2 furnizează unelte de dezvoltare Windows și un mediu de comandă asemănător Unix. MinGW/MinGW-w64 oferă unelte pentru construirea programelor native Windows. UCRT64 este unul dintre mediile de build selectabile din MSYS2. Aceste nume descriu lucruri conexe, dar diferite.
- **Consolă, shell, Bash, Git Bash și cmd:** o consolă este fereastra în care apar introducerea și afișarea textului; un shell interpretează comenzile introduse acolo. Bash este un shell de tip Unix, Git Bash oferă un mediu Bash împreună cu Git pentru Windows, iar `cmd` este Command Prompt din Windows. Setările lor pot diferi.
- **Pachet și manager de pachete:** un pachet grupează software pentru instalare. Un manager de pachete descarcă și instalează acele grupuri; MSYS2 folosește `pacman`, folosit de asemenea și de Arch Linux.
- **Fișier sursă, extensie, editor de text simplu și executabil:** un fișier sursă conține textul programului, de obicei cu extensia `.cpp` pentru C++. O extensie este sufixul de după ultimul punct dintr-un nume de fișier. Un editor de text simplu modifică textul fără formatare de document. Un executabil este fișierul compilat care poate fi lansat.
- **Folder curent, cale relativă, cale completă și argument de linie de comandă:** folderul curent este poziția de lucru a shell-ului. O cale relativă este interpretată pornind de acolo; o cale completă identifică o poziție pornind de la unitate sau de la rădăcina sistemului de fișiere. Argumentele sunt textul furnizat după numele programului unei comenzi.
- **Variabilă de mediu și PATH:** o variabilă de mediu este o setare cu nume, disponibilă unui program în execuție. PATH este o listă de directoare în care shell-ul caută atunci când trebuie să localizeze un program după nume. Un **proces** este un program în execuție, iar o **sesiune** aici înseamnă durata de viață a unui shell deschis.
- **set, echo și which:** `set` schimbă o variabilă de mediu cmd, `echo` afișează text, iar `which` raportează calea unui program în mediul Bash.
- **Fn-lock:** o setare a tastaturii care schimbă comportamentul anumitor taste; contează pentru scurtătura de lipire de pe tastatura demonstrată.
- **Antet, funcție și punct de intrare:** un antet oferă declarațiile necesare pentru folosirea facilităților din bibliotecă. O funcție este o unitate de cod cu nume, care poate fi apelată. `main` este punctul de intrare al acestui mic program C++: instrucțiunile sale proprii încep acolo. Un **tip de întoarcere** descrie felul rezultatului pe care îl întoarce o funcție, o **listă de parametri** descrie intrările ei, iar o **instrucțiune** este o comandă din corpul ei.
- **Obiect, flux, spațiu de nume și operator suprascărcat:** un obiect este o valoare cu un tip și operații; un flux gestionează un curent de intrare sau de ieșire. Un spațiu de nume grupează nume, iar un operator suprascărcat oferă unui simbol de operator un sens pentru anumite tipuri. `std::cout` este obiectul fluxului de ieșire standard, iar `<<` inserează date în el.
- **Literal de șir, intrare standard și get:** un literal de șir este text scris între ghilimele duble. Intrarea standard este sursa obișnuită de intrare a programului, în acest exemplu tastatura. `std::cin` este obiectul fluxului său, iar `get()` citește un caracter.
- **Fișiere ascunse și Git:** intrările ascunse sunt fișiere sau foldere pe care Explorer le poate ascunde. Git este o unealtă de control al versiunilor care înregistrează istoricul proiectului; directorul său `.git` este relevant când pregătești Explorer pentru lucrul ulterior.

Practica se află în [laboratorul de instalare a compilatorului](../../../en/labs/common/05_compiler_install.md). Această notă urmează configurarea GCC din video, nu variantele alternative de compilator pe care laboratorul le permite.

**Domeniul lecției:** instalarea compilatorului, crearea și compilarea unui program minimal, rularea lui, înțelegerea numelor de programe și a argumentelor, configurarea lui PATH și păstrarea deschisă a unui program de consolă lansat prin dublu clic. Implementarea mai adâncă a fluxurilor C++, a spațiilor de nume și a suprascărcării operatorilor este lăsată pentru mai târziu. Configurarea de build a editorului și un tratament detaliat al opțiunilor compilatorului sunt în afara acestei secvențe video. Exemplele de mai jos sunt reconstrucții scurte ale stărilor din înregistrarea legată, nu afirmații că un commit din repo conține textul lor exact.

## Alegerea și instalarea MSYS2

[00:00:15](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=15s) GCC este cunoscut din dezvoltarea pe Linux, iar înregistrarea descrie uneltele pentru Windows ca punând la dispoziție un mediu asemănător cu Linux. Mai precis, instalatorul prezentat este **MSYS2**, un mediu de dezvoltare pentru Windows; **MinGW-w64** furnizează toolchain-uri native Windows. Nu emulează un sistem de operare Linux. De asemenea, „inițial doar pentru Linux” nu este o istorie corectă: istoricul versiunilor lui GCC începe în 1987, înainte de Linux. Lecția utilă este că o distribuție pentru Windows face GCC disponibil pe Windows. Vezi [prezentarea generală MSYS2](https://www.msys2.org/) și [istoricul versiunilor GCC](https://gcc.gnu.org/releases.html).

[00:00:31](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=31s) Primul rezultat afișat în înregistrare este din 2021 și este respins ca fiind prea vechi pentru curs. Îngrijorarea privește suportul **standardului C++**: cursul folosește facilități mai noi decât C++17. Este o avertizare despre acea descărcare anume, nu o regulă că fiecare compilator lansat în 2021 suportă doar C++17.

Urmează secvența de descărcare și instalare din înregistrare:

1. [00:00:50](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=50s) Alege varianta de descărcare care oferă **toolchain-uri preconfigurate**, adică unelte deja compilate pentru instalare, în loc să descarci codul sursă și să încerci să construiești singur compilatorul. Înregistrarea parcurge ruta de descărcare MinGW-w64/SourceForge către MSYS2.
2. [00:01:00](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=60s) Poți merge direct la [MSYS2](https://www.msys2.org/). Descarcă instalatorul pentru **arhitectura** mașinii tale, adică platforma de procesor pe care o suportă.
3. [00:01:22](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=82s) Tratează aceasta ca instalarea mediului. Instalarea lui MSYS2 nu finalizează singură instalarea separată a pachetului de compilator, demonstrată în continuare.
4. [00:01:27](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=87s) Rulează instalatorul descărcat și acceptă valorile implicite demonstrate. Înregistrarea folosește locația implicită de pe unitatea C, sub `C:\msys64`. Reține folderul real de instalare, deoarece căile ulterioare depind de el.

## Instalarea pachetului de compilator

[00:01:56](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=116s) Deschide consola MSYS2 din scurtăturile instalate. Cele două metode de pornire comparate în înregistrare ajung la aceeași consolă pentru demonstrația respectivă, deci este suficientă una singură. Nu generaliza aceasta la fiecare scurtătură MSYS2: scurtăturile pentru diferite **medii de build**, precum UCRT64, selectează alte setări și alte căi de căutare. [Documentația mediilor MSYS2](https://www.msys2.org/docs/environments/) explică aceste diferențe.

[00:02:05](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=125s) Această consolă specială este necesară pentru instalarea unică a pachetului. După aceea compilatorul există ca program pe disc și poate fi apelat și dintr-o consolă Windows obișnuită, cu condiția ca fișierele sale necesare să rămână instalate și Windows să îl poată localiza.

1. [00:02:40](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=160s) Folosește `pacman`, **managerul de pachete** care îți instalează pachetele software. MSYS2 folosește aceeași unealtă de gestionare a pachetelor cunoscută utilizatorilor Arch Linux; grupul de software instalat aici este compilatorul.
2. [00:02:52](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=172s) Copiază comanda de instalare din descrierea video, în loc să o rescrii. Transcrierea vorbită nu păstrează comanda completă sau numele pachetului, deci nu este reprodusă aici ca o comandă exactă.
3. [00:02:58](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=178s) Lipește cu **Shift+Insert**. Pe tastatura demonstrată, **Fn+Esc** dezactivează mai întâi **Fn-lock**, setarea tastaturii care schimbă comportamentul tastelor, astfel încât combinația cu tasta Insert să funcționeze. Fn-lock este specific tastaturii, nu o cerință a instalării GCC.
4. Confirmă cererea de instalare cu **Y**, apoi **Enter**. Dacă cererea afișează `[Y/n]`, doar Enter acceptă răspunsul implicit „da”. Așteaptă terminarea instalării pachetului înainte de a testa compilatorul.

Compilatorul instalat în înregistrare este ulterior localizat sub `/usr/bin`. Alegerea pachetului contează: un pachet MinGW-w64 pentru UCRT64 ar folosi în schimb directorul acelui mediu. Potrivește pachetul de compilator, mediul și directorul, în loc să presupui că fiecare instalare are fișiere identice.

## Crearea unui fișier sursă C++ vizibil

[00:03:28](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=208s) Creează un folder de proiect pe desktop. Un **fișier sursă** este pur și simplu un fișier text care conține instrucțiuni C++; testul compilatorului va citi unul din acest folder.

1. [00:03:46](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=226s) Creează un fișier text nou. Explorer poate ascunde **extensiile de fișier** cunoscute, adică sufixele care disting `.txt`, `.cpp` și `.exe`, deci numele afișat poate ascunde ce fel de fișier ai creat de fapt.
2. [00:03:55](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=235s) În controalele **View > Show** din Explorer, activează **File name extensions**; pe versiunile cu setarea „Hide extensions for known file types”, dezactivează această ascundere. Acum verifică numele complet al fișierului.
3. [00:04:07](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=247s) Activează și **Hidden items**. Va fi util mai târziu, când Git, unealta de control al versiunilor, creează intrări precum directorul `.git`. Afișarea intrărilor ascunse și afișarea extensiilor sunt controale separate.
4. [00:04:22](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=262s) Redenumește fișierul astfel încât extensia sa reală să fie `.cpp`, eliminând orice `.txt` de la final. `main.cpp` este un nume convențional pentru fișierul sursă principal al unui proiect, dar fișierul folosit în comanda de compilare ulterioară este `a.cpp`. Folosește numele pe care l-ai salvat efectiv.
5. [00:04:37](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=277s) Deschide-l în Notepad, VS Code sau alt **editor de text simplu**, adică un editor care salvează text neformatat. Un fișier sursă C++ nu are nevoie de un format special de document.

<details>
<summary>Dacă Explorer afișează „main.cpp” în timp ce extensiile sunt ascunse, ai demonstrat că este un fișier sursă C++?</summary>

Nu. Numele real ar putea fi `main.cpp.txt`. Afișează extensiile de fișier și inspectează numele complet înainte de a compila.

</details>

## Apelarea compilatorului înainte de a schimba PATH

[00:04:53](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=293s) Primul test este dacă compilatorul poate fi pornit deloc. În consola de tip Bash folosită pe mașina din înregistrare, introducerea numelui compilatorului ajunge la programul instalat. Un răspuns al compilatorului despre fișiere de intrare lipsă stabilește totuși că acesta a fost găsit și pornit; nu stabilește că un fișier sursă s-a compilat cu succes.

[00:04:55](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=295s) Pe configurația demonstrată, `g++` este disponibil după nume prin **PATH-ul** consolei Bash, lista sa de directoare de căutare a programelor. Și Git Bash poate găsi un compilator atunci când propriul său PATH include directorul compilatorului; doar instalarea Git Bash nu garantează acest lucru. [00:05:05](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=305s) Într-un shell **cmd** nou, deschis pe această mașină, numele nu este recunoscut. Shell-urile diferite pot avea valori PATH diferite. [00:05:18](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=318s) Motivul și soluția permanentă sunt amânate intenționat până după prima compilare.

[00:05:21](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=321s) Localizează programele instalate. Înregistrarea găsește `gcc` și `g++` sub `/usr/bin` al MSYS2, adică `C:\msys64\usr\bin` pentru rădăcina de instalare demonstrată. Aici `usr` este un nume de director din interiorul MSYS2, nu directorul profilului de utilizator din Windows. Nu este o locație universală a compilatorului MinGW.

[00:05:45](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=345s) Folosește **g++**, driverul GCC cu valori implicite pentru C++. Și `gcc` poate compila cod C++, dar `g++` aranjează în plus, în mod implicit, **linkarea** către biblioteca C++, adică combinarea codului compilat cu codul de bibliotecă de care are nevoie. De aceea este alegerea comodă pentru programul construit. Vezi [explicația GCC despre apelarea lui g++](https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html).

[00:05:51](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=351s) Când un program nu este disponibil după nume, apelează-i **calea completă**, adică locația sa completă, inclusiv numele executabilului. [00:06:04](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=364s) Adaugă argumentul `--help` pentru a cere ajutorul compilatorului de pe linia de comandă. Acest exemplu cmd reconstruit folosește directorul afișat în înregistrare; înlocuiește-l cu calea ta reală:

~~~bat
"C:\msys64\usr\bin\g++.exe" --help
~~~

[00:06:12](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=372s) Pentru o simplă apelare a unui program extern, shell-ul citește primul element al comenzii ca nume sau cale de program. Restul furnizează **argumente de linie de comandă**, adică textul transmis acelui program. Ghilimelele păstrează ca un singur element o cale care conține spații; un argument precum `--help` cere compilatorului să îndeplinească o anumită acțiune.

[00:06:16](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=376s) Faptul că programul devine disponibil după nume este încă un pas amânat în acest moment. [00:06:26](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=386s) Modelul util este „program, apoi argumente”: shell-ul pornește programul, iar programul își interpretează șirurile de argumente. Nu compilează C++ doar pentru că shell-ul a primit un nume de fișier sursă. Ghilimelele și expansiunea din shell sunt detalii care depășesc acest model introductiv.

## Scrierea primului program Hello World

[00:06:37](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=397s) Începe cu un program mic care afișează un mesaj ușor de recunoscut. Următoarea este o reconstrucție simplificată a acestei stări din înregistrare:

~~~cpp
#include <iostream>

int main() {
    std::cout << "Hello World";
}
~~~

Citește noua sintaxă în ordinea construirii:

1. [00:06:45](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=405s) `#include <iostream>` face disponibile declarațiile din **antetul iostream**. Un antet furnizează declarații pentru facilitățile bibliotecii; acesta ne oferă fluxurile standard de intrare și ieșire. Fără o declarație potrivită, această utilizare a lui `std::cout` nu se va compila. Există și alte facilități de ieșire, dar acest exemplu folosește iostream.
2. [00:06:54](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=414s) `int main()` definește **funcția main** a programului, punctul de intrare pentru instrucțiunile sale proprii. `int` este tipul său de întoarcere întreg, `()` este lista de parametri, iar acoladele conțin corpul funcției. Ajungerea la sfârșitul lui `main` este permisă aici și implică o valoare de întoarcere de zero, adică succes.
3. [00:07:01](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=421s) `std::cout <<` folosește un **operator suprascărcat**: deși `<<` este și simbolul deplasării la stânga, sensul său cu acest flux de ieșire este inserarea. Prefixul `std::` îl selectează pe `cout` din **spațiul de nume** al bibliotecii standard, o grupare de nume.
4. [00:07:07](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=427s) Expresia scurtă de afișare se bazează pe abstracții: un **obiect** disponibil global, numit `cout`, un spațiu de nume și un operator suprascărcat. Aceste idei explică de ce o operație simplă de ieșire poate părea inițial complicată. Este posibilă o ieșire la nivel mai jos, dar aceasta necesită detalii pe care această lecție nu le dezvoltă.
5. [00:07:24](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=444s) Gândește-te la `cout` ca la locul în care scrii informații pentru consolă. Mai precis, `std::cout` este **obiectul fluxului de ieșire standard**, care gestionează datele de ieșire; în acest exemplu el reprezintă ieșirea către consolă, fără a fi chiar fereastra consolei. [00:07:29](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=449s) Scrierea în acel flux trimite informația către destinația sa de ieșire.
6. [00:07:38](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=458s) Operatorul de inserare `<<` trimite valoarea din dreapta sa în fluxul din stânga sa. [00:07:48](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=468s) `"Hello World"` este un **literal de șir**, adică text între ghilimele duble. Caracterele mesajului sunt afișate; ghilimelele delimitează literalul și nu sunt afișate. Punctul și virgula încheie instrucțiunea.

Lecția folosește această sintaxă pentru a testa instalarea. O explicație completă a implementării obiectelor, a spațiilor de nume și a suprascărcării operatorilor aparține lecțiilor viitoare.

## Transformarea textului sursă într-un executabil

[00:07:54](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=474s) Salvarea textului sursă nu este același lucru cu rularea unui program. Acesta trebuie mai întâi **compilat**, adică tradus într-o formă care poate fi rulată. Etapele conceptuale pentru sursa Hello World tocmai scrisă sunt:

1. Salvează textul `.cpp`.
2. [00:08:02](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=482s) Rulează compilatorul pentru a produce un **executabil**, fișierul rezultat pe care Windows îl poate lansa.
3. [00:08:06](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=486s) Pornește executabilul, fie prin dublu clic, fie introducând numele sau calea lui într-o consolă.

Editarea sursei schimbă intrarea compilării. Nu schimbă automat un executabil aflat deja pe disc.

## Compilare și rulare din folderul de proiect

[00:08:13](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=493s) Mai întâi mută shell-ul cmd în folderul care conține sursa. Acesta este **folderul curent**, poziția din care shell-ul interpretează căile relative ale fișierelor.

Urmează prima secvență de compilare:

1. [00:08:19](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=499s) Furnizează calea completă a compilatorului și dă-i numele fișierului sursă ca intrare.
2. [00:08:31](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=511s) Pentru a obține calea compilatorului, trage executabilul său din Explorer în consolă sau folosește **Shift+right-click > Copy as path** și lipește rezultatul.
3. [00:08:44](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=524s) Adaugă numele fișierului sursă relativ la folderul curent. O **cale relativă** este interpretată din acel folder, deci `a.cpp` înseamnă fișierul din folderul de proiect, nu pe cel din folderul compilatorului.
4. [00:08:54](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=534s) Execută comanda. Iată o reconstrucție folosind calea și numele de fișier discutate în înregistrare:

~~~bat
"C:\msys64\usr\bin\g++.exe" a.cpp
~~~

Dacă sursa ta se numește `main.cpp`, înlocuiește `a.cpp` cu acel nume. Calea executabilului identifică unealta de rulat; calea sursei identifică intrarea sa. Nu trebuie să fie în același director.

[00:09:07](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=547s) Înaintea compilării repetate, înregistrarea cere o comandă pregătitoare în consolă și amână explicarea scopului ei. Aceasta este configurarea temporară a lui PATH dezvoltată în secțiile următoare: păstreaz-o în aceeași consolă deschisă cât timp urmezi demonstrația, apoi repetă compilarea.

[00:09:13](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=553s) Compilarea produce un **fișier executabil**, un fișier care poate fi acum pornit ca program. [00:09:24](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=564s) Pentru aceste comenzi simple, primul element numește programul pornit. Pentru a rula programul generat din folderul lui în cmd, folosește numele executabilului. [00:09:37](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=577s) Rezultatul observat este exact mesajul **Hello World**, ceea ce confirmă atât compilarea, cât și execuția. O interacțiune reconstruită scurt este:

~~~bat
a.exe
~~~

~~~text
Hello World
~~~

[00:09:45](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=585s) Poți porni executabilul și din alt folder, specificându-i calea completă, exact cum ai făcut cu compilatorul. Exemplul următor ilustrează aceeași acțiune cu o locație de proiect fictivă; înlocuiește contul și folderul cu ale tale:

~~~bat
"C:\Users\YourName\Desktop\cpp\a.exe"
~~~

<details>
<summary>Dacă introduci comanda de compilare din alt folder, a.cpp se referă în continuare la aceeași sursă?</summary>

Nu. Acel nume relativ este interpretat din noul folder curent. Revino în folderul de proiect sau dă calea completă a sursei. Faptul că dai calea completă pentru compilator nu schimbă modul în care este rezolvat argumentul sursă.

</details>

## Încercarea unei modificări temporare a lui PATH

[00:09:56](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=596s) Scrierea căii complete a compilatorului de fiecare dată este inconvenientă. Ca să îl chemi pur și simplu `g++`, adaugă directorul care îl conține în **PATH**, lista de directoare a shell-ului folosită pentru găsirea programelor.

Comanda cmd temporară discutată aici pune directorul compilatorului înaintea listei existente. Aceasta este o reconstrucție pentru instalarea din înregistrare; folosește propriul tău director de compilator:

~~~bat
set "PATH=C:\msys64\usr\bin;%PATH%"
g++ a.cpp
~~~

[00:09:56](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=596s) `set` schimbă o **variabilă de mediu** cu nume, o setare păstrată de procesul cmd în execuție. `%PATH%` se extinde la valoarea anterioară a lui PATH; punctul și virgula separă directoare. Păstrarea valorii anterioare păstrează celelalte locații de căutare a programelor. Astfel, numele compilatorului devine imediat disponibil în consola deschisă. Forma cu ghilimele `set "NAME=value"` păstrează atribuirea laolaltă fără a pune ghilimelele în valoare. Vezi [documentația Microsoft pentru set](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1).

[00:10:12](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=612s) Aceasta este o modificare **doar pentru sesiunea curentă**: ține cât durează acest shell deschis. Nu salvează o nouă setare a contului Windows.

[00:10:19](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=619s) Înregistrarea demonstrează această limită:

1. Închide consola.
2. Deschide din nou cmd.
3. Revino în folderul de proiect.
4. Încearcă din nou numele compilatorului.

Noua consolă nu mai recunoaște `g++` pentru că intrarea temporară din PATH aparținea procesului închis. Compilatorul nu a fost dezinstalat. Doar setarea de căutare a acelei console a dispărut.

## Înțelegerea modului în care PATH găsește compilatorul

[00:10:45](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=645s) **PATH** este o variabilă de mediu care conține o listă de căi de directoare. [00:11:07](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=667s) Când dai unui program un nume în locul unei căi complete, shell-ul folosește această listă pentru a găsi un executabil cu acel nume. Pentru comenzile externe din cmd, directorul curent este verificat înaintea directoarelor din PATH; în interiorul lui PATH contează ordinea directoarelor. Vezi [documentația Microsoft despre căutarea în PATH](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/path).

[00:11:34](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=694s) Afișează valoarea curentă cu `echo %PATH%`. Aici `echo` afișează text, iar `%PATH%` se extinde la valoarea variabilei. Înregistrarea arată o listă lungă de intrări furnizate deja de Windows și de software-ul instalat:

~~~bat
echo %PATH%
~~~

[00:11:53](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=713s) Includerea folderului compilatorului în această listă este ceea ce îi face numele utilizabil. Comanda anterioară l-a pus la început; această demonstrație adaugă un director la final, folosind punct și virgulă. Ambele adaugă o locație de căutare, dar pozițiile diferă. Acest exemplu reconstruit păstrează lista existentă:

~~~bat
set "PATH=%PATH%;C:\msys64\usr\bin"
echo %PATH%
~~~

[00:12:08](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=728s) A doua afișare arată folderul nou adăugat la final. Acesta este rezultatul testului pentru schimbarea variabilei în sine.

[00:12:17](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=737s) Urmează acum căutarea după nume descrisă în video:

1. Introdu numele compilatorului.
2. Shell-ul verifică în ordine locațiile de căutare. În PATH-ul demonstrat, intrări anterioare precum System32 nu conțin un `g++` care să corespundă.
3. Căutarea ajunge la directorul adăugat al compilatorului și găsește executabilul.
4. [00:12:41](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=761s) Shell-ul rezolvă numele scurt la calea completă a acelui executabil și îl pornește.
5. [00:12:50](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=770s) Este același program compilator pornit anterior printr-o cale completă. [00:12:52](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=772s) Apoi compilatorul, nu shell-ul, traduce sursa furnizată ca argument.

PATH este o listă de **directoare**, nu o listă de nume de executabile sau de fișiere sursă. Dacă în căutare este găsit mai devreme un alt compilator care corespunde, acel program poate fi ales în schimb.

<details>
<summary>Adăugarea directorului compilatorului în PATH îi spune și lui g++ unde se află a.cpp?</summary>

Nu. PATH îl ajută pe shell să localizeze programul compilator. Argumentul relativ pentru sursă, `a.cpp`, este în continuare rezolvat din folderul curent. Sunt două căutări separate.

</details>

## Salvarea directorului compilatorului în PATH

[00:13:01](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=781s) Ca să nu repeți comanda temporară în fiecare consolă nouă, salvează directorul compilatorului în setările de variabile de mediu ale Windows. O **variabilă de mediu** salvată este o setare cu nume din care procesele ulterioare își pot primi valorile inițiale.

1. Deschide **Control Panel > System > Advanced system settings > Environment Variables** sau caută în Start **Edit environment variables for your account**.
2. [00:13:39](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=819s) Alege domeniul potrivit. **Variabilele de utilizator** se aplică contului tău; editarea lor este potrivită când nu ai acces de administrator. **Variabilele de sistem** se aplică tuturor conturilor și pot necesita credențiale de administrator.
3. [00:14:00](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=840s) Selectează variabila **Path** existentă, apasă **Edit**, apoi **New** pentru a adăuga o intrare de director.
4. [00:14:12](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=852s) Determină directorul real care conține compilatorul tău. Acesta depinde de locația instalării și de pachetul/mediul selectat; nu copia o cale doar pentru că altă mașină a folosit-o.
5. [00:14:29](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=869s) Instalarea pe 64 de biți din această înregistrare are compilatorul tot sub `usr\bin`. Aici `usr` aparține arborelui de instalare MSYS2; nu este un folder din `C:\Users` din Windows. Arhitectura singură nu determină directorul compilatorului.
6. [00:14:59](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=899s) Caută compilatorul în **directorul bin** al toolchain-ului instalat relevant, adică directorul care conține uneltele sale executabile. [00:15:07](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=907s) Într-o consolă Bash care găsește deja compilatorul, folosește `which`, o comandă care raportează executabilul ales de calea de căutare a shell-ului:

~~~bash
which g++
~~~

Pentru instalarea din înregistrare, calea raportată este sub `/usr/bin`. Cu o rădăcină de instalare `C:\msys64`, directorul care o conține este `C:\msys64\usr\bin`. Un alt pachet poate raporta în schimb un director precum `/ucrt64/bin`. Traduce calea MSYS2 în locația sa Windows efectivă; cele două notații de cale nu sunt interschimbabile în dialogul de setări din Windows. Vezi [documentația MSYS2 despre căi](https://www.msys2.org/docs/filesystem-paths/).

7. [00:15:23](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=923s) Lipește în noua intrare din PATH **directorul care conține executabilul**, nu numele executabilului. Folosește **Ctrl+V**, apoi confirmă cu **OK**.
8. [00:15:33](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=933s) Dacă lista ta de variabile de utilizator nu are o variabilă Path, creează o variabilă numită **Path** cu acel director ca valoare. Dacă Path există deja, adaugă o intrare în ea; nu înlocui valoarea existentă și nu crea o a doua variabilă inutilă.
9. [00:15:45](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=945s) Închide și redeschide consola după salvare. Un **proces** este un program în execuție; procesele deja pornite își păstrează propriile valori de mediu, deci noul shell trebuie să moștenească setarea actualizată de la un proces părinte reîmprospătat. Dacă moștenește totuși o valoare veche, repornește aplicația terminal sau deloghează-te și loghează-te din nou. Înregistrarea cere o reîncărcare/repornire înainte de a deschide din nou cmd. Vezi [explicația Microsoft despre moștenirea mediului](https://learn.microsoft.com/en-us/windows/win32/procthread/environment-variables).

Modificarea permanentă salvează o valoare de pornire pentru sesiunile viitoare; nu rescrie retroactiv mediul unei console deja deschise.

## Verificarea compilării într-o consolă nouă

[00:16:06](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=966s) Deschide o consolă cmd nouă, intră în folderul sursei și compilează după nume. Această comandă reconstruită este forma mai simplă la care se ajunge în înregistrare:

~~~bat
g++ a.cpp
~~~

Calea completă a compilatorului nu mai este necesară pentru că această consolă nouă a moștenit intrarea salvată în PATH. Numele relativ al sursei depinde în continuare de faptul că te afli în folderul de proiect. O compilare reușită verifică faptul că configurarea permanentă este utilizabilă, nu doar că un dialog a acceptat directorul.

## Păstrarea ferestrei de ieșire deschise

[00:16:25](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=985s) Pornirea executabilului prin dublu clic deschide o consolă pentru el, afișează mesajul și închide fereastra imediat ce programul se termină. O scurtă apariție a ferestrei nu înseamnă că compilarea a eșuat. Rularea lui dintr-o consolă deja deschisă este o modalitate de a citi ieșirea.

[00:16:42](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=1002s) Pentru fluxul de lucru cu dublu clic demonstrat, adaugă o operație de citire după instrucțiunea de ieșire. **std::cin** este obiectul fluxului de intrare standard, care primește în mod normal intrarea de la tastatură în acest exemplu. Operația sa **get()** citește un caracter. Dacă nu există niciun caracter în așteptare, ea așteaptă intrarea, deci programul nu s-a terminat încă.

Starea finală simplificată din înregistrare este:

~~~cpp
#include <iostream>

int main() {
    std::cout << "Hello World";
    std::cin.get();
}
~~~

Parantezele apelează funcția `get` pe `std::cin`; punctul selectează operația acelui obiect. Același antet `<iostream>` furnizează declarațiile fluxului standard de intrare. Această așteptare este utilă pentru testul minimal, dar nu este o funcție generală de gestionare a ferestrelor: dacă intrarea este deja disponibilă sau închisă, s-ar putea să nu aștepte.

[00:17:15](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=1035s) Completează testul final:

1. Salvează sursa modificată.
2. Compilează din nou cu comanda din secțiunea precedentă; editarea textului nu actualizează executabilul.
3. Dublu clic pe executabilul reconstruit.
4. Observă **Hello World** și o fereastră care rămâne deschisă.
5. Apasă **Enter**. Intrarea sa îi permite lui `get()` să se termine; programul ajunge la final și fereastra se închide.

Acest rezultat observat confirmă că programul recompilat include operația de citire adăugată.

## Istoricul modificărilor de cod

Stările relevante sunt păstrate în înregistrarea legată; nu a fost identificat niciun commit din repo care să corespundă exact acestor exemple. Lecția de instalare din repo-ul consultat descrie un alt flux de lucru cu compilatorul, deci commit-urile sale nu sunt folosite ca dovezi pentru instalarea GCC din video.

- [00:06:04](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=364s) — Compilatorul este apelat prin cale completă, cu un argument de ajutor.
- [00:06:37](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=397s) — Prima sursă include iostream și afișează Hello World din main.
- [00:08:54](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=534s) — Calea completă a compilatorului primește numele relativ al fișierului sursă pentru compilare.
- [00:09:37](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=577s) — Executabilul rezultat afișează Hello World.
- [00:09:56](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=596s) — O intrare temporară în PATH permite compilarea după numele scurt al compilatorului.
- [00:16:06](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=966s) — O consolă nouă compilează după nume după modificarea permanentă a lui PATH.
- [00:16:42](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=1002s) — Sursa adaugă o așteptare de intrare după ieșire.
- [00:17:15](https://www.youtube.com/watch?v=bQnbkV6xgY4&t=1035s) — Reconstruirea și dublu clic confirmă că fereastra rămâne deschisă până la Enter.