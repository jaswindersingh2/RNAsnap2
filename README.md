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

If you are using RNAsnap2 (SingleSeq) then Step-3 to Step-7 can be skipped as these steps are only required for profile feature generation.

3. `wget 'eddylab.org/infernal/infernal-1.1.3-linux-intel-gcc.tar.gz'`
4. `tar -xvzf infernal-*.tar.gz && rm infernal-*.tar.gz`
5. `wget 'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.10.0+-x64-linux.tar.gz'`
6. `tar -xvzf ncbi-blast-2.10.0+-x64-linux.tar.gz && rm ncbi-blast-2.10.0+-x64-linux.tar.gz`
7. `git clone 'https://github.com/LinearFold/LinearPartition.git'`
8. `cd LinearPartition/ && make && cd ../`

Either follow **virtualenv** column steps or **conda** column steps to create virtual environment and to install RNAsnap2 dependencies given in table below:<br />

|  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; virtualenv | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conda |
| :- | :-------- | :--- |
| 5. | `virtualenv -p python3.6 venv` | `conda create -n venv python=3.6` |
| 6. | `source ./venv/bin/activate` | `conda activate venv` | 
| 7. | *To run RNAsnap2 on CPU:*<br /> <br /> `pip install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run RNAsnap2 on GPU:*<br /> <br /> `pip install tensorflow-gpu==1.14.0` | *To run RNAsnap2 on CPU:*<br /> <br /> `conda install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run RNAsnap2 on GPU:*<br /> <br /> `conda install tensorflow-gpu==1.14.0` |
| 8. | `pip install -r requirements.txt` | `while read p; do conda install --yes $p; done < requirements.txt` | 

To run the RNAsnap2 (SingleSeq)
-----
```
./run_singleseq.sh inputs/sample_seq.fasta
```

To run the RNAsnap2
-----
```
./pred.sh inputs/sample_seq.fasta
```
