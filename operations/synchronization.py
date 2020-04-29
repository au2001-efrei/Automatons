#!/usr/bin/env python3

def get_recursive_next_states(state, letter):
	next_states = state.get_next_states(letter)

	epsilon = None
	for letter in state.automaton.alphabet.letters:
		if letter.epsilon:
			epsilon = letter
			break
	else: # No epsilon letter found, thus no epsilon transition
		return next_states

	for asynchronous_state in state.get_next_states(epsilon):
		next_states.update(get_recursive_next_states(asynchronous_state, letter))

	return next_states

def synchronize(automaton):
	if not automaton.is_asynchronous():
		return automaton

	synchronous_automaton = automaton.copy()

	letters = []
	for letter in synchronous_automaton.alphabet.letters:
		if not letter.epsilon:
			letters.append(letter)

	for state in synchronous_automaton.states:
		for letter in letters:
			next_states = get_recursive_next_states(state, letter)
			next_states -= state.get_next_states(letter)

			for next_state in next_states:
				Transition(state, next_state, letter)

		for transition in state.transitions_from.copy():
			if transition.letter.epsilon:
				transition.remove()

	return synchronous_automaton
