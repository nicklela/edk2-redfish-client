# Copyright Notice:
#
# Copyright (c) 2019, Intel Corporation. All rights reserved.<BR>
# Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause-Patent
#
# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Profile-Simulator/blob/master/LICENSE.md

# This program is dependent on the following Python packages that should be installed separately with pip:
#    pip install Flask
#
# standard python packages
import sys
import getopt
import os
import functools
import flask
import werkzeug

rfVersion = "0.9.6"
rfProgram1 = "redfishProfileSimulator"
rfProgram2 = "                "
rfUsage1 = "[-Vh]  [--Version][--help]"
rfUsage2 = "[-H<hostIP>] [-P<port>] [-C<cert>] [-K<key>] [-p<profile_path>]"
rfUsage3 = "[--Host=<hostIP>] [--Port=<port>] [--Cert=<cert>] [--Key=<key>] [--profile_path=<profile_path>]"


def rf_usage():
        print("Usage:")
        print("  ", rfProgram1, "  ", rfUsage1)
        print("  ", rfProgram1, "  ", rfUsage2)
        print("  ", rfProgram2, "  ", rfUsage3)


def rf_help():
        print(rfProgram1,"implements a simulation of a redfish service for the \"Simple OCP Server V1\" Mockup.")
        print(" The simulation includes an http/https server, RestEngine, and dynamic Redfish datamodel.")
        print(" You can GET, PATHCH,... to the service just like a real Redfish service.")
        print(" Both Basic and Redfish Session/Token authentication is supported (for a single user/passwd and token")
        print("    the user/passwd is:   root/password123456.    The authToken is: 123456SESSIONauthcode")
        print("    these can be changed by editing the redfishURIs.py file.  will make dynamic later.")
        print(" The http/https service and Rest engine is built on Flask, and all code is Python 3.4+")
        print(" The data model resources are \"initialized\" from the SPMF \"SimpleOcpServerV1\" Mockup.")
        print("     and stored as python dictionaries--then the dictionaries are updated with patches, posts, deletes.")
        print(" The program can be extended to support other mockup \"profiles\".")
        print("")
        print(" By default, the simulation runs over http, on localhost (127.0.0.1), on port 5000.")
        print(" These can be changed with CLI options: -P<port> -C<cert> -K<key> -H <hostIP> | --port=<port> --Cert=<cert> --Key=<key> --host=<hostIp>")
        print(" -C<cert> -K<key> | --Cert=<cert> --Key=<key> options must be used together with port 443 to enable https session.")
        print("")
        print("Version: ", rfVersion)
        rf_usage()
        print("")
        print("       -V,          --Version,                       --- the program version")
        print("       -h,          --help,                          --- help")
        print("       -H<hostIP>,  --Host=<hostIp>                  --- host IP address. dflt=127.0.0.1")
        print("       -P<port>,    --Port=<port>                    --- the port to use. dflt=5000")
        print("       -C<cert>,    --Cert=<cert>                    --- Server certificate.")
        print("       -K<key>,     --Key=<key>                      --- Server key.")
        print("       -p<profile_path>, --profile=<profile_path>    --- the path to the Redfish profile to use. "
              "dflt=\"./MockupData/SimpleOcpServerV1\" ")

