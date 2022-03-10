#!/usr/bin/env python
#
# Copyright (C) Greensocs
#

import sys
import argparse
import yaml

parser = argparse.ArgumentParser(description='Convert yaml array of qapi commands to qmp-shell format')

parser.add_argument('input', nargs='?')
parser.add_argument('--output', '-o')

args = parser.parse_args()

def print_cmd(name, args = None, file=sys.stdout):
    if args is None:
        args = []
    else:
        args = [ k + f"={args[k]}" for k in args.keys()]
    print(' '.join([name] + args), file=file)

def gen(cmds, file=sys.stdout):
    if not isinstance(cmds, list):
        raise TypeError('Expected a list of commands')
    for entry in cmds:
        if isinstance(entry, str):
            name = entry
            args = None
        elif isinstance(entry, dict) and len(entry.keys()) == 1:
            name = list(entry.keys())[0]
            args = entry[name]
        else:
            raise ValueError(f'Bad command format: `{entry}`')
        if args is None:
            pass
        elif not isinstance(args, dict):
            raise ValueError(f'Bad arguments format in `{entry}`')
        print_cmd(name, args, file=file)

if args.input:
    with open(args.input) as filein:
        cmds = yaml.safe_load(filein)
else:
    cmds = yaml.safe_load(sys.stdin)

if args.output:
    with open(args.output, mode='wt') as fileout:
        gen(cmds, fileout)
else:
    gen(cmds)
