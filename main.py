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

DIRECTORY = "./automatons/"
FILE_FORMAT = "Int1-8-%d.txt"

def main():
	automatas = set()
	for file in os.listdir(DIRECTORY):
		match = re.match(FILE_FORMAT.replace(r"%d", r"(\d+)"), file)
		if match:
			automatas.add(int(match.group(1)))

	automaton_list = ", ".join(map(str, sorted(automatas)))

	try:
		while True:
			automaton_id = None
			while automaton_id is None or automaton_id not in automatas:
				if automaton_id is not None:
					automaton_id = input("Invalid ID, use one amongst %s: " % automaton_list)
				else:
					automaton_id = input("Enter the ID of the automaton to use amongst %s: " % automaton_list)

				try:
					automaton_id = int(automaton_id)
				except ValueError:
					if automaton_id.lower() in ["quit", "exit", "end", "q"]:
						break

			print()
			print("1. Reading automaton...")
			file_path = os.path.join(DIRECTORY, FILE_FORMAT % automaton_id)
			automaton = Automaton.read_from_file(file_path)
			automaton.display()

			print()
			print("2. Determinizing and completing automaton...")
			automaton = determinize(automaton)
			automaton = complete(automaton)
			automaton.display()

			print()
			print("3. Minimizing automaton...")
			automaton = minimize(automaton)
			automaton.display()

			print()
			print("4. Starting word recognition...")
			recognize(automaton)

			print()
			print("5. Creating an automaton which recognizes the complementary language...")
			automaton = complement(automaton)
			automaton.display()

			print()
			print("6. Starting word recognition...")
			recognize(automaton)

			print()
			print("7. Standardizing automaton...")
			automaton = standardize(automaton)
			automaton.display()

			print()
			print("8. Starting word recognition...")
			recognize(automaton)
	except KeyboardInterrupt:
		print()
		pass

	print("Quitting...")

if __name__ == "__main__":
	main()
