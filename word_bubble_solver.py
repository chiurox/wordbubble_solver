#!/usr/bin/env python

from itertools import product

class WordBubbleSolver(object):

    def __init__(self, word_length_1=4, word_length_2=5, word_length_3=0,
                 bubbles=[], dictionary_filepath='./words_partial'):
        self.word_length_1 = word_length_1
        self.word_length_2 = word_length_2
        self.word_length_3 = word_length_3
        self.bubbles = ''.join(bubbles)
        self.dictionary_filepath = dictionary_filepath
        self.anagram_dict = {}
        self.possible_paths = self._build_possible_paths()
        self._build_anagram_dict()

    def _build_possible_paths(self):
        counter = 0
        matrix = []
        for rows in self.bubbles.split('|'):
            a = []
            for letter in rows:
                if letter is '#':
                    a.append('#')
                else:
                    a.append(counter)
                counter += 1
            matrix.append(a)

        paths = {}
        flattened = list(self.bubbles.replace('|', ''))
        positions = len(''.join(self.bubbles.replace('|', '')))
        for position in range(positions):
            matrix_position = self._to_matrix_position(
                position, len(matrix[0]))
            adjacent_positions = self._get_adjacent_positions(
                matrix_position[0], matrix_position[1], len(matrix[0]), len(matrix))
            paths[position] = set(sorted(
                [self._from_matrix_position(r, c, len(matrix[0])) for r, c in adjacent_positions]))
        print paths
        return paths

    def _to_matrix_position(self, n, columns_in_matrix):
        return (n / columns_in_matrix, n % columns_in_matrix)

    def _from_matrix_position(self, r, c, columns_in_matrix):
        return (r * columns_in_matrix) + (c % columns_in_matrix)

    def _get_adjacent_positions(self, r, c, columns_in_matrix, rows_in_matrix):
        adjacent_positions = []
        adjacent_positions.append((max(0, r - 1), (max(0, c - 1))))
        adjacent_positions.append((max(0, r - 1), c))
        adjacent_positions.append(
            (max(0, r - 1), (min(columns_in_matrix - 1, c + 1))))
        adjacent_positions.append((r, (max(0, c - 1))))
        adjacent_positions.append((r, (min(columns_in_matrix - 1, c + 1))))
        adjacent_positions.append(
            (min(rows_in_matrix - 1, r + 1), (max(0, c))))
        adjacent_positions.append(
            (min(rows_in_matrix - 1, r + 1), (max(0, c - 1))))
        adjacent_positions.append(
            (min(rows_in_matrix - 1, r + 1), (min(columns_in_matrix - 1, c + 1))))
        adjacent_positions = list(set(adjacent_positions))
        if (r, c) in adjacent_positions:
            adjacent_positions.remove((r, c))
        return set(adjacent_positions)

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
        print len(self.anagram_dict)
        return True

    def bfs(self, start, word_length):
        result = []
        q = [[start]]
        bubbles = self.bubbles.replace('|', '')
        while len(q):
            tmp_path = q.pop(0)
            last_node = tmp_path[-1]
            if len(tmp_path) == word_length:
                letter_path = ''.join([bubbles[x] for x in tmp_path])
                sorted_path = ''.join(sorted(letter_path))
                if letter_path in self.anagram_dict.get(sorted_path, []):
                    result.append(letter_path)
            for node in self.possible_paths.get(last_node, []):
                if node not in tmp_path:
                    new_path = []
                    new_path = tmp_path + [node]
                    q.append(new_path)
        return list(set(result))

    def find_all_words(self):
        word_lengths = [
            self.word_length_1, self.word_length_2, self.word_length_3]
        start_positions = len(''.join(self.bubbles.replace('|', '')))
        result = []
        grouped_result = {}
        for word_length in word_lengths:
            if word_length <= 0:
                continue
            grouped_result[word_length] = []
            for start in range(start_positions):
                existing_list = grouped_result[word_length]
                existing_list.extend(self.bfs(start, word_length))
                grouped_result[word_length] = existing_list

        return self.find_possible_sets_of_words(grouped_result)

    def find_possible_sets_of_words(self, grouped_result):
        bubble = ''.join(sorted(self.bubbles.replace('|', '')))
        result = []
        word_lengths = sorted([
            self.word_length_1, self.word_length_2, self.word_length_3], reverse=True)
        result_as_list = grouped_result.values()
        product_result = [p for p in product(*result_as_list)]

        for pairs in product_result:
            for i in pairs:
                sub_bubble = bubble
                for letter in i:
                    sub_bubble = sub_bubble.replace(letter, '', 1)
                for j in pairs[1:]:
                    if ''.join(sorted(j)) in sub_bubble:
                        descending_pairs = sorted(pairs, key=len, reverse=True)
                        if descending_pairs not in result:
                            result.append(descending_pairs)
        return result





