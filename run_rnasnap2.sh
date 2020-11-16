#!/bin/bash

input="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
input_dir=$(dirname $input)
seq_id=$(basename $(basename $input) | cut -d. -f1)

#################### convert multiline fasta to one line fasta #####################
awk -i inplace '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' $input
sed -i '/^$/d' $input

path_blastn=./ncbi-blast-*+/bin
path_blastn_database=./nt_database/nt
path_infernal=./infernal-*-linux-intel-gcc/binaries
path_infernal_database=./nt_database/nt

start=`date +%s`

if [ -f $input_dir/$seq_id.profile ];	then
        echo ""
        echo "=============================================================================================================================================="
        echo "    PSSM file $input_dir/$seq_id.profile already exists for query sequence. "
		echo "    RNAsnap2 will use $input_dir/$seq_id.profile file predictions. "
		echo "    Please delete existing file $input_dir/$seq_id.profile if want to generate new PSSM file"
        echo "=============================================================================================================================================="
        echo ""
else

	if [ -f $input_dir/$seq_id.out ];	then
        echo ""
        echo "=============================================================================================================================================="
        echo "    MSA file $input_dir/$seq_id.out from Infernal Pipeline already exists for query sequence.  "
		echo "    RNAsnap2 will use $input_dir/$seq_id.out file for PSSM feature extraction. "
		echo "    Please delete existing file $input_dir/$seq_id.out if want to generate new MSA file from Infernal Pipeline."
        echo "=============================================================================================================================================="
        echo ""
	else
		######## run blastn ################
		if [ -f $input_dir/$seq_id.aln ];	then
	        echo ""
		    echo "=============================================================================================================================================="
		    echo "    MSA file $input_dir/$seq_id.aln from BLAST-N already exists for query sequence.  "
			echo "    RNAsnap2 will use $input_dir/$seq_id.aln file to build Covariance Model (CM). "
			echo "    Please delete existing file $input_dir/$seq_id.aln if want to generate new MSA file from BLAST-N."
		    echo "=============================================================================================================================================="
		    echo ""
		else
            echo ""
            echo "=================================================================================================================="
            echo "      Start Running BLASTN for first round of homologous sequence search for query sequence $input.           "
            echo "      May take 5 mins to few hours depending on sequence length and no. of homologous sequences in database.              "
            echo "=================================================================================================================="
            echo ""
			$path_blastn/blastn -db $path_blastn_database -query $input -out $input_dir/$seq_id.bla -evalue 0.001 -num_descriptions 1 -num_threads 8 -line_length 1000 -num_alignments 50000

		    ######## reformat the output ################
		    echo ""
		    echo "======================================================================================"
		    echo "         Converting $input_dir/$seq_id.bla from BLASTN to $input_dir/$seq_id.sto.         "
		    echo "======================================================================================"
		    echo ""
			./utils/parse_blastn_local.pl $input_dir/$seq_id.bla $input $input_dir/$seq_id.aln
			./utils/reformat.pl fas sto $input_dir/$seq_id.aln $input_dir/$seq_id.sto
		fi

		######## run infernal ################
        echo ""
        echo "=============================================================================================================="
        echo "      Building Covariance Model from BLASTN alignment file $input_dir/$seq_id.sto         "
        echo "=============================================================================================================="
        echo ""
		$path_infernal/cmbuild --noss --hand -F $input_dir/$seq_id.cm $input_dir/$seq_id.sto
		#$path_infernal/cmcalibrate $input_dir/$seq_id.cm
        echo ""
        echo "======================================================================================================================"
        echo "        Second round of homologous sequences search using the covariance model $input_dir/$seq_id.cm.          "
        echo "                      May take 15 mins to few hours for this step                                              "
        echo "======================================================================================================================"
        echo ""
		timeout 7200s $path_infernal/cmsearch -o $input_dir/$seq_id.out --cpu 30 --incE 10.0 $input_dir/$seq_id.cm $path_infernal_database
	fi

	######### get pssm from either from infernal and blstn alignment #############
	if [ -s $input_dir/$seq_id.out ];	then
		./utils/parse_cmsearch.pl $input_dir/$seq_id.out $input $input_dir/$seq_id.inf_aln
		./utils/getpssm.pl $input $input_dir/$seq_id.inf_aln $input_dir/$seq_id.pssm
	else
		echo "infernal alignment does not exits, therefore blastn alignment is used to get profile"
		./utils/getpssm.pl $input $input_dir/$seq_id.aln $input_dir/$seq_id.pssm
	fi

	######## run linearpartition to get bp probability ###########
    echo ""
    echo "======================================================================================================"
    echo "       Predicting Secondary Structure probability of query sequence $seq_id using LinearPartition. "
    echo "======================================================================================================"
    echo ""
	tail -n +2 $input | LinearPartition/linearpartition -V -r $input_dir/$seq_id.prob
	python3 ./utils/ss_feat.py $input

	########## combining all the features ###############
	./utils/combine_feat.pl $input_dir $seq_id $input
fi

########## run trained rnasnap2 model ###########
echo ""
echo "======================================================================================================"
echo "       Running RNAsnap2 for query sequence $seq_id. "
echo "======================================================================================================"
echo ""
python3 ./utils/rna-snap2.py --seq_id $input
end=`date +%s`

runtime=$((end-start))

echo -e "\ncomputation time = "$runtime" seconds"

