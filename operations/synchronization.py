#!/usr/bin/env python3

from automaton_types.transition import Transition

def get_epsilon(automaton):
	for letter in automaton.alphabet.letters:
		if letter.epsilon:
			return letter
			break

	return None

def get_recursive_next_states(state, letter, parents=set()):
	next_states = state.get_next_states(letter)

	epsilon = get_epsilon(state.automaton)
	if epsilon is None: # No epsilon letter found, thus no epsilon transition
		return next_states

	parents.add(state)

	for asynchronous_state in state.get_next_states(epsilon):
		if asynchronous_state not in parents:
			next_states.update(get_recursive_next_states(asynchronous_state, letter))

	return next_states

def is_recursive_initial(state, parents=set()):
	if state.initial:
		return True

	epsilon = get_epsilon(state.automaton)
	if epsilon is None: # No epsilon letter found, thus no epsilon transition
		return next_states

	parents.add(state)

	for asynchronous_state in state.get_previous_states(epsilon):
		if asynchronous_state not in parents and is_recursive_initial(asynchronous_state):
			return True

	return False

def is_recursive_terminal(state, parents=set()):
	if state.terminal:
		return True

	epsilon = get_epsilon(state.automaton)
	if epsilon is None: # No epsilon letter found, thus no epsilon transition
		return next_states

	parents.add(state)

	for asynchronous_state in state.get_next_states(epsilon):
		if asynchronous_state not in parents and is_recursive_terminal(asynchronous_state):
			return True

	return False

def synchronize(automaton):
	if not automaton.is_asynchronous():
		return automaton

	# Copy the automaton not to break the references to the previous one
	synchronous_automaton = automaton.copy()

	# Find all the non-epsilon letters
	letters = []
	for letter in synchronous_automaton.alphabet.letters:
		if not letter.epsilon:
			letters.append(letter)

	for state in synchronous_automaton.states:
		for letter in letters:
			# For each state and letter, find the ones connected to it through an epsilon and add a direct transition
			next_states = get_recursive_next_states(state, letter)
			next_states -= state.get_next_states(letter)

			for next_state in next_states:
				Transition(state, next_state, letter)

		# If the state is connected to an initial state through incomming epsilon transitions, mark it as initial
		if is_recursive_initial(state):
			state.initial = True
			synchronous_automaton.initial_states.add(state)

		# If the state is connected to a terminal state through outgoing epsilon transitions, mark it as terminal
		if is_recursive_terminal(state):
			state.terminal = True
			synchronous_automaton.terminal_states.add(state)

		# Remove all epsilon transitions which are now useless
		for transition in state.transitions_from.copy():
			if transition.letter.epsilon:
				transition.remove()

	return synchronous_automaton
