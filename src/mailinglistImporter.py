# UCS mailinglist importer
# author: derMicha

import argparse
import os

parser = argparse.ArgumentParser(description='Extend UCS mailing lists')
parser.add_argument('-ln', '--listname', help="name of listobject (cn)", metavar="CN", required=True)
parser.add_argument('-dc', '--domaincomponent', help="domain component (dc)", metavar="DC", default="esbmz")
parser.add_argument('-f', '--filename', help="filename of csv file", metavar="FILE", required=True)
parser.add_argument('-o', '--offset', help="number of column which contains a mailadress to be imported (starting with 0)",
                    metavar="OFFSET", type=int, required=True)
parser.add_argument('-s', '--separator', help="csv file separator", metavar="SEPARATOR", default=";")
parser.add_argument('-dr', '--dryrun', help="dryrun just prints statements", action='store_true')
args = parser.parse_args()

listname = args.listname
dc = args.domaincomponent
filename = args.filename
offset = args.offset - 1
sep = args.separator
drun = True if args.dryrun else False

dn = "'cn={},cn=mailinglists,cn=mail,dc={},dc=de'".format(listname, dc)
cmd = "udm oxmail/oxlists modify --dn {} --append members=".format(dn)

print("dn used: {}".format(dn))

# sudo udm oxmail/oxlists modify --dn cn=ESBZ-SV,cn=mailinglists,cn=mail,dc=esbmz,dc=de --set mailAddress=esbz-sv@esbmz.de
# sudo udm oxmail/oxlists modify --dn cn=ESBZ-SV,cn=mailinglists,cn=mail,dc=esbmz,dc=de --append members=dermicha@indarium.de

inputFile = open(filename, 'r', newline='\n', encoding='UTF-8')

for line in inputFile:
    cols = line.split(sep)
    if offset <= len(cols):
        email = cols[offset].lower().replace(" ", "").replace(",", "").replace(";", "")
        if (email != "" and "@" in email and "." in email):
            c = "{}{}".format(cmd, email)
            if (drun):
                print(c)
            else:
                os.system(c)
                # print("exec: {}".format(c))
    else:
        print("invalid offset size {}, max offset is {}".format(offset, len(cols)))
        exit(1)

exit(0)
