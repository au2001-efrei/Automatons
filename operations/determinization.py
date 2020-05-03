#!/usr/bin/env python3

from automaton_types.automaton import Automaton
from automaton_types.state import State
from automaton_types.transition import Transition
from .synchronization import synchronize

def determinize(automaton):
	automaton = synchronize(automaton)

	if automaton.is_deterministic():
		return automaton

	# Create a new automaton not to break the references to the previous one
	deterministic_automaton = Automaton(automaton.alphabet)
	to_process = [(None, None, automaton.initial_states)]

	# Start by regrouping all the input nodes, then regroup each destination of this state and start again
	while to_process:
		from_state, from_letter, processing = to_process.pop(0)
		new_state_id = ",".join(sorted(map(lambda state: state.state_id, processing)))

		# Create a new single state from the list of previous states which are to be activated at the same time
		new_state = deterministic_automaton.get_state(new_state_id)
		processed = True
		if new_state is None:
			processed = False
			new_state = State(deterministic_automaton, new_state_id)

		# Create the incomming transition (either set it to initial or create a transition from the previous state)
		if from_state is not None and from_letter is not None:
			Transition(from_state, new_state, from_letter)
		else:
			new_state.initial = True
			deterministic_automaton.initial_states.add(new_state)

		# If this new state "group" was just created, analyze its outgoing transitions
		if processed:
			continue

		# Store all transitions in the format {[letter]: set([transition])}
		new_transitions = {}
		for state in processing:
			# If at least one of the previous states in the group is terminal, the group is terminal
			if state.terminal:
				new_state.terminal = True
				deterministic_automaton.terminal_states.add(new_state)

			# For each previous state in the group, and each transition of these states, store them in the dictionary
			for transition in state.transitions_from:
				if transition.letter not in new_transitions:
					new_transitions[transition.letter] = set()

				new_transitions[transition.letter].add(transition.state_to)

		# From the dictionary, reconstruct the groups which have to be made and add them to the pending array
		for letter, next_states in new_transitions.items():
			to_process.append((new_state, letter, next_states))

	return deterministic_automaton
