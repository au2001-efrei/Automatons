#!/usr/bin/env python3

import re

from .letter import Letter
from .alphabet import Alphabet
from .state import State
from .transition import Transition

LETTERS = "abcdefghijklmnopqrstuvwxyz"
STATES = list(map(str, range(100)))

class Automaton(object):

	def __init__(self, alphabet=None, states=None, transitions=None, initial_states=None, terminal_states=None):
		super(Automaton, self).__init__()

		self.alphabet = alphabet if alphabet is not None else Alphabet()
		self.states = states if states is not None else set()
		self.transitions = transitions if transitions is not None else set()
		self.initial_states = initial_states if initial_states is not None else set()
		self.terminal_states = terminal_states if terminal_states is not None else set()

	def copy(self, alphabet=None):
		if alphabet is None:
			alphabet = self.alphabet

		automaton_copy = Automaton(alphabet)

		for state in self.states:
			state.copy(automaton_copy)

		for transition in self.transitions:
			transition.copy(automaton_copy)

		return automaton_copy

	def get_state(self, state_id):
		for state in self.states:
			if state.state_id == state_id:
				return state

		return None

	def is_asynchronous(self):
		for transition in self.transitions:
			if transition.letter.epsilon:
				return True

		return False

	def is_deterministic(self):
		pairs = set()

		# There must be at most one entry state
		if len(self.initial_states) > 1:
			return False

		for transition in self.transitions:
			pair = (transition.state_from, transition.letter)
			if pair in pairs: # There must be at most one pair (from state, letter)
				return False

			pairs.add(pair)

		return True

	def is_complete(self):
		pairs = set()

		for transition in self.transitions:
			if transition.letter.epsilon: # A complete automaton must be synchronous
				return False

			pairs.add((transition.state_from, transition.letter))

		letter_count = 0
		for letter in self.alphabet.letters:
			if not letter.epsilon:
				letter_count += 1

		return len(pairs) == len(self.states) * letter_count # There must be at least one pair (from state, letter)

	def is_standard(self):
		# There must be at most one entry state
		if len(self.initial_states) > 1:
			return False

		initial_state = next(iter(self.initial_states))

		for transition in self.transitions:
			if transition.state_to == initial_state: # There must be no transition pointing to the (unique) initial state
				return False

		return True

	def display(self):
		# Print the letters without the epsilon
		letters = []
		for letter in self.alphabet.letters:
			if not letter.epsilon:
				letters.append(letter.character)
		letters.sort()
		print("Alphabet:", *letters)

		# Print the initial states
		initial_states = []
		for state in self.initial_states:
			initial_states.append(state.state_id)
		initial_states.sort()
		print("Initial states:", *initial_states)

		# Print the terminal states
		terminal_states = []
		for state in self.terminal_states:
			terminal_states.append(state.state_id)
		terminal_states.sort()
		print("Terminal states:", *terminal_states)

		# Generate and print the transition table
		print("Transition table:")

		# Filter letters to keep only the ones used
		letters = []
		for letter in self.alphabet.letters:
			for transition in self.transitions:
				if transition.letter == letter:
					letters.append(letter)
					break

		# Calculate each column's width
		columns_width = [0] * (len(letters) + 1)
		for i, letter in enumerate(sorted(letters, key=lambda letter: letter.character)):
			columns_width[i + 1] = max(columns_width[i + 1], len(letter.character))

		for state in sorted(self.states, key=lambda state: state.state_id):
			column_width = len(state.state_id)
			if state.initial or state.terminal:
				column_width += 1
			if state.initial:
				column_width += 1
			if state.terminal:
				column_width += 1

			columns_width[0] = max(columns_width[0], column_width)
			for i, letter in enumerate(sorted(letters, key=lambda letter: letter.character)):
				next_states = state.get_next_states(letter)
				column_width = sum(map(lambda state: len(state.state_id), next_states)) + len(next_states) - 1
				columns_width[i + 1] = max(columns_width[i + 1], column_width)

		# Print the table's header
		print("/".center(columns_width[0] + 2), end="")
		for i, letter in enumerate(sorted(letters, key=lambda letter: letter.character)):
			print("|" + letter.character.center(columns_width[i + 1] + 2), end="")
		print()
		print("-" * (columns_width[0] + 2), end="")
		for i in range(len(letters)):
			print("+" + "-" * (columns_width[i + 1] + 2), end="")
		print()

		# Print each line (state) of the transition table
		for state in sorted(self.states, key=lambda state: state.state_id):
			line_header = state.state_id
			if state.initial or state.terminal:
				line_header = " " + line_header
			if state.initial:
				line_header = "→" + line_header
			if state.terminal:
				line_header = "←" + line_header
			print(line_header.center(columns_width[0] + 2), end="")

			for i, letter in enumerate(sorted(letters, key=lambda letter: letter.character)):
				next_states = state.get_next_states(letter)
				next_states = " ".join(map(lambda state: state.state_id, next_states))
				print("|" + next_states.center(columns_width[i + 1] + 2), end="")
			print()

	def read_from_file(file):
		# Read the contents of the file
		with open(file, "r") as f:
			alphabet_length = int(f.readline())
			states_count = int(f.readline())

			initial_states_ids = f.readline().split()
			initial_states_count = initial_states_ids[0]
			initial_states_ids = set(initial_states_ids[1:])

			terminal_states_ids = f.readline().split()
			terminal_states_count = terminal_states_ids[0]
			terminal_states_ids = set(terminal_states_ids[1:])

			transition_count = int(f.readline())
			transitions_descs = []
			for i in range(transition_count):
				transitions_descs.append(f.readline())

		# Create the alphabet composed of each letter + epsilon
		alphabet = Alphabet()

		for character in LETTERS[:alphabet_length]:
			Letter(alphabet, character)
		Letter(alphabet, epsilon=True)

		# Create a first (empty) automaton
		automaton = Automaton(alphabet)

		# Add each state
		for state_id in STATES[:states_count]:
			initial = state_id in initial_states_ids
			terminal = state_id in terminal_states_ids
			State(automaton, state_id, initial=initial, terminal=terminal)

		# Decode and add each transition
		for i, transitions_desc in enumerate(transitions_descs):
			match = re.match(r"^(\d+)(\D+)(\d+)\n?$", transitions_desc)
			if match:
				state_from_id = match.group(1)
				character = match.group(2)
				state_to_id = match.group(3)

				state_from = automaton.get_state(state_from_id)
				state_to = automaton.get_state(state_to_id)
				letter = alphabet.get_letter(character)

				Transition(state_from, state_to, letter)
			else:
				raise Exception("Invalid file format at transition #%d: expected number-character-number in transition but got \"%s\"" % (i, transitions_desc))

		return automaton
