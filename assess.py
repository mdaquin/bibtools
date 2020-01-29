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

print("there are "+str(len(bib_data.entries.keys()))+" entries in "+sys.argv[1])

titles = {}
entries_without_venue = []
not_sure = []
unknown_entry_types = []
duplicates = []

for key in bib_data.entries:
    entry = bib_data.entries[key]
    title = entry.fields["title"]
    for key2 in titles:
        if difflib.SequenceMatcher(None, title, titles[key2]).ratio() > 0.75:
            duplicates.append((key,key2))
    titles[key]=title        
    if entry.type == "article":
        if "journal" not in entry.fields:
            entries_without_venue.append(key)
    elif entry.type == "inproceedings":
        if "booktitle" not in entry.fields:
            entries_without_venue.append(key)
    elif entry.type == "inbook":
        if "booktitle" not in entry.fields:
            entries_without_venue.append(key)
    elif entry.type == "book":
        not_sure.append(key)
    elif entry.type == "techreport":
        not_sure.append(key)
    elif entry.type == "incollection":
        not_sure.append(key)
    elif entry.type == "misc":
        not_sure.append(key)
    else:
        unknown_entry_types.append(entry.type)
        
print("Entries without venues:")
print(entries_without_venue)
print("Not sure what to do:")
print(not_sure)
print("Unknown entry types:")
print(unknown_entry_types)
print("Possible duplicates (based on title):")
print(duplicates)
