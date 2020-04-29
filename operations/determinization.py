#!/usr/bin/env python3

from .synchronization import synchronize

def determinize(automaton):
	# Copy the synchronized automaton not to break the references to the previous one
	automaton = synchronize(automaton).copy()

	if automaton.is_deterministic():
		return automaton

	print("Determinize") # TODO

	return automaton
