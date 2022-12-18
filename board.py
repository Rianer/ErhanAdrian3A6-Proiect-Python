from cards import Game_Deck
from cards import Game_Card, Game_Slot

VERTICAL_CARD_GAP = 20


def check_cards(card1, card2):
    """Checks if card2 can be placed on top of card1"""
    if card1[0] == -1 and card2[0] == 13:
        return True
    color1 = card1[1] % 2
    color2 = card2[1] % 2
    if card1[0] - 1 == card2[0] and color1 != color2:
        return True
    return False


class Card_Collumn:
    """
    A class to represent a collumn of cards

    ...

    Attributes
    ----------
    cards : list
        list of cards that are in the collumn

    Methods
    -------
    insert(cards) : None
        inserts cards in the card collumn
    get_cards() : list
        returns a copy of the card list
    validate_move(cards) : bool
        checks if putting a cards list on top of the card collumn is a valid move
    """

    _cards = list()

    def __init__(self, cards):
        if type(cards) != list:
            self._cards = list()
        else:
            self._cards = list(cards)
            self._cards[-1].is_visible = True

    def insert(self, cards):
        """
        Inserts a list of cards in the card collumn, by appending them

        Parameters
        ----------
        cards : list
            The list of cards to be appended

        Returns
        -------
        None
        """
        if self.validate_move(cards):
            cards_list = cards.get_cards()
            for card in cards_list:
                print(card)
                self._cards.append(card)

    def get_cards(self):
        """
        Returns a copy of the card list in the card collumn

        Parameters
        ----------
        None

        Returns
        -------
        List of cards
        """
        return list(self._cards)

    def validate_move(self, cards):
        """
        Checks if putting a list of cards on top of the card collumn is a valid move

        Parameters
        ----------
        cards : list
            The list of cards to be checked for appending
        Returns
        -------
        bool : Is the move valid
        """
        last_card = self._cards[-1]
        if type(cards) == Card_Collumn or type(cards) == Game_Collumn:
            new_card = cards.get_cards()[0]
            return check_cards(last_card.getInfo(), new_card.getInfo())
        return False

    def __str__(self) -> str:
        return str(self._cards)


