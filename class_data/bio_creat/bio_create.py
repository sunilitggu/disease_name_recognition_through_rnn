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
	cm = sd = m = dc = 1
	for j in xrange(len(sents[i])):
		if(tag_sents[i][j] == 1 and cm == 1):
			tag.append("B-CM")
			cm = 0
			sd = m = dc = 1

		elif(tag_sents[i][j] == 1 and cm == 0):
			tag.append("I-CM")

		elif(tag_sents[i][j] == 2 and sd == 1):
			tag.append("B-SD")
			sd = 0
			cm = m = dc = 1

		elif(tag_sents[i][j] == 2 and sd == 0):
			tag.append("I-SD")
			
		elif(tag_sents[i][j] == 3 and m == 1):
			tag.append("B-M")
			m = 0
			cm = sd = dc = 1

		elif(tag_sents[i][j] == 3 and m == 0):
			tag.append("I-M")

		elif(tag_sents[i][j] == 4 and dc == 1):
			tag.append("B-DC")
			dc = 0
			cm = sd = m = 1
		elif(tag_sents[i][j] == 4 and dc == 0):
			tag.append("I-DC")

		else:
			tag.append("O")
			cm = sd = m = dc = 1

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

