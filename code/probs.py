import numpy as np
from os import path
import sys

output_folder = str(sys.argv[1])
method = str(sys.argv[2])

if(method == "3"):
	f = open("../train.txt.conll", "r")
	m = open("../test.txt.conll", "r")
else:
	f = open("../train.txt", "r")
	m = open("../test.txt", "r")
g = open(path.join(output_folder, "iob.txt"), "w")
h = open(path.join(output_folder, "utterances.txt"), "w")
n = open(path.join(output_folder, "text_utterances.txt"), "w")
o = open(path.join(output_folder, "lex.txt"), "w")

# create file with text only sentences
first = 1
for line in m:
	if line.strip():
		l = line.split()

		if(first):
			first = 0
		else:
			n.write(" ")

		n.write(l[0])
	else:
		first = 1
		n.write("\n")

tags = list()
words = list()
lines = list()
tag_utterances = list()

first = 1

# extract tags and words and remove \n from lines
for line in f:
	if line.strip():
		l = line.split()
		tag = ""
		if(method == "2" and l[1] == "O"):
			tag = l[1].strip() + "-" + l[0]
			lines.append(l[0] + "\t" + l[1] + "-" + l[0])				
		else:
			tag = l[1].strip()
			lines.append(l[0] + "\t" + l[1])
		tags.append(tag)
		words.append(l[0])

		if(first):
			first = 0
		else:
			tag_utterances.append(" ")
		tag_utterances.append(tag)
	else:
		first = 1
		tag_utterances.append("\n")

# write tag utterances file for language model
for u in tag_utterances:
	h.write(u)

u_tags = set(tags)
u_tags = sorted(u_tags)
u_words = set(words)
u_words = sorted(u_words)
tag_counts = list()

# count tag occurencies
for tag in u_tags:
	c = tags.count(tag)
	tag_counts.append(c)

# tags count
n_tags = len(u_tags)
print("Number of tags: " + str(n_tags))

u_word_tag = set(lines)
pair_counts = list()

# count word-tag pairs occurencies
for pair in u_word_tag:
	c = lines.count(pair)
	pair_counts.append("%s\t%d" % (pair, c))

probs = list()

print("Computing probabilities...")
# compute probability P(w|t) = C(t,w)/C(t)
for pair in pair_counts:
	p = pair.split("\t")
	i = u_tags.index(p[1])
	c = tag_counts[i]
	probs.append(float(p[2]) / c)

# write automaton with negative log of probability
# to avoid underflow and because automaton works with weights
i = 0
for pair in pair_counts:
	p = pair.split("\t")
	prob = -np.log(probs[i])
	g.write("0\t0\t%s\t%s\t%e\n" % (p[0], p[1], prob))
	i = i + 1

# unknown words, P(<unk>|t) = 1/#tags
prob = -np.log(float(1)/float(n_tags))
for t in u_tags:
	g.write("0\t0\t<unk>\t" + t + "\t%e\n" % prob)
g.write("0")

i = 1
o.write("<epsilon>\t0\n")
for w in u_words:
	o.write(w + "\t" + str(i) + "\n")
	i = i + 1
for t in u_tags:
	o.write(t + "\t" + str(i) + "\n")
	i = i + 1
o.write("<unk>\t" + str(i))

f.close()
g.close()
h.close()
m.close()
n.close()
o.close()
