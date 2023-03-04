#!/bin/bash

SOURCE=$1
TARGET=$2
LINE=$3

SENTENCE="`sed -n ${LINE}p test_sentences/${SOURCE}.txt`"

ace="/usr/local/bin/ace"

#Look at transfer output
#echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat 2>/dev/null | $ace -g tm/$TARGET/$TARGET.dat 2>/dev/null | more

#Look at transfer output & errors
echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat 2>/dev/null | $ace -g tm/$TARGET/$TARGET.dat -vv #| more


#Look at parser output
#echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat 2>/dev/null | more

#Look at parser output, verbose
#echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat | more

#Round trip src tgt src
#echo $SENTENCE | $ace -g grammars/$SOURCE/$SOURCE.dat 2>/dev/null | $ace -g tm/$TARGET/$TARGET.dat 2>/dev/null | $ace -g grammars/$TARGET/$TARGET.dat -e --disable-subsumption-test | $ace -g grammars/$TARGET/$TARGET.dat 2>/dev/null | $ace -g tm/$SOURCE/$SOURCE.dat 2>/dev/null | $ace -g grammars/$SOURCE/$SOURCE.dat -e --disable-subsumption-test
