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

from standalone_cloud_api.util.templating import register_template_plugin, PythonFormatTemplate

userdata_directory = "examples/userdata"
key_directory = "examples/keys"

machine_identity_order = ("get_dns_name","get_mac_address", "get_ip_address")


register_template_plugin(PythonFormatTemplate("\.pf$"))

##Customize the search path for looking for ssh keys
#
#def example_key_search(request):
#   import os.path
#   return os.path.join(key_directory, "default")
#
#
key_search_function = None

##By defining userdata_search_function you can customize the way we find
##the userdata directory.
#
#def example_userdata_search(request):
#   import os.path
#   return os.path.join(userdata_directory, "default")
#
#userdata_search_function = example_userdata_search
#
userdata_search_function = None


##When the userdata template plugin is run, it is passed a namespace from which
##to get its variables from. By default it is passed: {"hostname":request.hostname}
##If you wish to customize the namespace then see this example:
#
#def example_userdata_template_namespace(request):
#    return {"hostname":request.hostname}
#
#userdata_template_namespace = example_userdata_template_namespace
#
userdata_template_namespace = None