# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # python2
from http.server import BaseHTTPRequestHandler, HTTPServer  # python3
import json
import yaml
import time
import cgi
from urllib.parse import parse_qs

def cybercreation():
    print('initializing')
    time.sleep(1)
    print('completed')

class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("received get request")

    def do_POST(self):
        self._set_headers()
        print("in post method")
        #self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        #self.wfile.write(bytes("{\"result\": 200}", "utf-8"))

        # length = int(self.headers.get('content-length'))
        # field_data = self.rfile.read(length)
        # dec = field_data.decode('utf-8')
        # with open(r'/home/ubuntu/POSTADATA.yaml', 'w') as fh:
        #     fh.write(dec)
        # #self.send_response(200)
        # cybercreation()
        # print(str(field_data))

        print(self.headers.get("content-type"))
        content_type, pdict = cgi.parse_header(self.headers.get("content-type"))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
        fields = cgi.parse_multipart(self.rfile, pdict)
        if fields['code'][0].decode('utf-8') == '100':
            with open(r'/home/ubuntu/POSTADATA.yaml', 'w') as fh:
                fh.write(fields['file_yaml'][0].decode('utf-8'))
            #self.wfile.write(bytes('ciao', 'utf-8'))
            self.wfile.write(bytes(json.dumps({'status': 'received', 'code': 100}), 'utf-8'))

        # length = int(self.headers.get('Content-length', 0))
        # body = self.rfile.read(length).decode()
        # params = parse_qs(body)
        # messagecontent = params["message"][0]
        # print(messagecontent)

        self.end_headers()


    def do_PUT(self):
        self.do_POST()


host = ''
port = 8000
HTTPServer((host, port), HandleRequests).serve_forever()