class Board:
    """
    A class to represent the game board

    ...

    Atributes
    ---------
    cards_in_hand : bool
        Shows if there are cards currently dragged by the player
    moving_buffer : bool
        Shows if the player is currently dragging the deck buffer card
    _board : list
        The list of card collumns that represent the main 7 collumns of cards
    slots : list
        The list of final card slots
    game_won : bool
        Shows if the game is won or not
    col_gap : int
        Represents the distance between card columns
    y_offset : int
        Represents the offset from the left border for the card collumns
    _buffer_card : Game_Card | None
        Represents the deck's buffer card
    moving_cards : Game_Collumn | None
        Represents the cards that are being dragged by the player
    moving_cards_origin_col : int
        Represents the index of the colomn from where the player took the moving cards
    _deck : Game_Deck
        Represents the deck of cards

    Methods
    -------
    show_board():
        prints to console the state of the main 7 card collumns
    clicked_deck(position):
        checks if the player has clicked on the deck
    clicked_buffer(position):
        checks if the player has clicked on the deck's buffer card
    clicked_slots(position):
        returns the index of the slot that was clicked by the player, if any was clicked
    return_cards():
        makes the cards that are being moved to return to the origin collumn
    confirm_placement():
        unhides the last card from the origin collumn of the moved cards
    reset_card_move():
        resets the values for moving cards
    check_win_condition():
        checks if the player has won
    handle_mouse_click():
        handles player's clicks on different parts of the board and in different states
    """

    def __init__(self, col_gap, y_offset):
        self.cards_in_hand = False
        self.moving_buffer = False
        self._board = list()
        self.slots = list()
        self.game_won = False
        self.col_gap = col_gap
        self.y_offset = y_offset
        self._buffer_card = None
        self.moving_cards = None
        self.moving_cards_origin_col = None
        self._deck = Game_Deck((col_gap, col_gap / 2), col_gap + 89)
        for col_index in range(1, 8):
            cards = self._deck.draw_cards(col_index)
            column = Game_Collumn(
                cards, (col_gap * col_index + (col_index - 1) * 89, y_offset), True
            )
            self._board.append(column)
        for symbol in range(0, 4):
            position = (
                self._board[3 + symbol].position[0],
                self._deck.deck_position[1],
            )
            self.slots.append(Game_Slot(position, symbol))
        self._deck.initialize_game()

    def show_board(self):
        """
        Prints to console the state of the main 7 card collumns. Used only for debugging.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for index in range(0, 7):
            print("Column {}: {}".format(index + 1, self._board[index]))

    def clicked_deck(self, position):
        """
        Checks if the player has clicked on the deck

        Parameters
        ----------
        position : tuple
            A tuple of 2 integers representing mouse (x,y) coordinates

        Returns
        -------
        bool : the player has clicked the deck
        """
        if self.cards_in_hand:
            return False
        if (
            position[0] < self._deck.deck_position[0]
            or position[0] > self._deck.deck_position[0] + 89
        ):
            return False
        if (
            position[1] < self._deck.deck_position[1]
            or position[1] > self._deck.deck_position[1] + 120
        ):
            return False
        return True

    def clicked_buffer(self, position):
        """
        Checks if the player has clicked on the deck's buffer card

        Parameters
        ----------
        position : tuple
            A tuple of 2 integers representing mouse (x,y) coordinates
        Returns
        -------
        bool : the player has clicked on the buffer card
        """
        if (
            position[0] < self._deck.buffer_position[0]
            or position[0] > self._deck.buffer_position[0] + 89
        ):
            return False
        if (
            position[1] < self._deck.buffer_position[1]
            or position[1] > self._deck.buffer_position[1] + 120
        ):
            return False
        if self.cards_in_hand:
            print("Clicked Buffer => Returning")
            self.return_cards()
            self.reset_card_move()
            return False
        return True

    def clicked_slots(self, position):
        """
        Returns the index of the slot that was clicked by the player, if any was clicked

        Parameters
        ----------
        position : tuple
            A tuple of 2 integers representing mouse (x,y) coordinates
        Returns
        -------
        int : the index of the slot clicked by the player.
            Returns negative numbers if the player has not clicked on the slots
            or is not allowed to
        """
        if self.cards_in_hand:
            if len(self.moving_cards._cards) > 1:
                return -1
        if (
            position[1] < self._deck.deck_position[1]
            or position[1] > self._deck.deck_position[1] + 120
        ):
            return -2
        index = 0
        for slot in self.slots:
            if position[0] >= slot.position[0] and position[0] <= slot.position[0] + 89:
                return index
            index += 1
        return -2

    def return_cards(self):
        """
        Makes the cards that are being moved to return to the origin collumn

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        card = self.moving_cards._cards[0]
        if self.slots[card._symbol].card_taken:
            self.slots[card._symbol].card_taken = False
            card.position = self.slots[card._symbol].position
            self.slots[card._symbol].insert_card(card)
            return
        if self.moving_buffer:
            self.moving_cards._cards[0].position = self._deck.buffer_position
            self._deck.buffer_deck.append(self.moving_cards._cards[0])
        else:
            self._board[self.moving_cards_origin_col].force_insert(self.moving_cards)

    def confirm_placement(self):
        """
        Unhides the last card from the origin collumn of the moved cards

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not self.moving_buffer:
            self._board[self.moving_cards_origin_col].unhide_last()

    def reset_card_move(self):
        """
        Resets the values for moving cards

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.cards_in_hand = False
        self.moving_cards = None
        self.moving_buffer = False
        self.moving_cards_origin_col = -1

    def check_win_condition(self):
        """
        Checks if the player has won

        Parameters
        ----------
        None

        Returns
        -------
        bool: the player has won
        """
        for slot in self.slots:
            if len(slot.cards) != 13:
                return False
        self.game_won = True
        return True

    def handle_mouse_click(self, mouse_position):
        """
        Handles player's clicks on different parts of the board and in different states

        Parameters
        ----------
        position : tuple
            A tuple of 2 integers representing mouse (x,y) coordinates

        Returns
        -------
        bool : Returns False if no cards were selected, True otherwise
        """
        index = 0
        slot_clicked = self.clicked_slots(mouse_position)

        for col in self._board:
            if col.is_cursor_on_collumn(
                mouse_position
            ):  # searching the column where the cursor clicked
                if not self.cards_in_hand:  # selecting cards to move
                    selected_cards = col.take_cards_from_position(
                        mouse_position
                    )  # cards selected by cursor
                    if selected_cards == None:
                        return False
                    self.moving_cards = (
                        selected_cards  # saving the cards that are moved by cursor
                    )
                    self.moving_cards_origin_col = (
                        index  # saving the original column of the cards
                    )
                    self.cards_in_hand = True
                    return True
                else:  # cards are already selected, checking for placement
                    if col.validate_move(self.moving_cards):
                        print("Valid Move")
                        col.force_insert(self.moving_cards)
                        self.confirm_placement()
                    else:
                        self.return_cards()
                    self.reset_card_move()
                    return True
            index += 1

        # checking for click on deck
        if self.clicked_deck(mouse_position):
            if len(self._deck.deck) != 0:
                self._deck.take_card()
            else:
                self._deck.return_deck()

        if self.clicked_buffer(mouse_position):
            buffer_card = self._deck.get_buffer_top()
            buffer_col = Game_Collumn([buffer_card], buffer_card.position)
            self.cards_in_hand = True
            self.moving_cards = buffer_col
            self.moving_buffer = True
            self._deck.buffer_deck.pop()
            print(buffer_col)

        if slot_clicked >= 0:
            if self.cards_in_hand:
                if self.slots[slot_clicked].validate_insertion(
                    self.moving_cards._cards[0]
                ):
                    self.slots[slot_clicked].insert_card(self.moving_cards._cards[0])
                    self.confirm_placement()
                    self.reset_card_move()
            else:

                card = self.slots[slot_clicked].extract_card()
                if card != None:
                    card_col = Game_Collumn([card], card.position)
                    self.cards_in_hand = True
                    self.moving_cards = card_col
                    self.slots[slot_clicked].card_taken = True

        self.check_win_condition()


