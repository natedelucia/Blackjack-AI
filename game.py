import random
#Have dealer hand and score built into game, game initialization accepts an instance of the AI agent as the opposing player

suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
numDecks = 3

class Character:
    def __init__(self) -> None:
        self.currentScore = 0.0
        self.hand: list[tuple[str,str]] = []

class Dealer(Character):
    def __init__(self) -> None:
        super()

class Player(Character):
    def __init__(self) -> None:
        super()
        self.money = 1000.0
        self.bet = 0.0

class Game:
    def __init__(self, agent) -> None:
        self.gameDeck = [(value, suit) for suit in suits for value in values for deck in range(numDecks)]
        random.shuffle(self.gameDeck)
        self.dealer = Dealer()
        self.player = Player()

    def handScore(self, cards: list[tuple[str, str]]) -> float:
        score = 0
        cards.sort(key = lambda card: "z" if card[0] == "Ace" else str.casefold(card[0])) # Sorts the list so that all aces are considered last
        for card in cards:
            if card[0] in ["Jack", "Queen", "King"]:
                score += 10
            elif card[0] == "Ace" and score + 11 <= 21:
                score += 11
            elif card[0] == "Ace" and score + 11 > 21:
                score += 1
            else:
                score += float(card[0])
        return score

    def dealHand(self, character: Character) -> list[tuple[str, str]]:
        character.hand = []
        for _ in range(2):
            card = self.gameDeck.pop()
            character.hand.append(card)
        character.currentScore = self.handScore(character.hand)
        return character.hand

    def hit(self, character: Character) -> None:
        character.hand.append(self.gameDeck.pop())
        character.currentScore = self.handScore(character.hand)

    def doubleDown(self, player: Player) -> None:
        player.hand.append(self.gameDeck.pop())
        player.currentScore = self.handScore(player.hand)
        player.bet *= 2

def playGame() -> None:
    game = Game(0)
    numOfGames = 10
    for _ in range(numOfGames):
        #If Player runs out of money
        if game.player.money <= 0:
            break

        #Setup
        bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")
        game.player.bet = float(bet)
        game.player.money -= float(bet)
        print(f"Bet amount: {game.player.bet}")
        print(f"Your Hand: {game.dealHand(game.player)}, score: {int(game.player.currentScore)}")
        #Hide second dealer card
        print(f"Dealer's Hand: {game.dealHand(game.dealer)[0]}, Hidden")

        #Blackjack
        if game.player.currentScore == 21:
            print(f"Dealer's Hand: {game.dealer.hand}\r\n Dealer Score: {game.dealer.currentScore}")
            if not game.dealer.currentScore == 21:
                print("You win")
                game.player.money += float(game.player.bet) * 2.5
            else:
                print("Push")
                game.player.money += game.player.bet
            continue

        #Choices for current hand
        while game.player.currentScore <= 21:
            print("")
            choice = ""
            if game.player.currentScore in [9,10,11]:
                choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
                while choice not in ["H","S","D"] or choice == "D" and game.player.money < game.player.bet:
                    if choice not in ["H","S","D"]:
                        print("Invalid input, choose again")
                        choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
                    else:
                        print("Not enough money to double down, choose again")
                        choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
            else:
                choice = input("Choice: H for Hit, S for Stand\r\n")
                while choice not in ["H","S","D"]:
                    print("Invalid input, choose again")
                    choice = input("Choice: H for Hit, S for Stand\r\n")

            if choice == "H":
                game.hit(game.player)
                print(f"Your Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
            elif choice == "D":
                game.doubleDown(game.player)
                print(f"Your Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
            
            # Dealer draws until score is above 17. I don't know if he does this all at once or only once per turn though
            while game.handScore(game.dealer.hand) < 17:
                game.hit(game.dealer)
            print(f"Dealer's hand: {game.dealer.hand}\r\nDealer Score: {game.dealer.currentScore}")

            if game.dealer.currentScore > 21:
                print("Dealer busted")
                print("You win")
                game.player.money += float(game.player.bet) * 2.5
                break
            if choice == "S" and game.player.currentScore > game.dealer.currentScore:
                print("You win")
                game.player.money += float(game.player.bet) * 2.5
                break
            elif choice == "S":
                print("You lose")
                break
        
if __name__ == "__main__":
    playGame()
