import random

class Player(object):
    def __init__(self, first_name, last_name, average_speed, ball_weight):
        self.first_name = first_name
        self.last_name = last_name
        self.average_speed = average_speed
        self.ball_weight = ball_weight

        self.games = []

        self.career_games = 0
        self.career_score = 0
        self.career_spares = 0
        self.career_strikes = 0

    def play_game(self, event="-", date="-"):
        game = Game(self, event, date)
        game.bowl_game()
        self.career_score += game.score
        self.career_spares += game.spares
        self.career_strikes += game.strikes
        self.career_games += 1
        self.games.append(game)

    def show_games(self):
        for game in self.games:
            game.show_game()

    def show_career(self):
        print(self.first_name, self.last_name)
        print("Total Games", self.career_games)
        print("Total Score", self.career_score)
        print("Total Strikes", self.career_strikes)
        print("Total Spares", self.career_spares)


class Shot(object):
    def __init__(self, speed, ball_weight, pins):
        self.speed = speed
        self.ball_weight = ball_weight
        self.pins = pins


class Frame(object):
    def __init__(self):
        self.shots = []

        self.is_strike = False
        self.is_spare = False

        self.score = 0

    def take_shot(self, speed, ball_weight, max_pins):
        shot = Shot(speed, ball_weight, random.randint(0, max_pins))
        self.shots.append(shot)

    def show_frame(self):
        if len(self.shots) > 1:
            if self.is_spare:
                print(self.shots[0].pins, "/")
            elif self.shots[0].pins == 0:
                print("G", self.shots[1].pins)
            else:
                print(self.shots[0].pins, self.shots[1].pins)
        else:
            print("X")


class Game(object):
    def __init__(self, player, event_name, event_date):
        self.event_name = event_name
        self.event_date = event_date
        self.player = player

        self.frames = []

        self.score = 0

        self.strikes = 0
        self.spares = 0

    def update_score(self):
        self.score = 0

        for frame in self.frames:
            self.score += frame.score

    def bowl_frame(self):
        frame = Frame()
        frame.take_shot(
            random.randint(self.player.average_speed - 4,
                           self.player.average_speed + 4),
            self.player.ball_weight, 10)

        if frame.shots[0].pins == 10:
            frame.is_strike = True
            frame.score = 10
            self.strikes += 1
        else:
            frame.take_shot(
                random.randint(self.player.average_speed - 4,
                               self.player.average_speed + 4),
                self.player.ball_weight, 10 - frame.shots[0].pins)
            if frame.shots[0].pins + frame.shots[1].pins == 10:
                frame.is_spare = True
                frame.score = 10
                self.spares += 1
            else:
                frame.score = frame.shots[0].pins + frame.shots[1].pins

        if len(self.frames) > 0:
            previous_frame = self.frames[len(self.frames) - 1]
            if previous_frame.is_strike:
                previous_frame.score += 10 + frame.shots[0].pins
            if previous_frame.is_spare:
                previous_frame.score += frame.shots[0].pins

        self.frames.append(frame)
        self.update_score()

    def bowl_game(self):
        for x in range(10):
            self.bowl_frame()

    def show_game(self):
        print('\n')
        print(self.event_name, "on", self.event_date)
        for frame in self.frames:
            frame.show_frame()
        print(self.score, "/", self.spares, "X", self.strikes)


kason = Player("Kason", "Suchow", 21, 12)
cooper = Player("Cooper", "Wilhoite", 21, 12)

for x in range(100):
    kason.play_game()
    cooper.play_game()

kason.show_career()
print('\n')
cooper.show_career()
