#!/usr/bin/env python3
#
# Copyright (C) Greensocs 2022
#
# SPDX-License-Identifier: MIT

import os
import sys
import argparse
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))
import qmpgen

def _expand_yaml_cmd(entry):
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
        cmds.append(_expand_yaml_cmd(entry))
    return cmds

parser = argparse.ArgumentParser(description='Convert qmp command formats',
                                 parents=(qmpgen.parser,))

parser.add_argument('input', nargs='?',
                    help='input file (stdin if not present)')

args = parser.parse_args()

if args.input:
    with open(args.input) as filein:
        cmds = read_short_yaml(filein)
else:
    cmds = read_short_yaml(sys.stdin)
qmpgen.load_commands(cmds)

qmpgen.conf_from_parser(args)
qmpgen.dump_commands()
