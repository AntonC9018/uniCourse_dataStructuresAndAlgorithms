# Командная строка

Интерфейс командной строки - это интерфейс, который позволяет запускать или выполнять команды (или программы) и взаимодействовать с ними. На Windows наиболее часто используемой, простой программой CLI (приложением) является CMD (сокращенно от "command").

> Чтобы открыть CMD, вы можете нажать кнопку ⊞ Win, чтобы открыть строку поиска,
> введите "cmd", чтобы найти программу CLI и нажмите Enter, чтобы запустить ее.

## Как запускать команды и программы?

Команды (и программы) запускаются путем ввода их имени (или пути) и нажатия Enter. Команды направлены на систему CLI (очистить экран, изменить текущий рабочий каталог и т. д.). Программы запускаются операционной системой. После запуска программы и до ее завершения все, что вы вводите в приложение CLI, может потенциально быть прочитано программой.

Например, предположим, у вас есть программа с именем `prog.exe`. Чтобы выполнить эту программу, вам нужно ввести ее имя в CLI и нажать Enter. Это выполнит файл с именем `prog.exe`, находящийся в текущем каталоге (подробнее об этом позже).

Введя `prog.exe` и нажав Enter, вы отправите запрос операционной системе на выполнение программы с именем `prog.exe`, которая прочитает файл и начнет выполнять инструкции из него.

> В Windows `.exe` можно не вводить, поэтому просто ввод `prog` также запустит ту же программу.
> `.exe` - это одно из нескольких специальных расширений, которые работают таким образом.
> Чтобы запустить программы с другими расширениями, вам нужно полностью ввести имя.

> `exe` означает "исполняемый файл".

## Текущий рабочий каталог

У приложений CLI есть понятие CWD (текущий рабочий каталог), который очень важно понимать при работе с CLI.

Текущий рабочий каталог указывает на папку, к которой будут привязаны имена программ. Таким образом, чтобы запустить файл с именем `prog.exe`, он должен находиться в текущем рабочем каталоге. Если этого нет, CLI не сможет его найти и даст вам ошибку, что не смог выполнить программу.

В любой момент времени может быть только один текущий рабочий каталог, и он обычно всегда виден в приложении CLI во время его использования. Он ссылается на любую отдельную папку на вашем компьютере и может быть изменен по желанию во время использования приложения CLI, вводя специальные команды (описанные ниже). Считайте CWD как переменную или состояние, за которым приложение CLI всегда следит.

CWD также может быть просмотрен и интерпретирован программами, которые вы запускаете из командной строки. Он может быть использован, например, для чтения файлов из той же папки, из которой вы запускаете программу.

### Навигация по CWD

Вы можете изменить рабочий каталог с помощью команды `cd`.
- Чтобы установить CWD (перейти) в подпапку с именем "A", выполните `cd A`.
- Чтобы установить CWD в родительский каталог, выполните `cd ..`.
  Двойная точка может использоваться несколько раз и даже сопровождаться обычными именами дочерних каталогов, например `cd ../../A` означает "вернуться назад, вернуться назад, перейти в каталог A", так что "перейти в каталог A в бабушке".
- Наконец, если вы хотите изменить рабочий каталог на некоторый **абсолютный путь**,
  например `C:/Users/Anton/Documents/projects` или `D:/Downloads/movies`,
  просто введите `cd`, за которым следует этот абсолютный путь.
- Если вы пытаетесь переключиться, например, с диска `C` на диск `D`,
  вам также нужно ввести имя диска, на который вы пытаетесь переключиться, в виде команды `D:` и нажать Enter.

## Переменные среды

Последнее понятие, связанное с CLI, описанное в этом документе, - это идея переменных среды. Они могут звучать страшно, но это просто некоторые именованные строки символов, которые могут быть использованы CLI или программами, которые вы запускаете из него.

CLI отслеживает значения всех этих переменных среды в любой данный момент времени. Он также позволяет пользователю изменять их с помощью команды `set` или "расширять" их, вводя `%variable_name%` в CLI.

Так же как и CWD, переменные среды могут быть прочитаны программами, которые вы запускаете.

### Переменная среды PATH

Самая важная переменная - это `PATH`, которая содержит папки, в которых операционная система должна искать имя программы.

Например, предположим, что CWD установлен в `D:/Downloads`, но ваша программа находится в `C:/Programs` и называется `prog.exe`. Вы могли бы перейти в каталог `C:/Programs`, изменив CWD, и запустить `prog.exe`, или вы можете запустить программу, введя ее абсолютный путь, `C:/Programs/prog.exe`, но это не так удобно, как просто ввести `prog.exe` и просто работать. Вот для чего предназначен `PATH`.

Если вы установите `PATH` на `C:/Programs` (где находится `prog.exe`), тогда вы сможете запустить `prog.exe` откуда угодно, введя его имя файла (`prog.exe`). Операционная система попробует найти `prog.exe`, исследуя каталог, указанный в переменной `PATH`, т. е. путь `C:/Programs`, где он найдет вашу программу. Но если он не найдет его в `PATH`, он затем будет искать его в текущем каталоге.

`PATH` может быть установлен на *список путей, разделенных символом ";*", что означает, что он может включать в себя несколько таких путей каталогов, в которых он должен искать программы, вам просто нужно разделить их ";". Например, `C:/Folder1;C:/Folder2`. Когда вы пытаетесь запустить программу, он попробует исследовать все это по порядку, пока не найдет программу.

Он всегда будет пытаться найти программу в порядке путей в `PATH` и только затем искать в текущем каталоге. Однако есть обходной путь, который позволяет запустить программу только из текущего каталога. Вы делаете это, указав относительный путь программы из текущего каталога. В этом случае он пропустит поиск в каталогах `PATH` и просто посмотрит в текущем каталоге. Вы делаете это, добавив к имени программы `./`, например `./prog.exe` (`.` означает "текущий каталог").

### Примеры PATH

Например, если `PATH` установлен на `C:/Folder1;C:/Folder2`, с папками, содержащими:
- `C:/Folder1`:
  - `prog1.exe`
  - `prog2.exe`
- `C:/Folder2`:
  - `prog2.exe`
  - `prog3.exe`
Тогда выполнение `prog1.exe` в любом каталоге запустит программу `prog1.exe` из `C:/Folder1`, выполнение `prog2.exe` запустит программу `prog2.exe` из `C:/Folder1` (потому что он найдет ее первой), выполнение `prog3.exe` запустит программу `prog3.exe` из `C:/Folder2`, и выполнение `prog4.exe` не найдет ее.

### Экспорт переменных среды

Крутая вещь в переменных среды заключается в том, что их можно переопределить для всех программ при запуске. Это называется экспортом переменной.

Вы можете сделать это в windows, используя их графический интерфейс, или используя команду [`setx`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx) в CLI.

Он также может быть изменен программами, например, при установке.

> Если вы обнаружите, что не можете получить доступ к какой-либо команде в командной строке, даже если знаете, что установили ее, это, вероятно, означает, что каталог, в котором находится эта программа, отсутствует в переменной `PATH`. Вам просто нужно найти программу и добавить каталог, в котором она находится, в переменную `PATH`. После перезагрузки системы это будет работать везде наверняка.
