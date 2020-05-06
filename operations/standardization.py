#!/usr/bin/env python3

from automaton_types.state import State
from automaton_types.transition import Transition

def standardize(automaton):
	# Copy the automaton not to break the references to the previous one
	automaton = automaton.copy()

	if automaton.is_standard():
		return automaton

	# Create a new initial state
	initial_state = State(automaton, "I", initial=True)

	for state in automaton.initial_states.copy():
		if state == initial_state:
			continue

		state.initial = False
		automaton.initial_states.remove(state)

		# For each current initial state, copy its transitions to the new initial state
		pairs = set()
		for transition in state.transitions_from:
			pair = (transition.letter, transition.state_to)

			if pair in pairs:
				continue

			Transition(initial_state, transition.state_to, transition.letter)
			pairs.add(pair)

	return automaton
