#!/usr/bin/env python3

class Letter(object):

	def __init__(self, alphabet, character=None, epsilon=None):
		super(Letter, self).__init__()

		# We initialize the object with the following structure:
		# the alphabet this letter belongs to,
		# whether this letter is an epsilon (asynchronous) transition,
		# and the character representing this letter (a string of length 1)
		self.alphabet = alphabet
		self.epsilon = epsilon if epsilon is not None else (character == "*")
		self.character = character if character is not None else "*" if self.epsilon else None

		self.alphabet.letters.add(self)

	def copy(self, alphabet=None):
		if alphabet is None:
			alphabet = self.alphabet

		return Letter(alphabet, self.character, self.epsilon)
