#!/usr/bin/env python3

class State(object):

	def __init__(self, automaton, state_id, input_state=False, output_state=False):
		super(State, self).__init__()

		self.automaton = automaton
		self.state_id = state_id
		self.transitions_from = set()
		self.transitions_to = set()
		self.input_state = input_state
		self.output_state = output_state

		self.automaton.states.add(self)
		if input_state:
			self.automaton.input_states.add(self)
		if output_state:
			self.automaton.output_states.add(self)
