import pygame
import sys
import random

pygame.init()

width, height = 1200, 600
screen = pygame.display.set_mode((width, height), vsync=1)
pygame.display.set_caption("Blackjack")
background = pygame.image.load("C:/Users/adria/OneDrive/Python/blackjack/bj_background.png")
background = pygame.transform.scale(background, (1200, 600))

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

font1 = pygame.font.SysFont("Calibri", 60, True)
font2 = pygame.font.SysFont("Calibri", 20, True)
font3 = pygame.font.SysFont("C:/Users/adria/OneDrive/Python/blackjack/October Crow.ttf", 120, True)
font4 = pygame.font.SysFont("C:/Users/adria/OneDrive/Python/blackjack/October Crow.ttf", 110, True)
deck = Deck(2)
card = None  
start = True
player_value = 22
card_list = []
dealer_card_list = []
dealer_card_count = 0
card_display = {11: "J", 12: "Q", 13: "K"}
start_text = font4.render("PRESS SPACE TO START", True, (255, 255, 255))  
shuffle_text = font4.render("SHUFFLING DECK", True, (255, 255, 255))
screen.blit(start_text, (55, 300))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                try:
                    start = False 
                    if player_value > 21:  
                        if sum(deck.cards.values()) <= 10:
                            deck = Deck(2)               
                        card_count = 0
                        card_list = []
                        dealer_card_list = []
                        d_card = deck.draw_card()
                        dealer_card_list.insert(0,d_card)
                        player_value = sum(10 if num in [11, 12, 13] else num for num in card_list)
                        card = deck.draw_card()
                        card_list.insert(card_count,card)
                        print(f"Drew card: {card}")


                    card_count += 1   
                    card = deck.draw_card()  
                    card_list.insert(card_count,card)
                    print(f"Drew card: {card}")
                    print(deck)
                    player_value = sum(10 if num in [11, 12, 13] else num for num in card_list)
                    
                    
                    
                    
                  
                 

                except ValueError:
                    card = "No Cards"
            if event.key == pygame.K_BACKSPACE:
                deck = Deck(2)
                card = None  
                card_list = []
                card_count = 0
                player_value = 22  
                start = True
                screen.blit(shuffle_text, (55, 200))
                

    
    if start == False:
        screen.blit(background, (0, 0))
       
        if card_count > 0:
            for i in range(card_count+1):   
                    place = 700 - 100 * i
                    display_value = card_display.get(card_list[i], card_list[i])
                    card_text = font1.render(str(display_value), True, (255, 255, 255))
                    screen.blit(card_text, (place, 500)) 

            for i in range(dealer_card_count+1):   
                    d_place = 700 - 100 * i
                    d_display_value = card_display.get(dealer_card_list[i], dealer_card_list[i])
                    dealer_text = font1.render(str(d_display_value), True, (255, 255, 255))
                    screen.blit(dealer_text, (d_place, 300))    

        deck_text = font2.render(str(deck), True, (255, 255, 255))  
        screen.blit(deck_text, (10, 20)) 

        cardsleft_text = font2.render(str(sum(deck.cards.values())), True, (255, 255, 255))
        screen.blit(cardsleft_text, (900, 20))
       

        value_text = font1.render(str(player_value), True, (255, 255, 255))  
        screen.blit(value_text, (500, 400)) 
        if player_value > 21:
            busted_text = font3.render("BUSTED", True, (255, 0, 0))  
            screen.blit(busted_text, (380, 150))  





    
    pygame.display.flip()
