> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Configurarea lui G++ în VS Code

[00:00:01](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=1s) Această lecție conectează un compilator C++ deja instalat la VS Code, astfel încât să poți construi fișierul sursă curent, să rulezi executabilul rezultat și să te oprești la o linie pentru a inspecta execuția. Pleacă de la un program existent, nu de la scrierea unuia nou. Relația centrală este: **F5 alege o configurație de pornire; această configurație cere o sarcină de compilare; sarcina produce executabilul pe care debuggerul îl pornește.**

Termenii pe care îi vei întâlni sunt:

- **Fișier sursă, compilator și executabil:** un fișier sursă conține textul programului; un compilator îl traduce într-un executabil rulabil, numit și binar. **GCC** este colecția de compilatoare GNU; **G++**, invocat ca `g++`, este comanda de compilare C++ a acesteia.
- **Terminal, comandă, argument și flag:** terminalul îți permite să introduci comenzi. O comandă numește un program de rulat; argumentele îi furnizează intrările și opțiunile. Un flag este o opțiune precum `-o`, care specifică un fișier de ieșire.
- **GDB, breakpoint și pas cu pas:** GDB este debuggerul GNU, care controlează execuția. Un breakpoint oprește execuția înainte de a rula o linie marcată. Pasul cu pas rulează linia următoare; **F10** realizează pasul folosit aici.
- **MSYS2, MinGW64 și pacman:** MSYS2 furnizează medii de dezvoltare și unelte pe Windows; MinGW64 este unul dintre mediile sale de compilare pentru Windows. `pacman` este managerul său de pachete, folosit pentru a instala software. `which` localizează executabilul unei comenzi.
- **PATH:** o variabilă de mediu care conține directoarele în care se caută atunci când o comandă este introdusă după nume.
- **Git, repository și clone:** Git gestionează fișierele versionate. Un repository conține aceste fișiere și istoricul lor; clonarea face o copie locală a repository-ului.
- **VS Code, extensie și workspace:** VS Code este editorul; o extensie adaugă funcționalități precum suportul C++. Un workspace este folderul de proiect deschis în editor. **Command Palette** este meniul său de comenzi căutabil.
- **Sarcină și configurație de pornire:** o sarcină descrie o acțiune precum compilarea. O configurație de pornire descrie ce executabil se pornește și cum se depanează. `preLaunchTask` leagă o configurație de pornire de o sarcină după eticheta acesteia.
- **JSON și variabile de configurare:** JSON exprimă setările ca valori cu nume, obiecte între acolade și liste între paranteze drepte. **JSONC** este JSON cu comentarii. O variabilă VS Code precum `${fileDirname}` este înlocuită cu o valoare din fișierul activ momentan.
- **Nume de bază al fișierului, extensie, cale relativă și director curent de lucru:** numele de bază este numele fișierului; extensia sa este sufixul precum `.cpp`. O cale relativă este interpretată din directorul curent de lucru, folderul în care rulează o comandă.
- **Standard C++, toolchain, IntelliSense și MSVC:** un standard definește o versiune a limbajului C++. Un toolchain este compilatorul împreună cu uneltele aferente. IntelliSense este analiza de cod și completarea oferite de extensia C++. MSVC este compilatorul C++ al Microsoft, asociat cu Visual Studio. Un **header** este un fișier cu declarații pe care fișierele sursă le pot include, precum interfața unei biblioteci.

Pentru lucrarea practică asociată, vezi [laboratorul de instalare a compilatorului](../../../en/labs/common/05_compiler_install.md). Lecția presupune că compilatorul și extensia C++ sunt instalate. Ea acoperă un singur fișier sursă activ și relația dintre construire și pornire. Operaționile detaliate ale debuggerului și câmpurile de configurare mai puțin importante sunt amânate.

## Verifică compilatorul și debuggerul

