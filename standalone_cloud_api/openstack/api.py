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

import uuid, json
from standalone_cloud_api.util.keys import find_public_keys
from standalone_cloud_api.util.network import create_api_routes, MetaDataAPIHandler

OPENSTACK_API_ID="Openstack"

Route = create_api_routes("Route", OPENSTACK_API_ID)

class OpenstackMetaDataAPI(MetaDataAPIHandler):
    def __init__(self, config):
        MetaDataAPIHandler.__init__(self, config, OPENSTACK_API_ID)

    def encode_results(self, request, results):
        if request.request_url.endswith(".json"):
            self.set_header("Content-Type","application/json")
            return json.dumps(results)
        return results

@Route("/openstack/2012-08-10/uuid(.json)*")
def instance_id(request):
    return uuid.uuid5(uuid.NAMESPACE_DNS, hostname(request)).__str__()

@Route("/openstack/2012-08-10/availability_zone")
def availability_zone(request):
    return request.api_config.default_availability_zone

@Route("/openstack/2012-08-10/hostname")
def hostname(request):
    return request.hostname

@Route("/openstack/2012-08-10/launch_index")
def launch_index(request):
    return request.api_config.launch_index

@Route("/openstack/2012-08-10/meta")
def meta(request):
    return request.api_config.get_machine_meta_data(request.machine_id)

@Route("/openstack/2012-08-10/public_keys")
def public_keys(request):
    return find_public_keys(request)

@Route("/openstack/2012-08-10/name")
def name(request):
    return hostname(request)


@Route("/openstack/2012-08-10/meta_data.json")
def meta_data(request):
    return {
        "uuid":              instance_id(request),
        "availability_zone": availability_zone(request),
        "hostname":          hostname(request),
        "launch_index":      launch_index(request),
        "meta":              meta(request),
        "public_keys":       public_keys(request),
        "name":              name(request)
    }