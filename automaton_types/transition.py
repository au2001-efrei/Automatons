#!/usr/bin/env python3

class Transition(object):

	#We initialize the object with the following structure: the state before and after the transition,
	#and the name of the transition
	def __init__(self, state_from, state_to, letter):
		super(Transition, self).__init__()

		self.state_from = state_from
		self.state_to = state_to
		self.letter = letter

		assert self.state_from.automaton == self.state_to.automaton

		self.state_from.automaton.transitions.add(self)
		self.state_from.transitions_from.add(self)
		self.state_to.transitions_to.add(self)

	def copy(self, automaton=None):
		if automaton is None:
			automaton = self.automaton

		state_from_copy = automaton.get_state(self.state_from.state_id)
		state_to_copy = automaton.get_state(self.state_to.state_id)
		letter_copy = automaton.alphabet.get_letter(self.letter.character)

		return Transition(state_from_copy, state_to_copy, letter_copy)

	def remove(self):
		self.state_from.automaton.transitions.remove(self)
		self.state_from.transitions_from.remove(self)
		self.state_to.transitions_to.remove(self)
