from cards import Deck, Card
from board import Card_Collumn, Board

def testBoard():
    b = Board(20, 50)
    b.show_board()
    col1 = int(input("C1:"))
    col2 = int(input("C2:"))
    h = int(input("H:"))

    if b.move_cards(col1,col2,h):
        b.show_board()

def testCardCol():
    deck = Deck()
    deck.shuffleDeck()
    cards = deck.drawCards(8)
    col1 = Card_Collumn(cards)
    print(col1)
    n = int(input('Number:'))
    print(col1.take_cards(n))
    print(col1)


def main():
    # testCardCol()
    testBoard()


    

if __name__ == "__main__":
    main()