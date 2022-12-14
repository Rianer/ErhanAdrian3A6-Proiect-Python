import pygame as pg
from cards import Game_Card
from board import Board
from os import path
#cards size 89x120 
#colors
TABLE_COLOR = (52, 162, 73)
RED_COLOR = (255, 20, 0)

#other constants
GAME_WON = pg.image.load(path.join('Assets\Textures', 'GAME_WON.png'))

#display
WIDTH, HEIGHT = 1200, 700
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Solitaire')

#settings
FPS = 60


#game objects
card1 = Game_Card(10,1)
game_board = Board(70, 250)

#game states


def draw_card(card):
    if card.is_visible and card.rendered:
        WIN.blit(card.texture, card.position)
    elif card.rendered:
        WIN.blit(card.card_back, card.position)
    else:
        print('Card {} is not rendered'.format(card))


def draw_cards_in_hand():
    if not game_board.cards_in_hand:
        return
    mouse_relative_pos = list(pg.mouse.get_pos())
    mouse_relative_pos[0] -= 40
    mouse_relative_pos[1] -= 10
    game_board.moving_cards.change_position(tuple(mouse_relative_pos))
    # print(game_board.moving_cards)
    for card in game_board.moving_cards._cards:
        draw_card(card)

def draw_card_slots():
    for slot in game_board.slots:
        WIN.blit(slot.texture, slot.position)
        card = slot.get_top_card()
        if card != None:
            WIN.blit(card.texture, slot.position)

def draw_deck_section():
    WIN.blit(game_board._deck.deck_base.texture, game_board._deck.deck_position)
    WIN.blit(game_board._deck.buffer_base.texture, game_board._deck.buffer_position)
    deck_top = game_board._deck.get_deck_top()
    if deck_top != None:
        # WIN.blit(deck_top.texture, game_board._deck.deck_position)
        draw_card(deck_top)
    buffer_top = game_board._deck.get_buffer_top()
    if buffer_top != None:
        # WIN.blit(buffer_top.texture, game_board._deck.buffer_position)
        draw_card(buffer_top)

def draw_board():
    draw_deck_section()
    draw_card_slots()
    for column in game_board._board:
        for card in column._cards:
            draw_card(card)

def draw_window():
    WIN.fill(TABLE_COLOR)
    if not game_board.game_won:
        draw_board()
        draw_cards_in_hand()
    else:
        WIN.blit(GAME_WON, (0, 0))
    pg.display.update()

def main():
    
    clock = pg.time.Clock()
    print("----NEW GAME----")
    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_presses = pg.mouse.get_pressed()
                if mouse_presses[0]:
                    if game_board.handle_mouse_click(pg.mouse.get_pos()):
                        pass
        draw_window()


    pg.quit()

if __name__ == "__main__":
    main()