First use filter.cpp to filter out using information content. 
    Input: raw.chen
    Output: filtered.chen, names.txt

Then type this in command line: ./chen2meme filtered.chen > query.meme
    Input: filtered.chen
    Output: query.meme

Then type this in command line: tomtom query.meme database.meme
    Input: query.meme, database.meme
    Output: tomtom_out database

Run label.py
    Input: tomtom_out, names.txt
    Output: labelled.txt


raw.chen: the unprocessed chen files downloaded
filtered.chen: processed chen file with information content
names.txt: a list of high information content files after filtered (for use in labelling process)
query.meme: file converted from filtered.chen to a meme file format
database.meme: database of motifs
tomtom_out: file containing tomtom_out_tsv, which contains the identified overlapping regions
labelled.txt: a list of 0s and 1s in the order of that listed in filtered.chen