#!/usr/bin/env python3

import re

from .letter import Letter
from .alphabet import Alphabet
from .state import State
from .transition import Transition

LETTERS = "abcdefghijklmnopqrstuvwxyz"
STATES = list(range(99))
COLUMN_WIDTH = 5

class Automaton(object):

	def __init__(self, alphabet=None, states=None, transitions=None, initial_states=None, terminal_states=None):
		super(Automaton, self).__init__()

		self.alphabet = alphabet if alphabet is not None else Alphabet()
		self.states = states if states is not None else set()
		self.transitions = transitions if transitions is not None else set()
		self.initial_states = initial_states if initial_states is not None else set()
		self.terminal_states = terminal_states if terminal_states is not None else set()

	def copy(self):
		alphabet_copy = self.alphabet.copy()
		automaton_copy = Automaton(alphabet_copy)

		for state in self.states:
			state.copy(automaton_copy)

			if state.initial:
				automaton_copy.initial_states.append(state)

			if state.terminal:
				automaton_copy.terminal_states.append(state)

		for transition in self.transitions:
			transition.copy(automaton_copy)

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

		for transition in self.transitions:
			pair = (transition.state_from, transition.letter)
			if pair in pairs:
				return False

			pairs.add(pair)

		return True

	def is_complete(self):
		pairs = set()

		for transition in self.transitions:
			if transition.letter.epsilon: # A complete automaton must be synchronous?
				return False

			pair = (transition.state_from, transition.letter)
			if pair in pairs: # A complete automaton must be deterministic?
				return False

			pairs.add(pair)

		letter_count = 0
		for letter in self.alphabet_length:
			if not letter.epsilon:
				letter_count += 1

		return len(pairs) == len(self.states) * letter_count # There must be exactly one pair (from state, letter)

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

		# Print the table's header
		print("/".center(COLUMN_WIDTH), end="")
		for letter in sorted(letters, key=lambda letter: letter.character):
			print("|" + letter.character.center(COLUMN_WIDTH), end="")
		print()
		print(("-" * COLUMN_WIDTH + "+") * len(letters) + "-" * COLUMN_WIDTH)

		# Print each line (state) of the transition table
		for state in sorted(self.states, key=lambda state: state.state_id):
			line_header = str(state.state_id)
			if state.initial_state or state.terminal_state:
				line_header = " " + line_header
			if state.initial_state:
				line_header = ">" + line_header
			if state.terminal_state:
				line_header = "<" + line_header
			print(line_header.center(COLUMN_WIDTH), end="")

			for letter in sorted(letters, key=lambda letter: letter.character):
				next_states = state.get_next_states(letter)
				next_states = " ".join(map(lambda state: str(state.state_id), next_states))
				print("|" + next_states.center(COLUMN_WIDTH), end="")
			print()

	def read_from_file(file):
		# Read the contents of the file
		with open(file, "r") as f:
			alphabet_length = int(f.readline())
			states_count = int(f.readline())

			initial_states_ids = list(map(int, f.readline().split()))
			initial_states_count = initial_states_ids[0]
			initial_states_ids = set(initial_states_ids[1:])

			terminal_states_ids = list(map(int, f.readline().split()))
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
			initial_state = state_id in initial_states_ids
			terminal_state = state_id in terminal_states_ids
			State(automaton, state_id, initial_state=initial_state, terminal_state=terminal_state)

		# Decode and add each transition
		for i, transitions_desc in enumerate(transitions_descs):
			match = re.match(r"^(\d+)(\D+)(\d+)\n?$", transitions_desc)
			if match:
				state_from_id = int(match.group(1))
				character = match.group(2)
				state_to_id = int(match.group(3))

				state_from = automaton.get_state(state_from_id)
				state_to = automaton.get_state(state_to_id)
				letter = alphabet.get_letter(character)

				Transition(automaton, state_from, state_to, letter)
			else:
				raise Exception("Invalid file format at transition #%d: expected number-character-number in transition but got \"%s\"" % (i, transitions_desc))

		return automaton
