# RNAsnap2
Single-sequence and Profile-based Prediction of RNA Solvent Accessibility Using Dilated Convolution Neural Network.

SYSTEM REQUIREMENTS
====
Hardware Requirments:
----
RNAsnap2 predictor requires only a standard computer with around 8 GB RAM to support the in-memory operations for RNAs sequence length less than 20,000.

Software Requirments:
----
* [Python3](https://docs.python-guide.org/starting/install3/linux/)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) or [Anaconda](https://anaconda.org/anaconda/virtualenv)
* [CUDA 10.0](https://developer.nvidia.com/cuda-10.0-download-archive) (Optional If using GPU)
* [cuDNN (>= 7.4.1)](https://developer.nvidia.com/cudnn) (Optional If using GPU)

RNAsnap2 has been tested on Ubuntu 14.04, 16.04, and 18.04 operating systems.

USAGE
====

Installation:
----

To install RNAsnap2 and it's dependencies following commands can be used in terminal:

1. `git clone https://github.com/jaswindersingh2/RNAsnap2.git`
2. `cd RNAsnap2`

If using RNAsnap2 (SingleSeq) only then Step-3 to Step-6 can be skipped as these steps are only required for profile feature generation.

If Infernal tool is not installed in the system, please use follwing 2 command to download and extract it. In case of any problem and issue regarding Infernal download, please refer to [Infernal webpage](http://eddylab.org/infernal/) as following commands only tested on Ubuntu 18.04, 64 bit system.

3. `wget 'eddylab.org/infernal/infernal-1.1.3-linux-intel-gcc.tar.gz'`
4. `tar -xvzf infernal-*.tar.gz && rm infernal-*.tar.gz`

If BLASTN tool is not installed in the system, please use follwing 2 command to download and extract it. In case of any problem and issue regarding BLASTN download, please refer to [BLASTN webpage](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) as following commands only tested on Ubuntu 18.04, 64 bit system.

5. `wget 'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.10.0+-x64-linux.tar.gz'`
6. `tar -xvzf ncbi-blast-2.10.0+-x64-linux.tar.gz && rm ncbi-blast-2.10.0+-x64-linux.tar.gz`

The following 2 commands for cloning LinearPartition respository from GITHUB and then making files. In case of any problem and issue, please refer to the [LinearPartition](https://github.com/LinearFold/LinearPartition) repository.

7. `git clone 'https://github.com/LinearFold/LinearPartition.git'`
8. `cd LinearPartition/ && make && cd ../`

Either follow **virtualenv** column steps or **conda** column steps to create virtual environment and to install RNAsnap2 dependencies given in table below:<br />

|  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; virtualenv | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conda |
| :- | :-------- | :--- |
| 9. | `virtualenv -p python3.6 venv` | `conda create -n venv python=3.6` |
| 10. | `source ./venv/bin/activate` | `conda activate venv` | 
| 11. | *To run RNAsnap2 on CPU:*<br /> <br /> `pip install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run RNAsnap2 on GPU:*<br /> <br /> `pip install tensorflow-gpu==1.14.0` | *To run RNAsnap2 on CPU:*<br /> <br /> `conda install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run RNAsnap2 on GPU:*<br /> <br /> `conda install tensorflow-gpu==1.14.0` |
| 12. | `pip install -r requirements.txt` | `while read p; do conda install --yes $p; done < requirements.txt` | 

To run the RNAsnap2 (SingleSeq)
-----
```
./run_singleseq.sh inputs/sample_seq.fasta
```
The output of this command will be the "*.rnasnap2_single" file in the "outputs" folder consists of predicted solvent accessibility by RNAsnap2 (SingleSeq) for a given input RNA sequence.

To run the RNAsnap2
-----
Before running RNAsnap2, please download the reference database ([NCBI's nt database](ftp://ftp.ncbi.nlm.nih.gov/blast/db/)) for BLASTN and INFERNAL. The following command can used for NCBI's nt database. Make sure there is enough space on the system as NCBI's nt database is of size around 270 GB after extraction and it can take couple of hours to download depending on the internet speed. In case of any issue, please rerfer to [NCBI's database website](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download).

```
wget -c "ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz -O ./nt_database && gunzip ./nt_database/nt.gz
```

This NCBI's database need to formated to use with BLASTN. To format the NCBI's database, the following command can be used. Please make sure system have enough space as formated database is of size around 120 GB and it can few hours for it.
```
./ncbi-blast-2.10.0+/bin/makeblastdb -in ./nt_database -dbtype nucl
```

To run the RNAsnap2, the following command can be used.
```
./run_rnasnap2.sh inputs/sample_seq.fasta
```
The output of this command will be the "*.rnasnap2_profile" file in the "outputs" folder consists of predicted solvent accessibility by RNAsnap2 for a given input RNA sequence.

Datasets
====

The following dataset was used for Training, Validation, and Testing of RNAsnap2:

[Dropbox](https://www.dropbox.com/s/fl1upqsvd7rpyrl/RNAsnap2_data.zip) or [Nihao Cloud](https://app.nihaocloud.com/f/afea8e005a964bf8bb0f/)

References
====
If you use RNAsnap2 for your research please cite the following papers:
----
Kumar, A., Singh, J., Paliwal, K., Singh, J., Zhou, Y., 2020. Single-sequence and Profile-based Prediction of RNA Solvent Accessibility Using Dilated Convolution Neural Network. (Under review)

Other references:
----
[1] Sun, S., Wu, Q., Peng, Z. and Yang, J., 2019. Enhanced prediction of RNA solvent accessibility with long short-term memory neural networks and improved sequence profiles. Bioinformatics, 35(10), pp.1686-1691.

[2] Yang, Y., Li, X., Zhao, H., Zhan, J., Wang, J. and Zhou, Y., 2017. Genome-scale characterization of RNA tertiary structures and their functional impact by RNA solvent accessibility prediction. Rna, 23(1), pp.14-22. 

[3] H.M. Berman, J. Westbrook, Z. Feng, G. Gilliland, T.N. Bhat, H. Weissig, I.N. Shindyalov, P.E. Bourne. (2000) The Protein Data Bank Nucleic Acids Research, 28: 235-242.

[4] Zhang, H., Zhang, L., Mathews, D.H. and Huang, L., 2019. LinearPartition: Linear-Time Approximation of RNA Folding Partition Function and Base Pairing Probabilities. arXiv preprint arXiv:1912.13190.

Licence
====
Mozilla Public License 2.0


Contact
====
jaswinder.singh3@griffithuni.edu.au, yaoqi.zhou@griffith.edu.au

