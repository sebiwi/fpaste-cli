#!/usr/bin/env python

import argparse
import requests
from subprocess import Popen, PIPE
import sys

class FPaste:

    fpaste_api = "http://www.fpaste.org/"
    
    def __init__(self):
        self.data = []
    
    def post_code(self, paste_data):
        payload = (('paste_lang', 'text'), ('mode', 'json'), ('paste_data', paste_data), ('api_submit', 'true'))
        request = requests.get(self.fpaste_api, params=payload)
        return self.fpaste_api + request.json()['result']['id']

def copy_text(text):
    
    cb_name = get_clipboard_name()
    
    if cb_name is not None:
        clipboard = Popen(cb_name, shell=True, stdin=PIPE).stdin
        clipboard.write(text)
        clipboard.close()

def get_clipboard_name():

    cb_list = ['pbcopy', 'xclip', 'putclip']

    cb_name = None
    for cb in cb_list:
        if cli_exists(cb):
            cb_name = cb
            break

    return cb_name


def cli_exists(command):

    exists = False
    test = 'type %s >> /dev/null 2>&1' % command
    process = Popen(test, shell=True, stdout=PIPE)
    process.stdout.close()
    if not process.wait():
        exists = True

    return exists

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filename",help="Upload the specified file, instead of stdin")
    args = parser.parse_args()
 
    if args.filename is not None:
        code = open(args.filename, 'r')
    else:
        code = sys.stdin

    fpaste = FPaste()
    
    copy_text(fpaste.post_code(code.read()))
    code.close()
        
if __name__ == "__main__": 
    main()
