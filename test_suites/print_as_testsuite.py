import os
import re
import csv
import sys
from collections import Counter
import lingpy


def load_toolbox_data(path):
    with open(path, "r") as f:
        toolbox_lines = f.readlines()
    return toolbox_lines


def get_data_store(toolbox_lines):
    toolbox_data = []
    for line in toolbox_lines:
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
            toolbox_data.append(curr_ref)
    return toolbox_data

def print_as_test_example(num, data, vet="f", judge="g", phenom=""):
    source = "Source: ref {} in tsz_toolbox".format(str(num))
    vetted = "Vetted: {}".format(vet)
    judgement = "Judgement: {}".format(judge)
    phenomena = "Phenomena: {}".format(phenom)
    ortho = data[num+1]["tph"].strip()
    morpho = data[num+1]["form_mph"].strip()
    gloss = data[num+1]["mgl"].strip()
    transl = data[num+1]["eng"].strip()
    print(source, 
        vetted,
        judgement,
        phenomena,
        ortho,
        morpho,
        gloss,
        transl,
        sep="\n")

def get_ilengths(data):
    ilengths = {}
    for example in data:
        ises = example['form_mph'].split()
        ilength = len(ises)
        ilengths[int(example['ref'])] = ilength
    if len(ilengths) > 0:
        print("Loaded {} i-lengths...".format(len(ilengths)))
    return ilengths

def get_at_threshold_length(length=3):
    return set([key-1 for key in ilengths if ilengths[key]<length])

def search_for_item(search_string, data, field="mph"):
    # ex: search_for_item("-mpu", toolbox_data, "mph")
    out = []
    for idx, item in enumerate(data):
        if search_string in item[field]:
            out.append(idx)
    return set(out)

def get_glosses_for_string(search_string, data, field="mgl"):
    # get_glosses_for_string("on", toolbox_data, "mgl")
    out = {}
    for idx, item in enumerate(data):
        for id2, token in enumerate(item[field].split()):
            if search_string in token:
                out.setdefault(item["mgl"].split()[id2], [])
                out[item["mgl"].split()[id2]].append(idx)
    return out

def get_gloss_dictionary(data):
    gloss_dictionary = {}
    # Get all glosses and their references in the toolbox
    for idx, item in enumerate(data):
        for id2, token in enumerate(item["mgl"].split()):
            gloss_dictionary.setdefault(token, [])
            gloss_dictionary[token].append(idx)
    return gloss_dictionary

def get_gloss_orths(data):
    # Get all words and their glosses (may not line up exactly)
    glosses_to_orth_tokens = {}
    for idx, item in enumerate(data):
        for orth_tok, gloss_tok in zip(re.sub("([-=])", " \\1", item["tph"].strip()).split(), item["mgl"].split()):
            glosses_to_orth_tokens.setdefault(gloss_tok, set())
            glosses_to_orth_tokens[gloss_tok].add(orth_tok)
    return glosses_to_orth_tokens

def get_gloss_to_morphs_count(data):
    # Get all morphs and their glosses
    gloss_to_morph_count = {}
    glosses_to_morph_tokens = {}
    for idx, item in enumerate(data):
        for orth_tok, gloss_tok in zip(item["mph"].strip().split(), item["mgl"].split()):
            glosses_to_morph_tokens.setdefault(gloss_tok, set())
            glosses_to_morph_tokens[gloss_tok].add(orth_tok)
            gloss_to_morph_count.setdefault(gloss_tok, Counter())
            gloss_to_morph_count[gloss_tok][orth_tok] += 1
    return gloss_to_morph_count, glosses_to_morph_tokens

def write_uninterpretable_gloss_count(path='gloss_count.csv'):
    # Print a file of the glosses and their counts
    with open(path,'w+') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['gloss','count'])
        for row in gloss_count:
            if (row[0][0].isupper() or row[0][0].isnumeric()) and (row[0][-1].isupper() or row[0][-1].isnumeric()):
                csv_out.writerow(row)

def write_interpretable_gloss_count(path="gloss_interpretable_count.csv"):
    # Print a file of the glosses and their counts
    with open(path,'w+') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['gloss','count'])
        for row in sorted_gloss_count:
            if not (row[0][0].isupper() or row[0][0].isnumeric()) and not (row[0][-1].isupper() or row[0][-1].isnumeric()):
                csv_out.writerow(row)

def print_searched_samples_to_file(searched,
                                data,
                                field="mgl",
                                ilength=10):
    # Print a file of a search across the toolbox at a particular ilength
    results = search_refs_at_ilength(searched, data, field, ilength)
    with open(searched+".txt", 'w+') as f:
        original_stdout = sys.stdout
        sys.stdout = f # Change the standard output to the file we created.
        for item in results:
            sample = str(print_as_test_example(item-1, data))
            print("\n")
        sys.stdout = original_stdout


def search_refs_at_ilength(searched, data, field="mgl", ilength=10):
    return get_max_length(ilength).intersection(search_for_item(searched, data, field))


