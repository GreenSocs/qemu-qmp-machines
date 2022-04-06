#!/usr/bin/env python
#
# Copyright (C) Greensocs
#

import sys
import argparse
import yaml
import json

parser = argparse.ArgumentParser(description='Convert qmp command formats')

parser.add_argument('--mode', '-m', choices=('qmpshell','raw'),
                    default='qmpshell',
                    help='output format')
parser.add_argument('input', nargs='?',
                    help='input file (stdin if not present)')
parser.add_argument('--output', '-o',
                    help='output file (stdout if not present)')

args = parser.parse_args()

def expand_yaml_cmd(entry):
    if isinstance(entry, str):
        return { 'execute': entry }
    elif not isinstance(entry, dict) or len(entry.keys()) != 1:
        raise ValueError(f'Bad command format: `{entry}`')
    cmd = list(entry.keys())[0]
    args = entry[cmd]
    if args is None:
        return { 'execute': cmd }
    if not isinstance(args, dict):
        raise ValueError(f'Bad arguments format in `{entry}`')
    return { 'execute': cmd, 'arguments': args }

def read_short_yaml(filein):
    entries = yaml.safe_load(filein)
    if not isinstance(entries, list):
        raise ValueError('Expected a yaml list of commands')
    cmds = []
    for entry in entries:
        cmds.append(expand_yaml_cmd(entry))
    return cmds

def write_qmpshell(cmds, file):
    # qmpshell format: cmdname key1=val1 ke2=val2 ...
    for cmd in cmds:
        line = str(cmd['execute'])
        if 'arguments' in cmd:
            args = cmd['arguments']
            args = [f"{k}={args[k]}" for k in args.keys()]
            line = ' '.join([line] + args)
        print(line, file=file)

def write_raw(cmds, file):
    # raw qmp format
    for cmd in cmds:
        print(json.dumps(cmd), file=file)


def write_output(cmds, mode, file):
    if mode == "qmpshell":
        write_qmpshell(cmds, file)
    elif mode == "raw":
        write_raw(cmds, file)
    else:
        raise ValueError(f"incorrect mode {mode}")

if args.input:
    with open(args.input) as filein:
        cmds = read_short_yaml(filein)
else:
    cmds = read_short_yaml(sys.stdin)

fileout = sys.stdout
if args.output:
    fileout = open(args.output, mode='wt')
with fileout:
    write_output(cmds, args.mode, fileout)
