#!/usr/bin/env python

import sys


class WordBubbleSolver(object):

    def __init__(self, word_length_1=4, word_length_2=5,
                 bubbles=[], dictionary_filepath='./words_partial'):
        self.word_length_1 = word_length_1
        self.word_length_2 = word_length_2
        self.bubbles = bubbles
        self.dictionary_filepath = dictionary_filepath
        self.anagram_dict = {}
        self.possible_paths = {
            0: set([1, 3, 4]),
            1: set([0, 2, 3, 4, 5]),
            2: set([1, 4, 5]),
            3: set([0, 1, 4, 6, 7]),
            4: set([0, 1, 2, 3, 5, 6, 7, 8]),
            5: set([1, 2, 4, 7, 8]),
            6: set([3, 4, 7]),
            7: set([3, 4, 5, 6, 8]),
            8: set([4, 5, 7])
        }

        self._build_anagram_dict()

    def _build_anagram_dict(self):
        with open(self.dictionary_filepath, 'r') as words:
            for word in words:
                word = word.rstrip('\n').lower()
                sorted_word = ''.join(sorted(word))
                if sorted_word in self.anagram_dict:
                    existing_list = self.anagram_dict[sorted_word]
                    existing_list.append(word)
                    self.anagram_dict[sorted_word] = existing_list
                else:
                    self.anagram_dict[sorted_word] = [word]
        return True

    def bfs(self, start, word_length):
        result = []
        q = [[start]]
        while len(q):
            tmp_path = q.pop(0)
            last_node = tmp_path[-1]
            if len(tmp_path) == word_length:
                letter_path = ''.join([self.bubbles[x] for x in tmp_path])
                sorted_path = ''.join(sorted(letter_path))
                if letter_path in self.anagram_dict.get(sorted_path, []):
                    result.append(letter_path)
            for node in self.possible_paths[last_node]:
                if node not in tmp_path:
                    new_path = []
                    new_path = tmp_path + [node]
                    q.append(new_path)
        return result

    def find_all_words(self):
        word_lengths = [self.word_length_1, self.word_length_2]
        start_positions = len(self.bubbles)
        result = []
        for word_length in word_lengths:
            for start in range(start_positions):
                result.extend(self.bfs(start, word_length))
        print result
        return set(result)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: python wordbubble_solver.py <dictionary_file> <word>'
    else:
        solver = WordBubbleSolver(4, 5, list('%s' % sys.argv[2]), './%s' % sys.argv[1])
        solver.find_all_words()
