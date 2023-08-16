import random
from enum import Enum
import numpy as np

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
        self.game_iteration = 0
        self.run_reward = 0
        
        
        
        
    def deal_cards(self):
        first_card = random.choice(self.deck)
        self.deck.remove(first_card)
        second_card = random.choice(self.deck)
        self.deck.remove(second_card)
        
        return ([first_card, second_card])
    
    def play_step(self,action):
        game_over = False
        round_over = False
        self.game_iteration += 1
        
        if self.game_iteration == 100:
            game_over = True
            reward_save = self.run_reward
            self.reset()
            print("HMMMMMMMMMMMMMMMM")
            return self.reward, True, reward_save
        
        print("Player Cards:", self.player_cards)
        print("Dealer Cards: ", self.dealer_cards)
        
        #define_rounds
        if self.player_cards == ['A',10] or self.player_cards == [10,'A']:
            round_over = True
            self.reward = 10
            print("blackjack")
            #return reward, round_over,self.score
        
        if self.dealer_cards == ['A',10] or self.dealer_cards == [10,'A']:
            round_over = True
            self.reward = -10
            print("dealer blackjack")
            #return reward, round_over,self.score
        
        #while round_over == False:
        self._move(action)
        print("Action: ", action)
        print("New Hand: ", self.player_cards)
        
        if self.player_card_sum() > 21:
                self.reward = -20
                round_over = True
                print("player bust")
                
        if self.player_card_sum() == 21:
                self.reward = +20
                round_over = True
                print("player 21")
                
        if self.player_card_sum() < 21:
                self.reward = +2
                round_over = False
                
        if action == [0,1]:
                self.dealer_AI()
                
                if self.dealer_card_sum()>21:
                    self.reward = +10
                    round_over = True
                    print("dealer bust")
                    #self.reset()
                    #return reward, game_over,self.score
                
                elif self.player_card_sum() > self.dealer_card_sum():
                    self.reward = +10
                    round_over= True
                    print("player win")
                else:
                    print("Player lose")
                    self.reward = -10
                    round_over= True
            
                    
                    
                
        if round_over == True:
            self.deck = []
            for i in range(self.number_of_decks):
                self.deck = self.deck + self.card_list[:]
        
            self.player_cards = self.deal_cards()
            self.dealer_cards = self.deal_cards()
        
        
        
        #self.play_step(action)
        self.run_reward +=self.reward
        return self.reward, False,self.run_reward
    
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
        if action == [1,0]:#Actions.HIT:
            added_card = random.choice(self.deck)
            self.deck.remove(added_card)
            self.player_cards = self.player_cards + [added_card]
        
