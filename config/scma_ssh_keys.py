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


##Customize the search path for looking for ssh keys
#
#def example_key_search(request):
#   import os.path
#   return os.path.join(key_directory, "default")
#
#ssh_key_search_function = example_key_search
#
ssh_key_search_function = None