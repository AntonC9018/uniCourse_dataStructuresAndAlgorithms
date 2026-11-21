> Această notă a fost generată de AI (gpt-6.1-sol) pe baza videoclipului asociat și poate conține greșeli. Verificați videoclipul și sursele citate atunci când acuratețea contează.
> Traducerea în limba română a fost generată de AI (opencode/space-bunny-free) din nota în limba engleză și poate conține greșeli. Verificați nota originală atunci când acuratețea contează.

# Memoria, procesorul și codul mașină

## Scop și termeni

[00:00:00](https://www.youtube.com/watch?v=Bmae710korE&t=0s) Lecția construiește un mic model de calculator, ca să poți explica modul în care un program citește două valori, le adună și scrie un rezultat. C++ este studiat aici cu un nivel puțin mai jos decât C#, așa că înțelegerea biților, octeților și a motivului pentru care diferite tipuri de date ocupă cantități diferite de memorie te va ajuta la lecțiile următoare.

Termenii folosiți pe parcurs sunt:

- **RAM (memorie cu acces aleator), sau memorie principală:** spațiul de lucru reprezentat aici ca o bandă finită de celule. O **celulă** este o poziție de stocare adresabilă; **contiguu** înseamnă că aceste poziții se succed fără goluri. Un **gigabyte** este o unitate de capacitate egală cu un miliard de octeți.
- **Adresă:** numărul care identifică o poziție din RAM. Adresa unei celule și valoarea stocată acolo sunt lucruri distincte.
- **Date și tip:** datele sunt valoarea asupra căreia lucrează un program; un tip descrie cum este interpretată o valoare și ce operații au sens pentru ea.
- **Caracter și șir de caractere:** un caracter este un simbol de text, precum `A`; un șir de caractere este o succesiune de caractere.
- **Procesor (CPU, unitate centrală de prelucrare):** componenta care execută instrucțiunile. O **instrucțiune** este o [redacted] disponibilă procesorului.
- **ISA (arhitectură de set de instrucțiuni):** instrucțiunile acceptate de procesor și regulile pentru reprezentarea și utilizarea lor.
- **Registru:** o locație mică de stocare în interiorul CPU, folosită ca memorie de lucru. Un **indice de registru** identifică un registru distinct de adresele RAM.
- **Încărcare și stocare:** o încărcare copiază o valoare din RAM într-un registru; o stocare copiază o valoare dintr-un registru în RAM.
- **Cod de operație (opcode):** identificatorul numeric al unei instrucțiuni. **Operandii**, numiți aici și argumente sau parametri, spun unei instrucțiuni ce valori sau ce locații să folosească.
- **Cod mașină și fișier executabil:** codul mașină este succesiunea codificată de instrucțiuni pe care procesorul o poate executa direct; un fișier executabil conține acel cod pentru un program.
- **IP (instruction pointer, indicator de instrucțiune):** registrul special care urmărește locația instrucțiunii în memorie.
- **Bit și octet:** un bit are una dintre două stări, reprezentată ca `0` sau `1`; un octet este alcătuit din opt biți și reprezintă o celulă în acest model. O interpretare **fără semn** (unsigned) reprezintă doar numere întregi nenegative.
- **Sistem de numerație:** o modalitate de a reprezenta numere prin cifre. Binarul folosește două cifre, `0` și `1`; zecimalul folosește zece, de la `0` la `9`.
- **Codificarea caracterelor și ASCII:** o codificare asociază caracterele cu reprezentări numerice. ASCII, American Standard Code for Information Interchange, este exemplul simplu folosit aici.

Lecția conexă de [arhitectură de calculator](../../../en/01_computer_architecture/doc.md) dezvoltă același model conceptual cu un alt set de instrucțiuni jucărie.

**Domeniul de aplicare.** [00:00:33](https://www.youtube.com/watch?v=Bmae710korE&t=33s) „Memoria” înseamnă inițial doar RAM. Stocarea pe disc, unde sunt păstrate fișierele, și memoria cache a procesorului, adică stocarea folosită pentru a accelera accesul la memorie, sunt excluse. [00:00:45](https://www.youtube.com/watch?v=Bmae710korE&t=45s) Registrii sunt lăsați inițial pentru mai târziu; exemplul introduce doar suficiente informații despre ei cât să poată explica execuția, fără o arhitectură de CPU în detaliu. Aceasta este o demonstrație conceptuală, nu o implementare în C++ sau o specificație pentru un cip real. Numerele de cod de operație de mai jos sunt inventate pentru această lecție.

## RAM-ul ca o bandă adresabilă

[00:00:14](https://www.youtube.com/watch?v=Bmae710korE&t=14s) Imaginează RAM-ul ca pe o bandă de lungime finită, împărțită în celule. O celulă este o poziție mică de stocare, cu o capacitate limitată. [00:00:52](https://www.youtube.com/watch?v=Bmae710korE&t=52s) Celulele sunt contigue: fiecare se află imediat după cea precedentă.

[00:01:01](https://www.youtube.com/watch?v=Bmae710korE&t=61s) Începe punând o literă într-o celulă și un număr în alta. Un caracter este un simbol de text. Un șir de caractere este o succesiune de asemenea simboluri; un șir întreg, cu mai multe caractere, nu încape în acest exemplu cu o singură celulă, așa că șirurile sunt amânate. Reprezentarea literei în sine este explicată la finalul lecției.

[00:01:17](https://www.youtube.com/watch?v=Bmae710korE&t=77s) Numerotează pozițiile benzii pornind de la zero. [00:01:26](https://www.youtube.com/watch?v=Bmae710korE&t=86s) Această poziție este **adresa** celulei, locul unde celula începe. Celula care conține `A` are adresa zero. [00:01:38](https://www.youtube.com/watch?v=Bmae710korE&t=98s) Deoarece fiecare celulă ocupă o poziție în acest model, adresele următoare sunt unu, doi și așa mai departe.

| Adresă | Conținut în ilustrație |
| --- | --- |
| 0 | `A` |
| 1 | `123` |
| 2 | altă valoare |
| 3 | `1`, posibil intenționat ca o adresă |

[00:02:00](https://www.youtube.com/watch?v=Bmae710korE&t=120s) O celulă poate conține și adresa altei celule. Finalul `1` ar putea însemna numărul unu, sau ar putea identifica celula de la adresa unu. Conținutul brut nu anunță care dintre sensuri a fost intenționat. Un **tip** furnizează acea interpretare într-un program; mecanismele limbajului pentru a face asta apar mai târziu.

[00:02:21](https://www.youtube.com/watch?v=Bmae710korE&t=141s) Cele două operații fundamentale asupra RAM-ului sunt:

1. **Scriere:** pune o valoare în celula de la o adresă aleasă.
2. **Citire:** obține valoarea memorată în acel moment la o adresă aleasă.

Schimbarea unei valori nu schimbă adresa celulei. [00:02:34](https://www.youtube.com/watch?v=Bmae710korE&t=154s) Motivul mai larg pentru care memoria contează la proiectarea programelor este amânat până la videoclipul cursului despre algoritmi.

De ce nu poți decide doar privind `1` dacă ultima celulă conține un număr sau o adresă?

<details>
<summary>Răspuns</summary>

Ambele interpretări folosesc aceeași valoare numerică stocată. Tipul din program și operația care folosește acea valoare îi determină sensul. Adresa celulei care conține valoarea este, la rândul ei, un alt număr.

</details>

## Procesorul și setul său de instrucțiuni

[00:02:42](https://www.youtube.com/watch?v=Bmae710korE&t=162s) **Procesorul**, sau CPU, este a doua componentă. El poate citi valori din memorie, dar sarcina lui principală este executarea **instrucțiunilor**: [redacted] definite pentru acel procesor.

[00:02:56](https://www.youtube.com/watch?v=Bmae710korE&t=176s) Exemple includ citirea unei valori, adunarea, scăderea, înmulțirea și testarea unei proprietăți a unui număr. Înregistrarea menționează și testarea divizibilității cu unu; pentru un întreg, acel test reușește întotdeauna. Ideea exemplelor este mica anvergură a fiecărei acțiuni, nu un anumit catalog de instrucțiuni al unui CPU real.

[00:03:05](https://www.youtube.com/watch?v=Bmae710korE&t=185s) Procesoare diferite pot accepta mulțimi diferite de operații. [00:03:20](https://www.youtube.com/watch?v=Bmae710korE&t=200s) O **ISA**, adică o arhitectură de set de instrucțiuni, descrie instrucțiunile pe care le înțelege un procesor. Un program în cod mașină trebuie să folosească instrucțiuni acceptate de procesorul țintă. Nu presupune că codurile numerice dintr-o ISA au același sens în alta.

## Registrii ca memorie de lucru

[00:03:45](https://www.youtube.com/watch?v=Bmae710korE&t=225s) Ca să construiești un program, desenează două zone de stocare: RAM-ul și mica memorie de lucru a CPU-ului.

[00:03:54](https://www.youtube.com/watch?v=Bmae710korE&t=234s) RAM-ul conține un număr foarte mare de adrese și poate avea o capacitate de câțiva gigabyteți; un gigabyte este un miliard de octeți. El asigură stocarea principală în acest model. [00:04:11](https://www.youtube.com/watch?v=Bmae710korE&t=251s) Un **registru** este o locație de stocare din interiorul procesorului. Desenul îi tratează pe registri ca pe niște celule, asemenea celulelor RAM, dar sunt mult mai puține. Această asemănare este o simplificare pedagogică.

[00:04:22](https://www.youtube.com/watch?v=Bmae710korE&t=262s) Dă celor doi registri indicii zero și unu. Un **indice de registru** identifică o locație a CPU-ului; o adresă RAM identifică o locație din memoria principală. Adresa RAM zero și registrul zero sunt locații de stocare distincte, chiar dacă identificatorii lor folosesc același număr. Identificatorii reali ai registrilor pot fi nume sau indici, inclusiv identificatori pentru registri specializați.

[00:04:49](https://www.youtube.com/watch?v=Bmae710korE&t=289s) CPU-ul poate selecta fiecare registru individual. [00:04:52](https://www.youtube.com/watch?v=Bmae710korE&t=292s) Aceste locații identificate individual formează memoria sa de lucru. [00:05:02](https://www.youtube.com/watch?v=Bmae710korE&t=302s) Registrii sunt utili în ciuda existenței RAM-ului, pentru că oferă o stocare de lucru mult mai rapidă. În designul jucărie, instrucțiunile aritmetice lucrează cu registrii, așa că valorile sunt aduse mai întâi din RAM. Aceasta descrie designul exemplului, nu o regulă potrivit căreia orice instrucțiune reală trebuie să folosească doar registri.

## Construirea programului de adunare

[00:05:13](https://www.youtube.com/watch?v=Bmae710korE&t=313s) Valori precum cinci și șase ilustrează conținutul registrilor. [00:05:18](https://www.youtube.com/watch?v=Bmae710korE&t=318s) Sarcina programului este însă „adună conținutul primelor două celule RAM”. Nu trebuie să aibă valorile concrete cinci, șase sau zece încorporate în instrucțiunile sale. Aceste valori sunt **date**, adică intrările asupra cărora operează programul.

Folosim cinci la adresa RAM zero și șase la adresa RAM unu pentru a urmări rezultatul. Aceste valori fac modificările vizibile; aceleași operații pot citi alte intrări. Urmând [construcția din video](https://www.youtube.com/watch?v=Bmae710korE&t=337s), planul simplificat este:

```text
R0 <- RAM[0]
R1 <- RAM[1]
R0 <- R0 + R1
RAM[3] <- R0
```

Aici `RAM[n]` înseamnă conținutul de la adresa `n`, `R0` și `R1` înseamnă registrul zero, respectiv registrul unu, iar `<-` înseamnă „copiază sau atribuie valoarea din dreapta”. Această notație explică acțiunile; nu este C++ și nici sintaxa unui procesor real.

1. [00:05:37](https://www.youtube.com/watch?v=Bmae710korE&t=337s) **Încarcă** prima valoare: copiază adresa RAM zero în registrul zero. O încărcare mută o valoare din memoria principală în stocarea de lucru a CPU-ului. Acum registrul zero conține cinci.
2. [00:05:45](https://www.youtube.com/watch?v=Bmae710korE&t=345s) Încarcă adresa RAM unu în registrul unu. Acum cei doi registri conțin cinci și șase.
3. [00:05:57](https://www.youtube.com/watch?v=Bmae710korE&t=357s) Adună registrul zero și registrul unu, înlocuind vechiul conținut al registrului zero cu suma. Registrul zero conține acum unsprezece; registrul unu conține în continuare șase.
4. [00:06:12](https://www.youtube.com/watch?v=Bmae710korE&t=372s) **Stochează** răspunsul: copiază registrul zero în adresa RAM trei. O stocare mută o valoare dintr-un registru în memoria principală. Afișarea răspunsului este menționată ca o altă acțiune posibilă următoare, dar acest program alege stocarea.

[00:06:24](https://www.youtube.com/watch?v=Bmae710korE&t=384s) Acești pași sunt instrucțiunile programului. Rezultatul său este suma din celula trei, nu o modificare a celor două celule de intrare. Aceasta este o urmărire manuală a modelului jucărie; videoclipul nu compilează și nu testează aici un program C++.

| Stare după acțiune | Registrul 0 | Registrul 1 | Adresa RAM 3 |
| --- | --- | --- | --- |
| Prima încărcare | 5 | încă nefolosit | nemodificat |
| A doua încărcare | 5 | 6 | nemodificat |
| Adunare | 11 | 6 | nemodificat |
| Stocare | 11 | 6 | 11 |

De ce trebuie ca a doua încărcare să folosească un alt registru?

<details>
<summary>Răspuns</summary>

Încărcarea lui șase în registrul zero ar suprascrie valoarea cinci înainte de adunare. Folosirea registrului unu păstrează ambele intrări disponibile. Adunarea suprascrie apoi, în mod deliberat, registrul zero cu răspunsul.

</details>

## Codificarea celor două încărcări

[00:06:36](https://www.youtube.com/watch?v=Bmae710korE&t=396s) CPU-ul nu poate executa planul doar pentru că este scris în engleză. Fiecare instrucțiune are nevoie de un **cod de operație**, identificatorul său numeric de operație.

[00:06:50](https://www.youtube.com/watch?v=Bmae710korE&t=410s) Documentația ISA a unui procesor descrie operațiile acceptate, codificările lor și sensul operanzilor. Procesorul implementează aceste reguli; nu citește un manual în timpul execuției.

[00:07:10](https://www.youtube.com/watch?v=Bmae710korE&t=430s) Să presupunem că această ISA jucărie asociază codul de operație `64` copierii din RAM într-un registru. [00:07:22](https://www.youtube.com/watch?v=Bmae710korE&t=442s) Acesta ia doi **operanzi**, adică argumentele care precizează de unde se citește și unde se scrie, în această ordine:

1. Adresa RAM sursă.
2. Indicele registrului destinație.

Prin urmare, [prima încărcare, la 00:07:38](https://www.youtube.com/watch?v=Bmae710korE&t=458s), devine:

```text
64 0 0
```

Primul zero este o adresă RAM. Al doilea zero este un indice de registru. Au roluri diferite, deși valorile scrise sunt identice.

[00:07:57](https://www.youtube.com/watch?v=Bmae710korE&t=477s) Păstrează codul de operație pentru a doua încărcare, pentru că operația nu se schimbă; modifică doar operanzii:

```text
64 0 0
64 1 1
```

[Exemplul de arhitectură corespunzător, aflat în repo](https://github.com/AntonC9018/uniCourse_dataStructuresAndAlgorithms/blob/e6a198dd9d5f56bde01e2f74f0d71bf253316d82/en/01_computer_architecture/doc.md#instructions-and-a-computer-program-example) folosește alte coduri de operație și alte adrese inventate. Este o sursă conceptuală conexă, nu o copie exactă în repo a programului din acest videoclip. Încărcarea sa simplificată corespunzătoare este:

```text
15 102 0
```

În acel exemplu separat, `15` copiază adresa RAM `102` în registrul zero. Identificatorul diferit întărește de ce trebuie ca ISA să definească codificarea.

## Alegerea unei instrucțiuni fixe de adunare

[00:08:18](https://www.youtube.com/watch?v=Bmae710korE&t=498s) Dă adunării codul de operație `72`. [00:08:33](https://www.youtube.com/watch?v=Bmae710korE&t=513s) Inițial, explicația ia în calcul furnizarea a doi parametri: de unde să fie luat fiecare intrare.

[00:08:41](https://www.youtube.com/watch?v=Bmae710korE&t=521s) Instrucțiunea aleasă fixează apoi acele locații ca parte din definiția sa: adună registrul zero cu registrul unu și pune rezultatul în registrul zero. Așadar, nu are **operanzi expliciți**. Valorile de intrare există în continuare; locațiile lor sunt implicate de codul de operație.

[Programul intermediar, la 00:09:16](https://www.youtube.com/watch?v=Bmae710korE&t=556s), este:

```text
64 0 0
64 1 1
72
```

[00:08:58](https://www.youtube.com/watch?v=Bmae710korE&t=538s) O altă variantă de adunare ar putea fixa registrul zero, dar accepta un al doilea registru diferit drept operand, după codul său de operație. O asemenea variantă ar avea nevoie de propria regulă de codificare. Aici însă, după `72` nu urmează niciun argument; următorul număr va începe instrucțiunea următoare.

## Stocarea rezultatului și schimbarea operanzilor

[00:09:16](https://www.youtube.com/watch?v=Bmae710korE&t=556s) Încheie cu o copiere din registrul zero în adresa RAM trei. [00:09:34](https://www.youtube.com/watch?v=Bmae710korE&t=574s) Codul de operație `65` reprezintă această **stocare**, copiind valoarea unui registru în memoria principală. Cei doi operanzi ai săi sunt indicele registrului sursă și adresa RAM destinație.

[Programul de sumă completat](https://www.youtube.com/watch?v=Bmae710korE&t=574s) este:

```text
64 0 0
64 1 1
72
65 0 3
```

Ordinea este întotdeauna sursă urmată de destinație, dar tipurile de locații depind de codul de operație: `64` folosește RAM apoi registru; `65` folosește registru apoi RAM.

[00:09:47](https://www.youtube.com/watch?v=Bmae710korE&t=587s) Exercițiul separat de încărcare întreabă cum se pune valoarea zece în registrul unu. Explicația rostită îi identifică sursa drept **adresa RAM doi**. Așadar, operandul sursă este doi, nu zero; zece este data găsită acolo, nu un operand încorporat în această instrucțiune de încărcare.

[Exercițiile de încărcare și stocare](https://www.youtube.com/watch?v=Bmae710korE&t=587s) se pot scrie așa:

```text
64 2 1
65 1 4
```

[00:10:00](https://www.youtube.com/watch?v=Bmae710korE&t=600s) A doua linie stochează conținutul registrului unu în adresa RAM patru. [00:10:17](https://www.youtube.com/watch?v=Bmae710korE&t=617s) Demonstrația descrie valoarea șase apărând în destinație, folosind un registru care conține șase. Dacă încărcarea lui zece precedă imediat stocarea, acolo apare zece în locul ei. Stocarea copiază conținutul curent al registrului; nu selectează singură șase sau zece. Aceste exerciții ilustrează schimbarea operanzilor separat de suma cu patru instrucțiuni.

## Un singur flux continuu de cod mașină

[00:10:25](https://www.youtube.com/watch?v=Bmae710korE&t=625s) Întreaga listă de instrucțiuni poate fi reprezentată prin numere. [00:10:41](https://www.youtube.com/watch?v=Bmae710korE&t=641s) **Codul mașină** este forma codificată a instrucțiunilor pe care procesorul le poate executa direct.

[Programul de sumă ca flux numeric](https://www.youtube.com/watch?v=Bmae710korE&t=625s) este:

```text
64 0 0 64 1 1 72 65 0 3
```

[00:10:55](https://www.youtube.com/watch?v=Bmae710korE&t=655s) Golurile aparente dintre instrucțiuni din desen sunt doar o convenție de afișare. În această dispunere jucărie a memoriei nu există celule de separare: numerele ocupă poziții consecutive. Spațiile și întreruperile de rând din aceste exemple îi ajută pe om să le citească.

[00:11:09](https://www.youtube.com/watch?v=Bmae710korE&t=669s) Rezultă o problemă de explicat: dacă CPU-ul primește doar numere, cum deosebește un cod de operație de un operand și cum găsește următoarea instrucțiune?

Prezică dacă zero de după primul `64` va fi tratat drept cod de operație.

<details>
<summary>Răspuns</summary>

Este un operand. Regula de codificare pentru codul de operație 64 spune să consume următoarele două numere: o adresă RAM și un indice de registru. Doar numărul de după cei doi operanzi începe o instrucțiune nouă.

</details>

## Decodificarea fluxului

[00:11:25](https://www.youtube.com/watch?v=Bmae710korE&t=685s) Pornește de la primul număr și procesează instrucțiunile în ordine. [Demonstrația de decodificare](https://www.youtube.com/watch?v=Bmae710korE&t=703s) folosește același flux:

```text
64 0 0 | 64 1 1 | 72 | 65 0 3
```

Barele verticale de mai sus sunt doar marcaje explicative; nu sunt stocate în memorie.

1. [00:11:43](https://www.youtube.com/watch?v=Bmae710korE&t=703s) Citește codul de operație `64`. Regula sa implementată spune „încărcare, cu doi operanzi”, așa că consumă exact următoarele două numere.
2. [00:12:02](https://www.youtube.com/watch?v=Bmae710korE&t=722s) Interpretează `0 0` ca adresa RAM zero și registrul zero și copiază valoarea. [00:12:21](https://www.youtube.com/watch?v=Bmae710korE&t=741s) După ce a consumat cei doi operanzi, reia citirea codurilor de operație.
3. [00:12:41](https://www.youtube.com/watch?v=Bmae710korE&t=761s) Citește următorul `64` și operanzii săi `1 1`. Aceasta copiază adresa RAM unu în **registrul unu**, păstrând prima intrare în registrul zero. O referire la registrul zero în recapitularea rostită ar suprascrie acea intrare; a doua încărcare stabilită mai devreme furnizează registrul unu.
4. [00:12:58](https://www.youtube.com/watch?v=Bmae710korE&t=778s) Citește `72`. Acesta adună **registrul zero și registrul unu**, stocând rezultatul în registrul zero, așa cum a fost definit mai devreme. Nu introduce un al treilea registru și nu acceptă argumente.
5. [00:13:19](https://www.youtube.com/watch?v=Bmae710korE&t=799s) Deoarece `72` nu are operanzi, `65` care urmează imediat este deja un cod de operație. Consumă operanzii săi `0 3` și copiază registrul zero în adresa RAM trei.

Limitele instrucțiunilor urmează regulile de codificare, nu valoarea unui număr privită izolat. De exemplu, un număr egal cu un cod de operație ar putea fi totuși un operand, dacă instrucțiunea curentă așteaptă unul în acea poziție.

## Încărcarea unui executabil în RAM

[00:13:33](https://www.youtube.com/watch?v=Bmae710korE&t=813s) Un **fișier executabil** conține cod mașină: instrucțiuni și operanzii de care acestea au nevoie. Lecția se concentrează pe acel cod, nu pe celelalte structuri pe care un fișier executabil real le poate conține.

[00:13:51](https://www.youtube.com/watch?v=Bmae710korE&t=831s) Deoarece programul codificat este stocat ca numere, acele numere pot fi puse în RAM. [00:14:06](https://www.youtube.com/watch?v=Bmae710korE&t=846s) Procedura simplificată de pornire este:

1. Rezervă o regiune din RAM pentru codul programului.
2. Încarcă codul mașină din executabil în acea regiune.
3. Lasă procesorul să execute instrucțiunile din memorie.

Încărcarea pregătește programul pentru execuție; doar copierea octeților nu efectuează adunarea.

[00:14:26](https://www.youtube.com/watch?v=Bmae710korE&t=866s) În acest model, CPU-ul urmărește codul din RAM, în loc să execute direct un fișier de pe disc. Fiecare element numeric din codificarea jucărie încape într-o celulă. [Exemplul de cod mașină încărcat](https://www.youtube.com/watch?v=Bmae710korE&t=866s) este tot:

```text
64 0 0 64 1 1 72 65 0 3
```

[00:14:40](https://www.youtube.com/watch?v=Bmae710korE&t=880s) Un **octet** este aici o celulă, iar domeniul său numeric fără semn se termină la 255. [00:14:45](https://www.youtube.com/watch?v=Bmae710korE&t=885s) CPU-ul nu inspectează întreaga bandă de memorie dintr-o dată. [00:14:47](https://www.youtube.com/watch?v=Bmae710korE&t=887s) Modelul pedagogic cere conținutul unei celule anume și îl încarcă într-un registru pentru operații ulterioare. Acest model cu o singură celulă este o simplificare, nu o afirmație că procesorele reale nu pot citi mai mulți octeți într-o singură operație.

## Urmărirea execuției cu IP

[00:14:54](https://www.youtube.com/watch?v=Bmae710korE&t=894s) Un registru special consemnează poziția curentă din cod. Rolul său mai detaliat este amânat până la videoclipul despre execuția funcțiilor.

[00:15:01](https://www.youtube.com/watch?v=Bmae710korE&t=901s) **IP**, instruction pointer, conține adresa instrucțiunii curente în modelul lecției. [00:15:10](https://www.youtube.com/watch?v=Bmae710korE&t=910s) Să presupunem că programul începe la adresa RAM 32. Există poziții RAM înaintea ei; codul programului nu trebuie să înceapă la începutul benzii.

[Ilustrarea adreselor de la 00:15:18](https://www.youtube.com/watch?v=Bmae710korE&t=918s), aplicată programului de sumă, dă această dispunere:

```text
Address: 32 33 34 35 36 37 38 39 40 41
Value:   64  0  0 64  1  1 72 65  0  3
```

Adresele 32, 33, 34 și 35 sunt **poziții de octet** consecutive, nu patru începuturi succesive de instrucțiune. Prima instrucțiune își include operanzii la 33 și 34; a doua începe la 35.

[00:15:30](https://www.youtube.com/watch?v=Bmae710korE&t=930s) La pornire, IP indică prima instrucțiune. [00:15:45](https://www.youtube.com/watch?v=Bmae710korE&t=945s) Execuția secvențială repetă apoi acești pași:

1. Găsește codul de operație la adresa indicată de IP.
2. Decodifică codul de operație și citește orice operanzi de care are nevoie.
3. Efectuează operația.
4. Avansează IP către următoarea instrucțiune, ținând cont de operanzii deja consumați.

[00:15:50](https://www.youtube.com/watch?v=Bmae710korE&t=950s) Pentru această dispunere, începuturile de instrucțiune vizitate sunt 32, 35, 38 și 39. Cele două încărcări ocupă fiecare trei celule; adunarea fixă ocupă una; stocarea ocupă trei. Avansarea lui IP nu înseamnă tratarea unui octet operand drept un cod de operație nou. Apelurile de funcții și comportamentul detaliat al registrilor specializați rămân în afara acestei lecții.

Dacă IP indică valoarea `72` de la adresa 38, unde este următoarea instrucțiune?

<details>
<summary>Răspuns</summary>

La adresa 39. Această adunare fixă nu are operanzi expliciți, așa că ocupă o singură celulă în codificarea jucărie.

</details>

## Octeți, biți și domeniul de la zero la 255

[00:16:01](https://www.youtube.com/watch?v=Bmae710korE&t=961s) Am folosit celule care conțin valori, dar cum poate o celulă să reprezinte un număr sau un caracter? [00:16:13](https://www.youtube.com/watch?v=Bmae710korE&t=973s) Răspunsul detaliat aparține videoclipurilor despre sistemele de numerație și numerele negative. Aici ne trebuie modelul de bază al stocării.

[00:16:23](https://www.youtube.com/watch?v=Bmae710korE&t=983s) Un **octet** este o celulă adresabilă în acest model. [00:16:31](https://www.youtube.com/watch?v=Bmae710korE&t=991s) Fiecare octet este alcătuit din opt **biți**, fiecare reprezentând o cifră binară.

[00:16:36](https://www.youtube.com/watch?v=Bmae710korE&t=996s) Un bit este fie zero, fie unu. Înregistrarea ilustrează aceste stări ca absența sau prezența curentului; aceasta este o analogie fizică pentru două stări distincte. Un bit nu are în model o a treia stare „goală”. Zero este o stare stocată, nu o absență a stocării.

[00:16:47](https://www.youtube.com/watch?v=Bmae710korE&t=1007s) Un **sistem de numerație** dă sens unei succesiuni de cifre. Interpretând stările biților ca cifre binare, celula poate reprezenta un număr. [00:16:58](https://www.youtube.com/watch?v=Bmae710korE&t=1018s) Acel număr trebuie să încapă în cele opt cifre disponibile.

[00:17:05](https://www.youtube.com/watch?v=Bmae710korE&t=1025s) Într-o interpretare **fără semn**, biții reprezintă un număr întreg nenegativ. Cea mai mare valoare fără semn apare când toți cei opt biți sunt unu. [00:17:17](https://www.youtube.com/watch?v=Bmae710korE&t=1037s) Toți biții zero reprezintă zero.

| Tipar de opt biți | Valoare zecimală |
| --- | --- |
| `00000000` | 0 |
| `00000001` | 1 |
| `11111111` | 255 |

[00:17:25](https://www.youtube.com/watch?v=Bmae710korE&t=1045s) Așadar, un octet are un domeniu fără semn de **0 până la 255**, inclusiv. Dimensiunea sa limitează numărul de tipare de biți distincte disponibile. Modul în care un program reprezintă numerele negative este amânat în mod deliberat.

## Caracterele și sensul unui octet

[00:17:35](https://www.youtube.com/watch?v=Bmae710korE&t=1055s) O **codificare a caracterelor** asociază un simbol de text cu o reprezentare numerică. ASCII este exemplul de codificare simplu numit în înregistrare; descrierea sa drept „cea mai populară” nu este necesară pentru a înțelege mecanismul de stocare.

[00:17:53](https://www.youtube.com/watch?v=Bmae710korE&t=1073s) În ASCII, fiecare caracter reprezentat are un număr asociat. [00:18:04](https://www.youtube.com/watch?v=Bmae710korE&t=1084s) O celulă de memorie stochează un tipar de biți care poate fi citit ca număr; programul interpretează acea reprezentare drept caracter. Celula nu se etichetează singură drept „caracter”, „număr obișnuit” sau „adresă”. Este aceeași problemă de interpretare întâlnită mai devreme cu valoarea unu.

[00:18:07](https://www.youtube.com/watch?v=Bmae710korE&t=1087s) Celulele alăturate pot fi folosite împreună pentru a oferi mai multe cifre binare și a reprezenta valori mai mari. Asta închide legătura cu observația de la început că tipurile de date pot ocupa cantități diferite de memorie. Lecția se oprește la această idee; dispunerile pe mai mulți octeți, șirurile de caractere, reprezentările numerelor negative și execuția detaliată a funcțiilor sunt subiecte ulterioare.

De ce faptul că vezi o valoare numerică în RAM nu îți spune dacă ea reprezintă un caracter?

<details>
<summary>Răspuns</summary>

Reprezentarea singură nu alege o interpretare. Programul trebuie să aplice o codificare a caracterelor pentru a o citi ca text, la fel cum are nevoie de interpretarea potrivită pentru a folosi o valoare drept număr sau adresă.

</details>

## Exerciții opționale ulterioare

Nepredat în acest videoclip: [laboratorul de instrucțiuni C++](../../../en/labs/cpp/01_instruction.md) exersează enunțurile C++, afișarea și apelurile simple de funcții. Este un exercițiu ulterior, la nivelul limbajului, nu sursa acestei ISA jucărie și nici dovada unui pas de instalare.

## Istoricul modificărilor de cod

Acestea sunt stările succesive ale lecției în video, de la cea mai veche la cea mai recentă. Niciun commit inspectat din repo nu conține codificarea jucărie exactă folosită aici.

- [00:05:37 — planul de acțiuni](https://www.youtube.com/watch?v=Bmae710korE&t=337s): încarcă două intrări RAM în registri separați, adună în registrul zero și stochează la adresa trei.
- [00:07:38 — încărcări numerice](https://www.youtube.com/watch?v=Bmae710korE&t=458s): introduce codul de operație 64, cu operanzi pentru adresa sursă și registrul destinație.
- [00:08:41 — adunare fixă](https://www.youtube.com/watch?v=Bmae710korE&t=521s): alege codul de operație 72, cu registre implicate și fără operanzi expliciți.
- [00:09:16 — suma completată](https://www.youtube.com/watch?v=Bmae710korE&t=556s): adaugă stocarea, codul de operație 65, cu operanzii zero și trei.
- [00:10:25 — cod mașină continuu](https://www.youtube.com/watch?v=Bmae710korE&t=625s): reprezintă instrucțiunile ca pe un singur flux numeric neîntrerupt.
- [00:15:45 — poziția de execuție](https://www.youtube.com/watch?v=Bmae710korE&t=945s): urmărește începuturile instrucțiunilor cu IP, avansând peste operanzii fiecărei instrucțiuni.
