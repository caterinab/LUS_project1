import sys

op = str(sys.argv[1])

if(op == "1"):
	f = open("../train.txt.conll", "r")
	m = open("../test.txt.conll", "r")
else:
	f = open("../train.txt", "r")
	m = open("../test.txt", "r")
p = open("analysis.txt", "w")

tags = list()
words = list()
lines = list()
tag_utterances = list()

# extract tags and words and remove \n from lines
for line in f:
	if line.strip():
		l = line.split()
		tag = l[1].strip()
		tags.append(tag)
		words.append(l[0])

u_tags = set(tags)
u_tags = sorted(u_tags)
u_words = set(words)
u_words = sorted(u_words)
tag_counts = list()

p.write("Tag counts:\n")
# count tag occurencies
for tag in u_tags:
	c = tags.count(tag)
	p.write(tag + "," + str(c) + "\n")

p.write("Word counts:\n")
# count word occurencies
for word in u_words:
	c = words.count(word)
	p.write(word + "," + str(c) + "\n")

'''p.write("Pair counts:\n")
# count word-tag pairs occurencies
for pair in u_word_tag:
	c = lines.count(pair)
	p.write("%s,%d" % (pair, str(c)) + "\n")'''

f.close()
m.close()
p.close()
