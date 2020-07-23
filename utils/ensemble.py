import numpy as np
import pandas as pd
import sys, os


with open(sys.argv[1] + '.rnasnap2_single', 'r') as f:
	asa_single = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values
#print(asa_single.shape)
asa_single = [i for i in asa_single[:,2]]

with open(sys.argv[1] + '.rnasnap2_profile', 'r') as f:
	asa_profile = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values

seq = [i for i in asa_profile[:,1][:]]
asa_profile = [i for i in list(asa_profile[:,2])]

pred_asa = [(i+j)/2 for i,j in zip(asa_profile, asa_single)]

col1 = np.array([i+1 for i,I in enumerate(seq)])[None, :]
col2 = np.array([I for i,I in enumerate(seq)])[None, :]
col3 =  np.array(pred_asa)[None, :]

temp = np.vstack((np.char.mod('%d', col1), col2, np.char.mod('%d', col3))).T
#print(temp)

np.savetxt(sys.argv[1] +'.rnasnap2', (temp), delimiter='\t\t', fmt="%s", header='#\t' + sys.argv[1] + '\t' + 'RNAsnap-2' + '\n', comments='')
