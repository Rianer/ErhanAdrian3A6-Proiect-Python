import pygame as pg
from cards import Game_Card
from board import Board
#cards size 89x120 
#colors
TABLE_COLOR = (52, 162, 73)

#display
WIDTH, HEIGHT = 1200, 700
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Solitaire')

#settings
FPS = 60


#game objects
card1 = Game_Card(10,1)
game_board = Board(70, 250)

def draw_board():
    for column in game_board._board:
        for card in column._cards:
            if card.is_visible == True:
                WIN.blit(card.texture, card.position)
            else:
                WIN.blit(card.card_back, card.position)

def draw_window():
    WIN.fill(TABLE_COLOR)
    # WIN.blit(card1.card_back, card1.position)
    # WIN.blit(card1.card_back, (0,10))
    # WIN.blit(card1.texture, (0,20))
    draw_board()
    pg.display.update()

def main():
    clock = pg.time.Clock()
    game_board.show_board()
    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        draw_window()


    pg.quit()

if __name__ == "__main__":
    main()