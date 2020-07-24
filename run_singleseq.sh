#!/bin/bash

input="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
input_dir=$(dirname $input)
seq_id=$(basename $(basename $input) | cut -d. -f1)

#################### convert multiline fasta to one line fasta #####################
awk -i inplace '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' $input
sed -i '/^$/d' $input

start=`date +%s`

######## run linearpartition to get bp probability ###########
echo ""
echo "======================================================================================================"
echo "       Predicting Secondary Structure probability of query sequence $seq_id using LinearPartition. "
echo "======================================================================================================"
echo ""
tail -n +2 $input | LinearPartition/linearpartition -V -r $input_dir/$seq_id.prob
python3 ./utils/ss_feat.py $input

########## run rnasnap2 model ###########
echo ""
echo "======================================================================================================"
echo "       Running RNAsnap2 (SingleSeq) for query sequence $seq_id. "
echo "======================================================================================================"
echo ""
python3 ./utils/rna-snap2_single.py --seq_id $input

end=`date +%s`
runtime=$((end-start))

echo -e "\ncomputation time = "$runtime" seconds"
