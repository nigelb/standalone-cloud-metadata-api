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

import glob, os, scma_ssh_keys

def find_key_path(request):
    for order in request.api_config.machine_identity_order:
        if order in request.machine_id and request.machine_id[order] is not None:
            kp = os.path.join(request.api_config.key_directory, request.machine_id[order])
            if os.path.exists(kp):
                return kp
    kp = os.path.join(request.api_config.key_directory, request.hostname)
    if os.path.exists(kp):
        return kp
    kp =  os.path.join(request.api_config.key_directory, "default")
    if os.path.exists(kp):
        return kp
    return None

def find_public_keys(request):
    key_path = None
    if scma_ssh_keys.ssh_key_search_function is not None:
        key_path = scma_ssh_keys.ssh_key_search_function(request)
    else:
        key_path = find_key_path(request)
        if key_path is None:
            raise Exception("The default public key directory does not exist")

    if key_path is None or not os.path.exists(key_path):
        raise Exception("The specified key directory: %s does not exist."%key_path)

    keys = {}
    for i in glob.glob1(key_path, "*"):
        key_file = open(os.path.join(key_path, i))
        keys[i] = key_file.read()
        key_file.close()
    return keys
