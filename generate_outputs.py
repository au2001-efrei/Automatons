#!/usr/bin/env python3

import os
import re

from automaton_types.automaton import Automaton
from operations.determinization import determinize
from operations.completion import complete
from operations.minimization import minimize
from operations.complementation import complement
from operations.standardization import standardize
from operations.recognition import recognize

AUTOMATONS_DIRECTORY = "./automatons/"
OUTPUTS_DIRECTORY = "./outputs/"
FILE_FORMAT = "Int1-8-%d.txt"

def main():
	automatas = set()
	for file in os.listdir(AUTOMATONS_DIRECTORY):
		match = re.match(FILE_FORMAT.replace(r"%d", r"(\d+)"), file)
		if match:
			automatas.add(int(match.group(1)))

	for automaton_id in automatas:
		output_path = os.path.join(OUTPUTS_DIRECTORY, FILE_FORMAT % automaton_id)
		with open(output_path, "w") as f:
			print(file=f)
			print("1. Reading automaton...", file=f)
			file_path = os.path.join(AUTOMATONS_DIRECTORY, FILE_FORMAT % automaton_id)
			automaton = Automaton.read_from_file(file_path)
			automaton.display(file=f)

			print(file=f)
			print("2. Determinizing and completing automaton...", file=f)
			automaton = determinize(automaton)
			automaton = complete(automaton)
			automaton.display(file=f)

			print(file=f)
			print("3. Minimizing automaton...", file=f)
			automaton = minimize(automaton)
			automaton.display(file=f)

			print(file=f)
			print("4. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

			print(file=f)
			print("5. Creating an automaton which recognizes the complementary language...", file=f)
			automaton = complement(automaton)
			automaton.display(file=f)

			print(file=f)
			print("6. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

			print(file=f)
			print("7. Standardizing automaton...", file=f)
			automaton = standardize(automaton)
			automaton.display(file=f)

			print(file=f)
			print("8. Starting word recognition...", file=f)
			print("This step was skipped in this output file.", file=f)
			print("Execute the program to test word recognition by yourself.", file=f)

if __name__ == "__main__":
	main()
