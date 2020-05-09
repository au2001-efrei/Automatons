#!/usr/bin/env python3

def is_dead_end(state, parents=None):
	if parents is None:
		parents = set()
	elif state in parents:
		return True

	if state.terminal:
		return False

	for transition in state.transitions_from:
		if transition.state_to not in parents and not is_dead_end(transition.state_to, parents=parents.union({state,})):
			return False

	return True

def recognize(automaton):
	while True:
		word = input("Enter the word to test (or q to quit): ")

		if word.lower() in ["quit", "exit", "end", "q"]:
			break

		active_states = automaton.initial_states

		for i, character in enumerate(word):
			letter = automaton.alphabet.get_letter(character)

			if letter is None:
				active_states = set()
				print("Letter \"%s\" is not in the alphabet." % character)
				break

			next_active_states = set()
			for active_state in active_states:
				for next_state in active_state.get_next_states(letter):
					next_active_states.add(next_state)

			active_states = next_active_states

			for active_state in active_states:
				if not is_dead_end(active_state):
					break
			else:
				print("Starting from \"%s\", the word can no longer be recognized." % word[:i+1])
				break

		for active_state in active_states:
			if active_state.terminal:
				print("The word \"%s\" IS recognized by this automaton." % word)
				break
		else:
			print("The word \"%s\" is NOT recognized by this automaton." % word)
