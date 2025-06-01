from bindings import ITTEEngine
import threading
from time import sleep


# @TODO Duży test nie wiem czy to zostanie. HACK 
class player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.x = 0
        self.y = 6
    
    def up(self):
        if self.y > 1:
            self.y -= 1
    def down(self):
        if self.y < 7:
            self.y += 1
    def left(self):
        if self.x > 1:
            self.x -= 1
    def right(self):
        if self.x < 9:
            self.x += 1

    def __str__(self):
        return f"Player: {self.name}, Score: {self.score}"

def movment(engine, player):
    while True:
        user_input = engine.get_input()
        if user_input == 'w':
            player.up()
            player.up()
            player.up()
        elif user_input == 's':
            player.down()
        elif user_input == 'a':
            player.left()
        elif user_input == 'd':
            player.right()
        elif user_input == 'q':
            print("Exiting game.")
            break
        # sleep(0.1)

def main():
    player1 = player("%", 0)
    player1.x = 1
    # Create an instance of the iTTE engine
    engine = ITTEEngine()
    
    # engine._test_connection(420)
    
    # Initialize the game space
    rows, cols = engine.initialize()
    print(f"Game space initialized with dimensions: {rows}x{cols}")
    # Start a thread for player movement
    movement_thread = threading.Thread(target=movment, args=(engine, player1))
    movement_thread.daemon = True
    movement_thread.start()
    # Render the game state
    while True:
        game_state = engine.get_game_state()
        game_state[player1.y][player1.x] = player1.name
        engine.render(game_state)
        player1.down()
        sleep(0.1)

    engine.__del__()
if __name__ == "__main__":
    main()