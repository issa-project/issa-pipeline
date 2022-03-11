#!/bin/bash

TRAIN_SET=/training/data-sets/en/train
TEST_SET=/training/data-sets/en/test

VOCAB_FILE=/training/data-sets/en/agrovoc-en.ttl
EVAL_FILE=/training/data-sets/en/evaluation_all

echo $(date "+%Y/%m/%d %H:%M:%S") " start training models for en"

annif loadvoc cirad-mllm-en $VOCAB_FILE

echo "*********** TF-IDF ************"
annif clear cirad-tfidf-en
annif train cirad-tfidf-en "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.tfidf.txt" cirad-tfidf-en "$TEST_SET"
annif eval cirad-tfidf-en "$TEST_SET"

echo "*********** Omikuji Parabel ************"
annif clear cirad-omikuji-parabel-en
annif train cirad-omikuji-parabel-en "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.parabel.txt" cirad-omikuji-parabel-en "$TEST_SET"
annif eval  cirad-omikuji-parabel-en "$TEST_SET"

echo "*********** MLLM ************"
annif clear cirad-mllm-en
annif train cirad-mllm-en "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.mllm.txt" cirad-mllm-en "$TEST_SET"
annif eval cirad-mllm-en "$TEST_SET"

echo "*********** Parabel&MLLM ************"
#annif clear cirad-ensemble-en
#annif eval -r "$EVAL_FILE.ensemble.txt" cirad-ensemble-en "$TEST_SET"
annif eval cirad-ensemble-en "$TEST_SET"

#echo "*********** Parabel&MLLM NN ************"
annif clear cirad-nn-ensemble-en
annif train cirad-nn-ensemble-en "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.nn-ensemble.txt" cirad-nn-ensemble-en "$TEST_SET"
annif eval cirad-nn-ensemble-en "$TEST_SET"

echo $(date "+%Y/%m/%d %H:%M:%S") " done en"
