from cards import Deck, Card

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
    _deck = None
    _shelf = list()
    _board = list()
    _buffer_card = None

    def __init__(self):
        self._deck = Deck()
        self._deck.shuffleDeck()
        for col_index in range(1,8):
            cards = self._deck.drawCards(col_index)
            column = Card_Collumn(cards)
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
        
    