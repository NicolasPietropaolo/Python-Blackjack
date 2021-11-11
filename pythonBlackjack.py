
# Python Blackjack

from random import sample   # imports only sample function from random library 
from time import sleep      # imports sleep function from time library; input is number of seconds to pause program for

# possible values for value: 2,3,4,5,6,7,8,9,T,J,Q,K,A 
# possible values for suit: "C" = clubs♣, "D" = diamonds♦, "H" = hearts♥, "S" = spades♠

class Card:
    def __init__(self,value,suit):
        if value == 'T':            # check if the value is T so value can be changed to the number 10
            self.value = "10"
        else:
            self.value = str(value) # Convert the given value into a string
        suit_dict = {'C': 1, 'D': 2, 'H': 3, 'S': 4}    # dictionary maps a given suit to a number that can be used as a list index
        self.suit = '♣♦♥♠'[suit_dict[str(suit)]-1]      # 1,2,3,4 = ♣♦♥♠; indexing the string: ♣ = index 1, ♦ = index 2, etc...

    def card_front(self):     # returns a list of strings that represents the "front" of card, with suit and proper value
        return[                             
                '┌───────┐',                
                f'| {self.value:<2}    |', 
                '|       |',
                f'|   {self.suit}   |',
                '|       |',
                f'|    {self.value:>2} |',
                '└───────┘'
                ]
    def card_back(self):    # returns list of strings for the "back" of the card so dealers cards are hidden
        #creates back of card as a list of strings, used mainly for dealer
        return[
                '┌───────┐',
                '│░░░░░░░│', 
                '│░░░░░░░│',
                '│░░░░░░░│',
                '│░░░░░░░│',
                '│░░░░░░░│',
                '└───────┘'
                ]
    def get_value(self):      # checks numerical value of a card, according to blackjack rules
        """Returns the card's numerical value"""    
        if self.value in ['T', 'J', 'Q', 'K']:      
            card_value = 10
        elif self.value == "A":    # aces in blackjack have two possible values 
            card_value = [1,11]    # So ace returns a list of two values instead of a single value
        else:
            card_value = int(self.value)
        return card_value

def create_deck():
    
    """ Generates a full deck of 52 cards using the Card class. The deck is
    returned as a list of Card objects and is shuffled."""
    
    suits = ["C", "D", "H", "S"]
    values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    deck = []    # define empty list for the deck
    for suit in suits:
        for value in values:
            myCard = Card(value, suit)
            deck.append(myCard)   # add new card to  deck
    deck = sample(deck,52)   # shuffle the deck
    return deck         # return the deck

def start_of_game_deal(deck):
   
    """Used at the start of a game to deal player and dealer two cards each"""
    #define lists for player and dealer
    dealer_hand = []
    player_hand = []
   
    # deal two cards to both the player and dealer
    for i in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
    return player_hand, dealer_hand

def check_hand_value(hand):
    
    # checks numerical value of cards in the given hand
    
    hand_value = 0
    num_aces = 0
    # sum up all non-Ace card values 
    for card in hand:
        card_value = card.get_value()# get the card's value 
        if type(card_value) == list: # isolate ace cards as only Aces return a list for their value
            card_value = 0 # set the Ace card's value to 0
            num_aces=num_aces+1  # increment Aces by one
        hand_value += card_value # add the value of the card to the hand
        
    # check if value of an Ace should be 1 or 11 in the given hand
    if num_aces == 0 :    # check if an ace is in the hand
        return hand_value
    elif (hand_value+11) > 21: # if counting the first ace as 11 and all other aces as 1 puts the hand value over 21 
        hand_value += 1*(num_aces) # Add the value of the aces to the hand, in this case they all have a value of 1
        return hand_value
    elif (hand_value+11+(1*(num_aces-1))) > 21: #changes all ace values to 1 if hand surpasses 21 when hand has multiple aces and other card values
        hand_value+= 1*(num_aces)
    else:        # runs if first ace has a value of 11 and the rest of the aces have a value of 1 without going over 21
        hand_value += 11 + 1*(num_aces-1) # Add value of the aces to the hand, first ace counts as 11 and the rest are 1
        return hand_value

def show_hand_unhidden_cards(hand):
    
    """Prints the cards for the given hand to the shell, with no hidden cards."""
    
    hand_graphics_unhidden = []
    
    # create a list of lists of strings, containing all card graphics that need to be printed
    for card in hand:
        hand_graphics_unhidden.append(card.card_front())   # append to list of card graphics
        
    # Each card has seven lines to print
    for i in range(7):
        card_str = ""           # initialize empty string to add card graphics to
        for j in range(len(hand)):    # runs for the number of cards in hand
            card_str += hand_graphics_unhidden[j][i] + " " 
        print(card_str)         # prints all cards in the hand
        
def show_hand_hidden_cards(hand):
    
    """Prints the cards for the given hand to the shell, with all cards except the first hidden."""
    
    hand_graphics_hidden = [hand[0].card_front()] # first value list is the list of strings for the front of the first card
    for i in range(1, len(hand)):           # skips first card in the hand and covers the rest of the cards
        hand_graphics_hidden.append(hand[i].card_back())     # Add the back of the cards to list 
        
    # each card has 7 lines to print
    for i in range(7):
        card_str = ""    # initialize empty string to add card graphics to
        for j in range(len(hand)): # runs for number of cards in the hand
            card_str += hand_graphics_hidden[j][i] + " " 
        print(card_str)


