#!/usr/bin/env python3

from automaton_types.transition import Transition

def get_epsilon(automaton):
	for letter in automaton.alphabet.letters:
		if letter.epsilon:
			return letter
			break

	return None

def get_asynchronous_states(state, epsilon=None, parents=None):
	# This function returns all states connected with an empty state transition
	if parents is None:
		parents = set()
	elif state in parents:
		return set()

	if epsilon is None:
		epsilon = get_epsilon(state.automaton)
		if epsilon is None: # No epsilon letter found, thus no epsilon transition
			return set()

	asynchronous_states = set()

	# Add each state connected with an epsilon transition to asynchronous states, and repeat recursively
	for asynchronous_state in state.get_next_states(epsilon):
		asynchronous_states.add(asynchronous_state)
		if asynchronous_state not in parents: # Avoid infinite loops
			asynchronous_states.update(get_asynchronous_states(asynchronous_state, parents.union({state,})))

	return asynchronous_states

def get_recursive_next_states(state, letter, parents=None):
	if parents is None:
		parents = set()
	elif state in parents:
		return set()

	next_states = state.get_next_states(letter)

	# Add all states which are letter transition + epsilon transition(s)
	for next_state in next_states.copy():
		next_states.update(get_asynchronous_states(next_state))

	# Find all "equivalent" states, and start again recursively
	for asynchronous_state in get_asynchronous_states(state):
		if asynchronous_state not in parents: # Avoid infinite loops
			next_states.update(get_recursive_next_states(asynchronous_state, letter, parents.union({state,})))

	return next_states

def is_recursive_initial(state, parents=None):
	# This definition returns true if there is an epsilon transition on an intial state
	if state.initial:
		return True
	if parents is None:
		parents = set()
	elif state in parents:
		return False

	epsilon = get_epsilon(state.automaton)
	if epsilon is None: # No epsilon letter found, thus no epsilon transition
		return next_states

	for asynchronous_state in state.get_previous_states(epsilon):
		if asynchronous_state not in parents and is_recursive_initial(asynchronous_state, parents.union({state,})):
			return True

	return False

def is_recursive_terminal(state, parents=None):
	# This definition returns true if there is an epsilon transition on an terminal state
	if state.terminal:
		return True
	if parents is None:
		parents = set()
	elif state in parents:
		return False

	epsilon = get_epsilon(state.automaton)
	if epsilon is None: # No epsilon letter found, thus no epsilon transition
		return next_states

	for asynchronous_state in state.get_next_states(epsilon):
		if asynchronous_state not in parents and is_recursive_terminal(asynchronous_state, parents.union({state,})):
			return True

	return False

def synchronize(automaton):
	# Copy the automaton not to break the references to the previous one
	synchronous_automaton = automaton.copy()

	if not automaton.is_asynchronous():
		return automaton

	# Find all the non-epsilon letters
	letters = []
	for letter in synchronous_automaton.alphabet.letters:
		if not letter.epsilon:
			letters.append(letter)

	for state in synchronous_automaton.states:
		for letter in letters:
			# For each state and letter, find the ones connected to it through an epsilon and add a direct transition between them
			next_states = get_recursive_next_states(state, letter)
			next_states -= state.get_next_states(letter)

			for next_state in next_states:
				Transition(state, next_state, letter)

		# If the state is connected to an initial state through incoming epsilon transitions, mark it as initial
		if is_recursive_initial(state):
			state.initial = True
			synchronous_automaton.initial_states.add(state)

		# If the state is connected to a terminal state through outgoing epsilon transitions, mark it as terminal
		if is_recursive_terminal(state):
			state.terminal = True
			synchronous_automaton.terminal_states.add(state)

	# Remove all epsilon transitions which are now useless
	for transition in synchronous_automaton.transitions.copy():
		if transition.letter.epsilon:
			transition.remove()

	return synchronous_automaton
