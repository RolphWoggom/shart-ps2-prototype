# Simpsons: Hit and Run PS2 Prototype

This prototype was shared by [MattJ155](https://hiddenpalace.org/MattJ155), many thanks to him!

It can be downloaded from [Hidden Palace](https://hiddenpalace.org/The_Simpsons:_Hit_%26_Run_(Jul_10,_2003_prototype))
([direct download link](https://hiddenpalace.org/w/images/c/c3/The_Simpsons_-_Hit_and_Run_%28Jul_10%2C_2003_prototype%29.7z))
or from the [GitHub backup](https://github.com/RolphWoggom/shart-ps2-prototype/releases/tag/download)
([direct download link](https://github.com/RolphWoggom/shart-ps2-prototype/releases/download/download/The_Simpsons_-_Hit_and_Run_.Jul_10._2003_prototype.7z)).

The 7z archive contains a iso disc image, both can be extracted using the 7z tool:

```
$ wget https://hiddenpalace.org/w/images/c/c3/The_Simpsons_-_Hit_and_Run_%28Jul_10%2C_2003_prototype%29.7z
$ 7z x "The_Simpsons_-_Hit_and_Run_(Jul_10,_2003_prototype).7z"
$ 7z x -odata "Simpsons Hit and Run July 2003 10.07.2003.iso"
```

The disc contents can then be found in the `data` folder. Everything but the game assets (.RCF files) is included in this repo.

## Linker Map

The `SRR2.MAP` file is a linker map created with GCC 2.95.3.
GCC 2.x used a custom mangling scheme before switching to the Itanium ABI with GCC 3.x.
Support for demangling GCC 2.x mangled names was removed in GCC 9, an easy way to get GCC 8 is to use Docker:

```
$ sudo docker run --rm -v "$PWD":/workdir -w /workdir gcc:8 /bin/bash -c 'cat data/SRR2.MAP | c++filt >demangled.map'
```

The demangled map can be then found in the `demangled.map` file.

