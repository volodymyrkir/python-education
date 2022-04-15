"""This module is used for parsing sentences"""
import re


class MultipleSentenceError(Exception):
    """Class tht implements exceptions for inappropriate strings"""


class Sentence:
    """CLass, that implements major part of functionality for parsing sentences"""
    def __init__(self, sentence: str):
        """Magic method that initiates only ONE sentence with following engings (.?!...)"""
        if not isinstance(sentence, str):
            raise TypeError("Sentence must be string type")
        if not re.match(r"[^.]+(\.{1}|\?{1}|\!{1}|\.{3})$", sentence):
            raise MultipleSentenceError("Only one sentence required")
        if not re.match(r".+[a-zA-Z](\.{1}|\?{1}|\!{1}|\.{3})$", sentence):
            raise ValueError('Sentence must end correctly(look at __init__ doc)')
        self._sentence = sentence

    def __repr__(self):
        """Method that overloads converting Sentence object to str"""
        words = len(re.findall(r'\w+', self._sentence))
        other_chars = len(re.findall(r'[,.?!]', self._sentence))
        return f"<Sentence(words={words},other_chars={other_chars})>"

    @property
    def _words(self):
        """Property, that returns lazy iterator for words in sentence"""
        return (word for word in re.sub(r'[^\w+]', " ", self._sentence).split())

    @property
    def words(self):
        """Property that returns list of words"""
        return re.sub(r'[^\w+]', " ", self._sentence).split()

    @property
    def other_chars(self):
        """Property,that returns list of other chars in sentence ,. etc."""
        return re.sub(r'[\w+]', " ", self._sentence).split()

    def __len__(self):
        """Magic method that returns length of sentence(in words)"""
        return len(self.words)

    def __getitem__(self, item):
        """Magic method that implements indexing and slicing on the sentence"""
        if isinstance(item, slice):  # Срез
            return self.words[item.start:item.stop:item.step]
        if item >= len(self) or item < -len(self):  # Индекс
            raise IndexError("Out of list of words")
        return self.words[item]

    def __iter__(self):
        """Magic method, that returns SentenceIterator obj for iteration on"""
        return SentenceIterator(self)


class SentenceIterator:
    """CLass, that implements iterating over sentence"""
    def __init__(self, sentence: Sentence):
        """Magic method that initiates SentenceIterator obj based on Sentence"""
        self.__words = sentence.words
        self.current = -1

    def __next__(self):  #Можно было сделать также через ленивый итератор
        """Magic method that implements iterating itself"""
        self.current += 1
        if self.current >= len(self.__words):
            raise StopIteration
        return self.__words[self.current]

    def __iter__(self):
        """Magic method that returns SentenceIterator object as object to iterate over"""
        return self


if __name__ == "__main__":
    s = Sentence("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    print(s)
    print(s[:7:2])
    print(len(s))
    print(s.words)
    print(s.other_chars)
    itobj = iter(s)
    for word in itobj:
        print(word)
