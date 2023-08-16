import random
from enum import Enum
import numpy as np
import pygame

class Actions(Enum):
    HIT = 1
    STAY = 2
    
    
class BlackJackAI:
    def __init__(self):
        self.number_of_decks = 8
        self.card_list = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 
                 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 
                 10, 10, 10, 10, 10, 10, 10, 'A', 'A', 'A', 'A']
        self.player_cards = []
        self.score = 0
        self.reset()
    
    def reset(self):
        self.deck = []
        for i in range(self.number_of_decks):
            self.deck = self.deck + self.card_list[:]
        
        self.player_cards = self.deal_cards()
        self.dealer_cards = self.deal_cards()
        print(self.player_cards)
        print(self.dealer_cards)
        
        self.game_iteration = 0
        
    def deal_cards(self):
        first_card = random.choice(self.deck)
        self.deck.remove(first_card)
        second_card = random.choice(self.deck)
        self.deck.remove(second_card)
        
        return ([first_card, second_card])
    
    def play_step(self):
        game_over = False
        reward = 0
        round_over = False
        self.game_iteration += 1
        if self.game_iteration == 100:
            game_over = True
            return game_over
        #define_rounds
        if self.player_cards == ['A',10] or self.player_cards == [10,'A']:
            round_over = True
            reward = 10
            #return reward, round_over,self.score
        
        if self.dealer_cards == ['A',10] or self.dealer_cards == [10,'A']:
            round_over = True
            reward = -10
            #return reward, round_over,self.score
        
        while round_over == False:
            actionz = input("Hit for hit Stay for stay: ")
            if actionz == 'Hit':
                action = 'HIT'#Actions.HIT
            else:
                action = 'STAY'#Actions.STAY
            self._move(action)
            print(self.player_cards)
        
            if self.player_card_sum() > 21:
                print("called rover")
                reward = -20
                round_over = True
                print("OVER!")
                
            if self.player_card_sum() == 21:
                print("called rover")
                reward = +20
                round_over = True
                print("21!!!!")
                
            if action == 'STAY':
                self.dealer_AI()
                
                print(self.player_cards)
                print(self.dealer_cards)
                
                if self.dealer_card_sum()>21:
                    print("dealer bust")
                    reward = +10
                    round_over = True
                    self.reset()
                    return reward, game_over,self.score
                
                if self.player_card_sum() > self.dealer_card_sum():
                    print("BEAT DEALER!")
                    reward = +10
                    round_over= True
                else:
                    print("DEALER WINS!")
                    reward = -10
                    round_over= True
                
        if round_over == True:
            self.reset()
        
        return reward, game_over,self.score
    
    def dealer_AI(self):
        while self.dealer_card_sum()<17:
            added_card = random.choice(self.deck)
            self.deck.remove(added_card)
            self.dealer_cards = self.dealer_cards + [added_card]
            
    
    def player_card_sum(self):
        player_sum = 0
        ace_count = 0
        if 'A' not in self.player_cards:
            return sum(self.player_cards)
        else:
            copy_player_cards = self.player_cards[:]
            for x in copy_player_cards:
                if x == 'A':
                    ace_count +=1
                    x = 11
                player_sum +=x
            while player_sum > 21 and ace_count>0:
                player_sum -=10
                ace_count -=1
                """player_sum = 0
                copy_player_cards = self.player_cards[:]
                for x in copy_player_cards:
                    if x == 'A':
                        x = 1
                    player_sum +=x"""
        print(player_sum)
        return player_sum
    
    def dealer_card_sum(self):
        dealer_sum = 0
        ace_count = 0
        if 'A' not in self.dealer_cards:
            return sum(self.dealer_cards)
        else:
            copy_dealer_cards = self.dealer_cards[:]
            for x in copy_dealer_cards:
                if x == 'A':
                    x = 11
                dealer_sum +=x
            while dealer_sum > 21 and ace_count>0:
                dealer_sum -=10
                ace_count -=1
        return dealer_sum
    
    def _move(self, action):
        if action == 'HIT':#Actions.HIT:
            added_card = random.choice(self.deck)
            self.deck.remove(added_card)
            self.player_cards = self.player_cards + [added_card]
        
        
if __name__ == '__main__':
    game = BlackJackAI()
    
    # game loop
    while True:
        reward,game_over, score = game.play_step()
        
        if game_over == True:
            break