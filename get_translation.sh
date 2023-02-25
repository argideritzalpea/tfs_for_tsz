#!/bin/bash

# Use like: ./get_translation.sh -i test_sentences/eng.txt -o test_sentences/tsz.txt -f outtest.txt

while getopts i:o:f: flag
do
    case "${flag}" in
        i) inlanguage=${OPTARG};;
        o) outlanguage=${OPTARG};;
        f) outfile=${OPTARG};;
    esac
done

printf $outfile
touch "${outfile}"

TRANS_LINES=$(cat ${inlanguage} | wc -l)

echo $TRANS_LINES

for (( j=1; j<$TRANS_LINES + 1; j++ ));
do
  printf "$j Getting the translation of '%s'\n" "$(head -n $j ${inlanguage} | tail -1)"
  printf "$j Translating into '%s'\n" "$(head -n $j ${outlanguage} | tail -1)"
  printf "\n\n"

  in=$(basename ${inlanguage} .txt)
  out=$(basename ${outlanguage} .txt)

  sh ./translate-line.sh $in $out $j
  printf "\n\n\n\n"
  printf "_______________________________________"
  printf "\n\n\n\n"

done &> "${outfile}"