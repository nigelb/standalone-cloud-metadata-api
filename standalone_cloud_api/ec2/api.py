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

import os, uuid
from standalone_cloud_api.util.keys import find_public_keys
from standalone_cloud_api.util.network import create_api_routes, MetaDataAPIHandler
from StringIO import StringIO
from standalone_cloud_api.util.userdata import create_user_data

EC2_API_ID="EC2"

Route = create_api_routes("Route", EC2_API_ID)

class EC2MetaDataAPI(MetaDataAPIHandler):
    def __init__(self, config):
        MetaDataAPIHandler.__init__(self, config, EC2_API_ID)

    def encode_results(self, request, results):
        return results


class metadata:
    metadata_funcs = []

    def __init__(self, name=None):
        self.name = name

    def __call__(self, fn):
        if self.name is None:
            self.metadata_funcs.append(fn.__name__)
        else:
            self.metadata_funcs.append(self.name)

        return fn

    def methods(self):
        return self.metadata_funcs


@Route("/2009-04-04/meta-data(/*)$")
def list_methods(request):
    toRet = []
    for i in metadata().methods():
        if i is not "":
            toRet.append(i)
    return "\n".join(toRet)


@metadata("instance-id")
@Route("/2009-04-04/meta-data/instance-id")
def instance_id(request):
    return uuid.uuid5(uuid.NAMESPACE_DNS, request.hostname)


@metadata()
@Route("/2009-04-04/meta-data/hostname")
def hostname(request):
    return request.hostname

@metadata("public-keys/")
@Route("/2009-04-04/meta-data/public-keys(/*)$")
def public_key_list(request):
    public_keys = find_public_keys(request)
    ks = public_keys.keys()
    ks.sort()
    out = StringIO()
    for i in range(len(ks)):
        out.write("%s=%s\n"%(i, ks[i]))
    out.flush()
    toRet = out.getvalue()
    out.close()
    return toRet

@Route("/2009-04-04/meta-data/public-keys/(?P<key_number>[0-9]+)/openssh-key")
def public_key(request):
    public_keys = find_public_keys(request)
    ks = public_keys.keys()
    ks.sort()
    return public_keys[ks[int(request.key_number)]]

@Route("/2009-04-04/user-data")
def user_data(request):
    return create_user_data(request)

