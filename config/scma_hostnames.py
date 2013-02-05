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

static_hostnames = {
    "aa:bb:cc:dd:ee:00":"test_machine_1",
    "aa:bb:cc:dd:ee:01":"test_machine_2",
    "169.254.3.2": "test_machine_3",
    "example.com": "test_machine_4",
    "192.168.1.1": "test_machine_0"
}

def generate_hostname(machine_identifier, machine_identity_order):
    for i in machine_identity_order:
        if i in machine_identifier and machine_identifier[i] is not None:
            return machine_identifier[i]
    return "Undefined"