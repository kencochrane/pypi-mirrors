#!/usr/bin/env python

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    fin = open('/home/dotcloud/output/index.html', "rb")
    start_response(status, response_headers)
    return iter(lambda: fin.read(1024), '')