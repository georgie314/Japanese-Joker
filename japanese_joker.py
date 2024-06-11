import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.face_up = []
        self.face_down = []
        self.tricks_won = 0

    def display_hand(self):
        print(f"{self.name}'s hand: {self.hand}")

    def display_face_up(self):
        print(f"{self.name}'s face-up cards: {self.face_up}")

    def display_face_down(self):
        print(f"{self.name}'s face-down cards: {self.face_down}")

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.face_up:
            index = self.face_up.index(card)
            self.face_up.pop(index)
            if self.face_down:
                self.face_up.insert(index, self.face_down.pop(0))
        else:
            raise ValueError("Card not found in player's hand or face-up cards.")


def get_unique_player_names():
    players = set()
    while len(players) < 2:
        name = input(f"Enter name for player {len(players) + 1}: ")
        if name not in players:
            players.add(name)
        else:
            print("Name already exists. Please choose a different name.")
    return list(players)


def create_deck():
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    values = list(range(6, 11)) + ['J', 'Q', 'K', 'A']
    deck = [f"{value} of {suit}" for value in values for suit in suits]
    deck.extend(['Black Joker', 'Red Joker'])
    random.shuffle(deck)
    return deck


def deal_initial_cards(deck, players):
    for _ in range(3):
        for player in players:
            player.hand.append(deck.pop())
    return deck


def choose_trump(non_dealer):
    while True:
        trump = input(f"{non_dealer.name}, choose a trump suit (Clubs, Diamonds, Hearts, Spades) or 'No Trump': ")
        if trump.lower() in ['clubs', 'diamonds', 'hearts', 'spades', 'no trump']:
            return trump.capitalize()
        else:
            print("Invalid input. Please choose a valid trump suit or 'No Trump'.")


def deal_remaining_cards(deck, players):
    for _ in range(5):
        for player in players:
            player.face_down.append(deck.pop())
            player.face_up.append(deck.pop())

    for _ in range(5):
        for player in players:
            player.hand.append(deck.pop())


def get_card_rank(value):
    if value.isdigit():
        return int(value)
    elif value == 'J':
        return 11
    elif value == 'Q':
        return 12
    elif value == 'K':
        return 13
    elif value == 'A':
        return 14
    elif value == 'Black Joker' or value == 'Red Joker':
        return 15


def play_trick(players, trump):
    lead_player = players[0]
    follow_player = players[1]
    trick_cards = []

    lead_player.display_hand()
    lead_player.display_face_up()
    lead_card = input(f"{lead_player.name}, play a card from your hand or face-up cards: ")
    while lead_card not in lead_player.hand and lead_card not in lead_player.face_up:
        lead_card = input(f"Invalid card. {lead_player.name}, play a card from your hand or face-up cards: ")
    lead_player.remove_card(lead_card)
    trick_cards.append((lead_card, lead_player))

    follow_player.display_hand()
    follow_player.display_face_up()
    follow_card = input(f"{follow_player.name}, play a card from your hand or face-up cards: ")
    while follow_card not in follow_player.hand and follow_card not in follow_player.face_up:
        follow_card = input(f"Invalid card. {follow_player.name}, play a card from your hand or face-up cards: ")
    follow_player.remove_card(follow_card)
    trick_cards.append((follow_card, follow_player))

    lead_suit = lead_card.split(' of ')[1] if ' of ' in lead_card else ''
    follow_suit = follow_card.split(' of ')[1] if ' of ' in follow_card else ''
    lead_value = lead_card.split(' of ')[0]
    follow_value = follow_card.split(' of ')[0]

    lead_card_rank = get_card_rank(lead_value)
    follow_card_rank = get_card_rank(follow_value)

    if follow_suit == lead_suit:
        if follow_card_rank > lead_card_rank:
            winner = follow_player
        else:
            winner = lead_player
    elif follow_suit == trump:
        winner = follow_player
    else:
        winner = lead_player

    winner.tricks_won += 1
    print(f"{winner.name} wins the trick with {lead_card if winner == lead_player else follow_card}")

    return winner


def play_game():
    player_names = get_unique_player_names()
    players = [Player(name) for name in player_names]

    dealer = random.choice(players)
    non_dealer = players[1] if dealer is players[0] else players[0]

    print(f"{dealer.name} is the dealer.")
    deck = create_deck()
    deck = deal_initial_cards(deck, players)

    for player in players:
        player.display_hand()

    trump = choose_trump(non_dealer)
    print(f"Trump suit: {trump}")

    deal_remaining_cards(deck, players)

    for player in players:
        player.display_hand()
        player.display_face_up()
        player.display_face_down()

    current_winner = play_trick(players, trump)
    while len(players[0].hand) > 0 or len(players[1].hand) > 0 or len(players[0].face_up) > 0 or len(players[1].face_up) > 0:
        players = [current_winner, players[1] if current_winner is players[0] else players[0]]
        current_winner = play_trick(players, trump)

    print(f"{players[0].name} won {players[0].tricks_won} tricks.")
    print(f"{players[1].name} won {players[1].tricks_won} tricks.")

    if players[0].tricks_won > players[1].tricks_won:
        print(f"{players[0].name} wins the game!")
    elif players[1].tricks_won > players[0].tricks_won:
        print(f"{players[1].name} wins the game!")
    else:
        print("The game is a draw!")


if __name__ == "__main__":
    play_game()
