#!/usr/bin/env python3

from L2_Int1_8_transition import Transition

def get_epsilon(automaton):
	for letter in automaton.alphabet.letters:
		if letter.epsilon:
			return letter

	return None

# This function returns all states connected with an empty state transition
def get_asynchronous_states(state, epsilon=None, parents=None):
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
		next_states.update(get_recursive_next_states(asynchronous_state, letter, parents.union({state,})))

	return next_states

# This function returns true if there is one or more epsilon transition from any initial state to the given state
def is_recursive_initial(state, parents=None):
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
		if is_recursive_initial(asynchronous_state, parents.union({state,})):
			return True

	return False

# This functions returns true if there is one or more epsilon transition from the given state to any terminal state
def is_recursive_terminal(state, parents=None):
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

def synchronize(automaton, file=None):
	# Copy the automaton not to break the references to the previous one
	automaton = automaton.copy()

	if not automaton.is_asynchronous(file=file):
		return automaton

	# Find all the non-epsilon letters
	letters = []
	for letter in automaton.alphabet.letters:
		if not letter.epsilon:
			letters.append(letter)

	for state in automaton.states:
		for letter in letters:
			# For each state and letter, find the ones connected to it through an epsilon and add a direct transition between them
			next_states = get_recursive_next_states(state, letter)
			next_states -= state.get_next_states(letter)

			for next_state in next_states:
				Transition(state, next_state, letter)

		# If the state is connected to an initial state through incoming epsilon transitions, mark it as initial
		if is_recursive_initial(state):
			state.initial = True
			automaton.initial_states.add(state)

		# If the state is connected to a terminal state through outgoing epsilon transitions, mark it as terminal
		if is_recursive_terminal(state):
			state.terminal = True
			automaton.terminal_states.add(state)

	# Remove all epsilon transitions which are now useless
	for transition in automaton.transitions.copy():
		if transition.letter.epsilon:
			transition.remove()

	return automaton
