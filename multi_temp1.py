# 					Disease mention recognition with class

#This code is a modified version of the code provided by Matthieu Labeau in "Non-lexical neural architecture for fine-grained POS Tagging" https://github.com/MatthieuLabeau/NonlexNN

from model1 import *
import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet as nnet

from data_proc import *
from dataset import Dataset
from utils import *
from emb import *
from hidden import *
from output import *
from trainer import *

N = 100000 # training set size
M = 10000 # after every 10k sentence, check validation and testing datas
n_f = 100 # dim of word embedding
n_hidden = 100 #number of nodes in hidden layer
model = 'ff' # model used for classification : 'ff' or 'biRNN'
viterbi = True #structure output or not
trainer = 'AdagradTrainer' # Training method
lr = 0.05 #learning rate
batch_size = 1 #batch_size 
activation = T.tanh
output_fname_dev = "multi_results/nn_dev_res_100d_cbow_wu_"
output_fname_test = "multi_results/rnn_test_res_100d_cbow_wu_"

# input file names
path = "class_data/"
train_w = "train_words.txt"
train_t = "train_tags.txt"
dev_w = "dev_words.txt"
dev_t = "dev_tags.txt"
test_w = "test_words.txt"
test_t = "test_tags.txt"

fvocab = "word2vec/vocab.txt"		# word list
fname = "word2vec/cbow_100d.txt"	# its corresponding vector we have assigne random vector for OoV word

# Creating vocabularies 
wl = create_wl(fvocab) 
print "word len", len(wl)

id2word = invert_dict(wl)

tl = {"O":0, "B-CM":1, "I-CM":2, "B-SD":3, "I-SD":4, "B-M":5, "I-M":6, "B-DC":7, "I-DC":8}

trainset = Dataset(path+train_w, path+train_t, wl, tl, batch_size)
devset = Dataset(path+dev_w, path+dev_t, wl, tl, batch_size)
testset = Dataset(path+test_w, path+test_t, wl, tl, batch_size)

print "trainset", trainset.tot
print "devset", devset.tot
print "testset", testset.tot

sampler = trainset.sampler()
dev_sampler = devset.sampler()
test_sampler = testset.sampler()

l_vocab_w = len(wl)
l_vocab_out=len(tl) 

model = SLLModel(l_vocab_w = l_vocab_w, l_vocab_out = l_vocab_out, n_f = n_f, n_hidden = n_hidden, lr = lr, trainer = trainer, activation=T.tanh, model = model, viterbi = viterbi, fname = fname, wl = wl)

#train_res = []
j=1
for i in range(N):
	if(i == 0):
		continue
	inputs, tags, = sampler.next() 
	res = model.train_perplexity(inputs[0],tags[0])
	if(i%500 == 0):
		print res
	if(i%M == 0):
		print "res", res
		f = open(output_fname_dev +str(j),"w+")
		dev_pred = []
		dev_true = []
				#DEV DATA
		for m in range(939):
 			dev_inputs, dev_tags  = dev_sampler.next()		#dev data
			res = model.eval_perplexity(dev_inputs[0], dev_tags[0])
			pred = model.predict(dev_inputs[0])

			viterbi_max, viterbi_argmax =  model.output_decode(dev_inputs[0]) 	
			first_ind = np.argmax(viterbi_max[-1])
			viterbi_pred =  backtrack(first_ind, viterbi_argmax)
			vi_pre = np.array(viterbi_pred)
 			dev_true = list(dev_tags[0])
			for k,l,n in zip(vi_pre, dev_true, dev_inputs[0]):
 				dev_true.extend(str(l))
				dev_pred.extend(str(k))
				f.write(id2word[n])
				f.write(" ")
				if(l == 0):
					f.write("O")
				if(l == 1):
					f.write("B-CM")
				if(l == 2):
					f.write("I-CM")	
				if(l == 3):
					f.write("B-SD")
				if(l == 4):
					f.write("I-SD")
				if(l == 5):
					f.write("B-M")	
				if(l == 6):
					f.write("I-M")
				if(l == 7):
					f.write("B-DC")
				if(l == 8):
					f.write("I-DC") 
				f.write(" ")

				if(k == 0):
					f.write("O")
				if(k == 1):
					f.write("B-CM")
				if(k == 2):
					f.write("I-CM")	
				if(k == 3):
					f.write("B-SD")
				if(k == 4):
					f.write("I-SD")
				if(k == 5):
					f.write("B-M")	
				if(k == 6):
					f.write("I-M")
				if(k == 7):
					f.write("B-DC")
				if(k == 8):
					f.write("I-DC") 
				f.write('\n')
			f.write('\n')
		f.close()

		g = open(output_fname_test +str(j),"w+")
		j += 1
				#TEST DATA
		for m in range(961):
#			print "vali", m
#			dev_inputs, dev_tags = dev_sampler.next()					 
			test_inputs, test_tags = test_sampler.next()		#dev data
			res = model.eval_perplexity(test_inputs[0], test_tags[0])
			pred = model.predict(test_inputs[0])

			viterbi_max, viterbi_argmax =  model.output_decode(test_inputs[0]) 	
			first_ind = np.argmax(viterbi_max[-1])
			viterbi_pred =  backtrack(first_ind, viterbi_argmax)
			vi_pre = np.array(viterbi_pred)

#			vi_pre = pred

			test_true = list(test_tags[0])
			for k,l,n in zip(vi_pre, test_true, test_inputs[0]):
				#print"pred", i
				#print"true", j
				dev_true.extend(str(l))
				dev_pred.extend(str(k))
				g.write(id2word[n])
				g.write(" ")
				if(l == 0):
					g.write("O")
				if(l == 1):
					g.write("B-CM")
				if(l == 2):
					g.write("I-CM")	
				if(l == 3):
					g.write("B-SD")
				if(l == 4):
					g.write("I-SD")
				if(l == 5):
					g.write("B-M")	
				if(l == 6):
					g.write("I-M")
				if(l == 7):
					g.write("B-DC")
				if(l == 8):
					g.write("I-DC") 
				g.write(" ")

				if(k == 0):
					g.write("O")
				if(k == 1):
					g.write("B-CM")
				if(k == 2):
					g.write("I-CM")	
				if(k == 3):
					g.write("B-SD")
				if(k == 4):
					g.write("I-SD")
				if(k == 5):
					g.write("B-M")	
				if(k == 6):
					g.write("I-M")
				if(k == 7):
					g.write("B-DC")
				if(k == 8):
					g.write("I-DC") 
				g.write('\n')
			g.write('\n')
		g.close()
	
