#!/usr/bin/env python3

class State(object):

	def __init__(self, automaton, state_id, initial_state=False, terminal_state=False):
		super(State, self).__init__()

		self.automaton = automaton
		self.state_id = state_id
		self.transitions_from = set()
		self.transitions_to = set()
		self.initial_state = initial_state
		self.terminal_state = terminal_state

		self.automaton.states.add(self)
		if initial_state:
			self.automaton.initial_states.add(self)
		if terminal_state:
			self.automaton.terminal_states.add(self)

	def get_next_states(self, letter):
		next_states = []

		for transition in self.transitions_from:
			if transition.letter == letter:
				next_states.append(transition.state_to)

		return next_states
