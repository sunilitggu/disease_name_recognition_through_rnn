fl = "test.txt"
f = open(fl, "r")

sent_list = f.read().strip().split("\n\n")
sents = []
tag_sents = []
for sent in sent_list :
	word_list = sent.split('\n')
	words = []
	tags = []
	for line in word_list :
		w,t = line.strip().split()
		words.append(w)
		tags.append(int(t))
	sents.append(words)
	tag_sents.append(tags)

print len(sents)
print len(tag_sents)

tag_list = []
for i in xrange(len(sents)):
	tag = []
	cond = 1
	for j in xrange(len(sents[i])):
		if(tag_sents[i][j] == 1 and cond == 1):
			tag.append("B-Dis")
			cond = 0
		elif(tag_sents[i][j] == 1 and cond == 0):
			tag.append("I-Dis")
		elif(tag_sents[i][j] == 0 and cond == 0):
			tag.append("O")
			cond = 1
		else:
			tag.append("O")
	tag_list.append(tag)

g = open("test_words.txt", "w")
h = open("test_tags.txt", "w")
for i in xrange(len(sents)):
	for j in xrange(len(sents[i])):
		g.write(sents[i][j])
		g.write(" ")
		h.write(tag_list[i][j])
		h.write(" ")
	g.write("\n")
	h.write("\n")

"""
pred = []
cond=1
for t in pred_r:
	if(t==1 and cond == 1):
		pred.append("B-Dis")
		cond = 0
	elif( t==1 and cond==0):
		pred.append("I-Dis")
	elif( t==0 and cond==0):
		pred.append("O")
		cond = 1
	else :
		pred.append("O")

true = []
cond=1
for t in true_r:
	if(t==1 and cond == 1):
		true.append("B-Dis")
		cond = 0
	elif( t==1 and cond==0):
		true.append("I-Dis")
	elif( t==0 and cond==0):
		true.append("O")
		cond = 1
	else :
		true.append("O") 

if len(true) == len(pred):
	for i in range(len(true)):
		print true[i] +" "+pred[i]

"""
