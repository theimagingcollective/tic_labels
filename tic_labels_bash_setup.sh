#!/usr/bin/env bash

export TIC_LABELS_PYTHONPATH=${TIC_LABELS_PATH}/labels
export PYTHONPATH=${TIC_LABELS_PYTHONPATH}:$PYTHONPATH

source ${TIC_LABELS}/other/tic_labels_aliases.sh
