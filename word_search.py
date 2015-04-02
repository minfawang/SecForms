class Solution:
	# @param board, a list of lists of 1 length string
	# @param word, a string
	# @return a boolean
	def exist(self, board, word):
		if not word:
			return True
		if not board:
			return False
		m = len(board)
		n = len(board[0])

		for row in board:
			start_idx = row.find(word[0])