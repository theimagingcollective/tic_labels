
export TIC_LABELS_PATH='/Users/bkraft/PycharmProjects/tic_labels'  # Add path information here
export TIC_LABELS_PYTHONPATH=${TIC_LABELS_PATH}/labels

export PYTHONPATH=${TIC_LABELS_PYTHONPATH}:$PYTHONPATH

alias  tic_labels_stats='python2 ${TIC_LABELS_PYTHONPATH}/stats.py'
alias  tic_labels_remove='python2 ${TIC_LABELS_PYTHONPATH}/remove.py'
alias  tic_labels_keep='python2 ${TIC_LABELS_PYTHONPATH}/keep.py'