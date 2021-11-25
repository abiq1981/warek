#Created on Tue Nov 16 22:33:07 2021

#@author: antoinebiquillon
# War card game as player by the Areks

import random
import collections

# Deck class initiates a shuffled deck for a War card game.
class Deck:
    def __init__(self, ranks: object, colors: object) -> object:
        self.ranks = ranks
        self.colors = colors
        self.cards = [i for i in range(self.ranks) for t in range(self.colors)]
        random.shuffle(self.cards)

# Player is either a cheater like Marek (sorts cards) or a normal player.
class Player:
    def __init__(self, name, is_sorting):
        self.is_sorting = is_sorting
        self.hand = []
        self.name = name

# Warek represents a game of War as played by Areks
class Warek:
    def __init__(self, deck, players):
        self.deck = deck
        self.players = players
        self.losers = []

    def deal(self):
        i = 0 # not very pythonic, sorry
        for card in self.deck.cards:
            self.players[i].hand.append(card)
            i = (i + 1) % (len(self.players))
          
    def turn(self):
        active_cards = {} #cards in play against other during a turn
        war_cards = [] # cards that needs to be replaced by the player in order to settle war
        stash_cards = [] # cards to be given to the winner
        
        # print the cards of player still in the game
        #for player in self.players:
        #  print(player.hand)  
        # 
        for player in self.players:
            try:
                active_cards[player] = player.hand.pop()
            except IndexError:
                 self.losers.append(player)
                 self.players.remove(player)       
        #print(active_cards.values())
        war_cards = [item for item, count in collections.Counter(list(active_cards.values())).items() if count > 1]
        
        while len(war_cards) > 0:
            #print("WAR")
            for player, card in active_cards.copy().items():
                if active_cards[player] in war_cards:
                    stash_cards.append(card)
                    try:
                        #retourne une carte
                        stash_cards.append(player.hand.pop())
                    except IndexError:
                        self.losers.append(player)
                        self.players.remove(player)
                        stash_cards.append(active_cards[player])
                        active_cards.pop(player)
                        continue
                    try:    
                        #joue une nouvelle carte
                        active_cards[player] = player.hand.pop()
                    except IndexError:
                        self.losers.append(player)
                        self.players.remove(player)
                        active_cards.pop(player)
            #print(active_cards.values())
            war_cards = [item for item, count in collections.Counter(list(active_cards.values())).items() if count > 1]
        winner = max(active_cards, key=active_cards.get)
        for player, card in active_cards.items():
            stash_cards.append(card)
        active_cards.clear()
        if winner.is_sorting:
            stash_cards.sort()
        else:
            random.shuffle(stash_cards)
        for card in stash_cards:
            winner.hand.insert(0, card)
        
    def run(self):
        while len(self.players)>1:
            try: 
                self.turn()
                #input("Press Enter to continue...")
            except ValueError:
                break
        return self.players[0].name
        
M = Player("Marek", True)
R = Player("Romain", False)
A = Player("Antoine", False)
T = Player("Tarik", False)
results = []

for i in range(1000):

    D = Deck(13,4)
    W = Warek(D,[M, R, A, T])
    W.deal()
    #input("Press Enter to continue...")
    WINNER = W.run()
    print(WINNER)