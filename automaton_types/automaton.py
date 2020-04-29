#!/usr/bin/env python3

import re

from .letter import Letter
from .alphabet import Alphabet
from .state import State
from .transition import Transition

LETTERS = "abcdefghijklmnopqrstuvwxyz"
STATES = list(range(99))

class Automaton(object):

	def __init__(self, alphabet=None, states=None, transitions=None, input_states=None, output_states=None):
		super(Automaton, self).__init__()

		self.alphabet = alphabet if alphabet is not None else Alphabet()
		self.states = states if states is not None else set()
		self.transitions = transitions if transitions is not None else set()
		self.input_states = input_states if input_states is not None else set()
		self.output_states = output_states if output_states is not None else set()

	def get_state(self, state_id):
		for state in self.states:
			if state.state_id == state_id:
				return state

		return None

	def read_automaton_from_file(file):
		# Read the contents of the file
		with open(file, "r") as f:
			alphabet_length = int(f.readline())
			states_count = int(f.readline())

			input_states_ids = list(map(int, f.readline().split()))
			input_states_count = input_states_ids[0]
			input_states_ids = set(input_states_ids[1:])

			output_states_ids = list(map(int, f.readline().split()))
			output_states_count = output_states_ids[0]
			output_states_ids = set(output_states_ids[1:])

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
			input_state = state_id in input_states_ids
			output_state = state_id in output_states_ids
			State(automaton, state_id, input_state=input_state, output_state=output_state)

		# Decode and add each transition
		for transitions_desc in transitions_descs:
			match = re.match(r"^(\d+)(\D+)(\d+)\n$", transitions_desc)
			if match:
				from_state_id = automaton.get_state(int(match.group(1)))
				character = match.group(2)
				to_state_id = automaton.get_state(int(match.group(3)))

				letter = alphabet.get_letter(character)

				Transition(automaton, from_state_id, to_state_id, letter)
			else:
				raise Exception("Invalid file format: expected number-character-number in transition")

		return automaton

	def display_automaton(self):
		pass
