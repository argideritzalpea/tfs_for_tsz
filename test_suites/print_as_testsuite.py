with open("/Users/mosaix/hpsg/tfs_for_tsz/tsz_toolbox.txt", "r") as f:
    data = f.readlines()

all_data = []
for line in data:
    line = line.strip()
    if line.startswith("\\ref"):
        curr_ref = {}
        curr_ref["ref"] = line.split("\\ref")[1].strip()
    if line.startswith("\\tph"):
        curr_ref["tph"] = line.split("\\tph")[1]
    if line.startswith("\\mph"):
        curr_ref["mph"] = line.split("\\mph")[1]
        curr_ref["form_mph"] = re.sub(" ([-=])", "\\1", curr_ref["mph"].strip())
    if line.startswith("\\mgl"):
        curr_ref["mgl"] = line.split("\\mgl")[1]
    if line.startswith("\\ps"):
        curr_ref["ps"] = line.split("\\ps")[1]
    if line.startswith("\\eng"):
        curr_ref["eng"] = line.split("\\eng")[1]
    if line.startswith("\\id"):
        curr_ref["id"] = line.split("\\id")[1]
        all_data.append(curr_ref)

import re
def print_as_test_example(num, vet="f", judge="g", phenom=""):
    source = "Source: ref {} in tsz_toolbox".format(str(num))
    vetted = "Vetted: {}".format(vet)
    judgement = "Judgement: {}".format(judge)
    phenomena = "Phenomena: {}".format(phenom)
    ortho = all_data[num+1]["tph"].strip()
    morpho = all_data[num+1]["form_mph"].strip()
    gloss = all_data[num+1]["mgl"].strip()
    transl = all_data[num+1]["eng"].strip()
    print(source, 
        vetted,
        judgement,
        phenomena,
        ortho,
        morpho,
        gloss,
        transl,
        sep="\n")

print_as_test_example(0)

from collections import Counter
ilengths = {}
for example in all_data:
    ises = example['form_mph'].split()
    ilength = len(ises)
    print(example['ref'])
    ilengths[int(example['ref'])] = ilength

all_data[4930]['form_mph'].split()

def get_max_length(length=3):
    return set([key-1 for key in ilengths if ilengths[key]<length])

def search_for_item(search_string, field="gloss"):
    out = []
    for idx, item in enumerate(all_data):
        if search_string in item[field]:
            out.append(idx)
    return set(out)

search_for_item("-mpu", "mph")

def get_glosses_for_string(search_string, field="gloss"):
    out = {}
    for idx, item in enumerate(all_data):
        for id2, token in enumerate(item[field].split()):
            if search_string in token:
                out.setdefault(item["mgl"].split()[id2], [])
                out[item["mgl"].split()[id2]].append(idx)
    return out

get_glosses_for_string("nkuni", "mph")
len(get_max_length(2))

# Get all glosses and their counts
gloss_dictionary = {}
for idx, item in enumerate(all_data):
    for id2, token in enumerate(item["mgl"].split()):
        gloss_dictionary.setdefault(token, [])
        gloss_dictionary[token].append(idx)

# Get all words and their glosses (may not line up exactly)
glosses_to_orth_tokens = {}
for idx, item in enumerate(all_data):
    for orth_tok, gloss_tok in zip(re.sub("([-=])", " \\1", item["tph"].strip()).split(), item["mgl"].split()):
        glosses_to_orth_tokens.setdefault(gloss_tok, set())
        glosses_to_orth_tokens[gloss_tok].add(orth_tok)

# Get all morphs and their glosses
glosses_to_morph_tokens = {}
for idx, item in enumerate(all_data):
    for orth_tok, gloss_tok in zip(item["mph"].strip().split(), item["mgl"].split()):
        glosses_to_morph_tokens.setdefault(gloss_tok, set())
        glosses_to_morph_tokens[gloss_tok].add(orth_tok)

gloss_dictionary["patio"]
glosses_to_orth_tokens["cat"]
glosses_to_morph_tokens["now"]

gloss_count = list(map(lambda x: (x, len(gloss_dictionary[x])), gloss_dictionary.keys()))

sorted_gloss_count = sorted(gloss_count, key=lambda x: x[1], reverse=True)


import csv
with open('gloss_count.csv','w+') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['gloss','count'])
    for row in sorted_gloss_count:
        if (row[0][0].isupper() or row[0][0].isnumeric()) and (row[0][-1].isupper() or row[0][-1].isnumeric()):
            csv_out.writerow(row)

import csv
with open('gloss_interpretable_count.csv','w+') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['gloss','count'])
    for row in sorted_gloss_count:
        if not (row[0][0].isupper() or row[0][0].isnumeric()) and not (row[0][-1].isupper() or row[0][-1].isnumeric()):
            csv_out.writerow(row)


short_instr = get_max_length(4).intersection(search_for_item("APPRX", "mgl"))


get_max_length(3)

import sys

def print_searched_samples_to_file(filename="sample.txt", ilength=4, search="APPRX", field="mgl"):
    ilength_cond_set = get_max_length(ilength)
    search = search_for_item(search, field)
    short_instr = ilength_cond_set.intersection(search)
    with open(filename, 'w+') as f:
        original_stdout = sys.stdout
        sys.stdout = f # Change the standard output to the file we created.
        for item in short_instr:
            sample = str(print_as_test_example(item-1))
            print("\n")
        sys.stdout = original_stdout

print_searched_samples_to_file(filename="sample.txt",
                            ilength=80,

                            search="COMP",
                            field="mgl")

import lingpy


msa = lingpy.align.pairwise.nw_align('iaxï', 'jaʃyï')

lingpy.align.pairwise.edit_dist('iaxï', 'jaʃyï')

def find_similar_pairs(strings):
    for 


candidates = []
for gloss_tup in sorted_gloss_count:
    gloss = gloss_tup[0]   
    morphlist = list(glosses_to_morph_tokens[gloss])
    for id1, morph1 in enumerate(morphlist):
        for id2, morph2 in enumerate(morphlist[id1+1:]):
            if lingpy.align.pairwise.edit_dist(morph1, morph2) <= 2:
                candidates.append([gloss]+list(lingpy.align.pairwise.nw_align(morph1, morph2)))

with open("candidates.txt", 'w+') as f:
    original_stdout = sys.stdout
    sys.stdout = f # Change the standard output to the file we created.
    for candidate in candidates:
        print(candidate[0])
        print(candidate[1])
        print(candidate[2])
        print()
    sys.stdout = original_stdout