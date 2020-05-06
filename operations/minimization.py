#!/usr/bin/env python3

from automaton_types.transition import Transition

def minimize(automaton):
	# Copy the automaton not to break the references to the previous one
	automaton = automaton.copy()

	partition = []
	if automaton.terminal_states:
		partition.append(automaton.terminal_states.copy())
	if len(automaton.terminal_states) < len(automaton.states):
		partition.append(set(filter(lambda state: not state.terminal, automaton.states)))

	divided = True
	while divided:
		new_partition = []
		divided = False

		for group in partition:
			if len(group) == 1:
				new_partition.append(group)
				continue

			subgroups = []
			for state in group:
				state_pattern = {}

				for transition in state.transitions_from:
					for i, in_group in enumerate(partition):
						if transition.state_to in in_group:
							state_pattern[transition.letter] = i
							break

				for pattern, subgroup in subgroups:
					if pattern == state_pattern:
						subgroup.add(state)
						break
				else:
					subgroups.append((state_pattern, {state,}))

			if len(subgroups) > 1:
				for pattern, subgroup in subgroups:
					new_partition.append(subgroup)
				divided = True
			else:
				new_partition.append(group)

		partition = new_partition

	for group in partition:
		if len(group) == 1:
			continue

		new_state = sorted(group, key=lambda state: state.state_id)[0]
		new_state.state_id = "+".join(sorted(map(lambda state: state.state_id, group)))

		for state in group:
			if state == new_state:
				continue

			for transition in state.transitions_from.copy():
				Transition(new_state, transition.state_to, transition.letter)
				transition.remove()

			for transition in state.transitions_to.copy():
				Transition(transition.state_from, new_state, transition.letter)
				transition.remove()

			state.remove()

	return automaton
