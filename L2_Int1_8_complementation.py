#!/usr/bin/env python3

from L2_Int1_8_determinization import determinize
from L2_Int1_8_completion import complete

def complement(automaton, file=None):
	# Copy the complete deterministic automaton not to break the references to the previous one
	automaton = complete(determinize(automaton, file=file), file=file).copy()

	for state in automaton.states:
		# Invert the terminal and non-terminal states
		state.terminal = not state.terminal

		if state.terminal:
			automaton.terminal_states.add(state)
		else:
			automaton.terminal_states.remove(state)

	return automaton
