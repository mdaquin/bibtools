from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
import difflib
import sys

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("provide (only) 2 bibtex files: file1 - file2, and optionally a similarity treashold (default: 80)")
    quit()

file1 = sys.argv[1]
file2 = sys.argv[2]
treshhold = 0.8
if len(sys.argv) == 4:
    treshhold = int(sys.argv[3])
    
parser = bibtex.Parser()
bib_data = parser.parse_file(file2)

titles = []

for key in bib_data.entries:
    entry = bib_data.entries[key]
    titles.append(entry.fields["title"])

bib_data = parser.parse_file(file1)
output = {}

for key in bib_data.entries:
    entry = bib_data.entries[key]
    title1 = entry.fields["title"]
    found = False
    for title2 in titles:
        if difflib.SequenceMatcher(None, title1, title2).ratio() > treshhold:
            found = True
            break
    if not found:
        output[key] = entry

print(BibliographyData(output).to_string('bibtex').encode('utf-8'))

        