[00:00:01](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=1s) Mai întâi verifică dacă terminalul poate găsi compilatorul după numele executabilului său. G++ este comanda de compilare C++: introdusă fără niciun fișier sursă, pornește compilatorul, dar nu îi oferă nimic de compilat. Verificarea înregistrată este:

```console
g++
g++: fatal error: no input files
```

Diagnosticul de intrare lipsă este rezultatul util: comanda a fost găsită și executată. Un mesaj care ar spune că însăși comanda nu poate fi găsită ar indica o problemă de instalare sau de PATH. Aceasta verifică accesibilitatea; nu testează încă compilarea unui program.

[00:00:19](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=19s) Și GDB trebuie să fie instalat. Debuggerul este unealta care pornește executabilul și îl oprește pentru inspecție, așa că instalarea doar a lui G++ lasă incompletă partea de depanare a acestei configurații.

[00:00:29](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=29s) În configurația MinGW64 instalează debuggerul prin `pacman`, managerul de pachete, apoi localizează-l cu `which`. Înregistrarea predă această procedură de instalare-urmată-de-localizare; ce urmează este un exemplu concret pentru MinGW64, cu numele pachetului verificat față de [fișa pachetului MSYS2 GDB](https://packages.msys2.org/packages/mingw-w64-x86_64-gdb), nu o pretenție de a reproduce comanda din înregistrare caracter cu caracter:

```sh
pacman -S mingw-w64-x86_64-gdb
which gdb
```

1. Rulează comanda de instalare în mediul MSYS2 corespunzător.
2. Rulează `which gdb` ca să vezi unde este localizat debuggerul instalat.
3. [00:00:54](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=54s) Adaugă directorul care conține acel executabil în PATH-ul Windows, exact cum ai procedat pentru GCC. PATH este lista de directoare folosite pentru a rezolva comenzi precum `g++` și `gdb`.

Calea afișată în shell-ul MSYS2 este relativă la structura instalării MSYS2. Folosește directorul Windows corespunzător atunci când editezi PATH-ul Windows. Și procesele de construire și depanare ale editorului trebuie să găsească aceste unelte; faptul că GDB este găsit într-un singur shell nu dovedește că fiecare proces îl poate găsi.

## Copiază configurația cursului

[00:01:07](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=67s) Configurația de proiect pregătită se află în folderul `.vscode` din repository-ul cursului. Copiază folderul întreg în proiectul tău propriu pentru a moșteni sarcinile și setările de pornire. [Folderul de configurare aferent, commitat](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/tree/c484907b6e6ac331c6ab4fe508ca432f6f2585d5/.vscode) ilustrează structura:

```text
your-project/
    .vscode/
        launch.json
        tasks.json
        c_cpp_properties.json
        settings.json
    a.cpp
```

Fișierul sursă există deja în această etapă. Copierea configurației furnizează instrucțiunile pentru construirea și pornirea lui; nu instalează compilatorul sau debuggerul.

[00:01:35](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=95s) Un clone este o copie locală a unui repository Git. Demonstrația pornește dintr-un folder de test gol și clonează cursul. Astfel se obține întregul repository, inclusiv temele și fișierele de configurare, într-un singur folder de curs. O comandă ilustrativă este:

```sh
git clone https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms.git
```

[00:01:47](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=107s) Pentru a folosi rezultatul:

1. Deschide folderul cursului clonat și găsește `.vscode`.
2. Copiază acel folder întreg.
3. Lipește-l în folderul de proiect care conține fișierul tău sursă.
4. Deschide acel folder de proiect în VS Code, cu extensia C++ instalată, și fă fișierul sursă activ.

Configurația poate fi refolosită în altă locație de proiect, pentru că se referă la fișierul activ prin variabile. „Lipește-l oriunde” înseamnă în proiectul pe care vrei să-l configurezi; folderul `.vscode` trebuie să fie în rădăcina proiectului deschis.

## Construiește, rulează și oprește-te la un breakpoint

[00:02:16](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=136s) Cu compilatorul, debuggerul, extensia și configurația copiată disponibile, apăsarea tastei **F5** poate compila și porni programul activ.

[00:02:36](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=156s) Prima selecție implicită din demonstrație nu este potrivită. Alege explicit intrarea GDB din meniul de configurări Run and Debug, apoi pornește-o. Deși este descrisă vag ca alegere a unei „sarcini”, opțiunea F5 este o **configurație de pornire**, care la rândul ei apelează o sarcină de construire. [Intrarea GDB aferentă, commitată](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/c484907b6e6ac331c6ab4fe508ca432f6f2585d5/.vscode/launch.json) are această relație simplificată:

```json
{
    "name": "(gdb) Launch",
    "preLaunchTask": "gcc_cpp_current_file"
}
```

Aici numele identifică opțiunea de pornire; eticheta sarcinii identifică acțiunea de compilare, care este separată.

[00:02:46](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=166s) Cu alegerea GDB selectată, testul înregistrat compilează programul, îl pornește și afișează răspunsul său. Aceasta este verificarea completă, de la un capăt la altul, nu doar găsirea uneltelor.

[00:02:53](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=173s) Un **breakpoint** marchează o linie la care depanarea trebuie să se oprească:

1. Marchează o linie cu un breakpoint.
2. Pornește sub GDB. Execuția se oprește la acea linie înainte de a o rula.
3. [00:03:03](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=183s) Apasă **F10**. Acest pas rulează linia marcată și trece la următoarea.

**Predicție:** Când debuggerul evidențiază linia cu breakpoint, a fost deja rulată acea linie?

<details>
<summary>Răspuns</summary>
<p>Nu. În această demonstrație linia evidențiată este următoarea linie care urmează să fie rulată. Ea rulează când apeși F10.</p>
</details>

[00:03:08](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=188s) O explicație mai detaliată a debuggerului este lăsată pentru o lecție ulterioară. Aici, breakpointul și pasul demonstrează că configurația funcționează.

## Urmează configurația de pornire

[00:03:10](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=190s) Urmează acum ce face de fapt F5. O **configurație de pornire** este un set cu nume de instrucțiuni pentru pornirea unui program; F5 folosește configurația selectată, iar tu poți alege alta din lista disponibilă.

[00:03:34](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=214s) Aceste intrări sunt declarate în `.vscode/launch.json`. JSON grupează setările cu nume în obiecte și grupează obiectele de configurare într-o listă. [00:03:46](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=226s) Intrarea GDB Launch examinată în înregistrare este a treia în acea listă. O [versiune anterioară a fișierului de pornire](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/c484907b6e6ac331c6ab4fe508ca432f6f2585d5/.vscode/launch.json) commitată are tot GDB pe poziția a treia; câmpurile sale esențiale sunt:

```json
{
    "name": "(gdb) Launch",
    "program": "${fileDirname}/${fileBasenameNoExtension}.exe",
    "cwd": "${fileDirname}",
    "preLaunchTask": "gcc_cpp_current_file"
}
```

Acesta este un fragment scurtat, nu o configurație completă de înlocuire.

[00:03:56](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=236s) Rolul principal al intrării de pornire este să execute programul de la calea `program`. [00:04:13](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=253s) Sintaxa cu semn de dolar și acolade desemnează o **variabilă de configurare**, un substituent expandat de VS Code:

| Variabilă | Semnificație cu un fișier activ la `D:/project/a.cpp` |
| --- | --- |
| `${fileDirname}` | Folderul fișierului activ: `D:/project` |
| `${fileBasenameNoExtension}` | Numele său fără extensie: `a` |
| Valoarea combinată pentru `program` | `D:/project/a.exe` |

Extensia `.cpp` aparține sursei; sufixul `.exe` identifică executabilul Windows. Semnul de dolar singur nu înseamnă „folder”: numele variabilei în sine decide ce valoare este înlocuită. Aceste semnificații coincid cu [referința pentru variabilele VS Code](https://code.visualstudio.com/docs/reference/variables-reference).

[00:04:43](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=283s) Câmpurile rămase configurează debuggerul și provin în mare parte din șablonul generat de acesta. Înțelegerea lor completă depășește scopul lecției. Următorul câmp relevant aici este legătura cu compilarea.

## Elimină pasul de construire și observă eșecul

[00:05:00](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=300s) O **sarcină** este o acțiune definită pentru ca editorul să o execute. În această configurație, `preLaunchTask` numește acțiunea de compilare care trebuie să se termine înainte ca debuggerul să pornească programul. Valoarea sa trebuie să coincidă cu eticheta sarcinii.

[Fișierul de pornire aferent, commitat](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/c484907b6e6ac331c6ab4fe508ca432f6f2585d5/.vscode/launch.json) conține legătura cu construirea. Exemplele scurtate de mai jos arată starea inițială și modificarea temporară din video; starea modificată este evidențiată de timestamp, nu se pretinde că există în acel commit.

```json
{
    "program": "${fileDirname}/${fileBasenameNoExtension}.exe",
    "preLaunchTask": "gcc_cpp_current_file"
}
```

[00:05:16](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=316s) Elimină linia cu `preLaunchTask` și salvează. Intrarea de pornire intermediară cere acum doar rularea binarului existent:

```json
{
    "program": "${fileDirname}/${fileBasenameNoExtension}.exe"
}
```

1. [00:05:19](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=319s) Șterge executabilul deja construit.
2. [00:05:23](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=323s) Apasă F5.
3. Observă eroarea înregistrată: executabilul nu există.

[00:05:28](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=328s) **Executabilul**, sau binarul, este rezultatul rulabil al compilării. Fișierul sursă există în continuare, dar eliminarea pasului de construire înseamnă că F5 nu mai are nicio instrucțiune să recreeze binarul. Pornirea și compilarea sunt acțiuni separate.

**Predicție:** Dacă ai eliminat pasul de construire, dar ai lăsat în loc un executabil mai vechi, ar dovedi o pornire reușită că sursa ta cea mai recentă a fost compilată?

<details>
<summary>Răspuns</summary>
<p>Nu. Pornirea ar fi putut rula executabilul mai vechi. Ștergerea din demonstrație face vizibilă lipsa pasului de compilare. Pentru fluxul intenționat de construire-urmată-de-rulare, păstrează sarcina de compilare legată prin preLaunchTask.</p>
</details>

## Găsește sarcina de compilare

[00:05:39](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=339s) Programul este construit de sarcina „G++ compile current file”. În versiunea repository-ului inspectată, eticheta sa reală este `gcc_cpp_current_file`. [00:05:59](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=359s) Este o sarcină definită de configurația cursului, nu o valoare implicită inerentă. Definiția ei este o intrare în lista de sarcini din `.vscode/tasks.json`.

[Fișierul de sarcini aferent, commitat](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/fef337c86c73ec8d197461ffe9327d69612ab81e/.vscode/tasks.json) dă structura relevantă. Acest fragment păstrează elementele esențiale ale comenzii și directorul curent de lucru, omite alte flag-uri și detalii administrative ale sarcinii:

```json
{
    "label": "gcc_cpp_current_file",
    "command": "g++",
    "args": ["${file}", "-o", "${fileBasenameNoExtension}.exe"],
    "options": {
        "cwd": "${fileDirname}"
    }
}
```

[00:06:14](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=374s) **Comanda** este programul care trebuie executat: G++. **Argumentele** sale sunt valorile transmise acelui program, aici aranjate într-un tablou. `${file}` se expandează la fișierul sursă activ momentan. **Flagul** `-o` îi spune lui G++ să scrie rezultatul în numele de fișier care îl urmează. Prin urmare, sarcina construiește fișierul sursă deschis și numește binarul după acea sursă.

Eticheta este și numele la care face referire `preLaunchTask`; scrierea ei identic le unește cele două definiții. Sarcina poate fi deci accesată prin configurația de pornire a lui F5.

[00:06:37](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=397s) Celelalte intrări din definiția sarcinii sunt mai puțin importante pentru explicația din această etapă. Lecția nu cere o descriere câmp cu câmp a lor.

## Compilează fără a rula și localizează ieșirea

[00:06:46](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=406s) Sarcinile pot rula și independent. Pentru a compila fără a porni debuggerul:

1. Păstrează activ fișierul sursă dorit.
2. [00:07:03](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=423s) Găsește **Run Task** în Command Palette, meniul de comenzi căutabil al editorului. Acesta listează cele două sarcini declarate în fișierul de sarcini înregistrat.
3. [00:07:23](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=443s) Selectează sarcina de compilare G++. Ea execută comanda de compilare configurată, fără acțiunea separată de pornire.

[Definiția de sarcină aferentă, commitată](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/fef337c86c73ec8d197461ffe9327d69612ab81e/.vscode/tasks.json) leagă aceste argumente esențiale de G++. [00:07:35](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=455s) Citește comanda rezultată în ordine: compilator, calea sursei curente, `-o`, numele fișierului de ieșire. Pentru o sursă numită `a.cpp`, o expandare simplificată este:

```sh
g++ D:/project/a.cpp -o a.exe
```

Sarcina commitată completă are flag-uri suplimentare; acest exemplu izolează relația dintre intrare și ieșire care este explicată.

[00:07:57](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=477s) **Numele de bază** este numele fișierului, iar eliminarea extensiei sale transformă `a.cpp` în `a`. Configurația adaugă `.exe`, obținând `a.exe`. Numele de ieșire este o **cale relativă**, așadar și destinația sa depinde de folderul în care rulează comanda.

[00:08:06](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=486s) Demonstrația mută sursa într-un folder imbricat și compilează din nou. [00:08:20](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=500s) Binarul apare lângă acea sursă, păstrându-și numele.

[00:08:27](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=507s) Se întâmplă pentru că **directorul curent de lucru** al sarcinii este folderul în care rulează comanda sa de consolă. Aceeași [definiție de sarcină, commitată](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/fef337c86c73ec8d197461ffe9327d69612ab81e/.vscode/tasks.json) îl stabilește explicit:

```json
{
    "options": {
        "cwd": "${fileDirname}"
    }
}
```

Pentru o sursă activă la `D:/project/nested/a.cpp`, compilatorul primește acea cale de sursă, rulează în `D:/project/nested` și scrie acolo ieșirea relativă `a.exe`. Calea de pornire indică apoi exact același binar. Setarea folderului sursă este cea care ține ieșirea construirii și intrarea pornirii aliniate pe măsură ce fișierul se mută.

## Aliniază editorul cu compilatorul

[00:08:54](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=534s) Fișierul de setări nu este esențial pentru explicația construirii și pornirii. El include asocieri care spun editorului cum să trateze anumite nume de fișiere sau extensii. Un exemplu scurt dintr-un [fișier de setări, commitat](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/cc744a22dcdfce37fa772561d7c9354af05b3b5a/.vscode/settings.json) este:

```json
{
    "files.associations": {
        "*.json": "jsonc"
    }
}
```

Aici `jsonc` înseamnă JSON cu comentarii. Aceste asocieri nu definesc comanda de compilare, iar lecția spune că pot fi ignorate deocamdată.

[00:09:07](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=547s) Fișierul de proprietăți al extensiei C/C++ furnizează viziunea editorului asupra **toolchain-ului**, adică compilatorul și uneltele de sprijin. **IntelliSense** analizează sursa și oferă completare și diagnostică folosind această viziune. Înregistrarea vorbește inițial despre configurația de compilare „obișnuită”, apoi explică efectul asupra editorului și standardul pe care îl presupune.

[00:09:21](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=561s) Un **standard C++** este o versiune a limbajului și a bibliotecii sale. [Fișierul de proprietăți, commitat](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/ec49d61932f626869f9cc0e4050733b56aba6696/.vscode/c_cpp_properties.json) selectează C++20 pentru analiza din editor:

```json
{
    "configurations": [
        {
            "name": "Default",
            "cppStandard": "c++20"
        }
    ],
    "version": 4
}
```

În configurația Windows discutată în înregistrare, ipotezele implicite ale editorului sunt asociate cu **MSVC**, compilatorul Visual Studio al Microsoft. [00:09:42](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=582s) Dacă acele ipoteze nu corespund compilatorului și standardului tău, editorul poate semnala facilități dintr-un standard mai nou chiar dacă toolchain-ul tău intenționat le acceptă.

[00:09:55](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=595s) Modificarea demonstrată selectează explicit G++ pentru câmpul compilatorului. Versiunea anterioară, [commitată](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/4548bceac3c7982861496f1d77d29ecb7eddf7a0/.vscode/c_cpp_properties.json), a proprietăților are `compilerPath` setat la o valoare implicită; nu conține această modificare exactă din video. Un fragment simplificat, înainte și după, este:

```json
{
    "cppStandard": "c++20",
    "compilerPath": "${default}"
}
```

```json
{
    "cppStandard": "c++20",
    "compilerPath": "g++"
}
```

După modificare, navigarea în sursele bibliotecii din înregistrare ajunge la header-urile instalării lui G++. Un **header** conține declarații pe care fișierele sursă le includ; aici, locația sa arată a cărei biblioteci de compilator se consultă editorul. [00:10:21](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=621s) Compilatorul specificat aici determină informațiile despre compilator folosite de această configurație a editorului.

Păstrează clare cele două roluri: `compilerPath` și `cppStandard` configurează IntelliSense; sarcina reală de construire execută în continuare propria `command` și propriile argumente. Modificarea doar a fișierului de proprietăți nu rescrie acea sarcină și nu adaugă un flag de standard comenzii sale de compilare. [Referința pentru setările extensiei C++](https://code.visualstudio.com/docs/cpp/customize-cpp-settings) confirmă că aceste proprietăți controlează analiza din editor. O cale completă până la compilator este modul neechivoc de a identifica instalarea atunci când îți configurezi propria mașină.

Configurația finală are, așadar, trei părți conectate: o sarcină care produce binarul, o configurație de pornire care construiește înainte de a-l rula și o analiză din editor care corespunde compilatorului și versiunii de limbaj intenționate. Setările detaliate ale debuggerului și câmpurile rămase ale sarcinii rămân în afara acestei lecții.

## Istoricul modificărilor de cod

Acestea sunt stările înregistrate în ordinea lecției. Fragmentele din repository legate mai sus sunt versiuni aferente, commitate; nu se pretinde că păstrează fiecare modificare temporară făcută în video.

- [00:03:59 — pornire configurată](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=239s): inspectează intrarea GDB, calea executabilului și dependența sa de compilare.
- [00:05:16 — dependența eliminată](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=316s): salvează intrarea de pornire fără pasul de construire; ștergerea binarului face ca F5 să eșueze.
- [00:05:39 — definiția construirii urmărită](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=339s): urmărește eticheta referită până la sarcina care invocă G++.
- [00:07:23 — sarcina rulată direct](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=443s): execută compilarea independent de pornire.
- [00:08:06 — sursa mutată](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=486s): mută sursa într-un folder imbricat; directorul său curent de lucru păstrează ieșirea lângă ea.
- [00:09:55 — compilatorul editorului schimbat](https://www.youtube.com/watch?v=lBVXv8Qaj9Y&t=595s): specifică G++ pentru analiza din editor și observă header-urile bibliotecii sale.

```text
launch + build dependency
    -> launch without build -> missing executable
    -> inspect and run the compilation task
    -> move source; output follows its folder
    -> align editor analysis with G++
```