#!/bin/bash

path_blastn=./blastn/bin
db_blastn=/mnt/hdd6/jaswinder/Documents/blastn_db/nt
path_infernal=./infernal/infernal-1.1.3-linux-intel-gcc/binaries
db_inf=/mnt/hdd6/jaswinder/Documents/infernal/nt_database/nt

input=$1

input_dir=$(dirname $1)
seq_id=$(basename $(basename $input) .fasta)

#echo $input_dir/$seq_id.bla

if [ -f $input_dir/$seq_id.profile ];	then
	echo "all the features already exists."
else
	######## run blastn ################
	if [ -f $input_dir/$seq_id.aln ];	then
		echo "blastn output exists";
	else
		$path_blastn/blastn -db $db_blastn -query $input -out $input_dir/$seq_id.bla -evalue 0.001 -num_descriptions 1 -num_threads 8 -line_length 1000 -num_alignments 50000
		./parse_blastn_local.pl $input_dir/$seq_id.bla $input_dir/$seq_id.fasta $input_dir/$seq_id.aln
	fi

	######## run infernal ################
	./reformat.pl fas sto $input_dir/$seq_id.aln $input_dir/$seq_id.sto
	$path_infernal/cmbuild --noss --hand -F $input_dir/$seq_id.cm $input_dir/$seq_id.sto
	#$path_infernal/cmcalibrate $input_dir/$seq_id.cm
	timeout 7200s $path_infernal/cmsearch -o $input_dir/$seq_id.out --cpu 30 --incE 10.0 $input_dir/$seq_id.cm $db_inf

	######### get pssm from either from infernal and blstn alignment #############
	if [ -s $input_dir/$seq_id.out ];	then
		./parse_cmsearch.pl $input_dir/$seq_id.out $input_dir/$seq_id.fasta $input_dir/$seq_id.inf_aln
		./getpssm.pl $input_dir/$seq_id.fasta $input_dir/$seq_id.inf_aln $input_dir/$seq_id.pssm
	else
		echo "infernal alignment does not exits, therefore blastn alignment is used to get profile"
		./getpssm.pl $input_dir/$seq_id.fasta $input_dir/$seq_id.aln $input_dir/$seq_id.pssm
	fi

	######## run linearpartition to get bp probability ###########
	tail -n +2 $input_dir/$seq_id.fasta | LinearPartition/linearpartition -V -o $input_dir/$seq_id.prob
	python3 ss_feat.py $input_dir/$seq_id

	########## combining all the features ###############
	./combine_feat.pl $input_dir $seq_id
fi

########## run rnasnap2 model ###########
start=`date +%s`
python3 rna-snap2.py --path_input $input_dir --seq_id $seq_id
#python3 rna-snap2_single.py --path_input $input_dir --seq_id $seq_id
#python3 ensemble.py outputs/$seq_id
end=`date +%s`

runtime=$((end-start))
echo $runtime

