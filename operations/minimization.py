#!/usr/bin/env python3

from automaton_types.transition import Transition

def minimize(automaton):
	# Copy the automaton not to break the references to the previous one
	automaton = automaton.copy()

	# At the beginning, partition the states by terminal and non-terminal
	partition = []
	if automaton.terminal_states:
		partition.append(automaton.terminal_states.copy())
	if len(automaton.terminal_states) < len(automaton.states):
		partition.append(set(filter(lambda state: not state.terminal, automaton.states)))

	# While there is at least one group which was split, continue to test and divide them
	divided = True
	while divided:
		new_partition = []
		divided = False

		for group in partition:
			# If the group is of size 1 (a state alone), it can't be divided
			if len(group) == 1:
				new_partition.append(group)
				continue

			subgroups = []
			for state in group:
				state_pattern = {}

				# For each outgoing transition of each state in the group, create its state pattern
				# (transition table where the groups in which the destinations are part of are displayed rather than the destinations themselves)
				for transition in state.transitions_from:
					for i, in_group in enumerate(partition):
						if transition.state_to in in_group:
							# The group's ID is its position in the list "partition"
							state_pattern[transition.letter] = i
							break

				# If there is a subgroup with the same pattern, add this state to the existing subgroup, otherwise create a new subgroup from this pattern
				for pattern, subgroup in subgroups:
					if pattern == state_pattern:
						subgroup.add(state)
						break
				else:
					subgroups.append((state_pattern, {state,}))

			# If the group has been divided, store the new one and remember to continue the while loop, otherwise keep the old group
			if len(subgroups) > 1:
				for pattern, subgroup in subgroups:
					new_partition.append(subgroup)
				divided = True
			else:
				new_partition.append(group)

		# At the end of each step, store the new partition and if needed, start again to try to divide it once again
		partition = new_partition

	# Once the final partition is found, merge the states in a same group
	for group in partition:
		# If the group is composed of a single state, no change is needed
		if len(group) == 1:
			continue

		# Otherwise, take one random state and rename it to the concatenation of all states in the group (using a plus sign to differentiate with determinization)
		new_state = next(iter(group))
		new_state.state_id = "+".join(sorted(map(lambda state: state.state_id, group)))

		# For each other state in the group
		for state in group:
			if state == new_state:
				continue

			# Move its incoming transitions to the new state
			for transition in state.transitions_from.copy():
				Transition(new_state, transition.state_to, transition.letter)
				transition.remove()

			# Move its outgoing transitions to the new state
			for transition in state.transitions_to.copy():
				Transition(transition.state_from, new_state, transition.letter)
				transition.remove()

			# Remove this state as it is now merged into "new_state"
			state.remove()

	return automaton
