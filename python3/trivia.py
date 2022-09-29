#!/usr/bin/env python3
import random

class Player:
    def __init__(self,n,p,t,b):
        self.name = n
        self.places = p
        self.points = t
        self.in_penalty_box = b


class Game ():
    def __init__(self):
        # [],[0]*6,[0]*6,[0]*6
        self.players = []
        
        
        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.now_player = None
        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        player1 = Player(player_name,0,0,False)
        self.players.append(player1)
        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self.now_player = self.players[self.current_player]
        print("%s is the current player" % self.now_player.name)
        print("They have rolled a %s" % roll)

        if self.now_player.in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.now_player.name)
                self.valid_roll_range(roll)

                self.print_loc_cat()
            else:
                print("%s is not getting out of the penalty box" % self.now_player.name)
                self.is_getting_out_of_penalty_box = False
        else:
            self.valid_roll_range(roll)
            self.print_loc_cat()
            

    def print_loc_cat(self):
        print(self.now_player.name + \
                            '\'s new location is ' + \
                            str(self.now_player.places))
        print("The category is %s" % self._current_category)
        self._ask_question()

    def valid_roll_range(self, roll):
        self.now_player.places = self.now_player.places + roll
        if self.now_player.places > 11:
            self.now_player.places = self.now_player.places - 12

    def _ask_question(self):
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.now_player.places == 0: return 'Pop'
        if self.now_player.places == 4: return 'Pop'
        if self.now_player.places == 8: return 'Pop'
        if self.now_player.places == 1: return 'Science'
        if self.now_player.places == 5: return 'Science'
        if self.now_player.places == 9: return 'Science'
        if self.now_player.places == 2: return 'Sports'
        if self.now_player.places == 6: return 'Sports'
        if self.now_player.places == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.now_player.in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                self.printAmtCoins()

                winner = self._did_player_win()
                self.change_player()
                if self.current_player == len(self.players): self.current_player = 0
                return winner
            else:
                self.change_player()
                self.now_player = self.players[self.current_player]
                return True



        else:
            self.printAmtCoins()

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def change_player(self):
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        

    def printAmtCoins(self):
        print('Answer was correct!!!!')
        self.now_player.points += 1
        print(self.now_player.name + \
                ' now has ' + \
                str(self.now_player.points) + \
                ' Gold Coins.')

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.now_player.name + " was sent to the penalty box")
        self.now_player.in_penalty_box = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.now_player.points == 6)




if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    random.seed(10)
    while True:
        game.roll(random.randrange(5) + 1)

        if random.randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break
