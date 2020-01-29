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

parser = bibtex.Parser()
bib_data = parser.parse_file(sys.argv[1])


# date (year and month)
# then sort by date before doing anything else
# authors should work better
for key in bib_data.entries:
    entry = bib_data.entries[key]
    title = ""
    venue = ""
    author = ""
    if "author" in entry.persons:
        for pers in entry.persons["author"]:
            print(str(pers.first_names)+" "+str(pers.middle_names)+" "+str(pers.last_names))
    print(entry.persons["author"])
    if "title" in entry.fields:
        title = entry.fields["title"]        
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
    print('<p class="bib_entry" id="bib_'+key+'">')
    print('span class="bib_title">'+title+'</span>')
    print('<span class="bib_author">'+author+'</span>')
    print('span class="bib_venue">'+venue+'</span>')
    print('</p>')
    
