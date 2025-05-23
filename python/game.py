from bindings import ITTEEngine

# @TODO Duży test nie wiem czy to zostanie. HACK 
class player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.x = 0
        self.y = 0
        

    def __str__(self):
        return f"Player: {self.name}, Score: {self.score}"

def main():
    player1 = player("%", 0)
    player1.x = 1
    # Create an instance of the iTTE engine
    engine = ITTEEngine()
    
    # engine._test_connection(420)
    
    # Initialize the game space
    rows, cols = engine.initialize()
    print(f"Game space initialized with dimensions: {rows}x{cols}")
    
    # Get the current game state
    game_state = engine.get_game_state()
    
    game_state[player1.y][player1.x] = player1.name
    
    print("Current game state:")
    for row in game_state:
        print(" ".join(row))
    # Render the game state
    engine.render(game_state)
    
    engine.__del__()
if __name__ == "__main__":
    main()