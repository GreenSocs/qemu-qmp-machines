# arm's virt machine

## 1. Environment setup

See main README at root.

## 2. Generate qmp and dtb configurations

```
make
```

This will generate some `.dtb` and `.qmp` files containing the device
trees and raw qmp lists in the current directory for various number of
cpus.

## 3. Get firmware images

### From lfs fw cache

Will update `./lfs` directory
```
git lfs pull
```

### Compile firmware

```
make fw
```

It will compile a bootloader and generate a kernel using buildroot (takes time...).
See `./Makefile`.

## 4. Run the vps

To use firmware images in the lfs cache:
```
./run.sh [qmp|vanilla] num-cpus
```

Or to use compiled firmware images:
```
FWDIR=output ./run.sh [qmp|vanilla] num-cpus
```

Supported `num-cpus` is 1 or 4. `vanilla` will do a standard qemu run. `qmp` will configure qemu form the _none_ machine.
