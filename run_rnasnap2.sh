#!/bin/bash

input=$1
input_dir=$(dirname $1)
seq_id=$(basename $(basename $input) .fasta)

path_blastn=./ncbi-blast-2.10.0+/bin/
path_blastn_database=./nt_database/nt
path_infernal=./infernal-1.1.3-linux-intel-gcc/binaries
path_infernal_database=./nt_database/nt

#echo $input_dir/$seq_id.bla

start=`date +%s`

if [ -f $input_dir/$seq_id.profile ];	then
	echo "all the features already exists."
else
	######## run blastn ################
	if [ -f $input_dir/$seq_id.aln ];	then
		echo "blastn output exists";
	else
		$path_blastn/blastn -db $path_blastn_database -query $input -out $input_dir/$seq_id.bla -evalue 0.001 -num_descriptions 1 -num_threads 8 -line_length 1000 -num_alignments 50000
		./utils/parse_blastn_local.pl $input_dir/$seq_id.bla $input_dir/$seq_id.fasta $input_dir/$seq_id.aln
	fi

	######## run infernal ################
	./utils/reformat.pl fas sto $input_dir/$seq_id.aln $input_dir/$seq_id.sto
	$path_infernal/cmbuild --noss --hand -F $input_dir/$seq_id.cm $input_dir/$seq_id.sto
	#$path_infernal/cmcalibrate $input_dir/$seq_id.cm
	timeout 7200s $path_infernal/cmsearch -o $input_dir/$seq_id.out --cpu 30 --incE 10.0 $input_dir/$seq_id.cm $path_infernal_database

	######### get pssm from either from infernal and blstn alignment #############
	if [ -s $input_dir/$seq_id.out ];	then
		./utils/parse_cmsearch.pl $input_dir/$seq_id.out $input_dir/$seq_id.fasta $input_dir/$seq_id.inf_aln
		./utils/getpssm.pl $input_dir/$seq_id.fasta $input_dir/$seq_id.inf_aln $input_dir/$seq_id.pssm
	else
		echo "infernal alignment does not exits, therefore blastn alignment is used to get profile"
		./utils/getpssm.pl $input_dir/$seq_id.fasta $input_dir/$seq_id.aln $input_dir/$seq_id.pssm
	fi

	######## run linearpartition to get bp probability ###########
	tail -n +2 $input_dir/$seq_id.fasta | LinearPartition/linearpartition -V -o $input_dir/$seq_id.prob
	python3 ./utils/ss_feat.py $input_dir/$seq_id

	########## combining all the features ###############
	./utils/combine_feat.pl $input_dir $seq_id
fi

########## run trained rnasnap2 model ###########
python3 ./utils/rna-snap2.py --path_input $input_dir --seq_id $seq_id
end=`date +%s`

runtime=$((end-start))

echo -e "\ncomputation time = "$runtime" seconds"

