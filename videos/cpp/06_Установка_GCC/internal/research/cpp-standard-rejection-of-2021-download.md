# Why the first download is rejected: C++ standard support, not age

- Transcript 00:00:37–00:00:47: "Видите дату двадцать первый год. Тут очень старый компилятор. C++ 17
  стандарт. Нам нужен будет стандарт более новый, потому что я буду использовать некоторые функции,
  которые только в новом [стандарте] есть." Recorded as ledger TP-003.
- The rejection is about the *C++ standard* the download supports, and it is scoped by
  `english_authoring` run 443 to that one download: the note warns "this is a warning about that
  particular download, not a rule that every compiler released in 2021 supports only C++17." The
  second sentence of the transcript ("because I will use functions that exist only in the newer
  standard") is why the note ties it to course content rather than to release year as such.
- Kept as an edge case in the ledger (`kind: edge_case`, 31920–47920 ms), i.e. it is a decision the
  student must make, not background trivia.
- Consequence for later steps: because the newer toolchain is chosen, the compiler ends up under
  `C:\msys64\usr\bin` and the recorded paths are MSYS2-specific; a different environment package
  would move them. See `toolchain-naming-msys2-vs-mingw.md`.
- Second link followed in the video (00:00:47–00:00:53) is the SourceForge route offering
  **prebuilt toolchains**; ledger TP-004. The note adds that prebuilt means "already compiled for
  you", i.e. you are not building GCC from source, because that is the ambiguity a newcomer
  reading "download the source" would hit here.