# Conditional Requests with ETags
# http://flask.pocoo.org/snippets/95/
def conditional(func):
    '''Start conditional method execution for this resource'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        flask.g.condtnl_etags_start = True
        return func(*args, **kwargs)
    return wrapper

class NotModified(werkzeug.exceptions.HTTPException):
    code = 304
    def get_response(self, environment):
        return flask.Response(status=304)

class PreconditionRequired(werkzeug.exceptions.HTTPException):
    code = 428
    description = ('<p>This request is required to be '
                   'conditional; try using "If-Match".')
    name = 'Precondition Required'
    def get_response(self, environment):
        resp = super(PreconditionRequired,
                     self).get_response(environment)
        resp.status = str(self.code) + ' ' + self.name.upper()
        return resp

def main(argv):
    #Monkey patch the set_etag() method for conditional request.
    _old_set_etag = werkzeug.wrappers.Response.set_etag
    @functools.wraps(werkzeug.wrappers.Response.set_etag)
    def _new_set_etag(self, etag, weak=False):
        # only check the first time through; when called twice
        # we're modifying
        if (hasattr(flask.g, 'condtnl_etags_start') and
                                   flask.g.condtnl_etags_start):
            if flask.request.method in ('PUT', 'DELETE', 'PATCH'):
                if not flask.request.if_match:
                    raise PreconditionRequired
                if etag not in flask.request.if_match:
                    flask.abort(412)
            elif (flask.request.method == 'GET' and
                  flask.request.if_none_match and
                  etag in flask.request.if_none_match):
                raise NotModified
            flask.g.condtnl_etags_start = False
        _old_set_etag(self, etag, weak)
    werkzeug.wrappers.Response.set_etag = _new_set_etag

    # set default option args
    rf_profile_path = os.path.abspath("./MockupData/SimpleOcpServerV1")
    rf_host = "0.0.0.0"
    rf_port = 5000
    rf_cert =""
    rf_key=""

    try:
        opts, args = getopt.getopt(argv[1:], "VhH:P:C:K:p:",
                                   ["Version", "help", "Host=", "Port=", "Cert=", "Key=", "profile="])
    except getopt.GetoptError:
        print(rfProgram1, ":  Error parsing options")
        rf_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            rf_help()
            sys.exit(0)
        elif opt in ("-V", "--Version"):
            print("Version:", rfVersion)
            sys.exit(0)
        elif opt in ("-p", "--profile"):
            rf_profile_path = arg
        elif opt in "--Host=":
            rf_host = arg
        elif opt in "--Port=":
            rf_port=int(arg)
        elif opt in "--Cert=":
            rf_cert=arg
        elif opt in "--Key=":
            rf_key=arg
        else:
            print("  ", rfProgram1, ":  Error: unsupported option")
            rf_usage()
            sys.exit(2)

    if rf_port == 443:
        if rf_cert == "" or rf_key == "":
            print("  ", rfProgram1, ":  Error: port 443 must be used together with -C<cert> and -K<key> to enable https session")
            sys.exit(2)
    else:
        if rf_cert != "" or rf_key != "":
            print("  ", rfProgram1, ":  Error: -C<cert> and -K<key> options must be used together with port 443 to enable https session")
            sys.exit(2)

    print("{} Version: {}".format(rfProgram1,rfVersion))
    print("   Starting redfishProfileSimulator at:  hostIP={},  port={}".format(rf_host, rf_port))
    print("   Using Profile at {}".format(rf_profile_path))

    if os.path.isdir(rf_profile_path):
        # import the classes and code we run from main.
        from v1sim.serviceVersions import RfServiceVersions
        from v1sim.serviceRoot import RfServiceRoot
        # rfApi_SimpleServer is a function in ./RedfishProfileSim/redfishURIs.py.
        # It loads the flask APIs (URIs), and starts the flask service
        from v1sim.redfishURIs import rfApi_SimpleServer

        # create the root service resource
        root_path = os.path.normpath("redfish/v1")

        # create the version resource for GET /redfish
        versions = RfServiceVersions(rf_profile_path, "redfish")
        root = RfServiceRoot(rf_profile_path, root_path)

        # start the flask REST API service
        rfApi_SimpleServer(root, versions, host=rf_host, port=rf_port, cert=rf_cert, key=rf_key)
    else:
        print("invalid profile path")


if __name__ == "__main__":
    main(sys.argv)




    #http://127.0.0.1:5000/

    #app.run(host="0.0.0.0") # run on all IPs
    #run(host=None, port=None, debug=None, **options)
    #   host=0.0.0.0 server avail externally -- all IPs
    #   host=127.0.0.1 is default
    #   port=5000 default, or port defined in SERVER_NAME config var



