from cards import Card
from random import shuffle

class Deck:
    _drawed = list()
    cards = list()
    size = 0

    def __init__(self):
        for symbol in range(0,4):
            for value in range(1,14):
                self.cards.append(Card(value, symbol))
                self.size += 1
    
    def showDeck(self):
        for card in self.cards:
            print("{} of {}".format(card.getStringValue(), card.getStringSymbol()))
    
    def shuffleDeck(self):
        shuffle(self.cards)
    
    def showLastCards(self, number):
        if number <= 0 or number >= self.size:
            raise IOError('Number of cards must be between 0 and {}'.format(self.size))
        for index in range(self.size-number-1, self.size):
            print(self.cards[index].getFullName())

    def showFirstCards(self, number):
        if number <= 0 or number >= self.size:
            raise IOError('Number of cards must be between 0 and {}'.format(self.size))
        for index in range(0, number):
            print(self.cards[index].getFullName())
    
    def drawLastCard(self):
        if self.size == 0:
            return None
        self.size -= 1
        last = self.cards.pop()
        self._drawed.append(last)
        return last

    def drawCards(self, number):
        if number <= 0 or number >= self.size:
            raise IOError('Number of cards must be between 0 and {}'.format(self.size))
        drawedCards = list()
        while len(drawedCards) < number:
            drawedCards.append(self.drawLastCard())


    def replenishDeck(self):
        for card in self._drawed:
            self.cards.append(card)
            self.size += 1
