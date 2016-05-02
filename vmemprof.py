#!/usr/bin/env python
""" Usage: vmemprof <vmprof.dat>

Run with output of vmprof run with memory profiling (like vmprof.enable(fileno, 0.01, True))
"""

import vmprof
import os, json, sys
from flask import Flask, Response, request
app = Flask(__name__)

if len(sys.argv) != 2:
    print __doc__
    sys.exit(1)

stats = vmprof.read_profile(sys.argv[1])

MAX = 60

def strip(s):
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    l = s.split(":")
    if len(l[3]) > MAX:
        l[3] = "..." + l[3][-(MAX - 3):]
    l[1] = "<b>" + l[1] + "</b>"
    return "%s %s:%s" % (l[1], l[3], l[2])

def resample_and_pack(profiles, start, end, window_size):
    next = []
    mem = []
    i = start
    skip = (end - start) / window_size
    while i < end:
        prof = profiles[int(i)]
        stack_trace = "<br/>".join([strip(stats.adr_dict.get(x, '<unknown>')) for x in prof[0]])
        mem.append((i, prof[3], stack_trace))
        i += skip
    return {'mem': mem}

@app.route('/get_json', methods=['GET'])
def get_json():
    default_size = 800
    x0 = float(request.args.get("x0", "0"))
    x1 = float(request.args.get("x1", len(stats.profiles)))
    content = resample_and_pack(stats.profiles, x0, x1, default_size)    
    return Response(json.dumps(content), mimetype="text/json")

@app.route('/')
def get_resource():  # pragma: no cover
    return app.send_static_file('main.html')

if __name__ == '__main__':
    app.run(debug=True)
