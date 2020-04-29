#!/usr/bin/env python3

class Letter(object):

	def __init__(self, alphabet, character=None, epsilon=None):
		super(Letter, self).__init__()

		self.alphabet = alphabet
		self.epsilon = epsilon if epsilon is not None else (character == "*")
		self.character = character if character is not None else "*" if self.epsilon else None

		self.alphabet.letters.add(self)
