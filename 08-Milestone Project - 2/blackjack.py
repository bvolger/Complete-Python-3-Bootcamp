#!/usr/bin/python3

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.suit} {self.rank}"


class Deck():
    
    def __init__(self):
        self.deck = []
        for color in suits:
            for rank in ranks:
                self.deck.append(Card(color, rank))

        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __len__(self):
        return len(self.deck)

class Player():

    def __init__(self, name='Dealer', balance='inf'):
        self.name = name
        self.balance = balance
        self.cards = []
        if self.name != 'Dealer':
            print(f"Welcome {self.name}. Your starting balance is {self.balance}")

    def bet(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Not enough money in account!")

    def winnings(self, amount):
        self.balance += amount

    def balance(self):
        return self.balance

    def show_hand(self):
        for card in self.cards:
            print(card)

    def __str__(self):
        return f"{self.name} has {self.balance} left in account"

def check_hand(player):
    aces = 0
    hand_value = 0

    for card in player.cards:
        hand_value += card.value
        if card.rank == 'Ace':
            aces += 1

    if hand_value == 21:
        return 21
    elif hand_value > 21 and aces != 0:
        hand_value -= 10*aces
        #return hand_value
    
    if hand_value > 21:
        return 'Bust'
    else:
        return hand_value

def reset(*players):
    deck = Deck()
    for player in players:
        player.cards = []


def turn(player, cards):
    
    for i in range(cards):
        player.cards.append(deck.deal_card())
    
    print(f"\n{player.name} got:")
    player.show_hand()
    hand_worth = check_hand(player)
    print(f"Worth of hand: {hand_worth}")
    return hand_worth

def play_rotation(**players):

    # First, set a betting amount
    while True:
        try:
            betting_amount = int(input(f"How much do you want to wager? (1-{player.balance}) "))
        except:
            print("Integer please..")
        else:
            player.bet(betting_amount)
            break

    player_done = False
    # Game begins
    while player_done == False:
        # Always start with two cards to the player, and one card to the dealer
        player_value = turn(player, 2)
        dealer_value = turn(dealer, 1)
        
        # Then, players turn
        while True:
            if player_value == 21 or player_value == 'Bust':
                player_done = True
                break
            choice = input((f"\n{player.name}, it's your turn. Do you want to hit or stand? ")).lower()
            if not choice in ['hit', 'stand']:
                print("Please enter 'hit' or 'stand'")
                continue

            if choice == 'hit':
                player_value = turn(player, 1)
            else:
                player_done = False
                break

    # Dealers turn
    while True:
    #while dealer_value < 17 and dealer_value != 'Bust':
        dealer_value = turn(dealer, 1)
        if dealer_value == 'Bust':
            break
        elif dealer_value >= 17:
            break
        else:
            continue
    #break

    if dealer_value == 'Bust':
        print(f"Dealer went bust. {player.name} wins!")
        player.winnings(betting_amount*2)
    elif player_value == 'Bust':
        print(f"{player.name} went bust")
    elif player_value > dealer_value:
        print(f"{player.name} wins!")
        player.winnings(betting_amount*2)
    elif player_value < dealer_value:
        print(f"Dealer wins!")
    elif player_value == dealer_value:
        print(f"It's a draw..")
        player.winnings(betting_amount)


# Start playing
if __name__ == "__main__":

    # init the deck
    deck = Deck()

    """
    # Ask for player name, and the amount of betting money
    name = input("What's your name? ")
    while True:
        try:
            money = int(input("How much money did you bring? "))
        except:
            print("Please provide an integer..")
        else:
            break

    player = Player(name, money)
    """
    player = Player('Bram', 100)
    dealer = Player()

    while True:
        play_rotation()
        print("\n")
        print(player)

        choice = input(f"Do you wish to play on? [Y/N] ").lower()
        if not choice in ['y', 'n']:
            print("Y/N please..")
            
        if choice == 'y':
            reset(player, dealer)
            continue
        else:
            break
    