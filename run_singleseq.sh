#!/bin/bash

input=$1
input_dir=$(dirname $1)
seq_id=$(basename $(basename $input) .fasta)

start=`date +%s`

######## run linearpartition to get bp probability ###########
tail -n +2 $input_dir/$seq_id.fasta | LinearPartition/linearpartition -V -o $input_dir/$seq_id.prob
python3 ss_feat.py $input_dir/$seq_id

########## run rnasnap2 model ###########
python3 rna-snap2_single.py --path_input $input_dir --seq_id $seq_id

end=`date +%s`
runtime=$((end-start))

echo "computation time = "$runtime
