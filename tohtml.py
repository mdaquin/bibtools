from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
import difflib
import sys

if len(sys.argv) != 2:
    print("provide (only) bibtex file as argument")
    quit()

with open(sys.argv[1]) as f:
    for line in f:
        try:
            line.decode('utf-8')
        except UnicodeDecodeError:
            print("Line not decoding: ")
            print(line)

parser = bibtex.Parser(encoding="utf-8")
bib_data = parser.parse_file(sys.argv[1])
all_bibs = {}

for key in bib_data.entries:
    entry = bib_data.entries[key]
    title = ""
    venue = ""
    st = '<span class="bib_authors">'    
    if "author" in entry.persons:
        first = True
        for pers in entry.persons["author"]:
            if not first:
                st = st + ', '
            first = False
            st = st + '<span class="bib_author">'
            if len(pers.first_names) > 0:
                st = st + str(pers.first_names[0]).encode('utf-8').decode('utf-8')
            if len(pers.middle_names) > 0:
                st = st + " "+str(pers.middle_names[0]).encode('utf-8').decode('utf-8')
            if len(pers.last_names) > 0:
                st = st + " " +str(pers.last_names[0].encode('utf-8')).decode('utf-8')
            st = st + '</span>'    
    if "title" in entry.fields:
        title = entry.fields["title"].encode('utf-8').decode('utf-8')
    if "author" in entry.fields:
        author = entry.fields["author"]
    if "journal" in entry.fields:
        venue = entry.fields["journal"]            
    elif "booktitle" in entry.fields:
        venue = entry.fields["booktitle"]            
    elif "howpublished" in entry.fields:
        venue = entry.fields["howpublished"]            
    elif "publisher" in entry.fields:
        venue = entry.fields["publisher"]
    date = "1990-"
    if "year" in entry.fields:
        date = str(entry.fields["year"])+"-"
    if "month" in entry.fields:
        date = date + str(entry.fields["month"])
    ast = '<p class="bib_entry" id="bib_'+key+'">'+'<span class="bib_title">'+title+'</span>'+st+'<span class="bib_venue">'+venue+'</span>'+'</p>'
    if date not in all_bibs:
        all_bibs[date] = []
    all_bibs[date].append(ast)


for date in sorted(all_bibs.keys(), reverse=True):
    for bib in all_bibs[date]:
        print(bib.encode('utf-8'))

