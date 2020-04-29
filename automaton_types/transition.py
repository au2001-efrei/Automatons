#!/usr/bin/env python3

class Transition(object):

	def __init__(self, automaton, state_from, state_to, letter):
		super(Transition, self).__init__()

		self.automaton = automaton
		self.state_from = state_from
		self.state_to = state_to
		self.letter = letter

		self.automaton.transitions.add(self)
		self.state_from.transitions_from.add(self)
		self.state_to.transitions_to.add(self)

	def copy(self, automaton=None):
		if automaton is None:
			automaton = self.automaton

		state_from_copy = automaton.get_state(self.state_from.state_id)
		state_to_copy = automaton.get_state(self.state_to.state_id)
		letter_copy = automaton.alphabet.get_state(self.letter.character)

		return Transition(automaton, state_from_copy, state_to_copy, letter_copy)
