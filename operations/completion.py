#!/usr/bin/env python3

from automaton_types.state import State
from automaton_types.transition import Transition
from .determinization import determinize

def complete(automaton):
	# Copy the determinized automaton not to break the references to the previous one
	automaton = determinize(automaton).copy()

	if automaton.is_complete():
		return automaton

	# Create a new trash state
	trash_state = State(automaton, "X")

	for state in automaton.states:
		# For each state, find the letters which do not have an outgoing transition
		outgoing_letters = set()
		for transition in state.transitions_from.copy():
			outgoing_letters.add(transition.letter)

		# Add a transition to the trash state for each missing transition, except epsilon ones
		for letter in set(automaton.alphabet.letters) - outgoing_letters:
			if not letter.epsilon:
				Transition(state, trash_state, letter)

	return automaton
