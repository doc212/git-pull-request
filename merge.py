#!/usr/bin/env python
"""
Merge a git hub pull request by its number

Copyright (c) 2015 Tuan-Tu Tran

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pygithub3

import sys
import logging
import subprocess
import os
import re
import pygithub3
logging.basicConfig(level=logging.DEBUG)

def shell(cmd, *accepted_codes):
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out,err=p.communicate()
    if p.returncode!=0 and p.returncode not in accepted_codes:
        raise RuntimeError, ("shell error",cmd,p.returncode, accepted_codes)
    return out

def githubConfig(key):
    item = shell("git config github."+key, 1)
    if not item:
        logging.error("github."+key+" is not configured")
        sys.exit(1)
    return item.strip()
logging.debug(sys.argv)

login = githubConfig("login")
password = githubConfig("password")
repo = githubConfig("repo")

prNumber = int(sys.argv[1])

g=pygithub3.Github(login=login, password=password, user=login, repo=repo)
pr=g.pull_requests.get(prNumber)

msgFile = "/tmp/githubprmsg%s"%prNumber
if not os.path.exists(msgFile):
    with open(msgFile,"w") as fh:
        fh.write("\n\n#enter a message to merge pull request #%s\n"%pr.number)
        fh.write("#from %s into %s\n"%(pr.head["ref"], pr.base["ref"]))
        fh.write("\n#an empty message will abort the merge\n")
shell("gvim %s"%msgFile)
lines=[]
with open(msgFile) as fh:
    for l in fh:
        if not l.startswith("#"):
            lines.append(l)
msg="".join(lines).strip()
if msg!="":
    g.pull_requests.merge(prNumber, msg)
    os.remove(msgFile)
else:
    logging.warn("aborting because of empty msg")
    sys.exit(1)
