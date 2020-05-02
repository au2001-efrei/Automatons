#!/usr/bin/env python3

from automaton_types.automaton import Automaton
from automaton_types.state import State
from automaton_types.transition import Transition
from .synchronization import synchronize

def determinize(automaton):
	# Copy the synchronized automaton not to break the references to the previous one
	automaton = synchronize(automaton)

	if automaton.is_deterministic():
		return automaton

	deterministic_automaton = Automaton(automaton.alphabet)
	to_process = [(None, None, automaton.initial_states)]

	while to_process:
		from_state, from_letter, processing = to_process.pop(0)
		new_state_id = ",".join(map(str, sorted(map(lambda state: state.state_id, processing))))

		new_state = deterministic_automaton.get_state(new_state_id)
		processed = True
		if new_state is None:
			processed = False
			new_state = State(deterministic_automaton, new_state_id)

		if from_state is not None and from_letter is not None:
			Transition(from_state, new_state, from_letter)
		else:
			new_state.initial = True

		if processed:
			continue

		new_transitions = {}
		for state in processing:
			if state.terminal:
				new_state.terminal = True

			for transition in state.transitions_from:
				if transition.letter not in new_transitions:
					new_transitions[transition.letter] = set()

				new_transitions[transition.letter].add(transition.state_to)

		for letter, next_states in new_transitions.items():
			to_process.append((new_state, letter, next_states))

	return deterministic_automaton
