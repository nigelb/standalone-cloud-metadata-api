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

import sys, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mime_types = {
    '#include' :        'text/x-include-url',
    '#!' :              'text/x-shellscript',
    '#cloud-config' :   'text/cloud-config',
    '#upstart-job' :    'text/upstart-job',
    '#part-handler' :   'text/part-handler',
    '#cloud-boothook' : 'text/cloud-boothook'
}

def find_mimetype(data, default=""):
    for key in mime_types:
        if data.startswith(key):
            return mime_types[key]
    return default

def encode(files, template_dictionary, boundary=None, template_function=lambda data, filename, template_dictionary, mime_type: (data, filename)):
    msg = MIMEMultipart(boundary=boundary)
    files.sort()
    for fl in files:
        f = open(fl)
        data = f.read()
        f.close()
        mime_type = find_mimetype(data).split("/")
        data, filename = template_function(data, fl, template_dictionary, mime_type)
        maintype, subtype =  mime_type
        entry = MIMEText(data, subtype)
        entry.add_header("Content-Disposition", "attachment", filename=os.path.basename(filename))
        msg.attach(entry)

    return msg.as_string(unixfrom=False)


#if __name__ == "__main__":
#    import glob
#    files = []
#    for i in  sys.argv[1:]:
#        for j in glob.glob(i):
#            files.append(j)
#    print encode(files, {})
