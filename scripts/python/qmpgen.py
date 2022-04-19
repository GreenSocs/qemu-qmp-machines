#
# QEMU Monitor Protocol dump tool
#
# Copyright Greensocs 2022
#
# SPDX-License-Identifier: MIT

import json
import argparse

parser = argparse.ArgumentParser(description="QMP generator", add_help=False)
parser.add_argument('--output', '-o', help='output file (default: stdout)')
parser.add_argument('--mode', '-m', choices=('qmpshell','raw'),
                    default='qmpshell',
                    help='output format')

class QmpGen:
    def __init__(self, commands=None):
        if commands is None:
            commands = []
        self.load(commands)

    def load(self, commands):
        self._commands = commands

    def append(self, command):
        self._commands.append(command)

    def set_output_file(self, file):
        self.output = file

    def set_output_mode(self, mode):
        self.mode = mode

    def conf_from_parser(self, args):
        if args.output is None:
            import sys
            self.set_output_file(sys.stdout)
        else:
            self.set_output_file(open(args.output, 'wt'))
        self.set_output_mode(args.mode)

    def _write_qmpshell(self, file):
        # qmpshell format: cmdname key1=val1 ke2=val2 ...
        for cmd in self._commands:
            line = str(cmd['execute'])
            if 'arguments' in cmd:
                args = cmd['arguments']
                args = [f"{k}={args[k]}" for k in args.keys()]
                line = ' '.join([line] + args)
            print(line, file=file)

    def _write_raw(self, file):
        # raw qmp format
        for cmd in self._commands:
            print(json.dumps(cmd), file=file)

    def _write_file(self, mode, file):
        if mode == "qmpshell":
            self._write_qmpshell(file)
        elif mode == "raw":
            self._write_raw(file)
        else:
            raise ValueError(f"incorrect mode {mode}")

    def dump(self):
        self._write_file(self.mode, self.output)

_qmpgen = QmpGen()

def conf_from_parser(args):
    _qmpgen.conf_from_parser(args)

def load_commands(commands):
    _qmpgen.load(commands)

def append_command(command):
    _qmpgen.append(command)

def dump_commands():
    _qmpgen.dump()

def execute(cmd, **kwargs):
    entry = {'execute' : cmd }
    if len(kwargs) != 0:
        entry['arguments'] = kwargs
    _qmpgen.append(entry)

def qom_set(path, prop, value):
    execute('qom-set', path=path, property=prop, value=value)

def device_add(driver, devid, **props):
    args = {'driver': driver, 'id': devid}
    args.update(props)
    execute('device_add', **args)
    return devid

def sysbus_mmio_map(device, addr, mmio=None, alias=False, size=None, offset=None):
    args = {'device': device, 'addr': addr}
    if mmio is not None:
        args['mmio'] = mmio
    if alias:
        args['alias'] = True
        if offset is not None:
            args['offset'] = offset
        if size is not None:
            args['size'] = size
    else:
        if offset is not None:
            raise ValueError('offset only allowed when aliasing')
        if size is not None:
            raise ValueError('size only allowed when aliasing')
    execute('sysbus-mmio-map', **args)

def exit_preconfig():
    execute('x-exit-preconfig')

