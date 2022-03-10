
Archlinux's notes.

## SiFive's RiscvV toolchain

We cannot compile [freedom-tools](https://github.com/sifive/freedom-tools)
directecly. As of v2020.12.0 version, this gcc cannot be compiled by gcc11
(first issue is about the lto-plugin configure, see [1])

In order to compile a toolchain equivalent to the one in
[freedom-tools](https://github.com/sifive/freedom-tools). The multilib
generator and configure parameters need to be updated to allow more
combinations (this come from freedomtools's Makefile).

Using the ubuntu [prebuilt toolchain](https://github.com/sifive/freedom-tools/releases/tag/v2020.12.0)
works.

## SiFive's freedom-e-sdk python

With too recent versions of python, freedom-e-sdk fails to setup its
environment (issues with ast module).

A solution is to use pyenv and defining a python version v3.7.7 for this
directory.
```
pyenv install 3.7.7
pyenv local 3.7.7
```

Note: 3.8.7 seems to work too, but 3.7.7 is the version shipped with the
sifive v2020.12.0 toolchain.
