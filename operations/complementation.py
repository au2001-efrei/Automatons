#!/usr/bin/env python3

from .determinization import determinize

def complement(automaton):
	# Copy the determinized automaton not to break the references to the previous one
	automaton = determinize(automaton).copy()

	for state in automaton.states:
		# Invert the terminal and non-terminal states
		state.terminal = not state.terminal

	return automaton
