#A standalone implementation of some cloud metadata APIs to test VM images against.
#Copyright (C) 2013  NigelB
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict
import os, sys, socket, subprocess, re, scma_hostnames
from standalone_cloud_api.util import config_helper

def get_dns_name(ip_addr):
    try:
        return socket.gethostbyaddr(ip_addr)[0]
    except:
        return None

def get_hostname(machine_id, machine_identity_order):
    hostname = None
    for mido in machine_identity_order:
        if mido in machine_id and machine_id[mido] is not None and machine_id[mido] in scma_hostnames.static_hostnames:
            return scma_hostnames.static_hostnames[machine_id[mido]]
    if hostname is None:
        hostname = scma_hostnames.generate_hostname(machine_id, machine_identity_order)
    if hostname is None:
        hostname = machine_id.get_ip_address
    return hostname

def get_ip_address(ip_addr):
    return ip_addr

def get_mac_address(ip_addr):
    """
    Gets the MAC address of the give ip address.
    May require the following:
        #root> setcap cap_net_raw+ep `which arping`
    """
    import network_settings
    try:
        try:
            subprocess.check_output(["ping", "-c", "1", ip_addr])
        except: pass
        for i in subprocess.check_output(["/sbin/arp", "-n"]).split("\n"):
            if "(incomplete)" not in i and i.startswith(ip_addr):
                return i.split()[2]
    except Exception, e:
        sys.stderr.write("Error getting MAC address with ping/arp, trying arping. Details: \n")
        sys.stderr.write(e.message)
        sys.stderr.write("\n")

    try:
        if "arping_interface" in network_settings.__dict__:
            output = subprocess.check_output(["arping", "-c", "1", "-I", network_settings.arping_interface, ip_addr])
        else:
            output = subprocess.check_output(["arping", "-c", "1", ip_addr])
    except Exception, e:
        msg="Could not get MAC address of %s\n"%ip_addr
        sys.stderr.write(msg)
        sys.stderr.write(e.message)
        return None
    m = re.search(".*\[(.*)\].*", output)
    if m is not None:
        return m.group(1)
    return None

def identify_machine(ip_addr, order=("get_mac_address", "get_dns_name", "get_ip_address")):
    _current = globals()
    toRet = {}
    for name in order:
        if name in _current:
            toRet[name] = _current[name](ip_addr)
    return toRet

all_route = {}

def create_api_routes(name, api_name):
    global all_route
    def __init__(self, _route=None):
        if _route is not None:
            self.path = _route
            self.route_order.append(_route)
            self.__class__.route_order = sorted(self.route_order, lambda x,y: len(y) - len(x))

    def __call__(self, fn):
        self.routes[self.path] = fn
        return fn


    def route_request(self, uri):
        for r in self.route_order:
            m = re.match(r, uri)
            if m:
                return self.routes[r], m.groupdict()
        return None, None

    class_dict = {
        "__init__":__init__,
        "__call__":__call__,
        "route_request":route_request,
        "routes" : {},
        "route_order" : [],
        "api_name":api_name
    }
    toRet =  type(name, (), class_dict)
    all_route[api_name] = toRet
    return toRet

def get_api_routes(api_name):
    global all_route
    return all_route[api_name]


class MetaDataAPIHandler:
    def __init__(self, config, api):
        self.config = config
        self.api = api
        self.headers = defaultdict(list)
        self.set_header("Content-Type", "text/html")

    def clear_header(self, key):
        if key in self.headers:
            del self.headers[key]

    def set_header(self, key, value):
        if key in ["Content-Type"]:
            self.clear_header(key)
        self.headers[key].append(value)

    def encode_results(self, request, results):
        raise Exception("Not Implemented")

    def handle(self):
        uri = os.environ['REQUEST_URI']
        Route = get_api_routes(self.api)
        routing = Route()
        method, request_values = routing.route_request(re.sub("/+", "/", uri))

        if method is None:
            self.set_header("Content-Type","text/plain")
            self.__render_output(501, "HTTP/1.1 501 Not Implemented")
            sys.exit(501)
        else:
            if self.config.SCMA_ENABLE_CGITB:
                self.__handle_request(uri, method, request_values)
            else:
                try:
                    self.__handle_request(uri, method, request_values)
                except Exception, e:
                    print >> sys.stderr, "Error processing request:"
                    print >> sys.stderr, "    %s"%e.message
                    self.set_header("Content-Type","text/plain")
                    self.__render_output(503, "HTTP/1.1 503 Service Unavailable")
                    sys.exit(503)

    def __handle_request(self, uri, method, request_values):
        remote_addr = os.environ['REMOTE_ADDR']
        machine_id = identify_machine( remote_addr, self.config.machine_identity_order)
        request = config_helper({
            "machine_id": machine_id,
            "api_config": self.config,
            "request_url": uri,
            "remote_addr": remote_addr,
            "hostname":get_hostname(machine_id, self.config.machine_identity_order),
            "set_header": lambda key, value: self.set_header(key, value)
        })
        for i in request_values:
            if i not in request:
                request[i] = request_values[i]
        results = method(request)
        self.__render_output(200, self.encode_results(request, results))

    def __render_output(self, status, content):
        print "Status:%s"%status
        for header in self.headers:
            for header_val in self.headers[header]:
                print "%s: %s"%(header, header_val)
        print ""
        print content