class Game_Collumn(Card_Collumn):
    """
    A class to represent a collumn of cards for the GUI.
    Extends the class Card_Collumn

    ...

    Atributes
    ---------
    cards : list
        list of cards that are in the collumn
    is_board_column : bool
        is this collumn one of the board's main collumns
    position : tuple
        (x,y) coordinates of the top left corner of the collumn's base card

    Methods
    -------

    insert(cards): None
        inserts cards in the game collumn, on top of the last card
    is_cursor_on_collumn(cursor_coordinates) : bool
        checks if the cursor is on the game collumn
    take_cards_from_position(position) : Game_Collumn | None
        handles grabbing the cards from a specific position within the game collumn
    get_last_card() : Game_Card | None
        returns the last card in the collumn
    unhide_last() : None
        sets the last card's in the collumn visibility to True
    change_position(new_pos) : None
        changes game collumn's position to the new position
    force_insert(cards) : None
        inserts a list of cards in the collumn, avoiding the move validation check
    clear_not_rendered(unhide_last) : None
        deletes all the cards which are set to not be rendered from the collumn
    refresh_rendered() : None
        sets all the cards in the collumn to be rendered
    """

    def __init__(self, cards, position, is_board_column=False):
        super().__init__(cards)
        self.is_board_column = is_board_column

        if type(position) == tuple and len(position) == 2:
            self.position = position
        else:
            self.position = (0, 0)
        index = 0

        for card in self._cards:
            card.position = (
                self.position[0],
                self.position[1] + VERTICAL_CARD_GAP * index,
            )
            index += 1

        if is_board_column:
            base = Game_Card(-1, -1)
            base.position = self.position
            base.is_visible = True
            self._cards.insert(0, base)

    # Overriden
    def insert(self, cards):
        """
        Inserts cards in the game collumn, on top of the last card

        Parameters
        ----------
        cards : list
            The list of cards to be inserted at the collumns top

        Returns
        -------
        None
        """

        if self.validate_move(cards):
            cards_list = cards.get_cards()
            last_position = self._cards[-1].position
            index = 1
            for card in cards_list:
                card.position = (
                    last_position[0],
                    last_position[1] + (VERTICAL_CARD_GAP * index),
                )
                self._cards.append(card)
                index += 1

    def __str__(self) -> str:
        return "[Card collumn at position {}]: ".format(self.position) + str(
            self._cards
        )

    def is_cursor_on_collumn(self, cursor_coordinates):
        """
        Checks if the cursor is on the game collumn

        Parameters
        ----------
        cursor_coordinates : tuple
            (x,y) coordinates of the current cursor position

        Returns
        -------
        bool : the cursor is on the collumn

        """
        if len(self._cards) == 0:
            return False
        if cursor_coordinates[0] < self.position[0] or cursor_coordinates[0] > (
            self.position[0] + 89
        ):
            return False
        if cursor_coordinates[1] < self.position[1] or cursor_coordinates[1] > (
            self.position[1] + (len(self._cards) - 1) * VERTICAL_CARD_GAP + 120
        ):
            return False
        return True

    def take_cards_from_position(self, position):
        """
        Handles grabbing the cards from a specific position within the game collumn

        Parameters
        ----------
        position : tuple
            A tuple of 2 integers representing mouse (x,y) coordinates

        Returns
        -------
        Game_Collumn | None : the game collumn of cards that are under the cursor

        """
        delta_y = abs(self.position[1] - position[1])
        card_index = delta_y // VERTICAL_CARD_GAP
        if self.is_board_column:
            card_index += 1
            if len(self._cards) == 1:
                return None
        if card_index > len(self._cards) - 1:
            card_index = len(self._cards) - 1
        if self._cards[card_index].is_visible:
            grabbed_cards = Game_Collumn(
                self._cards[card_index:], self._cards[card_index].position
            )
            del self._cards[card_index:]
            return grabbed_cards

    def get_last_card(self):
        """
        Returns the last card in the collumn

        Parameters
        ----------
        None

        Returns
        -------
        Game_Card | None : the last card in the collumn
        """
        if len(self._cards > 0):
            return self._cards[-1]

    def unhide_last(self):
        """
        Sets the last card's in the collumn visibility to True

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._cards[-1].is_visible = True

    def change_position(self, new_pos):
        """
        Changes game collumn's position to the new position

        Parameters
        ----------
        new_pos : tuple
            A tuple of 2 integers representing new collumn's (x,y) coordinates

        Returns
        -------
        None
        """
        self.position = new_pos
        index = 0
        for card in self._cards:
            if card.is_base:
                continue
            card.position = (
                self.position[0],
                self.position[1] + VERTICAL_CARD_GAP * index,
            )
            index += 1

    def force_insert(self, cards):
        """
        Inserts a list of cards in the collumn, avoiding the move validation check

        Parameters
        ----------
        cards : list
            The list of cards to be inserted at the collumns top

        Returns
        -------
        None
        """
        last_position = self._cards[-1].position
        if self.is_board_column and len(self._cards) == 1:
            print("Inserting card on base")
            last_position = (self.position[0], self.position[1] - VERTICAL_CARD_GAP)
        index = 1
        for card in cards._cards:
            card.position = (
                self.position[0],
                last_position[1] + (VERTICAL_CARD_GAP * index),
            )
            self._cards.append(card)
            index += 1

    def clear_not_rendered(self, unhide_last):
        """
        Deletes all the cards which are set to not be rendered from the collumn

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        last_rendered = -1
        print("Checking rendering:\n\n")
        for card in self._cards:
            print("{}".format(card))
            if card.rendered:
                last_rendered += 1
            else:
                break
        del self._cards[last_rendered:]

        if len(self._cards) > 0:
            self._cards[last_rendered - 1].is_visible = unhide_last

    def refresh_rendered(self):
        """
        Sets all the cards in the collumn to be rendered

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for card in self._cards:
            card.rendered = True
