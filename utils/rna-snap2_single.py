import tensorflow as tf
import numpy as np
import pandas as pd
import os, argparse
import pickle as pkl
import time
start = time.time()
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser()
parser.add_argument('--seq_id',default='', type=str, help='name of input sequence')
parser.add_argument('--batch_size',default=1, type=str, help='number of sequences predicts simultaneously')
parser.add_argument('--outputs',default='./outputs', type=str, help='Path to output files; default = ''outputs/\n', metavar='')
parser.add_argument('--gpu', default=-1, type=int, help='To run on GPU, specifiy GPU number. If only one GPU in computer specifiy 0; default = -1 (no GPU)\n', metavar='')
args = parser.parse_args()

norm_mu = [0.24231204, 0.18269396, 0.32596249, 0.24903151, 0.31261292]
norm_std = [0.42848211, 0.38641542, 0.46873334, 0.4324521, 0.41229352]

with open(args.seq_id) as file:
    input_data = [line.strip() for line in file.read().splitlines() if line.strip()]

count = int(len(input_data)/2)

#ids = [input_data[2*i].replace(">", "") for i in range(count)]
ids = [args.seq_id.split('/')[-1]]

sequences = {}
for i,I in enumerate(ids):
    sequences[I] = input_data[2*i+1].replace(" ", "").replace("T", "U")

BASES = 'AUGC'
bases = np.array([base for base in BASES])

feat_dic = {}
for i,I in enumerate(ids):
	feat_onehot = np.concatenate([[(bases==base.upper()).astype(int)] if str(base).upper() in BASES else np.array([[0]*len(BASES)]) for base in sequences[I]])
	with open('inputs/' + I.split('.')[0] + '.prob', 'r') as f:
		prob = pd.read_csv(f, delimiter=None, delim_whitespace=True, header=None, skiprows=[0]).values
	bp_prob =  np.zeros((len(sequences[I]), len(sequences[I])))
	for i in prob:
		bp_prob[int(i[0])-1, int(i[1])-1] = i[2]
	bp_prob = np.sum(bp_prob, axis=1)
	feat_dic[I] = np.concatenate([feat_onehot, bp_prob[:,None]], axis=1)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

os.environ["CUDA_VISIBLE_DEVICES"]= str(args.gpu)

def sigmoid(x):
    return 1/(1+np.exp(-np.array(x, dtype=np.float128)))

def get_data(sample_feat, ids, batch_size, i, norm_mu,norm_std):
    data = [(sample_feat[j][:,:]-norm_mu)/norm_std for j in ids[i * batch_size:np.min([(i + 1) * batch_size, len(ids)])]]
    data = [np.concatenate([np.ones((j.shape[0], 1)), j], axis=1) for j in data]
    seq_lens = [j.shape[0] for j in data]
    batch_ids = [j for j in ids[i * batch_size:np.min([(i + 1) * batch_size, len(ids)])]]
    max_seq_len = max(seq_lens)
    data = np.concatenate([np.concatenate([j, np.zeros((max_seq_len - j.shape[0], j.shape[1]))])[None, :, :] for j in data])

    mask = np.concatenate([np.concatenate([np.ones((1, seq_lens[j])), np.zeros((1, max_seq_len - seq_lens[j]))], axis=1) for j in range(len(ids[i * batch_size:np.min(((i + 1) * batch_size, len(ids)))]))])

    return data, mask, seq_lens, batch_ids

def sigmoid(x):
  return 1 / (1 + np.exp(-x))


config = tf.compat.v1.ConfigProto()
config.allow_soft_placement=True
config.log_device_placement=False

outputs = {}
with tf.compat.v1.Session(config=config) as sess:
    saver = tf.compat.v1.train.import_meta_graph('models/tensorflow_model_single.meta')
    saver.restore(sess,'models/tensorflow_model_single')
    graph = tf.compat.v1.get_default_graph()
    tmp_out = graph.get_tensor_by_name('output_FC/fully_connected/BiasAdd:0')
    
    for batch_test in range(max(1,int(np.ceil(count/args.batch_size)))):
        feature, mask, seq_lens, batch_ids = get_data(feat_dic, ids, batch_size=args.batch_size, i=batch_test, norm_mu=norm_mu, norm_std=norm_std)
        out = sess.run([tmp_out],feed_dict={'input_feature:0': feature, 'zero_mask:0':mask, 'label_mask:0':mask, 'keep_prob:0':1.})
        pred_norm_asa = np.multiply(np.squeeze(sigmoid(out[0]), axis=2), mask)
        for i, id in enumerate(batch_ids):
            outputs[id] = pred_norm_asa[i,0:seq_lens[i]]
tf.compat.v1.reset_default_graph()

BASES = 'AUCG'
asa_std = [400, 350, 350, 400]
dict_rnam1_ASA = dict(zip(BASES, asa_std))

for id in ids:
    ASA_scale =  np.array([dict_rnam1_ASA[i] for i in sequences[id]])[:,None]
    pred_asa = np.multiply(outputs[id][:,None], ASA_scale).T

    col1 = np.array([i+1 for i,I in enumerate(sequences[id])])[None, :]
    col2 = np.array([I for i,I in enumerate(sequences[id])])[None, :]
    col3 =  pred_asa

    temp = np.vstack((np.char.mod('%d', col1), col2, np.char.mod('%d', col3))).T

    np.savetxt(os.path.join(args.outputs, str(id.split('.')[0]))+'.rnasnap2_single', (temp), delimiter='\t\t', fmt="%s", header='#\t' + str(id) + '\t' + 'RNAsnap-2' + '\n', comments='')
