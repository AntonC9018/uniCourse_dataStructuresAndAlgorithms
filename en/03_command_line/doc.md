# Command Line

A command line interface is an interface that allows launching or executing commands (or programs)
and communicating with them.
On Windows, the most commonly used, simple CLI application (program) is the CMD (short for "command").

> To open CMD, you can hit the ⊞ Win button to pop open the search bar, 
> type "cmd" to search for the CLI program and hit enter to run it.

## How to run commands and programs?

Commands (and programs) are run by typing their name (or path) and hitting Enter.
Commands are directed at the CLI system (clear the screen, change the current working directory, etc.).
Programs are run by the operating system.
After starting a program, and until it completes,
whatever you type into the CLI application can potentially be read by the program.

For example, let's say you have a program named `prog.exe`.
In order to execute this program, you need to type its name into the CLI, and hit Enter. 
This will execute the file named `prog.exe` found in the current directory (more on that later).

Typing in `prog.exe` and hitting Enter would issue a request to the operating system to run the program named `prog.exe`,
which would read the file and start executing the instructions from it.

> `.exe` is optional to type on Windows, so just typing `prog` would also start the same program.
> `.exe` is one of few special extensions that work like this.
> To run programs with other extensions you need to type the name fully.

> `exe` stands for "executable".

## Current working directory

CLI applications have the concept of the CWD (current working directory), 
which is a very important concept to understand when working with CLIs.

The current working directory refers to the folder that the program names will be resolved relative to.
So to start the file named `prog.exe`, it needs to be located in the current working directory.
If it's not, the CLI won't be able to locate it, and will give you an error that it couldn't execute the program.

There can only be a single current working directory at any given time, and it's typically always visible 
in the CLI application while you're using it.
It refers to any single folder on your computer, and it can be changed at will while using the CLI application,
by typing in special commands (described later).
Think of the CWD as a variable or a piece of state that the CLI application always keeps track of.

The CWD can also be viewed and interpreted by the programs you run on the command line.
It can be used to, for example, be able to read files in the same folder you run the program from.

### CWD navigation

You can change the working directory by using the `cd` command.
- To set the CWD (navigate) to a subfolder named "A", you do `cd A`.
- To set the CWD to the parent directory, you do `cd ..`.
  The double dot can be used multiple times and even accompanied with normal child directory names, for example `cd ../../A` would mean "go back, go back, go to directory A", so "go to directory A in the grandparent".
- Finally, if you want to change the working directory to some **absolute path**, 
  like `C:/Users/Anton/Documents/projects` or `D:/Downloads/movies`, 
  you just type `cd` followed by that absolute path.
- If you're trying to switch e.g. from disk `C` to disk `D`, 
  you also need to input the disk name you're trying to switch to as a command `D:` and hit Enter.

## Environment variables

The last concept related to CLIs described in this document is the idea of environment variables.
These might sound scary, but they are just some named strings of characters
that can be used by the CLI or the programs that you run from it.

The CLI keeps track of the values of all these environment variables at any given time.
It also allows the user to change them by using the `set` command, or "expand" them, 
by typing `%variable_name%` in the CLI.

Just like the CWD, the environment variables can be read by the programs that you run.

### The PATH Environment Variable

The most important is the `PATH` variable, which contains the folders 
into which the operating system should look to resolve a program name.

For example, say the CWD is `D:/Downloads`, but your program is in `C:/Programs` and is named `prog.exe`.
You could go to the `C:/Programs` directory by changing the CWD and run `prog.exe`,
or you can run the program by typing its absolute path, `C:/Programs/prog.exe`,
but it's not as convenient as just typing `prog.exe` and having it just work.
That's what `PATH` is for.

If you set `PATH` to `C:/Programs` (where `prog.exe` is located),
then you'll be able to run `prog.exe` from anywhere by typing its file name (`prog.exe`).
The operating system will try to find `prog.exe` in the current directory, 
and if it can't, it will try and look into the directory specified in the `PATH` variable,
aka the path `C:/Programs`, where it will find your program.

`PATH` can be set to a *";"-delimited list of paths*,
which means it can include multiple such directory paths in which it should look for programs,
you just have to separate them with ";".
For example, `C:/Folder1;C:/Folder2`.
When you try to run a program, it will try and look into all of these in order, until it finds the program.

### PATH Examples

For example, if `PATH` is set to `C:/Folder1;C:/Folder2`, with the folders containing:
- `C:/Folder1`:
  - `prog1.exe`
  - `prog2.exe`
- `C:/Folder2`:
  - `prog2.exe`
  - `prog3.exe`
Then running `prog1.exe` in any directory will run the program `prog1.exe` from `C:/Folder1`,
running `prog2.exe` will run the program `prog2.exe` from `C:/Folder1` (because it will find that first),
running `prog3.exe` will run the program `prog3.exe` from `C:/Folder2`,
and running `prog4.exe` will fail to find it.

However, if the path was just `C:/Folder2`, and you stayed in `C:/Folder1` and tried to run `prog2.exe`,
it would run the one in the folder that you're currently in, that is, `C:/Folder1/prog2.exe`,
because the CWD always takes priority over `PATH`.

### Exporting environment variables

The cool thing about environment variables is that they can be overridden for all programs on startup.
This is called exporting the variable.

You can either do that in windows by using their GUI, or by using the
[`setx`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx) command in the CLI.

It can also be modified by programs e.g. on installation.

> If you find that you can't access some command on the command line, even though you know you've installed it,
> it probably means that the directory that this program is inside is not present in the `PATH` variable.
> You just need to find the program, and add the directory it's in to the `PATH` variable.
> It will work everywhere for sure after a system reload.