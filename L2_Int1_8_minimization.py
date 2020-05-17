#!/usr/bin/env python3

from L2_Int1_8_state import State
from L2_Int1_8_transition import Transition

def minimize(automaton, file=None):
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
		print("Current partition:", *sorted(map(lambda group: "{%s}" % ", ".join(sorted(map(lambda state: "'%s'" % state.state_id, group))), partition)), file=file)
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
				# (transition table where are displayed the groups the destinations are part of, rather than the destinations themselves)
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

	# If all groups are of length 1, then the automaton was already minimized
	if max(map(len, partition)) == 1:
		print("This automaton is already minimized.", file=file)
		return automaton

	# Once the final partition is found, merge the states in a same group
	for group in partition:
		# If the group is composed of a single state, no change is needed
		if len(group) == 1:
			continue

		# Otherwise, create a new state with ID the concatenation of all states in the group (using a plus sign to differentiate with determinization)
		new_state = State(automaton, "+".join(sorted(map(lambda state: state.state_id, group))))

		incoming_pairs = set()
		outgoing_pairs = set()

		# For each state in the group
		for state in group:
			# If at least one state is initial/terminal, then the group is, too
			if state.initial:
				new_state.initial = True
				automaton.initial_states.add(new_state)

			if state.terminal:
				new_state.terminal = True
				automaton.terminal_states.add(new_state)

			# Move its incoming transitions to the new state
			for transition in state.transitions_to.copy():
				pair = (transition.state_from, transition.letter)
				if pair not in incoming_pairs:
					incoming_pairs.add(pair)
					Transition(transition.state_from, new_state, transition.letter)

				transition.remove()

			# Move its outgoing transitions to the new state
			for transition in state.transitions_from.copy():
				pair = (transition.state_to, transition.letter)
				if pair not in outgoing_pairs:
					outgoing_pairs.add(pair)
					Transition(new_state, transition.state_to, transition.letter)

				transition.remove()

			# Remove this state as it is now merged into "new_state"
			state.remove()

	return automaton
