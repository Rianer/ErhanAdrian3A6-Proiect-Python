from random import shuffle
from pygame import image
from os import path


class Card:
    """
    A class that represents a card

    ...

    Attributes:
    -----------
    _value : int
        the numeric representation of the card's value
    _symbol : int
        the numeric representation of the card's symbol/color
    is_visible : bool
        determines if the card can be displayed or not
    _string_value : str
        the string form or exact value of the card
    _string_symbol : str
        the string form or exact symbol of the card

    Methods:
    --------
    translateValue() : None
        translates the numeric value of the card to the corresponding string value
    translateSymbol() : None
        translates the numeric symbol of the card to the corresponding string symbol
    getSymbol() : int
        returns the card's symbol in numeric form
    getStringSymbol() : str
        returns the card's symbol in string form
    getValuel() : int
        returns the card's value in numeric form
    getStringValue() : str
        returns the card's value in string form
    getFullName() : str
        returns the name of the card in string form corresponding to the name of the card's texture file
    getInfo() : tuple
        returns a tuple of the card's value and symbol in numeric forms

    """

    def __init__(self, value, symbol):
        self._value = value
        self._symbol = symbol
        self.is_visible = False
        self.translateSymbol()
        self.translateValue()

    def translateValue(self):
        """
        Translates the numeric value of the card to the corresponding string value

        Parameters:
        ----------
        None

        Returns:
        -------
        None
        """
        if self._value == -1:
            self._string_value = "Base"
        elif self._value > 1 and self._value < 11:
            self._string_value = str(self._value)
        else:
            if self._value == 1:
                self._string_value = "A"
            if self._value == 11:
                self._string_value = "J"
            if self._value == 12:
                self._string_value = "Q"
            if self._value == 13:
                self._string_value = "K"

    def translateSymbol(self):
        """
        Translates the numeric symbol of the card to the corresponding string symbol

        Parameters:
        ----------
        None

        Returns:
        -------
        None
        """
        # even numbers = red color
        # odd numbers = black color
        if self._symbol == -1:
            self._string_symbol = "Collumn"
        if self._symbol == 0:
            self._string_symbol = "Hearts"
        if self._symbol == 2:
            self._string_symbol = "Tiles"
        if self._symbol == 1:
            self._string_symbol = "Clovers"
        if self._symbol == 3:
            self._string_symbol = "Pikes"

    def getSymbol(self):
        """
        Returns the card's symbol in numeric form

        Parameters:
        ----------
        None

        Returns:
        -------
        int : card's symbol in numeric form
        """
        return self._symbol

    def getStringSymbol(self):
        """
        Returns the card's symbol in string form

        Parameters:
        ----------
        None

        Returns:
        -------
        str : card's symbol in string form
        """
        return self._string_symbol

    def getValue(self):
        """
        Returns the card's value in numeric form

        Parameters:
        ----------
        None

        Returns:
        -------
        int : card's value in numeric form
        """
        return self._value

    def getStringValue(self):
        """
        Returns the card's value in string form

        Parameters:
        ----------
        None

        Returns:
        -------
        str : card's value in string form
        """
        return self._string_value

    def getFullName(self):
        """
        Returns the name of the card in string form corresponding to the name of the card's texture file

        Parameters:
        ----------
        None

        Returns:
        -------
        str : name of the card in string form corresponding to the name of the card's texture file
        """
        return self._string_value + "_of_" + self._string_symbol

    def getInfo(self):
        """
        Returns a tuple of the card's value and symbol in numeric forms

        Parameters:
        ----------
        None

        Returns:
        -------
        tuple : (value, symbol) of the card in numeric forms
        """
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
    """
    A class that represents a game card. Extends the card class.

    ...

    Attributes:
    -----------
    constant card's texture dimensions:
        WIDTH = 89
        HEIGHT = 120
    rendered : bool
        shall the card be displayed on the GUI
    position : tuple
        card's top left (x,y) coordinates
    is_base : bool
        shows if the card represents a base "invisible" card
    texture : image
        the card's texture
    card_back : image
        the card's back texture

    Methods:
    --------
    See Card class...
    """

    def __init__(self, value, symbol):
        super().__init__(value, symbol)
        self.WIDTH = 89
        self.HEIGHT = 120
        self.rendered = True
        self.position = (0, 0)  # left, right corner
        self.is_base = value == -1
        img_name = self.getFullName() + ".png"
        self.texture = image.load(path.join("Assets\Textures", img_name))
        self.card_back = image.load(path.join("Assets\Textures", "Card_Back.png"))

    def __str__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position) + " <render = {}>".format(
                self.rendered
            )
        return (
            self.getFullName()
            + " at {}".format(self.position)
            + " <render = {}>".format(self.rendered)
        )

    def __repr__(self):
        if not self.is_visible:
            return "|Hidden| at {}".format(self.position) + " <render = {}>".format(
                self.rendered
            )
        return (
            self.getFullName()
            + " at {}".format(self.position)
            + " <render = {}>".format(self.rendered)
        )


