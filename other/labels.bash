
export TIC_LABELS_PATH='/Users/bkraft/PycharmProjects/tic_labels'  # Add path information here
export TIC_LABELS_PYTHONPATH=${TIC_LABELS_PATH}/labels

export PYTHONPATH=${TIC_LABELS_PYTHONPATH}:$PYTHONPATH

alias  labels_stats='python2 ${TIC_LABELS_PYTHONPATH}/stats.py'