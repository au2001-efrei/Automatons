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
