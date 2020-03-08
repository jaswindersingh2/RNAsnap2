# RNAsnap2
Single-sequence and Profile-based Prediction of RNA Solvent Accessibility Using Dilated Convolution Neural Network

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

SPOT-RNA has been tested on Ubuntu 14.04, 16.04, and 18.04 operating systems.

USAGE
====

Installation:
----

To install SPOT-RNA and it's dependencies following commands can be used in terminal:

1. `git clone https://github.com/jaswindersingh2/RNAsnap2.git`
2. `cd RNAsnap2`

Either follow **virtualenv** column steps or **conda** column steps to create virtual environment and to install SPOT-RNA dependencies given in table below:<br />

|  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; virtualenv | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conda |
| :- | :-------- | :--- |
| 5. | `virtualenv -p python3.6 venv` | `conda create -n venv python=3.6` |
| 6. | `source ./venv/bin/activate` | `conda activate venv` | 
| 7. | *To run SPOT-RNA on CPU:*<br /> <br /> `pip install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run SPOT-RNA on GPU:*<br /> <br /> `pip install tensorflow-gpu==1.14.0` | *To run SPOT-RNA on CPU:*<br /> <br /> `conda install tensorflow==1.14.0` <br /> <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *or* <br /> <br />*To run SPOT-RNA on GPU:*<br /> <br /> `conda install tensorflow-gpu==1.14.0` |
| 8. | `pip install -r requirements.txt` | `while read p; do conda install --yes $p; done < requirements.txt` | 

To run the SPOT-RNA
-----

**For single sequence:**
```
python3 SPOT-RNA.py  --inputs sample_inputs/single_seq.fasta  --outputs 'outputs/'
```
The output come of above command will be three files (.bpseq, .ct, and .prob) in 'outputs' folder. The '.bpseq' and '.ct' file is the standard format to represent RNA secondary structure. '.prob' file consists of the base-pair probability of predicted secondary structure by SPOT-RNA which can be useful for plotting PR-curve and to check the confidence of predicted base-pair.
