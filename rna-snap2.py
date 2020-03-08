import tensorflow as tf
import numpy as np
import pandas as pd
import os, argparse
import pickle as pkl
import time
start = time.time()
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser()
parser.add_argument('--path_input', default='inputs', type=str, help='Path to input file in fasta format, accept multiple sequences as well in fasta format; default = ''sample_inputs/2zzm-1-B.fasta''\n', metavar='')
parser.add_argument('--seq_id',default='', type=str, help='name of input sequence')
parser.add_argument('--meta_file_path',default='', type=str, help='path to meta files')
parser.add_argument('--batch_size',default=1, type=str, help='number of sequences predicts simultaneously')
parser.add_argument('--outputs',default='./outputs', type=str, help='Path to output files; SPOT-RNA outputs at least three files .ct, .bpseq, and .prob files; default = ''outputs/\n', metavar='')
parser.add_argument('--gpu', default=-1, type=int, help='To run on GPU, specifiy GPU number. If only one GPU in computer specifiy 0; default = -1 (no GPU)\n', metavar='')
args = parser.parse_args()

#with open('feat_dic_rnasol_infernal_prob', 'rb') as f:
#    feat_dic = pkl.load(f)

norm_mu = [0.24231204, 0.18269396, 0.32596249, 0.24903151, 0.22588943, 0.14617564, 0.29558719, 0.20700315, 0.31261292]
norm_std = [0.42848211, 0.38641542, 0.46873334, 0.4324521,  0.61212416, 0.61543625, 0.63496662, 0.63862874, 0.41229352]

#print(args.path_input, args.seq_id)

with open(args.path_input + '/' + args.seq_id + '.fasta') as file:
    input_data = [line.strip() for line in file.read().splitlines() if line.strip()]

with open(args.path_input + '/' + args.seq_id + '.profile', 'r') as f:
	profile = pd.read_csv(f, delimiter='\t', header=None, usecols=[0,1,2,3,4,5,6,7,8,9]).values

count = int(len(input_data)/2)

ids = [input_data[2*i].replace(">", "") for i in range(count)]
sequences = {}
for i,I in enumerate(ids):
    sequences[I] = input_data[2*i+1].replace(" ", "").replace("T", "U")

feat_dic = {}
for i,I in enumerate(ids):
    feat_dic[I] = profile

#print(sequences)
#print(feat_dic[ids[0]].shape)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

os.environ["CUDA_VISIBLE_DEVICES"]= str(args.gpu)
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


def sigmoid(x):
    return 1/(1+np.exp(-np.array(x, dtype=np.float128)))

def get_data(sample_feat, ids, batch_size, i, norm_mu,norm_std):
    #print(sample_feat[ids[0]])
    #print(ids, batch_size, i, ids[i * batch_size:np.min([(i + 1) * batch_size, len(ids)])])
    data = [(sample_feat[j][:,1:]-norm_mu)/norm_std for j in ids[i * batch_size:np.min([(i + 1) * batch_size, len(ids)])]]
    data = [np.concatenate([np.ones((j.shape[0], 1)), j], axis=1) for j in data]
    seq_lens = [j.shape[0] for j in data]
    batch_ids = [j for j in ids[i * batch_size:np.min([(i + 1) * batch_size, len(ids)])]]
    max_seq_len = max(seq_lens)
    data = np.concatenate([np.concatenate([j, np.zeros((max_seq_len - j.shape[0], j.shape[1]))])[None, :, :] for j in data])

    mask = np.concatenate([np.concatenate([np.ones((1, seq_lens[j])), np.zeros((1, max_seq_len - seq_lens[j]))], axis=1) for j in range(len(ids[i * batch_size:np.min(((i + 1) * batch_size, len(ids)))]))])

    return data, mask, seq_lens, batch_ids

def sigmoid(x):
  return 1 / (1 + np.exp(-x))


#print(feature.shape)
#print(mask.shape)
#print(max_seq_len)

config = tf.compat.v1.ConfigProto()
config.allow_soft_placement=True
config.log_device_placement=False

outputs = {}
#print('\nPredicting for SPOT-RNA model '+str(MODEL))
with tf.compat.v1.Session(config=config) as sess:
    saver = tf.compat.v1.train.import_meta_graph(str(args.meta_file_path) + 'models/tensorflow_model_profile.meta')
    saver.restore(sess,str(args.meta_file_path) + 'models/tensorflow_model_profile')
    graph = tf.compat.v1.get_default_graph()
    tmp_out = graph.get_tensor_by_name('output_FC/fully_connected/BiasAdd:0')
    
    for batch_test in range(max(1,int(np.ceil(count/args.batch_size)))):
        feature, mask, seq_lens, batch_ids = get_data(feat_dic, ids, batch_size=args.batch_size, i=batch_test, norm_mu=norm_mu, norm_std=norm_std)
        #print(seq_lens, batch_ids)
        out = sess.run([tmp_out],feed_dict={'input_feature:0': feature, 'zero_mask:0':mask, 'label_mask:0':mask, 'keep_prob:0':1.})
        pred_norm_asa = np.multiply(np.squeeze(sigmoid(out[0]), axis=2), mask)
        for i, id in enumerate(batch_ids):
            outputs[id] = pred_norm_asa[i,0:seq_lens[i]]
tf.compat.v1.reset_default_graph()
#print(len(out[0][0]))

#print(pred_norm_asa.shape)
#print(outputs)

BASES = 'AUCG'
asa_std = [400, 350, 350, 400]
dict_rnam1_ASA = dict(zip(BASES, asa_std))

for id in ids:
    ASA_scale =  np.array([dict_rnam1_ASA[i] for i in sequences[id]])[:,None]
    #print(outputs[id].shape, ASA_scale.shape)

    pred_asa = np.multiply(outputs[id][:,None], ASA_scale).T
#    pred_asa = outputs[id][:,None].T
    #print(pred_asa)

    col1 = np.array([i+1 for i,I in enumerate(sequences[id])])[None, :]
    col2 = np.array([I for i,I in enumerate(sequences[id])])[None, :]
    col3 =  pred_asa

    temp = np.vstack((np.char.mod('%d', col1), col2, np.char.mod('%d', col3))).T
    #print(temp)

    np.savetxt(os.path.join(args.outputs, str(id))+'.rnasnap2_profile', (temp), delimiter='\t\t', fmt="%s", header='#\t' + str(id) + '\t' + 'RNAsnap-2' + '\n', comments='')
