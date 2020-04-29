#!/usr/bin/env python3

def determinize(automaton):
	if automaton.is_asynchronous():
		return determinize_asynchronous(automaton)

	if automaton.is_deterministic():
		return automaton

	print("Determinize")

def determinize_asynchronous(automaton):
	if not automaton.is_asynchronous():
		return determinize(automaton)

	print("Determinize asynchronous")