def print_similarly_spelled_items(gloss_count, glosses_to_morph_tokens, edit_distance=2, path="candidates.txt"):
    # Get a file with all the candidates that have the same glosses and similar surface orthographies 
    candidates = []
    for gloss_tup in gloss_count:
        gloss = gloss_tup[0]   
        morphlist = list(glosses_to_morph_tokens[gloss])
        for id1, morph1 in enumerate(morphlist):
            for id2, morph2 in enumerate(morphlist[id1+1:]):
                if lingpy.align.pairwise.edit_dist(morph1, morph2) <= edit_distance:
                    candidates.append([gloss]+list(lingpy.align.pairwise.nw_align(morph1, morph2)))
    with open(path, 'w+') as f:
        original_stdout = sys.stdout
        sys.stdout = f # Change the standard output to the file we created.
        for candidate in candidates:
            print(candidate[0])
            print(candidate[1])
            print(candidate[2])
            print()
        sys.stdout = original_stdout

def get_max_length(length=3):
    return set([key-1 for key in ilengths if ilengths[key]<length])

def get_orth_to_glosses_count(gloss_to_morph_count):
    # Inverts the gloss to morph counter
    orth_to_glosses_count = {}
    for gloss in gloss_to_morph_count:
        for orth, count in gloss_to_morph_count[gloss].items():
            orth_to_glosses_count.setdefault(orth, Counter())
            orth_to_glosses_count[orth][gloss] += count
    return orth_to_glosses_count

def get_gloss_from_string(sentence, orth_to_glosses_count):
    out = []
    for token in re.sub("([-=])", " \\1", sentence.strip()).split():
        print(token, " : ", orth_to_glosses_count[token])
        print("")
        out.append(orth_to_glosses_count[token].most_common()[0][0])
    return out

def print_as_test_example_from_string(source, vetted, judgement, phenomena, string, transl, orth_to_glosses_count):
    # Get a test suite example, formatted (TODO: must add hyphens to gloss)
    morph = string
    gloss = " ".join(get_gloss_from_string(morph, orth_to_glosses_count))
    print("Source: "+ source, 
        "Vetted: "+vetted,
        "Judgement: "+judgement,
        "Phenomena: "+phenomena,
        string,
        morph,
        gloss,
        transl,
        sep="\n")


PATH = "/Users/mosaix/hpsg/tfs_for_tsz/tsz_toolbox.txt"
toolbox_lines = load_toolbox_data(PATH)
toolbox_data = get_data_store(toolbox_lines)
ilengths = get_ilengths(toolbox_data)
gloss_dictionary = get_gloss_dictionary(toolbox_data)
gloss_count = sorted(list(map(lambda x: (x, len(gloss_dictionary[x])), gloss_dictionary.keys())), key=lambda x: x[1], reverse=True)
glosses_to_orth_tokens = get_gloss_orths(toolbox_data)
gloss_to_morphs_count, glosses_to_morph_tokens = get_gloss_to_morphs_count(toolbox_data)
orth_to_glosses_count = get_orth_to_glosses_count(gloss_to_morphs_count)

# Examples:
# Get the toolbox refs of gloss
gloss_dictionary["patio"]

# Get the different surface forms (orth / tph) of gloss
glosses_to_orth_tokens["cat"]

# Get the different morph tokens (mph) of gloss
glosses_to_morph_tokens["now"]

# Get a count of all the glosses
gloss_count = sorted(list(map(lambda x: (x, len(gloss_dictionary[x])), gloss_dictionary.keys())), key=lambda x: x[1], reverse=True)

# Search for something in the toolbox at a particular ilength
search_refs_at_ilength(searched="because", data=toolbox_data, field="mgl", ilength=10)

# Get all refs at a maximum length of 3
get_max_length(3)

# Print results of a search at ilength to a file
print_searched_samples_to_file(
                            searched="INSTR",
                            data=toolbox_data,
                            field="mgl",
                            ilength=80)


# Get a file of similar orthographies of a common gloss, aligned
print_similarly_spelled_items(gloss_count, glosses_to_morph_tokens)


print_as_test_example_from_string(source="2023 Chamoreau (ex. 50)",
                                    vetted="s",
                                    judgement="g",
                                    phenomena="adverbial clausal modifiers",
                                    string="no=kxï ni-nt'a-s-p-ti jimpo-ka=kxï t'ire-ni ja-p-ka",
                                    transl="They didn’t go because they were eating",
                                    orth_to_glosses_count=orth_to_glosses_count)

get_glosses_for_string("an", toolbox_data, "tph")

get_gloss_from_string("no=kxï ni-nt'a-s-p-ti jimpo-ka=kxï t'ire-ni ja-p-ka", orth_to_glosses_count)
get_gloss_from_string("hu-tsa ni-e-ra-p-ka", orth_to_glosses_count)
get_gloss_from_string("ji-ni=ksï ni=e-nt'a-ni ta-rhu ji-ni-nki=ksï hu-tsa ni-e-ra-p-ka", orth_to_glosses_count)

orth_to_glosses_count["himpoka"]\
orth_to_glosses_count["-ka"]

gloss_to_morphs_count["SBJV"]

no=kxï ni-nts’a-x-p-ti [jimpoka=kxï t’iré-ni ja-p-k’a]
NEG=S3PL go-IT-PST-ASS3S SUB=S3PL eat-NF be_there-AOR.PST-SBJV
‘They didn’t go because they were eating.’