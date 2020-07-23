import numpy as np
import pandas as pd
import sys

with open(sys.argv[1] + '.fasta', 'r') as f:
	seq = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values
seq = [i for i in seq[0][0]]

with open(sys.argv[1] + '.prob', 'r') as f:
	prob = pd.read_csv(f, delimiter=None, delim_whitespace=True, header=None, skiprows=[0]).values
bp_prob =  np.zeros((len(seq), len(seq)))
for i in prob:
	#print(i[0], i[1], i[2])
	bp_prob[int(i[0])-1, int(i[1])-1] = i[2]
bp_prob = np.sum(bp_prob, axis=1)

np.savetxt(sys.argv[1] + '.stru', bp_prob[None, :], fmt='%.18e', delimiter='\t')

#print(bp_prob[None, :].shape)
