#!/usr/bin/env python3

from .synchronization import synchronize

def complete(automaton):
	if automaton.is_complete():
		return automaton

	automaton = synchronize(automaton)

	print("Complete") # TODO

	return automaton
