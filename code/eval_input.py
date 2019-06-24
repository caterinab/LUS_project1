from shutil import copyfile
from os import path
import sys

output_folder = str(sys.argv[1])
method = str(sys.argv[2])

f = open("../test.txt", "r")
g = open(path.join(output_folder, "fst.txt"), "r")
h = open(path.join(output_folder, "fst_eval.txt"), "w")

original = f.readlines()
predictions = g.readlines()

for i in range (0, len(predictions)):
	o_line = original[i]
	if o_line.strip():	
		o_line = o_line.split()
		if(method == "2" and o_line[1] == "O"):
			h.write(o_line[0] + "\t" + o_line[1] + "-" + o_line[0])
		else:
			h.write(original[i].strip("\n"))
		p = predictions[i].split()
		h.write("\t" + p[3] + "\n")
	else:
		h.write("\n")

f.close()
g.close()
h.close()