class Deck:
    """
    A class that represents a deck of cards

    ...

    Attributes:
    -----------
    _drawed : list
        the list of cards that were drawed from the deck
    cards : list
        the deck's list of cards
    size : int
        the deck's cards list length or the size of the deck

    Methods:
    --------
    showDeck() : None
        prints to console the whole list of deck's cards
    getAllCards() : list
        returns all the deck's cards
    shuffleDeck() : None
        shuffles the deck's cards
    drawLastCard() : Card : None
        returns the last card from the deck if it exists
    drawCards(number) : list
        returns a list of specified number of cards from the deck
    replenishDeck() : None
        fills the deck's cards list with all the drawed cards

    """

    def __init__(self):
        self._drawed = list()
        self.cards = list()
        self.size = 0
        for symbol in range(0, 4):
            for value in range(1, 14):
                self.cards.append(Game_Card(value, symbol))
                self.size += 1

    def showDeck(self):
        """
        Prints to console the whole list of deck's cards

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        for card in self.cards:
            print("{} of {}".format(card.getStringValue(), card.getStringSymbol()))

    def getAllCards(self):
        """
        Returns all the deck's cards

        Parameters:
        -----------
        None

        Returns:
        --------
        list : all the deck's cards
        """
        return self.cards

    def shuffleDeck(self):
        """
        shuffles the deck's cards

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        shuffle(self.cards)

    def drawLastCard(self):
        """
        Returns the last card from the deck if it exists

        Parameters:
        -----------
        None

        Returns:
        --------
        Card : last card from the deck
        """
        if self.size == 0:
            return None
        self.size -= 1
        last = self.cards.pop()
        self._drawed.append(last)
        return last

    def drawCards(self, number):
        """
        Returns a list of specified number of cards from the deck

        Parameters:
        -----------
        number : int
            the number of cards to be drawn

        Returns:
        --------
        list : drawed cards
        """
        if number <= 0 or number >= self.size:
            raise IOError("Number of cards must be between 0 and {}".format(self.size))
        drawedCards = list()
        while len(drawedCards) < number:
            drawedCards.append(self.drawLastCard())
        return drawedCards

    def replenishDeck(self):
        """
        Fills the deck's cards list with all the drawed cards

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        for card in self._drawed:
            self.cards.append(card)
            self.size += 1


class Game_Deck:
    """
    A class that represents a game deck for the GUI

    ...

    Attributes:
    -----------
    cards : Deck
        the cards that are in the game
    deck : list
        list of cards that will be in the deck
    buffer_deck : list
        list of cards that will be in the buffer deck
    deck_position : tuple
        (x,y) coordinates of the deck's top left corner
    buffer_position : tuple
        (x,y) coordinates of the buffer deck's top left corner
    deck_base : Game_Card
        a "false" card representing the deck's base
    buffer_base : Game_Card
        a "false" card representing the buffer deck's base

    Methods:
    --------
    draw_cards(number): list
        draw a specific number of cards from the deck (cards attribute)
    reveal_deck() : None
        sets the deck's top card to visible
    reveal_buffer() : None
        sets the buffer deck's top card to visible
    take_card() : None
        takes a card from the deck and puts it on the buffer deck, revealing it
    return_deck() : None
        returns all the cards from the buffer deck to the main deck
    get_deck_top() : Game_Card | None
        returns the deck's top card
    get_buffer_top() : Game_Card | None
        returns the buffer deck's top card
    normalize_deck_positions() : None
        sets all the cards from the main and buffer deck to be positioned at their parrent deck's coordinates
    initialize_game() : None
        makes the initial setup for the game's deck
    """

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
        """
        Draw a specific number of cards from the deck (cards attribute)

        Parameters:
        -----------
        number : int
            the number of cards to be drawed

        Returns:
        --------
        list : the list of drawed cards
        """
        return self.cards.drawCards(number)

    def reveal_deck(self):
        """
        Sets the deck's top card to visible

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        if len(self.deck) < 1:
            return
        self.deck[-1].is_visible = True

    def reveal_buffer(self):
        """
        Sets the buffer deck's top card to visible

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        if len(self.buffer_deck) < 1:
            return
        self.buffer_deck[-1].is_visible = True

    def take_card(self):
        """
        Takes a card from the deck and puts it on the buffer deck, revealing it

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        self.buffer_deck.append(self.deck.pop())
        self.reveal_buffer()
        self.normalize_deck_positions()

    def return_deck(self):
        """
        Returns all the cards from the buffer deck to the main deck

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        for card in self.buffer_deck:
            card.is_visible = False
            card.position = self.deck_position
        self.deck = self.buffer_deck[::-1]
        self.buffer_deck = list()

    def get_deck_top(self):
        """
        Returns the deck's top card

        Parameters:
        -----------
        None

        Returns:
        --------
        Game_Card | None : the deck's top card or None if it does not exist
        """
        if len(self.deck) < 1:
            return None
        return self.deck[-1]

    def get_buffer_top(self):
        """
        Returns the buffer deck's top card

        Parameters:
        -----------
        None

        Returns:
        --------
        Game_Card | None : the buffer deck's top card or None if it does not exist

        """
        if len(self.buffer_deck) < 1:
            return None
        return self.buffer_deck[-1]

    def normalize_deck_positions(self):
        """
        Sets all the cards from the main and buffer deck to be positioned at their parrent deck's coordinates

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        for card in self.deck:
            card.position = self.deck_position
        for card in self.buffer_deck:
            card.position = self.buffer_position

    def initialize_game(self):
        """
        Makes the initial setup for the game's deck

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        self.deck = self.cards.getAllCards()
        self.normalize_deck_positions()
        self.reveal_buffer()


class Game_Slot:
    """
    A class that represents the game slot ( one of the 4 card places for the game completion)

    ...

    Attributes:
    -----------
    cards : list
        list of cards in the slot
    position : tuple
        (x,y) position of the top left corner of the slot
    symbol : int
        numeric value of the slot's corresponding symbol
    card_taken : bool
        indicates if a card is taken from the slot
    texture : image
        the slot's base texture

    Methods:
    --------
    get_top_card() : Game_Card | None
        returns the slot's top card if there is any
    validate_insertion(card) : bool
        checks if the insertion to the slot is valid
    insert_card(card) : None
        inserts a card on top of the slot's cards
    extract_card() : Game_Card | None
        removing and returning the top card from the slot
    """

    def __init__(self, position, symbol):
        self.cards = list()
        self.position = position
        self.symbol = symbol
        self.card_taken = False
        if self.symbol == 0:
            self.name = "Hearts"
        if self.symbol == 2:
            self.name = "Tiles"
        if self.symbol == 1:
            self.name = "Clovers"
        if self.symbol == 3:
            self.name = "Pikes"
        img_name = "Base_of_" + self.name + ".png"
        self.texture = image.load(path.join("Assets\Textures", img_name))

    def get_top_card(self):
        """
        Returns the slot's top card if there is any

        Parameters:
        -----------
        None

        Returns:
        --------
        Game_Card | None : slot's top card if there is any
        """
        if len(self.cards) == 0:
            return None
        return self.cards[-1]

    def validate_insertion(self, card):
        """
        Checks if the insertion to the slot is valid

        Parameters:
        -----------
        card : Game_Card
            the card to be inserted

        Returns:
        --------
        bool : the card is allowed to be inserted in the slot
        """
        if card._symbol == self.symbol:
            if card._value == 1 and len(self.cards) == 0:
                return True
            if len(self.cards) == 0:
                return False
            if card._value == self.get_top_card()._value + 1:
                return True
        return False

    def insert_card(self, card):
        """
        Inserts a card on top of the slot's cards

        Parameters:
        -----------
        card : Game_Card
            the card to be inserted

        Returns:
        --------
        None
        """
        card.position = self.position
        self.cards.append(card)

    def extract_card(self):
        """
        Removing and returning the top card from the slot

        Parameters:
        -----------
        None

        Returns:
        --------
        Game_Card | None : the top card from the slot
        """
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
