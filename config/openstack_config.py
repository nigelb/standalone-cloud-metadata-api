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

openstack_metadata_api_enabled = True

userdata_directory = "examples/userdata"
key_directory = "examples/keys"

machine_identity_order = ("get_dns_name","get_mac_address", "get_ip_address")

default_availability_zone = "nova"

launch_index = "0"


def _get_machine_meta_data(request):
    return {
        "role": "master"
    }

get_machine_meta_data =  _get_machine_meta_data


