#!/usr/bin/env python3

import os
import re

from automaton_types.automaton import Automaton
from operations.determinization import determinize

DIRECTORY = "./automatas/"
FILE_FORMAT = "Int1-8-%d.txt"

def main():
	automatas = set()
	for file in os.listdir(DIRECTORY):
		match = re.match(FILE_FORMAT.replace(r"%d", r"(\d+)"), file)
		if match:
			automatas.add(int(match.group(1)))

	automaton_list = ", ".join(map(str, sorted(automatas)))

	automaton_id = None
	while automaton_id is None or automaton_id not in automatas:
		if automaton_id is not None:
			automaton_id = int(input("Invalid ID, use one amongst %s: " % automaton_list))
		else:
			automaton_id = int(input("Enter the ID of the automaton to use amongst %s: " % automaton_list))

	print()
	print("1. Reading automaton...")
	file_path = os.path.join(DIRECTORY, FILE_FORMAT % automaton_id)
	automaton = Automaton.read_from_file(file_path)
	automaton.display()

	print()
	print("2. Determinizing automaton...")
	determinize(automaton)
	automaton.display()

if __name__ == "__main__":
	main()
