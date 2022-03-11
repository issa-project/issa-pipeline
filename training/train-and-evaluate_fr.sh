#!/bin/bash

TRAIN_SET=/training/data-sets/fr/train
TEST_SET=/training/data-sets/fr/test

VOCAB_FILE=/training/data-sets/fr/agrovoc-fr.ttl
EVAL_FILE=/training/data-sets/fr/evaluation_all

echo $(date "+%Y/%m/%d %H:%M:%S") " start training models for fr"


annif loadvoc cirad-mllm-fr $VOCAB_FILE


echo "*********** TF-IDF ************"
annif clear cirad-tfidf-fr
annif train cirad-tfidf-fr "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.tfidf.txt" cirad-tfidf-fr "$TEST_SET"
annif eval cirad-tfidf-fr "$TEST_SET"

echo "*********** Omikuji Parabel ************"
annif clear cirad-omikuji-parabel-fr
annif train cirad-omikuji-parabel-fr "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.parabel.txt" cirad-omikuji-parabel-fr "$TEST_SET"
annif eval  cirad-omikuji-parabel-fr "$TEST_SET"

echo "*********** MLLM ************"
annif clear cirad-mllm-fr
annif train cirad-mllm-fr "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.mllm.txt" cirad-mllm-fr "$TEST_SET"
annif eval cirad-mllm-fr "$TEST_SET"

echo "*********** Parabel&MLLM ************"
#annif eval -r "$EVAL_FILE.ensemble.txt" cirad-ensemble-fr "$TEST_SET"
annif eval cirad-ensemble-fr "$TEST_SET"

#echo "*********** Parabel&MLLM NN ************"
annif clear cirad-nn-ensemble-fr
annif train cirad-nn-ensemble-fr "$TRAIN_SET"
#annif eval -r "$EVAL_FILE.nn-ensemble.txt" cirad-nn-ensemble-fr "$TEST_SET"
annif eval cirad-nn-ensemble-fr "$TEST_SET"

echo $(date "+%Y/%m/%d %H:%M:%S") " done fr"
