#!/usr/bin/env python3

import os
import re

from L2_Int1_8_automaton import Automaton
from L2_Int1_8_determinization import determinize
from L2_Int1_8_completion import complete
from L2_Int1_8_minimization import minimize
from L2_Int1_8_complementation import complement
from L2_Int1_8_standardization import standardize

FILE_FORMAT = "Int1-8-%d.txt"
OUTPUT_FORMAT = "Int1-8-%d-trace.txt"

def main():
	automatas = set()
	for file in os.listdir("."):
		match = re.match(FILE_FORMAT.replace(r"%d", r"(\d+)"), file)
		if match:
			automatas.add(int(match.group(1)))

	for automaton_id in automatas:
		output_path = OUTPUT_FORMAT % automaton_id
		with open(output_path, "w") as f:
			print(file=f)
			print("1. Reading automaton...", file=f)
			file_path = FILE_FORMAT % automaton_id
			automaton = Automaton.read_from_file(file_path)
			automaton.display(file=f)

			print(file=f)
			print("2. Determinizing and completing automaton...", file=f)
			automaton = determinize(automaton, file=f)
			automaton = complete(automaton, file=f)
			automaton.display(file=f)

			print(file=f)
			print("3. Minimizing automaton...", file=f)
			automaton = minimize(automaton, file=f)
			automaton.display(file=f)

			print(file=f)
			print("4. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

			print(file=f)
			print("5. Creating an automaton which recognizes the complementary language...", file=f)
			automaton = complement(automaton, file=f)
			automaton.display(file=f)

			print(file=f)
			print("6. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

			print(file=f)
			print("7. Standardizing automaton...", file=f)
			automaton = standardize(automaton, file=f)
			automaton.display(file=f)

			print(file=f)
			print("8. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

if __name__ == "__main__":
	main()
