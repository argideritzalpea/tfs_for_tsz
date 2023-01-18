with open("tsz_toolbox.txt", "r") as f:
    data = f.readlines()

all_data = []
for line in data:
    line = line.strip()
    if line.startswith("\\ref"):
        curr_ref = {}
        curr_ref["ref"] = line.split("\\ref")[1]
    if line.startswith("\\tph"):
        curr_ref["tph"] = line.split("\\tph")[1]
    if line.startswith("\\mph"):
        curr_ref["mph"] = line.split("\\mph")[1]
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
    morpho = re.sub(" ([-=])", "\\1", all_data[num+1]["mph"].strip())
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