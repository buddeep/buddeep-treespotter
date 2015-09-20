#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "usage: ./models/scripts/train.sh path/to/model_dir"
  echo
  echo "example: ./models/scripts/train.sh models/naive_64px"
  exit
fi

caffe train --solver=$1/solver.prototxt
