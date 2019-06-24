#!/bin/bash

if [ "$#" -ne 3 ]; then
	echo "Provide ngram size, smoothing method and 1=IOB or 2=IOB_O or 3=NER"
	exit 1
fi

output_folder="$3_$2_$1gram"
mkdir $output_folder

# compute word-tag probabilities and output text automaton that translates single words to tags
python probs.py $output_folder $3

# generate fst from txt
fstcompile --isymbols="$output_folder"/lex.txt --osymbols="$output_folder"/lex.txt "$output_folder"/iob.txt > "$output_folder"/iob.fst

# generate tag language model
farcompilestrings --symbols="$output_folder"/lex.txt --unknown_symbol='<unk>' -keep_symbols=1 "$output_folder"/utterances.txt > "$output_folder"/lm.far
ngramcount --order=$1 "$output_folder"/lm.far > "$output_folder"/lm.cnts
# add smoothing to manage unseen n-grams probabilities
ngrammake --method=$2 "$output_folder"/lm.cnts > "$output_folder"/lm.lm

input="$output_folder/text_utterances.txt"
count=1

# concept tagging on the test set
while read -r string
do	
	echo -en "\rProcessing string $count of 1084"
	((count++))
	# create far from current text utterance and extract fsa (named '1' by default)
	echo $string | farcompilestrings --symbols="$output_folder"/lex.txt --unknown_symbol='<unk>' --generate_keys=1 | farextract --filename_suffix='.fsa'
	# compose current utterance fsa with word-tag fst and tag language model (fsa)
	# fstrmepsilon removes epsilon transitions
	fstcompose 1.fsa "$output_folder"/iob.fst | fstcompose - "$output_folder"/lm.lm | fstrmepsilon > "$output_folder"/out2.fst
	# find shortest path to extract most probable tagging	
	# fsttopsort orders the fst state indexes
	fstshortestpath "$output_folder"/out2.fst | fsttopsort > "$output_folder"/short.fst
	# append automaton for each test string in fst.txt
	fstprint --isymbols="$output_folder"/lex.txt --osymbols="$output_folder"/lex.txt "$output_folder"/short.fst >> "$output_folder"/fst.txt
done <"$input"

# prepare evaluation files
python eval_input.py $output_folder $3

echo "\nEvaluating..."

# execute evaluation
perl conlleval.pl -d "\t" < "$output_folder"/fst_eval.txt > "$output_folder"/eval.txt


