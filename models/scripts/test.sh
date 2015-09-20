#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "usage: ./models/scripts/test.sh path/to/model_dir"
  echo
  echo "example: ./models/scripts/test.sh models/naive_64px"
  exit
fi

caffemodel=`ls -1 models/naive_64px/trained/snapshot_iter_*.caffemodel | tail -1`
caffe test -model $1/train_test.prototxt -weights $caffemodel
