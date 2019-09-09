import string
import torch as th

class Helpers:
    # default constructor
    def __init__(self):
        self.char2index = {}
        self.index2char = {}

        for i,char in enumerate(' ' + string.ascii_lowercase + '0123456789' + string.punctuation):
            self.char2index[char] = i
            self.index2char[i] = char

    def string2values(self, str_input, max_len=8):

        str_input = str_input[:max_len].lower()

        # pad strings shorter than max len
        if(len(str_input) < max_len):
            str_input = str_input + "." * (max_len - len(str_input))

        values = list()
        for char in str_input:
            values.append(self.char2index[char])

        return th.tensor(values).long()

    def values2string(self, input_values):
        s = ""
        for value in input_values:
            s += self.index2char[int(value)]
        return s

    def strings_equal(self ,str_a, str_b):

        vect = (str_a * str_b).sum(1)

        x = vect[0]

        for i in range(vect.shape[0] - 1):
            x = x * vect[i + 1]

        return x

    def one_hot(self, index, length):
        vect = th.zeros(length).long()
        vect[index] = 1
        return vect

    def string2one_hot_matrix(self ,str_input, max_len=8):

        str_input = str_input[:max_len].lower()

        # pad strings shorter than max len
        if(len(str_input) < max_len):
            str_input = str_input + "." * (max_len - len(str_input))

        char_vectors = list()
        for char in str_input:
            char_v = self.one_hot(self.char2index[char], len(self.char2index)).unsqueeze(0)
            char_vectors.append(char_v)

        return th.cat(char_vectors, dim=0)
