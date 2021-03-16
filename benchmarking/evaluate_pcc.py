import pandas as pd
import numpy as np
import pickle as pkl

with open('ts45_ids', 'r') as f:
    ts45_ids = f.read().splitlines()

with open('ts31_ids', 'r') as f:
    ts31_ids = f.read().splitlines()

testsets = [ts45_ids, ts31_ids]
testsets_name = ['TS45', 'TS31']

BASES = 'AUCG'
asa_std = [400, 350, 350, 400]
dict_rnam1_ASA = dict(zip(BASES, asa_std))

predictors = ['RNAsnap2', 'RNAsnap2_single', 'RNAsol', 'RNAsnap']

for predictor in predictors:

	print('\n'+predictor+':')

	for test_count, testset in enumerate(testsets):

		count = 0
		save_pcc = []

		for id in testset:

			with open('sequences/' + id) as f:
				temp_dbn = pd.read_csv(f, comment='#', delim_whitespace=True, header=None).values
			seq = [i for i in temp_dbn[1,0]]

			asa_div =  np.array([dict_rnam1_ASA[i] for i in seq])

			with open('true_asa/' + id + '.asa') as f:
				asa_true = pd.read_csv(f, comment='#', header=None, usecols=[1], skiprows=[0], delimiter='\t').values
			asa_true = np.squeeze(asa_true)/asa_div

			if predictor=='RNAsnap2':
				with open('rnasnap2/' + id + '.rnasnap2', 'r') as f:
					asa_pred1 = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values  
				pred_rnasnap2 = [i for i in asa_pred1[:, 2]]		
				pred = (pred_rnasnap2/asa_div)

			elif predictor=='RNAsnap2_single':
				with open('rnasnap2_single/' + id + '.rnasnap2_single', 'r') as f:
					asa_pred1 = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values       
				pred_rnasnap2_single = [i for i in asa_pred1[:, 2]]		
				pred = (pred_rnasnap2_single/asa_div)

			elif predictor=='RNAsol':	
				with open('RNAsol/' + id + '.rnasol', 'r') as f:
					asa_pred = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True).values
				pred = [i for i in asa_pred[:,0]]	

			elif predictor=='RNAsnap':
				with open('RNAsnap/' + id + '.asa', 'r') as f:
					asa_pred = pd.read_csv(f, delimiter=None, header=None, delim_whitespace=True, skiprows=[0]).values
				pred_rnasnap = [i for i in asa_pred[:, 2]]	
				pred = (pred_rnasnap/asa_div)

			stacked = np.stack((pred, asa_true), axis=0)
			pcc = np.corrcoef(stacked)

			save_pcc.append(np.corrcoef(np.stack((np.array(pred), np.array(asa_true)), axis=0))[0][1])

			count += 1

			# uncomment next 2 lines to see the PCC of individual RNA
			#print(id, end='\t')
			#print('PCC = {:.3f}'.format(np.corrcoef(np.stack((np.array(pred), np.array(asa_true)), axis=0))[0][1]))

		print('{} Mean PCC = {:.3f}'.format(testsets_name[test_count], np.mean(save_pcc), count))

