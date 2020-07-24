RNAsnap2: *Single-sequence and Profile-based Prediction of RNA Solvent Accessibility Using Dilated Convolution Neural Network.*
====

Contents
----
  * [Introduction](#introduction-)
  * [Results](#results-)
  * [System Requirments](#system-requirments)
  * [Installation](#installation)
  * [Usage](#Usage)
  * [Datasets](#datasets)
  * [Citation guide](#citation-guide)
  * [Licence](#licence)
  * [Contact](#contact)

Introduction
----
RNA solvent accessibility, similar to protein solvent accessibility, reflects the structural regions that are accessible to solvents or other functional biomolecules, and plays an important role for structural and functional characterization. Unlike protein solvent accessibility, only a few tools are available for predicting RNA solvent accessibility despite the fact that millions of RNA transcripts have unknown structures and functions. Also, these tools have limited accuracy. Here, we have developed RNAsnap2 that employs a dilated convolutional neural network (Figure 1) with a new feature, based on predicted base-pairing probabilities from LinearPartition[4].

|![](./RNAsnap2_architecture.png)
|----|
| <p align="center"> <b>Figure 1:</b> The network architecture of RNAsnap2. The residual block is shown within dashed red line. k, d, DF , and BIN are the size of filter, dropout rate, dilation factor, and batch instance normalization, respectively, and L is the length of the input RNA. Scalar 10 and 64 represent the number of features per nucleotide and the number filters in each convolutional layer, respectively.|

Results
----
Using the same training set from the recent predictor RNAsol[1], RNAsnap2 provides an 11% improvement in median Pearson’s Correlation Coefficient (PCC) and 9% improvement in mean absolute errors for the same test set of 45 RNA chains (TS45 in Figure 2). A larger improvement (22% in median PCC) is observed for 31 newly deposited RNA chains (TS31 in Figure 2) that are non-redundant and independent from the training and the test sets. A single-sequence version of RNAsnap2 (i.e. without using sequence profiles generated from homology search by Infernal) has achieved comparable performance to the profile-based RNAsol[1].

|![](./benchmark_results.png)
|----|
| <p align="center"> <b>Figure 2:</b> Distribution of PCC score for individual RNA chains on test sets TS45, TS45 ∗ , and TS31. On each box, the central mark indicates the median, and the bottom and top edges of the box indicate the 25th and 75th percentiles, respectively. The outliers are plotted individually by using the “+” symbol.|

System Requirments
----

**Hardware Requirments:**
RNAsnap2 predictor requires only a standard computer with around 32 GB RAM to support the in-memory operations for RNAs sequence length less than 500 for RNAsnap2 and 2,000 for RNAsnap2 (SingleSeq).

**Software Requirments:**
* [Python3](https://docs.python-guide.org/starting/install3/linux/)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) or [Anaconda](https://anaconda.org/anaconda/virtualenv)
* [CUDA 10.0](https://developer.nvidia.com/cuda-10.0-download-archive) (Optional If using GPU)
* [cuDNN (>= 7.4.1)](https://developer.nvidia.com/cudnn) (Optional If using GPU)

RNAsnap2 has been tested on Ubuntu 14.04, 16.04, and 18.04 operating systems.


Installation
----

To install RNAsnap2 and it's dependencies following commands can be used in terminal:

1. `git clone https://github.com/jaswindersingh2/RNAsnap2.git`
2. `cd RNAsnap2`

If using RNAsnap2 (SingleSeq) only then Step-3 to Step-6 can be skipped as these steps are only required for profile feature generation.

If Infernal tool is not installed in the system, please use follwing 2 command to download it otherwise provide absolute path to binary files of Infernal in line-13 of **run_rnasnap2.sh** file. In case of any problem and issue regarding Infernal download, please refer to [Infernal webpage](http://eddylab.org/infernal/) as following commands only tested on Ubuntu 18.04, 64 bit system.

3. `wget 'eddylab.org/infernal/infernal-1.1.3-linux-intel-gcc.tar.gz'`
4. `tar -xvzf infernal-*.tar.gz && rm infernal-*.tar.gz`

If BLASTN tool is not installed in the system, please use follwing 2 command to download otherwise provide absolute path to binary files of BLAST-N in line-11 of **run_rnasnap2.sh** file. In case of any problem and issue regarding BLASTN download, please refer to [BLASTN webpage](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) as following commands only tested on Ubuntu 18.04, 64 bit system.

5. `wget 'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-*+-x64-linux.tar.gz'`
6. `tar -xvzf ncbi-blast-*+-x64-linux.tar.gz && rm ncbi-blast-*+-x64-linux.tar.gz`

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

Usage
----

**To run the RNAsnap2 (SingleSeq)**

```
./run_singleseq.sh inputs/sample_seq.fasta
```
The output of this command will be the **sample_seq.rnasnap2_single** file in the **./outputs/** folder consists of predicted solvent accessibility by **RNAsnap2 (SingleSeq)** for a given input RNA sequence. To verify the output, the predicted ASA **sample_seq.rnasnap2_single** for **sample_seq.fasta** should be same as in existing **6ol3_C.rnasnap2_single** as both sequences are same.

**To run the RNAsnap2**

Before running RNAsnap2, please download the reference database ([NCBI's nt database](ftp://ftp.ncbi.nlm.nih.gov/blast/db/)) for BLASTN and INFERNAL. If referecne database already exists then provide absolute path to folder contains **nt** database file for Infernal in line-14 of **run_rnasnap2.sh** file and absolute path to folder contains formatted **nt.--.nhr/nin/nsq** database files for BLAST-N in line-12 of **run_rnasnap2.sh** file. Otherwise, the following command can used for NCBI's nt database download. Make sure there is enough space on the system as NCBI's nt database is of size around 270 GB after extraction and it can take couple of hours to download depending on the internet speed. In case of any issue, please rerfer to [NCBI's database website](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download).

```
wget -c "ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz -O ./nt_database/nt.gz && gunzip ./nt_database/nt.gz
```

This NCBI's database need to formated to use with BLASTN. To format the NCBI's database, the following command can be used. Please make sure system have enough space as formated database is of size around 120 GB and it can few hours for it.
```
./ncbi-blast-2.10.0+/bin/makeblastdb -in ./nt_database/nt -dbtype nucl
```

To run the RNAsnap2, the following command can be used.
```
./run_rnasnap2.sh inputs/sample_seq.fasta
```
The output of this command will be the **sample_seq.rnasnap2_profile** file in the **./outputs/** folder consists of predicted solvent accessibility by RNAsnap2  for a given input RNA sequence. To verify the output, the predicted ASA **sample_seq.rnasnap2_profile** for **sample_seq.fasta** should be almost (may be updated nt database used) same as in existing **6ol3_C.rnasnap2_profile** as both sequences are same.

Datasets
----

The following dataset was used for Training, Validation, and Testing of RNAsnap2:

[Dropbox](https://www.dropbox.com/s/fl1upqsvd7rpyrl/RNAsnap2_data.zip) or [Nihao Cloud](https://app.nihaocloud.com/f/afea8e005a964bf8bb0f/)

Citation guide
----

**If you use RNAsnap2 for your research please cite the following papers:**

Kumar, A., Singh, J., Paliwal, K., Singh, J., Zhou, Y., 2020. Single-sequence and Profile-based Prediction of RNA Solvent Accessibility Using Dilated Convolution Neural Network. Bioinformatics (in press)

**If you use RNAsnap2 data sets and/or input feature pipeline, please consider citing the following papers:**

[1] Sun, S., Wu, Q., Peng, Z. and Yang, J., 2019. Enhanced prediction of RNA solvent accessibility with long short-term memory neural networks and improved sequence profiles. Bioinformatics, 35(10), pp.1686-1691.

[2] Yang, Y., Li, X., Zhao, H., Zhan, J., Wang, J. and Zhou, Y., 2017. Genome-scale characterization of RNA tertiary structures and their functional impact by RNA solvent accessibility prediction. Rna, 23(1), pp.14-22. 

[3] H.M. Berman, J. Westbrook, Z. Feng, G. Gilliland, T.N. Bhat, H. Weissig, I.N. Shindyalov, P.E. Bourne. (2000) The Protein Data Bank Nucleic Acids Research, 28: 235-242.

[4] Zhang, H., Zhang, L., Mathews, D.H. and Huang, L., 2020. LinearPartition: linear-time approximation of RNA folding partition function and base-pairing probabilities. Bioinformatics, 36(Supplement_1), pp.i258-i267.

Licence
----
Mozilla Public License 2.0


Contact
----
jaswinder.singh3@griffithuni.edu.au, yaoqi.zhou@griffith.edu.au

