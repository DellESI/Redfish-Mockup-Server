# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Mockup-Server/LICENSE.md

# redfishMockupServer.py
# v0.9.5
# tested and developed Python 3.4


import urllib
import cgi
import sys
import getopt
import time
import json
import ssl
import posixpath

import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockupServer(BaseHTTPRequestHandler):
    """
    returns index.json file for Server in the specified URL
    """
    server_version = "RedfishMockupHTTPD_v0.9.5"

    TOP_Header = "DFLT_RESPONSE_HEADERS.json"
    SUB_Header = "SUB_HEADERS.json"

        def do_GET(self):
                # for GETs always dump the request headers to the console
                # there is no request data, so no need to dump that
                print("   GET: Headers: {}".format(self.headers))
                sys.stdout.flush()
        self.command_delay(self.command)
        if os.path.isfile(fpath) is True:
                        self.send_response(200)
                self.send_header("Content-type", "application/json,charset=utf-8")
                self.send_header("Additional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))
                        # special cases to test etag for testing
                        # if etag is returned then the patch to these resources should include this etag
                if testEtagFlag is True:
                        if self.path == "/redfish/v1/Systems/1":
                                        self.send_header("Etag", "W/\"12345\"")
                        elif self.path == "/redfish/v1/AccountService/Accounts/1":
                                self.send_header("Etag", "W/\"123456\"")
                        self.end_headers()
                f = open(fpath, "r")
                        self.wfile.write(f.read().encode())
                        f.close()
        elif os.path.isfile(fpathxml) is True:
                        self.send_response(200)
                self.send_header("Content-type", "application/xml,charset=utf-8")
                self.send_header("Additional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))
                        self.end_headers()
                f = open(fpathxml, "r")
                        self.wfile.write(f.read().encode())
                        f.close()
                else:
                        self.send_response(404)
                        self.end_headers()
                        
    def do_HEAD(self):
            print("   HEAD: Headers: {}".format(self.headers))
            if "content-length" in self.headers:
                    len1 = int(self.headers["content-length"])
                    dataa = self.rfile.read(len1)
                    print("   HEAD: Data: {}".format(dataa))

            self.command_delay(self.command)
            self.send_response(200)
            self.send_header("Content-type", "application/json,charset=utf-8")
            self.send_header("Additional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))
            self.end_headers()

        def do_PATCH(self):
                print("   PATCH: Headers: {}".format(self.headers))
            if "content-length" in self.headers:
                    len1 = int(self.headers["content-length"])
                    dataa = self.rfile.read(len1)
                        print("   PATCH: Data: {}".format(dataa))
            self.command_delay(self.command)
            self.send_response(200)
            self.send_header("Content-type", "application/json,charset=utf-8")
            self.send_header("AAdditional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))

                self.end_headers()
                
        def do_POST(self):
                print("   POST: Headers: {}".format(self.headers))
            if "content-length" in self.headers:
                    len1 = int(self.headers["content-length"])
                    dataa = self.rfile.read(len1)
                        print("   POST: Data: {}".format(dataa))

            self.command_delay(self.command)
            self.send_response(200)
            self.send_header("Content-type", "application/json,charset=utf-8")
            self.send_header("Additional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))

                self.end_headers()
                
        def do_DELETE(self):
                print("DELETE: Headers: {}".format(self.headers))
            if "content-length" in self.headers:
                        # Deletes don't have data, so this doesnt execute
                    len1 = int(self.headers["content-length"])
                    dataa = self.rfile.read(len1)
                        print("DELETE: Data: {}".format(dataa))
            self.command_delay(self.command)

            self.send_response(200)
            self.send_header("Content-type", "application/json,charset=utf-8")
            self.send_header("Additional_Headers", self.json_headers(self.TOP_Header, self.SUB_Header))
                
                self.end_headers()
                
        def translate_path(self, path):
                """
                Translate a /-separated PATH to the local filename syntax.
                Components that mean special things to the local file system
                (e.g. drive or directory names) are ignored.  (XXX They should
                probably be diagnosed.)
                """
                # abandon query parameters
                path = path.split('?', 1)[0]
                path = path.split('#', 1)[0]
                path = posixpath.normpath(urllib.unquote(path))
                words = path.split('/')
                words = filter(None, words)
                path = os.getcwd()
                for word in words:
                        drive, word = os.path.splitdrive(word)
                        head, word = os.path.split(word)
                        if word in (os.curdir, os.pardir):
                            continue
                path = os.path.join(path, word)
                return path

    def file_path(self):
        global fpath, tpath, rpath, apath, xpathxml, rfileXml, fpathxml
        rfile = "index.json"
        rfileXml = "index.xml"
        Tfile = "TIME.json"
        if self.path[0] == '/':
            rpath = self.path[1:]
            rpath = rpath.split('?', 1)[0]
            rpath = rpath.split('#', 1)[0]
            apath = self.server.mockDir  # this is the real absolute path to the mockup directory
            # form the path in the mockup of the file
            #      old only support mockup in CWD:  apath=os.path.abspath(rpath)
            fpath = os.path.join(apath, rpath, rfile)
            fpathxml = os.path.join(apath, rpath, rfileXml)
            tpath = os.path.join(apath, rpath, Tfile)

    def command_delay(self, command):
        self.file_path()
        delay_time = responseTime
        if not tflag:
            if dflttimeflag:
                if os.path.isfile(tpath):
                    print("There is a TIME.json in the folder", rpath)
                    sys.stdout.flush()
                    with open(tpath, "r+") as jfile:
                        try:
                            djson = json.load(jfile)
                            delay_time = float(djson.get(self.command + "time", dflttime))
                        except ValueError:
                            delay_time = dflttime
                else:
                    delay_time = dflttime
        time.sleep(delay_time)

    def json_headers(self, top_header_name, sub_header_name):
        TOP_Header_Path = os.path.join(self.server.mockDir, top_header_name)
        SUB_Header_Path = ""
        merged_header = {}
        if self.path[0] == '/':
            rpath = self.path[1:]
            rpath = rpath.split('?', 1)[0]
            rpath = rpath.split('#', 1)[0]
            SUB_Header_Path = os.path.join(self.server.mockDir, rpath, sub_header_name)
        TOP_Header = ""
        SUB_Header = ""
        if os.path.isfile(TOP_Header_Path):  # merging headers
            TOP_Header = json.load(open(TOP_Header_Path))
        if os.path.isfile(SUB_Header_Path):
            SUB_Header = json.load(open(SUB_Header_Path))
        if TOP_Header:
            merged_header = {key: value for key, value in TOP_Header.items()}
        if SUB_Header:
            for (key, value) in SUB_Header.items():
                merged_header[key] = value
        if merged_header:
            return merged_header
        return 'No Additional Header'

def usage(program):
        print("usage: {}   [-h][-P][-H <hostIpAddr>:<port>]".format(program))
        print("      -h --help      # prints usage ")
        print("      -L --Load      # <not implemented yet>: load and Dump json read from mockup in pretty format with indent=4")
        print("      -H <IpAddr>   --Host=<IpAddr>    # hostIP, default: 127.0.0.1")
        print("      -d <responseTime> --dflttime=<executionTime> # time added to respond to any API from Time.json")   # Need to fix
        print("      -P <port>     --Port=<port>      # port:  default is 8000")
        print("      -D <dir>,     --Dir=<dir>        # the to the mockup directory. It may be relative to CWD")
        print("      -T --TestEtag  # etag testing--enable returning etag for certain APIs for testing.  See Readme")
        print("      -t <responseTime> --time=<executionTime> # time added to respond to any API")
        print("-" * 100)
        print("       Exit : ^C <Ctrl+C> ")
        sys.stdout.flush()


def main(argv):
        global  testEtagFlag
        global responseTime, tflag, dflttime, dflttimeflag, timePath, hostname, mockDir
        hostname = "127.0.0.1"
        port = 8000
        load = False
        program = argv[0]
        print(program)
        mockDirPath = os.getcwd()
        mockDir = os.path.realpath(mockDirPath)
        testEtagFlag = False
        responseTime = 0
        tflag = False
        dflttime = 0
        dflttimeflag = False
        tTime = 0
        DirFlag = 0
        
        try:
                opts, args = getopt.getopt(argv[1:], "hLTH:P:D:t:d:", ["help", "Load", "TestEtag", "Host=", "Port=", "Dir=", "time=", "dflttime="])
        except getopt.GetoptError:
                print("Error parsing options")
                sys.stderr.flush()
                usage(program)
                sys.exit(2)

        for opt, arg in opts:
                if opt in ("-h", "--help"):
                        usage(program)
                        sys.exit(0)
                elif opt in ("L", "--Load"):
                        load = True
                elif opt in ("-H", "--Host"):
                        hostname = arg
                elif opt in ("-P", "--Port"):
                        port = int(arg)
                elif opt in ("-D", "--Dir"):
                        DirFlag = 1
                        mockDirPath = arg
                        mockDir = os.path.realpath(mockDirPath)  # creates real full path including path for the arg
                elif opt in ("-T", "--TestEtag"):
                        testEtagFlag = True
                elif opt in ("-t", "--time"):
                        tflag = True
                        tTime = float(arg)
                elif opt in ("-d", "--dflttime"):
                        dflttimeflag = True
                        dflttime = float(arg)
                else:
                        print('unhandled option',)
                        sys.exit(2)

        # check that that -d and -t were not both specified
        if (tflag is True) and (dflttimeflag is True):
                print("ERROR: -t and -d dflttime not valid together here")
                sys.stderr.flush()
                sys.exit(1)

        print('program: ', program)
        sys.stdout.flush()
        print('Hostname:', hostname)
        sys.stdout.flush()
        print('Port:', port)
        sys.stdout.flush()

        if DirFlag:
                print("dir path specified by user:{}".format(mockDirPath))
        else:
                print("dir path specified by user: None")
        sys.stdout.flush()
        
        if tflag:
            responseTime = tTime

        print("Serving Mockup in abs real directory path:{}".format(mockDir))
        sys.stdout.flush()
        # check that we have a valid tall mockup--with /redfish in mockDir before proceeding
        slashRedFishDir = os.path.join(mockDir, "redfish")
        if os.path.isdir(slashRedFishDir) is not True:
                print("ERROR: Invalid Mockup Directory--no /redfish directory at top. Aborting")
                sys.stderr.flush()
                sys.exit(1)

        myServer = HTTPServer((hostname, port), MockupServer)
        # save the test flag, and real path to the mockup dir for the handler to use
        # myServer.socket = ssl.wrap_socket(myServer.socket, "cert.pem", "key.pem", True) #todo add certificate

        myServer.mockDir = mockDir
        myServer.testEtagFlag = testEtagFlag
        myServer.responseTime = responseTime
        # myServer.me="HELLO"
        
        print("Serving Redfish mockup on port: {}".format(port))
        sys.stdout.flush()

        if dflttimeflag:
            print("System Respose default Time is {} seconds".format(dflttime))
        else:
            print("System response time: {} seconds".format(responseTime))
        sys.stdout.flush()

        try:
                myServer.serve_forever()
        except KeyboardInterrupt:
                pass
        myServer.server_close()
        print("Shutting down http server")
        sys.stdout.flush()
        

# the below is only executed if the program is run as a script
if __name__ == "__main__":
        main(sys.argv)