def hit(deck, hand):
    """Allows a player to hit and draw one more card"""
    
    # Add a card from the deck to the hand
    hand.append(deck[-1])
    deck.pop()                 
    
    return hand

def dealer_turn(deck, hand):
    dealer_stands_on = 17   # defines minimum value the dealer's hand must reach before it is allowed to stop drawing cards
    print("Now it's the dealer's turn! The dealer stands on %s." % dealer_stands_on )
    print("Dealer's hand:")
    show_hand_hidden_cards(hand) # show the dealer's unhidden hand 
    while  check_hand_value(hand) < 17 : # Keep looping for as long as the value of the hand is less than what the dealer stands on
        print("The dealer draws a card.")
        hit (deck, hand)# add a card to the hand using hit function
        show_hand_unhidden_cards(hand)   # Show the unhidden hand of the dealer
        sleep(2)  # pause to allow the player to process what the dealer draws
    if check_hand_value(hand) > 21: # check if the dealer's hand has a value over 21 which means they bust (lose)
        print("The dealer busts!")
        return 0
    else:        # the dealer hit between 17 and 21
        print("The dealer is finished drawing cards.")
        print("Dealer's final hand:")
        show_hand_unhidden_cards(hand) # show the unhidden hand of the dealer
        sleep(2)    # pause 
        return check_hand_value(hand) # return final value of the hand


# start of Game Loop 
def game_loop():
    player_chips = 500
    print("Welcome to Python Blackjack! You start with %s chips." % (player_chips))
    print("The dealer's hand is shown first, followed by your hand.")
    while player_chips > 0:
        print("New hand!")
        print("You currently have %s chips." % player_chips)
        bet = int(input("What is your initial bet? "))
        while bet > player_chips or bet < 0:
            bet = int(input("That was an invalid bet. Make sure you aren't betting more than you have! Please enter a bet: "))
        deck = create_deck()
        player_hand, dealer_hand = start_of_game_deal(deck)
        print("Dealer's hand:")
        show_hand_hidden_cards(dealer_hand)
        print("Player's hand:")
        show_hand_unhidden_cards(player_hand)
        player_answer = "N/A"
        if check_hand_value(player_hand) == 21:
            print("You had a natural 21! Let's see what the dealer had:")
            show_hand_unhidden_cards(dealer_hand)
            sleep(2.5)
            if check_hand_value(dealer_hand) == 21:
                print("The dealer also had 21, so you tie. End of hand.")
            else:
                print("You win! Since you had a natural 21, you get your 1.5 times your bet back. Nice!")
                player_chips += int(bet*1.5)
        else: 
            player_turn = True
            while player_turn:
                print("The current value of the cards in your hand is %s. What would you like to do?"% (check_hand_value(player_hand)))
                player_answer = input("Type hit, stand, double down. Enter something else to quit the game: " )
                if player_answer == "hit":
                    player_hand = hit(deck, player_hand)
                    print("Dealer's hand:")
                    show_hand_hidden_cards(dealer_hand)
                    print("Player's hand:")
                    show_hand_unhidden_cards(player_hand)
                    if check_hand_value(player_hand) > 21:
                        player_turn = False
                elif player_answer == "double down":
                    hit(deck, player_hand)
                    print("Dealer's hand:")
                    show_hand_hidden_cards(dealer_hand)
                    print("Player's hand:")
                    show_hand_unhidden_cards(player_hand)
                    player_turn = False
                elif player_answer == "stand":
                    player_turn = False
                else:
                    print("GAME OVER")
                    print("You finished with %s chips." % player_chips)
                    player_turn = False
                    return None
            player_final_value = check_hand_value(player_hand)
            if player_final_value > 21:
                print("Dealer's final hand:")
                show_hand_unhidden_cards(dealer_hand)
                print("Player's final hand:")
                show_hand_unhidden_cards(player_hand)
                if player_answer == "double down": #increses bet by a factor of 2
                    bet = 2*bet
                    print("Oh no! You drew too many cards and busted. You lose this hand and %s chips." % bet)
                    player_chips -= bet
                else:
                    print("Oh no! You drew too many cards and busted. You lose this hand and %s chips." % bet)
                    player_chips -= bet
            else:
                dealer_final_value = dealer_turn(deck, dealer_hand)
                print("Player's final hand:")
                show_hand_unhidden_cards(player_hand)
                if dealer_final_value > 21:
                    print("The dealer busted. You win this hand! You received %s chips." % bet)
                    player_chips += bet
                else:
                   if player_final_value > dealer_final_value:
                       if player_answer == "double down": #increses bet by a factor of 2
                           bet = bet*2
                           print("You won this hand! Since you doubled down, you received %s chips." % bet)
                           player_chips += bet
                       else:
                           print("You won this hand! You received %s chips." % bet)
                           player_chips += int(bet)
                   elif player_final_value == dealer_final_value:
                       print("You tied with the dealer. You don't gain or lose any chips.")
                   else:
                       if player_answer == "double down": #increses bet by a factor of 2
                           bet = bet*2
                           print("The dealer had the better hand, you lose this hand and %s chips." % bet)
                           player_chips -= bet
                       else:
                           print("The dealer had the better hand, you lose this hand and %s chips." % bet)
                           player_chips -= bet
        if player_chips <= 0:     #no more chips player loses              
            print("You ran out of chips! Game over.")
        sleep(2.5)           
# end of Game Loop 
if __name__ == "__main__":
    game_loop()
