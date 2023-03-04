#!/bin/bash

SOURCE=$1
LINE=$2

SENTENCE="`sed -n ${LINE}p test_sentences/${SOURCE}.txt`"

ace="/usr/local/bin/ace"

#Look at parser output
echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat -vv
