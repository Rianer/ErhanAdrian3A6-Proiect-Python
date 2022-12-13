from cards import Deck


def check_cards(card1, card2):
    #card = (value, symbol)
    color1 = card1[1] % 2
    color2 = card2[1] % 2
    if card1[0] - 1 == card2[0] and color1 != color2:
        return True
    return False

class Card_Collumn:
    _cards = list()

    def __init__(self, cards):
        if type(cards) != list:
            self._cards = list()
        else:
            self._cards = list(cards)
            self._cards[-1].is_visible = True

    def insert(self, cards):
        if self.validate_move(cards):
            cards_list = cards.get_cards()
            for card in cards_list:
                print(card)
                self._cards.append(card)
            # self._cards[-1].is_visible = True

    def validate_move(self, cards):
        last_card = self._cards[-1]
        if type(cards) == Card_Collumn:
            new_card = cards.get_cards()[0]
            return check_cards(last_card.getInfo(), new_card.getInfo())
        return False

    def get_cards(self):
        return list(self._cards)

    def take_last(self):
        self._cards[-2].is_visible = True
        return self._cards.pop()
    
    def take_cards(self, number):
        if number > len(self._cards) or number < 0:
            return None
        taken_column = Card_Collumn(self._cards[len(self._cards)-number:])
        del self._cards[len(self._cards) - number:]
        if(len(self._cards) > 0):
            self._cards[-1].is_visible = True
        return taken_column
    
    def __str__(self) -> str:
        return str(self._cards)
    
class Board:
    def __init__(self, col_gap, y_offset):
        self._board = list()
        self._shelf = list()
        self._buffer_card = None
        self._deck = Deck()
        self._deck.shuffleDeck()
        for col_index in range(1,8):
            cards = self._deck.drawCards(col_index)
            column = Game_Collumn(cards, (col_gap * col_index + (col_index-1)*89, y_offset))
            self._board.append(column)
    

    def show_board(self):
        for index in range(0,7):
            print("Column {}: {}".format(index+1, self._board[index]))
    
    def move_cards(self, origin_column, target_column, height):
        #height = number of cards from bottom that will be moved
        origin_col_cards = self._board[origin_column].get_cards()
        origin_top_card = origin_col_cards[len(origin_col_cards)-height]
        target_last_card = self._board[target_column].get_cards()[-1]
        is_valid_move = check_cards(target_last_card.getInfo(),origin_top_card.getInfo())
        if is_valid_move:
            transfer = self._board[origin_column].take_cards(height)
            print(transfer.get_cards())
            self._board[target_column].insert(transfer)
            return True
        else:
            return False
        
# class Game_Board(Board):
#     def __init__(self):
#         super().__init__()

class Game_Collumn(Card_Collumn):
    def __init__(self, cards, position):
        super().__init__(cards)
        if type(position) == tuple and len(position) == 2:
            self.position = position
        else:
            self.position = (0,0)
        index = 0
        self.rendered = True
        for card in self._cards:
            card.position = (self.position[0], self.position[1] + 10 * index)
            index += 1
    
    #Overriden
    def insert(self, cards):
        if self.validate_move(cards):
            cards_list = cards.get_cards()
            last_position = self._cards[-1].position
            index = 1
            for card in cards_list:
                card.position = (last_position[0], last_position[1] + (10 * index))
                self._cards.append(card)
    
    def __str__(self) -> str:
        return "[Reder={} at position {}]: ".format(self.rendered, self.position) + str(self._cards)

    def is_cursor_on_collumn(self, cursor_coordinates):
        if len(self._cards) == 0:
            return False
        if cursor_coordinates[0] < self.position[0] or cursor_coordinates[0] > (self.position[0] + 89):
            return False
        if cursor_coordinates[1] < self.position[1] or cursor_coordinates[1] > ((len(self._cards)-1)*10 + 120):
            return False
        return True
    
    def card_on_cursor(self, cursor_coordinates):
        if not self.is_cursor_on_collumn():
            return None
        delta_y = self.position[1] - cursor_coordinates[1]
        card_index = delta_y % 10
        if card_index > len(self._cards)-1:
            card_index = len(self._cards)-1
        if self._cards[card_index].is_visible:
            return Game_Collumn(self._cards[card_index:], cursor_coordinates)
    
