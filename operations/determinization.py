#!/usr/bin/env python3

from .completion import complete

def determinize(automaton):
	if automaton.is_deterministic():
		return automaton

	automaton = complete(automaton)

	print("Determinize") # TODO

	return automaton
