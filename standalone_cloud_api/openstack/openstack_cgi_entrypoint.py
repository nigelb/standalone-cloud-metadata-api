#!/usr/bin/python
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

import os, sys, cgitb

if "SCMA_PYTHON_PATH_INCLUDE" in os.environ:
    sys.path.append(os.environ["SCMA_PYTHON_PATH_INCLUDE"])

if "SCMA_CWD_PYTHON_PATH_INCLUDE" in os.environ and os.environ['SCMA_CWD_PYTHON_PATH_INCLUDE'].lower() == "true":
    os.chdir(os.environ["SCMA_PYTHON_PATH_INCLUDE"])

from standalone_cloud_api import SCMA_CONFIG_DIR_ENVIRONMENT_VARIABLE, SCMA_ENABLE_CGITB


if __name__ == "__main__":
    if SCMA_CONFIG_DIR_ENVIRONMENT_VARIABLE not in os.environ:
        print "Status:503"
        print "Content-Type: text/html"
        print""
        print "HTTP/1.1 503 Service Unavailable"
        sys.stderr.write("""The environment variable %s needs to bet to the directory containing the standalone_cloud_api configuration
For Apache servers, set the "SetEnv" directive.
        """%SCMA_CONFIG_DIR_ENVIRONMENT_VARIABLE)
        sys.exit(503)

    sys.path.append(os.environ[SCMA_CONFIG_DIR_ENVIRONMENT_VARIABLE])
    import openstack_config
    if "openstack_metadata_api_enabled" not in openstack_config.__dict__ or not openstack_config.openstack_metadata_api_enabled:
        print "Status:404"
        print "Content-Type: text/html"
        print""
        print "HTTP/1.1 404 Not Found"
        sys.stderr.write("The configuration option openstack_metadata_api_enabled must exist and be set to True in openstack_config.py")
        sys.exit(404)
    from standalone_cloud_api.openstack.api import OpenstackMetaDataAPI
    openstack_config.SCMA_ENABLE_CGITB = False
    if SCMA_ENABLE_CGITB in os.environ and os.environ[SCMA_ENABLE_CGITB].lower() == "true":
        cgitb.enable()
        openstack_config.SCMA_ENABLE_CGITB = True
    OpenstackMetaDataAPI(openstack_config).handle()
