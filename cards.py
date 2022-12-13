from random import shuffle
from pygame import image
from os import path

class Card:
    # _value = int()
    # _symbol = int()
    # is_visible = bool()
    # _string_value = str()
    # _string_symbol = str()

    def __init__(self, value, symbol):
        self._value = value
        self._symbol = symbol
        self.is_visible = False
        self.translateSymbol()
        self.translateValue()
    
    def translateValue(self):
        if self._value > 1 and self._value<11:
            self._string_value = str(self._value)
        else:
            if self._value == 1: 
                self._string_value = 'A'
            if self._value == 11:
                self._string_value = 'J'
            if self._value == 12:
                self._string_value = 'Q'
            if self._value == 13:
                self._string_value = 'K'

    def translateSymbol(self):
        #even numbers = red color
        #odd numbers = black color
        if self._symbol == 0:
            self._string_symbol = 'Hearts'
        if self._symbol == 2:
            self._string_symbol = 'Tiles'
        if self._symbol == 1:
            self._string_symbol = 'Clovers'
        if self._symbol == 3:
            self._string_symbol = 'Pikes'
    
    def getSymbol(self):
        return self._symbol
    
    def getStringSymbol(self):
        return self._string_symbol
    
    def getValue(self):
        return self._value
    
    def getStringValue(self):
        return self._string_value
    
    def getFullName(self):
        return self._string_value + '_of_' + self._string_symbol

    def getInfo(self):
        return (self._value, self._symbol)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.getInfo() == other.getInfo():
            return True
        return False
    
    def __str__(self):
        if not self.is_visible:
            return "|Hidden|"
        return self.getFullName()

    def __repr__(self):
        if not self.is_visible:
            return "|Hidden|"
        return self.getFullName()

class Game_Card(Card):
    def __init__(self, value, symbol):
        super().__init__(value, symbol)
        self.WIDTH = 89
        self.HEIGHT = 120
        self.position = (0,0) #left, right corner
        img_name = self.getFullName() + '.png'
        self.texture = image.load(path.join('Assets\Textures', img_name))
        self.card_back = image.load(path.join('Assets\Textures', 'Card_Back.png'))
    
    def __str__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position)
        return self.getFullName() + " at {}".format(self.position) 
    
    def __repr__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position) 
        return self.getFullName() + " at {}".format(self.position) 

class Deck:
    _drawed = list()
    cards = list()
    size = 0

    def __init__(self):
        for symbol in range(0,4):
            for value in range(1,14):
                self.cards.append(Game_Card(value, symbol))
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
        return drawedCards


    def replenishDeck(self):
        for card in self._drawed:
            self.cards.append(card)
            self.size += 1