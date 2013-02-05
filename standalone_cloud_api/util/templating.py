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

import re

template_plugins = []

def register_template_plugin(template_plugin):
    global template_plugins
    template_plugins.append(template_plugin)

def find_template_plugin(filename):
    global template_plugins
    for plugin in template_plugins:
        if plugin.can_template(filename):
            return plugin
    return PassThroughTemplate()

class TemplateBase:
    def can_template(self, filename): return False
    def template_data(self, data, namespace, filename):pass

class PassThroughTemplate(TemplateBase):
    def can_template(self, filename): return False
    def template_data(self, data, namespace, filename):
        return data, filename



class PythonFormatTemplate(TemplateBase):
    def __init__(self, regex):
        self.regex = regex

    def can_template(self, filename):
        return re.search(self.regex, filename) is not None

    def template_data(self, data, namespace, filename):
        return data.format(**namespace), re.sub(self.regex, "", filename)

