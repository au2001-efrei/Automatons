#!/usr/bin/env python3

def is_dead_end(state, parents=None):
	if parents is None:
		parents = set()
	elif state in parents:
		return True

	# If we find a state which is terminal, the state is not a dead end
	if state.terminal:
		return False

	# Check all outgoing transitions, if there is at least one non-dead end, this state isn't one
	for transition in state.transitions_from:
		if transition.state_to not in parents and not is_dead_end(transition.state_to, parents=parents.union({state,})):
			return False

	# If all of them are dead ends, this state is a dead end
	return True

def recognize(automaton):
	# TODO: Work with asynchronous automatons

	while True:
		word = input("Enter the word to test (or q to quit): ")

		# Quit if the user enters one of those words
		if word.lower() in ["quit", "exit", "end", "q"]:
			break

		# Start with the initial states
		active_states = automaton.initial_states

		for i, character in enumerate(word):
			# Get the letter object corresponding to the character the user typed
			letter = automaton.alphabet.get_letter(character)

			# If the letter doesn't exist in the alphabet, the word can't be recognized
			if letter is None:
				active_states = set()
				print("Letter \"%s\" is not in the alphabet." % character)
				break

			# For each active state, find the ones it activates with this letter and store them
			next_active_states = set()
			for active_state in active_states:
				for next_state in active_state.get_next_states(letter):
					next_active_states.add(next_state)

			# Replace the old active states (at time T) with the new ones (at time T+1)
			active_states = next_active_states

			# If all the active states are dead ends, we are sure the word will not be recognized so we can stop here
			for active_state in active_states:
				if not is_dead_end(active_state):
					break
			else:
				print("Starting from \"%s\", the word can no longer be recognized." % word[:i+1])
				break

		# If at least one state activated at the end of the word is terminal, the word is recognized
		for active_state in active_states:
			if active_state.terminal:
				print("The word \"%s\" IS recognized by this automaton." % word)
				break
		else:
			print("The word \"%s\" is NOT recognized by this automaton." % word)
