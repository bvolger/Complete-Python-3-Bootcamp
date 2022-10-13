#!/usr/bin/python3

import random, sys, os

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
            print(f"\nWelcome {self.name}. Your starting balance is {self.balance}")

    def bet(self, **kwargs):
        if 'wager' in kwargs:
            self.amount = kwargs['wager']

            if self.balance >= self.amount:
            #self.balance -= amount
                return self.amount
            else:
                print("Not enough money in account!")
                return None
        else:
            return self.amount


    def winnings(self, amount, won):
        if won == True:
            self.balance += amount
        else:
            self.balance -= amount

    def balance(self):
        return self.balance

    def show_hand(self):
        for card in self.cards:
            print(card)

    def hand_value(self):
        value = 0
        # Keep track of aces
        aces = 0 
        for card in self.cards:
            value += card.value
            if card.rank == 'Ace':
                aces += 1

        # Reduce value for aces (if necessary)
        if value > 21 and aces != 0:
            value -= aces * 10

        return value

    def __str__(self):
        return f"\n{self.name} has {self.balance} left in account"


    def __len__(self):
        return len(self.cards)


def MyFn(t):
    return t[0]


def reset(*args):
    deck = Deck()
    
    for entry in args:
        if type(entry) == dict:
            for name, player in entry.items():
                player.cards = []
        else:
            entry.cards = []

    #for player in players:
        #player.cards = []


def turn(player, cards):

    print(f"\n{player.name}, cards dealt:")
    for i in range(cards):
        dealt_card = deck.deal_card()
        print(f">> {dealt_card} <<")
        player.cards.append(dealt_card)

    return player.hand_value()

# Start playing
if __name__ == "__main__":

    # init the deck
    deck = Deck()

    while True:
        try:
            num_of_players = int(input("How many players are playing? "))
            #test = int(num_of_players)
        except TypeError:
            print("Integer please..")
            continue
        else:
            break

    players = {}
    for i in range(1, num_of_players + 1):
        player_name = input("\nWhat is the name of player %d? " % i)
        #while True:
            #try:
                #money = int(input(f"And how much money did {player_name} bring? "))
            #except TypeError:
                #print("Integer please...")
            #else:
                #break

        players[player_name] = Player(player_name, 100)
        #print(players[player_name])
        
    # Dealer guy
    dealer = Player()
    
    # Game controlling loop
    while True:

        # Round starts with all players setting their bets
        for name,player in sorted(players.items(), key=MyFn):
            print(player)
            # First, set a betting amount
            betting_amount = None
            while betting_amount == None:
                try:
                    betting_amount = int(input(f"How much do you want to wager? (1-{player.balance}) "))
                    betting_amount = player.bet(wager=betting_amount)
                except ValueError:
                    print("Integer please..")
                except KeyboardInterrupt:
                    print("\n\nQuitting")
                    sys.exit(1)

        os.system('clear')

        # Then, two cards to each player, and a card to the dealer
        players_done = False
        for name,player in sorted(players.items(), key=MyFn):
            turn(player, 2)
        turn(dealer, 1)

        # Then, hitting begins
        all_players_done = False
        while all_players_done == False:
            
            for name,player in players.items():
                player_done = False
                
                print(f"\n++++++++++++++++++ {player.name}, it's your turn ++++++++++++++++++")
                while player_done == False:
                    print(f"\n{player.name}, your hand:")
                    player.show_hand()

                    hand_value = player.hand_value()
                    
                    if hand_value >= 21:
                        if hand_value == 21 and len(player) == 2:
                            print(">>>>> BLACKJACK! <<<<<")
                        elif hand_value == 21:
                            print(">>>>> 21! <<<<<")
                        else:
                            print(">>>>> BUST! <<<<<")
                        player_done = True
                        break


                    choice = input((f"\nDo you want to hit or stand? ")).lower()
                    if not choice in ['hit', 'stand']:
                        print("Please enter 'hit' or 'stand'")
                        continue
                    if choice == 'hit':
                        turn(player, 1)
                        #hand_value = turn(player, 1)
                    else:
                        player_done = True
                        break

            all_players_done = True

        # Then, dealers turn
        # Dealers turn
        while dealer.hand_value() < 17:
            turn(dealer, 1)

        # Show final hands
        print('\n=========================================================================\n')
        print("\nFinal hands:")
        for name, player in players.items():
            print(f"\n{name} wagered {player.bet()} and had hand value {player.hand_value()}")
            player.show_hand()

        print(f"\nDealer: {dealer.hand_value()}")
        dealer.show_hand()

        print("\n")
        for name, player in players.items():
            # Blackjack always wins, unless dealer has one too
            if player.hand_value() == 21 and len(player) == 2:
                if dealer.hand_value() == 21 and len(dealer) == 2:
                    # It's a draw
                    print(f"Both {player.name} and Dealer hit blackjack. It's a tie")
                else:
                    print(f"{player.name} had blackjack and wins from Dealer!")
                    player.winnings(player.bet(), True)
            # Player has 21, but dealer has blackjack
            elif player.hand_value() == 21 and len(player) > 2 and dealer.hand_value() == 21 and len(dealer) == 2:
                print(f"Dealer had blackjack, {player.name} did not and loses!")
                player.winnings(player.bet(), False)
            # Player went bust, always lose
            elif player.hand_value() > 21:
                print(f"{player.name} went bust!")
                player.winnings(player.bet(), False)
            elif player.hand_value() == dealer.hand_value():
                print(f"{player.name} and dealer tie!")
                # No money won or lost
            elif player.hand_value() < dealer.hand_value():
                print(f"{player.name} loses from dealer!")
                player.winnings(player.bet(), False)
            else:
                print(f"{player.name} wins from dealer!")
                player.winnings(player.bet(), True)

        broke = False
        for player in players.values():
            print(f"{player}")
            if player.balance <= 0:
                print(f"{player.name} went broke. Game ends!")
                broke = True
            
        if broke == True:
            sys.exit(1)
        while True:
            choice = input("Do you wish to play on? [Y/N] ").lower()
            if not choice in ['y', 'n']:
                print("Y/N please..")
            if choice == 'y':
                reset(players, dealer)
                #reset(dealer)
                os.system('clear')
                break
            else:
                sys.exit(1)
