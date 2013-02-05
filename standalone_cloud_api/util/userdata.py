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

import os, glob
from standalone_cloud_api.util.cloud_init_mime_encoder import encode
from standalone_cloud_api.util.templating import find_template_plugin

def template_data(data, filename, template_dictionary, mime_type):
    template_plugin = find_template_plugin(filename)
    return template_plugin.template_data(data, template_dictionary, filename)


def find_template_path(request):
    base_path = request.api_config.userdata_directory
    for order in request.api_config.machine_identity_order:
        if order in request.machine_id and request.machine_id[order] is not None:
            kp = os.path.join(base_path, request.machine_id[order])
            if os.path.exists(kp):
                return kp
    kp = os.path.join(base_path, request.hostname)
    if os.path.exists(kp):
        return kp
    kp =  os.path.join(base_path, "default")
    if os.path.exists(kp):
        return kp
    return None

def create_user_data(request):
    template_path = None
    if "template_search_function" in request.api_config.__dict__ and request.api_config.key_search_function is not None:
        template_path = request.api_config.template_search_function(request.machine_id)
    else:
        template_path = find_template_path(request)
        if template_path is None:
            raise Exception("The default public key directory does not exist")

    if template_path is None or not os.path.exists(template_path):
        raise Exception("Could not find a template directory. Not even the default one. %s"%template_path)

    files = [os.path.join(template_path, x) for x in glob.glob1(template_path, "*")]
    request.set_header("Content-Type","multipart/mixed")
    return encode(files, {"hostname":request.hostname}, template_function=template_data)