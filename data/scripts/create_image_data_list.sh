#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "usage: create_image_data_list.sh path/to/slices/directory [limit]"
  echo "  if limit is a integer, then used as a max"
  echo "  if limit is a positive float between 0 and 1, takes that ratio from the top of each label"
  echo "  if limit is a positive float between 0 and 1, takes that ratio from the bottom of each label"
  echo "example usage:"
  echo "    ./data/scripts/create_image_data_list.sh data/slices/2014_64px 0.7 > data/slices/2014_64px/train.txt"
  echo "    ./data/scripts/create_image_data_list.sh data/slices/2014_64px -0.7 > data/slices/2014_64px/test.txt"
  exit
fi

if [[ $# -eq 1 ]]; then
  limit_per_label=1000000000
else
  limit_per_label=$2
fi

SLICES_DIR=$1
cd $SLICES_DIR

for label in *; do
  if [ -d $label ]; then
    re_pos=^0\..+$
    re_neg=^-0\..+$
    if [[ $limit_per_label =~ $re_pos ]] ; then
      files_with_label=`ls -1 $label | wc -l`
      limit_for_label=`printf %.0f $(bc -l <<< "$files_with_label * $limit_per_label")`
      use_lte=1
    elif [[ $limit_per_label =~ $re_neg ]] ; then
      files_with_label=`ls -1 $label | wc -l`
      limit_for_label=`printf %.0f $(bc -l <<< "$files_with_label * (-1 * $limit_per_label)")`
      use_lte=0
    else
      limit_for_label=$2
      use_lte=1
    fi
    counter=$((0))
    for file in $label/* ; do
      counter=$((counter + 1))
      if [ $use_lte -eq 1 ]; then
        if [ "$counter" -lt "$limit_for_label" ]; then
          echo $SLICES_DIR/$file $label
        fi
      else
        if [ "$counter" -gt "$limit_for_label" ]; then
          echo $SLICES_DIR/$file $label
        fi
      fi
    done
  fi
done
