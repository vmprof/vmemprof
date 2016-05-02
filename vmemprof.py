#!/usr/bin/env python
""" Usage: vmemprof <vmprof.dat>

Run with output of vmprof run with memory profiling (like vmprof.enable(fileno, 0.01, True))
"""

import re, os, json, sys
import vmprof
from flask import Flask, Response, request, escape
app = Flask(__name__)

if len(sys.argv) != 2:
    print __doc__
    sys.exit(1)

stats = vmprof.read_profile(sys.argv[1])

MAX_SOURCEFILE_LEN = 60

def format_stracktrace_line(line):
    if line is None:
        return "<unknown>"
    _, funcname, lineno, sourcefile = line.split(':')
    sourcefile = re.sub('.*/lib/python[\d\.]+/(site-packages/)?', '', sourcefile)
    if len(sourcefile) > MAX_SOURCEFILE_LEN:
        sourcefile = "..." + sourcefile[-(MAX_SOURCEFILE_LEN - 3):]
    return "<span class=stacktrace-line><span>%s</span> <span>%s:%s</span></span>" \
        % (escape(funcname), escape(sourcefile), escape(lineno))

def resample_and_pack(profiles, start, end, window_size):
    next = []
    mem = []
    i = start
    skip = (end - start) / window_size
    while i < end:
        prof = profiles[int(i)]
        stack_trace = "".join([format_stracktrace_line(stats.adr_dict.get(x)) for x in prof[0]])
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
