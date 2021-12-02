#!/bin/env python3
####################################################################################################
## File Name     :  epy
## Author        :  Yuliang Tao(nerotao@foxmail.com)
## Created At    :  9/30/2021 4:06:32 PM
## Last Modified :  11/30/2021 4:38:33 PM
##
####################################################################################################
## Description   :  epython command line
##
####################################################################################################
## Change History:  R0.1 2021-09-30 | Initial creation.
##                  R0.2 2021-11-30 | Add yaml and param file option.
##
####################################################################################################

import argparse
import os
import re
import sys
import yaml
from epython import ePython


def parse_cli_args():
    """Parse command-line args"""
    parser = argparse.ArgumentParser(prog='python3 {}'.format(sys.argv[0]),
                                     description="Embedded python")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
    parser.add_argument('-y', '--yaml', type=str,nargs='+', help='Read yaml file as python variables')
    parser.add_argument('-p', '--param', type=str, nargs='+', help='Read param (NAME=VALUE) py file as python variables')
    parser.add_argument('-d', '--define', type=str, nargs='+', help='Define python variable, format is NAME=VALUE')
    parser.add_argument('-D', '--setenv', type=str, nargs='+', help='Define environment variable, format is NAME=VALUE')
    parser.add_argument('-x', '--debug', action='store_true', default=False, help='Enable debug')
    parser.add_argument('-c', '--cache', action='store_true', default=False, help='Enable cache for preprocessed file')
    parser.add_argument('--delimiter', type=str, default='%', help='Specify the code delimiter, default is %%')
    parser.add_argument('--indent', type=int, default=2, help='Python code indent spaces, default is 2')
    return parser.parse_args()


def gen_var_dict(args):
    """Generate variable dict for epy parsing"""

    var_dict = {}
    if args.define:
        for var_pair in args.define:
            var, val = var_pair.split('=', 1)
            var_dict[var] = val

    if args.setenv:
        for var_pair in args.setenv:
            var, val = var_pair.split('=', 1)
            os.environ[var] = val

    if args.yaml:
        for yaml_file in args.yaml:
            with open(yaml_file, 'r') as yml:
                var_dict.update(yaml.safe_load(yml))

    return var_dict


def gen_param_src(args):
    """"Generate prepend source code from py param files"""

    if not args.param:
        return None
    prepend_src = ['<% import os', 'import sys']
    for param_file in args.param:
        if not os.path.exists(param_file):
            print(f"[Warning]: {param_file} doesn't exist, will ignore it")
            continue
        param_file_name, param_file_ext = os.path.basename(param_file).split('.')
        if param_file_ext not in ('py', 'pyc'):
            print(f'[Warning]: {param_file} is not a python file, will ignore it')
            continue
        param_file_dirname = os.path.dirname(os.path.abspath(param_file))
        prepend_src.append(f"sys.path.append('{param_file_dirname}')")
        prepend_src.append(f"from {param_file_name} import *")
    prepend_src.append('%>')
    return '\n'.join(prepend_src)
 

def main():
    args = parse_cli_args()
    epython = ePython(filename=args.input, cache=args.cache, delim=args.delimiter, indentspace=args.indent)
    # import param files
    epython.prepend_src(gen_param_src(args))
    # render with input variables
    with open(args.output, 'w') as out:
        out.writelines(epython.render(gen_var_dict(args)))
    # enable debug output
    if args.debug:
        print(epython.pysrc)


if __name__ == '__main__':
    main()