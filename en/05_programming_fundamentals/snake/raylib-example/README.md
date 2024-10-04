# Raylib-Quickstart
A simple cross platform template for setting up a project with the bleeding edge raylib code.
Works with C or C++.

## Supported Platforms
Quickstart supports the main 3 desktop platforms
* Windows
* Linux
* MacOS

# VSCode Users (all platforms)
* Download the quickstart
* Rename the folder to your game name
* Open the folder in VSCode.
* Press F5 to build
* You are good to go.

# Windows Users
There are two compiler toolchains avialble for windows, MinGW-W64 (a free compiler using GCC), and Microsoft Visual Studio
## Using MinGW-W64
* Double click the build-MinGW-W64.bat file.
* cd into the folder in your terminal
* run make
* You are good to go

### Note on MinGW-64 versions
Make sure you have a modern version of MinGW-W64 (not mingw).
The best place to get it is from the W64devkit from
https://github.com/skeeto/w64devkit/releases
or the version installed with the raylib installer


## Microsoft Visual Studio
* Run the build-VisualStudio2022.bat
* double click the .sln file that is geneated.
* develop your game
* you are good to go.

# Linux Users

* CD into the build folder
* Install premake:
    - Download the zip from [here](https://premake.github.io/download/)
    - Unzip the file in `~/.premake`: `tar -xf zip-file-name.tar.gz`
    - Add the directory to your shell config, e.g. add `export PATH="$PATH:$HOME/.premake"` to .zshrc
* run `premake5 gmake2`
* CD back to the root
* run `make`
* you are good to go

If you want Clangd LSP support, you need to generate `compile_commands.json`. For this:

1. Install plugin for premake that does this for each target:
```
cd ~/.premake
git clone https://github.com/tarruda/premake-export-compile-commands
```

2. Go back to the build folder.

3. Run `premake5 export-compile-commands`

4. Copy the target you want to use for the LSP:
```
cd ..
cp compile_commands/debug_x64.json compile_commands.json
```

5. Restart the LSP.

# MacOS Users
* CD into the build folder
* Install premake
* run `premake5.osx gmake2`
* CD back to the root
* run `make`
* you are good to go

# Output files
The built code will be in the bin dir

# Working directories and the resources folder
The example uses a utility function from path_utils.h that will find the resources dir and set it as the current working directory. This is very useful when starting out. If you wish to manage your own working directory you can simply remove the call to the function and the header.

# Using your own code
Simply remove src/main.c and replace it with your code, and re-run the steps above and do a clean build.

# Building for other OpenGL targets
If you need to build for a different OpenGL version than the default (OpenGL 3.3) you can specify an openGL version in your premake command line. Just modify the bat file or add the following to your command line

## For OpenGL 1.1
--graphics=opengl11

## For OpenGL 2.1
--graphics=opengl21

## For OpenGL 4.3
--graphics=opengl43

## For OpenGLES 2.0
--graphics=opengles2

## For OpenGLES 3.0
--graphics=opengles3

# License
Copyright (c) 2020-2024 Jeffery Myers

This software is provided "as-is", without any express or implied warranty. In no event 
will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial 
applications, and to alter it and redistribute it freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not claim that you 
  wrote the original software. If you use this software in a product, an acknowledgment 
  in the product documentation would be appreciated but is not required.

  2. Altered source versions must be plainly marked as such, and must not be misrepresented
  as being the original software.

  3. This notice may not be removed or altered from any source distribution.
