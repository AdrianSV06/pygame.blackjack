#imports
import pygame
import sys
import random

#pygame setup
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height), vsync=1)
pygame.display.set_caption("Blackjack")
background = pygame.image.load("C:/Users/adria/OneDrive/Python/blackjack/bj_background.png")
background = pygame.transform.scale(background, (1200, 600))

#def functions
class Deck:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.reset_deck()
    
    def reset_deck(self):
        self.cards = {value: 4 * self.num_decks for value in range(1, 14)}  # 4 cards of each value per deck

    def total_cards(self):
        return sum(self.cards.values())
    
    def draw_card(self):
        available_cards = [value for value, count in self.cards.items() if count > 0]
        if not available_cards:
            raise ValueError("No cards left in the deck!")
        
        card = random.choice(available_cards)
        self.cards[card] -= 1       
        return card

    def remaining_cards(self):
        return self.cards

    def __str__(self):
        return f"Deck contains: {self.remaining_cards()}"
    

#variables
font1 = pygame.font.SysFont("Calibri", 60, True)
font2 = pygame.font.SysFont("Calibri", 20, True)
font3 = pygame.font.SysFont("C:/Users/adria/OneDrive/Python/blackjack/October Crow.ttf", 120, True)
font4 = pygame.font.SysFont("C:/Users/adria/OneDrive/Python/blackjack/October Crow.ttf", 110, True)
shuffle_text = font4.render("SHUFFLING DECK", True, (255, 255, 255))
deck = Deck(2)
card = None  
start = True
stand = True
soft = False
double = False
d_soft = False
bj = False
s_bj = False
double_split = False 
player_value = 0
split = False
acc_split_c1 = False
acc_split_c2 = False
card_list = []
dealer_card_list = []
player_balance = 1000
bet = 0
o_bet = 0
bet_choice = False
card_display = {1: "A", 11: "J", 12: "Q", 13: "K"}
#choose bet function
while not bet_choice:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and bet < 500:
                bet += 25
                o_bet += 25
            if event.key == pygame.K_DOWN and bet > 0:
                bet -= 25
                o_bet -= 25
            if event.key == pygame.K_SPACE and bet > 0:
                bet_choice = True
    screen.fill((0, 0, 0))  
    bet_text = font4.render("BET SIZE = " + str(bet) + "$", True, (255, 255, 255))
    info_text = font2.render("USE ARROW KEYS TO ADJUST BET SIZE (25$ - 500$)", True, (255, 255, 255))
    info_text2 = font2.render("PRESS SPACE TO CONFIRM", True, (255, 255, 255))
    screen.blit(bet_text, (50, 100))
    screen.blit(info_text, (50, 500))
    screen.blit(info_text2, (50, 550))
    pygame.display.update()

#render starting text
start_text = font4.render("PRESS SPACE TO START", True, (255, 255, 255))  
screen.blit(start_text, (55, 300))
pygame.display.update()




# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                try: 
                    #conditions for new hand               
                    if player_value > 21 or stand == True:     
                        #calculate payout for no split no bj                  
                        if start == False and split == False and bj == False:   
                            #change bet if double
                            if double == True:
                                bet = bet*2
                            if player_value > 21:
                                player_balance -= bet
                            elif dealer_value > 21:
                                player_balance += bet
                            else:
                                if dealer_value > player_value:
                                    player_balance -= bet
                                if player_value > dealer_value:
                                    player_balance += bet    

                        #ensure correct bet size   
                        bet = o_bet
                        
                        #calculate payout if split and no bj
                        if acc_split_c2 == True and s_bj == False:
                            if double_split == True:
                                bet += bet*2
                            if s_player_value > 21:
                                player_balance -= bet
                            elif dealer_value > 21:
                                player_balance += bet
                            else:
                                if dealer_value > s_player_value:
                                    player_balance -= bet
                                if s_player_value > dealer_value:
                                    player_balance += bet
                        
                        #ensure correct bet
                        bet = o_bet

                        #payout bj no split
                        if bj == True:
                            player_balance += 1.5*bet

                        #checks bj conditions for split
                        if sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list) == 21 and dealer_card_count == 1:
                            s_bj = False                
                        
                        #payout for split bj
                        if s_bj == True:
                            player_balance += 1.5*bet

                        #no decimals
                        bet = int(bet)

                        #start condition
                        start = False

                        #reset veriables and deck if nescesary
                        stand = False
                        bj = False
                        s_bj = False
                        soft = False                     
                        double = False  
                        double_split = False          
                        d_soft = False
                        acc_split_c1 = False
                        acc_split_c2 = False
                        if sum(deck.cards.values()) <= 20:
                            deck = Deck(2) 
                        #stores split value for second split hand 
                        if split == True:
                            s_d_card = dealer_card_list[0]
                            s_player_value = player_value
                        #reset num variables and lists
                        dealer_card_count = 0             
                        card_count = 0
                        card_list = []
                        dealer_card_list = []
                        #draws dealer card
                        d_card = deck.draw_card()
                        dealer_card_list.insert(0,d_card)
                        #checks if dealer soft
                        if 1 in dealer_card_list and sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list) < 22:
                            d_soft = True   
                        #calculates dealer sum           
                        dealer_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list)                  
                        #draws first player card
                        if split == False:
                            card = deck.draw_card()
                            card_list.insert(card_count,card) 
                        #protocol for second split hand  
                        if split == True:
                            acc_split_c2 = True
                            card_list.insert(card_count,s_card)
                            split = False  
                            dealer_card_list = []
                            dealer_card_list.insert(0,s_d_card)   
                            dealer_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list) 

                    
                    #draws next player card                  
                    card_count += 1   
                    card = deck.draw_card()  
                    card_list.insert(card_count,card)

                    #create temporary list, and checks split acces
                    temp_list = [10 if x in (11, 12, 13) else x for x in card_list]
                    if len(card_list) < 3 and temp_list[0] == temp_list[1]:
                        acc_split_c1 = True

                    #ensures if already split, deactivate split acces
                    if acc_split_c2 == True:
                        acc_split_c1 = False

                    
                    #checks if player soft
                    if 1 in card_list and sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in card_list) < 22:
                        soft = True
                    #calculates player value
                    player_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in card_list)
                    #checks if player over 21 and soft, if so, gives new value with ace = 1
                    if player_value > 21:
                        sum(10 if num in [11, 12, 13] else num for num in card_list)
                    
                    #bj function
                    if card_count == 1 and player_value == 21:
                        stand = True
                        d_card = deck.draw_card()
                        dealer_card_count += 1
                        dealer_card_list.insert(dealer_card_count, d_card)
                        bj = True
                        if sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list) == 21:
                            bj = False
                            
                    
                
                #if deck empty
                except ValueError:
                    card = "No Cards"  

            #stand function                  
            if event.key == pygame.K_f and not stand:
                stand = True
                if split == True:
                    break
                #dealer draws untill 17 or higher                   
                while dealer_value < 17:                         
                    dealer_card_count += 1                   
                    d_card = deck.draw_card()
                    dealer_card_list.insert(dealer_card_count, d_card)
                    if 1 in dealer_card_list:
                        d_soft = True 
                    dealer_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list)
                    #checks if dealer over 21 and soft, if so, gives new value with ace = 1
                    if dealer_value > 21 and d_soft == True:
                        d_soft = False
                        dealer_value = sum(10 if num in [11, 12, 13] else num for num in dealer_card_list)

            #split function
            if event.key == pygame.K_s and acc_split_c1 == True and stand == False and split == False and acc_split_c2 == False:
                acc_split_c2 = False
                split = True
                s_card = card_list[1]
                card_list.pop(1)
                card = deck.draw_card()
                card_list.insert(card_count, card)
                player_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in card_list)
                if player_value == 21:
                    s_bj = True

            #double function
            if event.key == pygame.K_d and card_count == 1:
                if split == True:
                    double_split = True
                double = True
                card_count += 1
                card = deck.draw_card()
                card_list.insert(card_count,card)  
                player_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in card_list)
                if sum(10 if num in [11, 12, 13] else num for num in card_list) < 22:                  
                    stand = True

                    #saves dealer draw to next split hand
                    if split == True:
                        break
                    #dealer draws untill 17 or higher                   
                    while dealer_value < 17:                      
                        if 1 in dealer_card_list:
                            d_soft = True   
                        dealer_card_count += 1                   
                        d_card = deck.draw_card()
                        dealer_card_list.insert(dealer_card_count, d_card)
                        dealer_value = sum(10 if num in [11, 12, 13] else 11 if num == 1 else num for num in dealer_card_list)
                        #checks if dealer over 21 and soft, if so, gives new value with ace = 1
                        if dealer_value > 21 and d_soft == True:
                            d_soft = False
                            dealer_value = sum(10 if num in [11, 12, 13] else num for num in dealer_card_list)


            #reset deck
            if event.key == pygame.K_BACKSPACE:
                deck = Deck(2)
                card = None  
                card_list = []
                card_count = 0
                player_value = 22  
                start = True
                screen.blit(shuffle_text, (150, 200))
                

    #graphics
    if start == False:
        screen.blit(background, (0, 0))
        if player_balance < 0:
            screen.fill("darkred")
       
        #player cards
        for i in range(card_count+1):   
                place = 700 - 100 * i
                display_value = card_display.get(card_list[i], card_list[i])
                card_text = font1.render(str(display_value), True, (255, 255, 255))
                screen.blit(card_text, (place, 500)) 

        #dealer cards
        for i in range(dealer_card_count+1):   
                d_place = 700 - 100 * i
                d_display_value = card_display.get(dealer_card_list[i], dealer_card_list[i])
                dealer_text = font1.render(str(d_display_value), True, (255, 255, 255))
                screen.blit(dealer_text, (d_place, 300))  
              
        deck_text = font2.render(str(deck), True, (255, 255, 255))  
        screen.blit(deck_text, (10, 20)) 

        cardsleft_text = font2.render(str(sum(deck.cards.values())), True, (255, 255, 255))
        screen.blit(cardsleft_text, (900, 20))
       
        value_text = font1.render(str(player_value) + ("S" if soft else ""), True, (255, 255, 255))
        screen.blit(value_text, (500, 400))

        d_value_text = font1.render(str(dealer_value) + ("S" if d_soft else ""), True, (255, 255, 255))
        screen.blit(d_value_text, (500, 200))

        balance_text = font1.render(str(player_balance) + "$", True, (0, 0, 0))
        screen.blit(balance_text,(900,500))

        #soft conditions, used to ensure no buggy graphics, other soft condition ensure correct logic
        if player_value > 21:
            soft = False
            player_value = sum(10 if num in [11, 12, 13] else num for num in card_list)

        #player bust
        if soft == False and player_value > 21:
            busted_text = font3.render("BUSTED", True, (255, 0, 0))  
            screen.blit(busted_text, (380, 100))  
        #dealer bust 
        if d_soft == False and dealer_value > 21:
            busted_text = font3.render("DEALER BUSTED", True, (255, 0, 0))  
            screen.blit(busted_text, (180, 100))  
   
    pygame.display.flip()
