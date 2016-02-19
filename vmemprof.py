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

def strip(s):
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    l = s.split(":")
    l[3] = ".".join(l[3].split("/")[-2:])
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

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', methods=['GET'])
def index():  # pragma: no cover
    content = get_file('main.html')
    return Response(content, mimetype="text/html")

@app.route('/get_json', methods=['GET'])
def get_json():
    default_size = 800
    x0 = float(request.args.get("x0", "0"))
    x1 = float(request.args.get("x1", len(stats.profiles)))
    content = resample_and_pack(stats.profiles, x0, x1, default_size)    
    return Response(json.dumps(content), mimetype="text/json")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

if __name__ == '__main__':
    app.run(debug=True)
