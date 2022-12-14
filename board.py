from cards import Game_Deck
from cards import Game_Card

VERTICAL_CARD_GAP = 20

def check_cards(card1, card2):
    #card = (value, symbol)
    if card1[0] == -1 and card2[0] == 13:
        return True
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

    def get_cards(self):
        return list(self._cards)

    def validate_move(self, cards):
        last_card = self._cards[-1]
        if type(cards) == Card_Collumn or type(cards) == Game_Collumn:
            new_card = cards.get_cards()[0]
            return check_cards(last_card.getInfo(), new_card.getInfo())
        return False

    
    def __str__(self) -> str:
        return str(self._cards)
    
class Board:
    def __init__(self, col_gap, y_offset):
        self.cards_in_hand = False
        self.moving_buffer = False
        self._board = list()
        self._shelf = list()
        self.col_gap = col_gap
        self.y_offset = y_offset
        self._buffer_card = None
        self.moving_cards = None
        self.moving_cards_origin_col = None
        # self.deck_position = 
        # self._buffer_card_position = (self.deck_position[0]+col_gap+89, self.deck_position[1])
        self._deck = Game_Deck((col_gap, col_gap/2), col_gap+89)
        for col_index in range(1,8):
            cards = self._deck.draw_cards(col_index)
            column = Game_Collumn(cards, (col_gap * col_index + (col_index-1)*89, y_offset), True)
            self._board.append(column)
        self._deck.initialize_game()
    

    def show_board(self):
        for index in range(0,7):
            print("Column {}: {}".format(index+1, self._board[index]))
    
    def clicked_deck(self, position):
        if self.cards_in_hand:
            return False
        if position[0] < self._deck.deck_position[0] or position[0] > self._deck.deck_position[0] + 89:
            return False
        if position[1] < self._deck.deck_position[1] or position[1] > self._deck.deck_position[1] + 120:
            return False
        return True
    
    def clicked_buffer(self, position):
        if self.cards_in_hand:
            return False
        if position[0] < self._deck.buffer_position[0] or position[0] > self._deck.buffer_position[0] + 89:
            return False
        if position[1] < self._deck.buffer_position[1] or position[1] > self._deck.buffer_position[1] + 120:
            return False
        return True
    
    def handle_mouse_click(self, mouse_position):
        index = 0
        for col in self._board:
            if col.is_cursor_on_collumn(mouse_position):#searching the column where the cursor clicked
                if not self.cards_in_hand: #selecting cards to move
                    selected_cards = col.take_cards_from_position(mouse_position) #cards selected by cursor
                    if selected_cards == None:
                        return False
                    self.moving_cards = selected_cards #saving the cards that are moved by cursor
                    self.moving_cards_origin_col = index #saving the original column of the cards
                    self.cards_in_hand = True
                    return True
                else: #cards are already selected, checking for placement
                    if col.validate_move(self.moving_cards):
                        print("Valid Move")
                        col.force_insert(self.moving_cards)
                        self._board[self.moving_cards_origin_col].unhide_last()
                    else:
                        print("Returning Card")
                        if self.moving_buffer:
                            self.moving_cards._cards[0].position = self._deck.buffer_position
                            self._deck.buffer_deck.append(self.moving_cards._cards[0])
                        else:
                            self._board[self.moving_cards_origin_col].force_insert(self.moving_cards)
                    self.cards_in_hand = False
                    self.moving_cards = None
                    self.moving_cards_origin_col = -1
                    return True
            index += 1

        #checking for click on deck
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



class Game_Collumn(Card_Collumn):
    def __init__(self, cards, position, is_board_column = False):
        super().__init__(cards)
        self.is_board_column = is_board_column
        
        if type(position) == tuple and len(position) == 2:
            self.position = position
        else:
            self.position = (0,0)
        index = 0
        
        for card in self._cards:
            card.position = (self.position[0], self.position[1] + VERTICAL_CARD_GAP * index)
            index += 1

        if is_board_column:
            base = Game_Card(-1, -1)
            base.position = self.position
            base.is_visible = True
            self._cards.insert(0, base)
    
    #Overriden
    def insert(self, cards):
        if self.validate_move(cards):
            cards_list = cards.get_cards()
            last_position = self._cards[-1].position
            index = 1
            for card in cards_list:
                card.position = (last_position[0], last_position[1] + (VERTICAL_CARD_GAP * index))
                self._cards.append(card)
                index += 1
    
    def __str__(self) -> str:
        return "[Card collumn at position {}]: ".format(self.position) + str(self._cards)

    def is_cursor_on_collumn(self, cursor_coordinates):
        if len(self._cards) == 0:
            return False
        if cursor_coordinates[0] < self.position[0] or cursor_coordinates[0] > (self.position[0] + 89):
            return False
        if cursor_coordinates[1] < self.position[1] or cursor_coordinates[1] > (self.position[1] + (len(self._cards)-1)*VERTICAL_CARD_GAP + 120):
            return False
        return True

    def take_cards_from_position(self, position):
        delta_y = abs(self.position[1] - position[1])
        card_index = delta_y // VERTICAL_CARD_GAP
        if self.is_board_column:
            card_index += 1
            if len(self._cards) == 1:
                return None
        if card_index > len(self._cards)-1:
            card_index = len(self._cards)-1
        if self._cards[card_index].is_visible:
            grabbed_cards = Game_Collumn(self._cards[card_index:], self._cards[card_index].position)
            del self._cards[card_index:]
            return grabbed_cards
    
    def get_last_card(self):
        return self._cards[-1]

    def unhide_last(self):
        self._cards[-1].is_visible = True
    
    def change_position(self, new_pos):
        self.position = new_pos
        index = 0
        for card in self._cards:
            if card.is_base:
                continue
            card.position = (self.position[0], self.position[1] + VERTICAL_CARD_GAP * index)
            index += 1
    
    def force_insert(self, cards):
        last_position = self._cards[-1].position
        if self.is_board_column and len(self._cards) == 1:
            print('Inserting card on base')
            last_position = (self.position[0], self.position[1] - VERTICAL_CARD_GAP)
        index = 1
        for card in cards._cards:
            card.position = (self.position[0], last_position[1] + (VERTICAL_CARD_GAP * index))
            self._cards.append(card)
            index += 1
    
    def clear_not_rendered(self, unhide_last):
        last_rendered = -1
        # if self.is_board_column:
        #     last_rendered += 1
        print("Checking rendering:\n\n")
        for card in self._cards:
            print("{}".format(card))
            # if card.is_base:
            #     continue
            if card.rendered:
                last_rendered += 1
            else:
                break
        del self._cards[last_rendered:]
        
        if len(self._cards) > 0:
            self._cards[last_rendered-1].is_visible = unhide_last
        
    def refresh_rendered(self):
        for card in self._cards:
            card.rendered = True
