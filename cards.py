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
        if self._value == -1:
            self._string_value = 'Base'
        elif self._value > 1 and self._value<11:
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
        if self._symbol == -1:
            self._string_symbol = 'Collumn'
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
        self.rendered = True
        self.position = (0,0) #left, right corner
        self.is_base = value == -1
        img_name = self.getFullName() + '.png'
        self.texture = image.load(path.join('Assets\Textures', img_name))
        self.card_back = image.load(path.join('Assets\Textures', 'Card_Back.png'))
    
    def __str__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position) + " <render = {}>".format(self.rendered)
        return self.getFullName() + " at {}".format(self.position) + " <render = {}>".format(self.rendered)
    
    def __repr__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position) + " <render = {}>".format(self.rendered)
        return self.getFullName() + " at {}".format(self.position) + " <render = {}>".format(self.rendered)

class Deck:
    # _drawed = list()
    # cards = list()
    # size = 0

    def __init__(self):
        self._drawed = list()
        self.cards = list()
        self.size = 0
        for symbol in range(0,4):
            for value in range(1,14):
                self.cards.append(Game_Card(value, symbol))
                self.size += 1
    
    def showDeck(self):
        for card in self.cards:
            print("{} of {}".format(card.getStringValue(), card.getStringSymbol()))
    
    def getAllCards(self):
        return self.cards

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

class Game_Deck:
    def __init__(self, deck_coordinates, deck_spacing):
        self.cards = Deck()
        self.deck = list()
        self.buffer_deck = list()
        self.deck_position = deck_coordinates
        self.buffer_position = (deck_coordinates[0] + deck_spacing, deck_coordinates[1])
        self.deck_base = Game_Card(-1, -1)
        self.deck_base.position = self.deck_position
        self.buffer_base = Game_Card(-1, -1)
        self.buffer_base.position = self.buffer_position
        self.cards.shuffleDeck()
    
    def draw_cards(self, number):
        return self.cards.drawCards(number)
    
    def reveal_deck(self):
        if len(self.deck) < 1:
            return
        self.deck[-1].is_visible = True

    def reveal_buffer(self):
        if len(self.buffer_deck) < 1:
            return
        self.buffer_deck[-1].is_visible = True

    def take_card(self):
        self.buffer_deck.append(self.deck.pop())
        self.reveal_buffer()
        self.normalize_deck_positions()
        # self.reveal_deck()

    def return_deck(self):
        for card in self.buffer_deck:
            card.is_visible = False
            card.position = self.deck_position
        self.deck = self.buffer_deck[::-1]
        self.buffer_deck = list()
        

    def get_deck_top(self):
        if len(self.deck) < 1:
            return None
        return self.deck[-1]

    def get_buffer_top(self):
        if len(self.buffer_deck) < 1:
            return None
        return self.buffer_deck[-1]

    def normalize_deck_positions(self):
        for card in self.deck:
            card.position = self.deck_position
        for card in self.buffer_deck:
            card.position = self.buffer_position

    def initialize_game(self):
        self.deck = self.cards.getAllCards()
        # self.reveal_deck()
        self.normalize_deck_positions()
        self.reveal_buffer()
        
class Game_Slot:
    def __init__(self, position, symbol):
        self.cards = list()
        self.position = position
        self.symbol = symbol
        self.card_taken = False
        if self.symbol == 0:
            self.name = 'Hearts'
        if self.symbol == 2:
            self.name = 'Tiles'
        if self.symbol == 1:
            self.name = 'Clovers'
        if self.symbol == 3:
            self.name = 'Pikes'
        img_name = "Base_of_" + self.name + ".png"
        self.texture = image.load(path.join('Assets\Textures', img_name))

    def get_top_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards[-1]

    def validate_insertion(self, card):
        if card._symbol == self.symbol:
            if card._value == 1 and len(self.cards) == 0:
                return True
            if card._value == self.get_top_card()._value + 1:
                return True
        return False
    
    def insert_card(self, card):
        card.position = self.position
        self.cards.append(card)
    
    def extract_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()