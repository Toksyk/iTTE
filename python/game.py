from bindings import ITTEEngine
import threading
from time import sleep

object_index = 0

class Block:
    def __init__(self, engine: ITTEEngine, character: str = '@', x: int = 1, y: int = 6):
        self.x = x
        self.y = y
        self.character = character
        self.engine = engine
        self.object_index = None
        
        # Add the player object to the engine
        self.engine.add_object(self.x, self.y, self.character)
        self.object_index = object_index
        object_index += 1
    
    def move_to(self, new_x: int, new_y: int):
        """Move player to new coordinates."""
        # Bounds checking (20x16 game field with borders)
        if 1 <= new_x <= 18 and 1 <= new_y <= 14:
            self.x = new_x
            self.y = new_y
            if self.object_index is not None:
                self.engine.move_object(self.object_index, self.x, self.y)
    
    def up(self):
        self.move_to(self.x, self.y - 1)
    
    def down(self):
        self.move_to(self.x, self.y + 1)
    
    def left(self):
        self.move_to(self.x - 1, self.y)
    
    def right(self):
        self.move_to(self.x + 1, self.y)

def get_char_of_x_y(engine: ITTEEngine, x: int, y: int) -> str:
    """Get the character at specified coordinates."""
    
    game_state = engine.get_game_state()
    print(game_state)
    if 0 <= y < len(game_state) and 0 <= x < len(game_state[y]):
        return game_state[y][x]
    return ' '

def movement_handler(engine: ITTEEngine, player: Block):
    """Handle player movement input in a separate thread."""
    
    while True:
        try:
            sleep(0.1)
            user_input = engine.get_input().lower()
            
            if user_input == ' ':
                player.up()
                sleep(0.1)
                player.up()
                sleep(0.1)
                player.up()
            elif user_input == 'a':
                player.left()
            elif user_input == 'd':
                player.right()
            elif user_input == 'q':
                print("Exiting game...")
                break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Input error: {e}")


def main():
    """Main game loop."""
    
    with ITTEEngine() as engine:
        # Initialize the game space
        rows, cols = engine.initialize()
        print(f"Game space initialized with dimensions: {rows}x{cols}")
        
        # Create player
        player1 = Block(engine, '@')
        print(f"Created {player1}")
        
        # Start movement handler in a separate thread
        movement_thread = threading.Thread(
            target=movement_handler, 
            args=(engine, player1),
            daemon=True
        )
        movement_thread.start()
        
        # Main render loop
        frame_count = 0
        try:
            while True:
                # Clear screen
                print("\033[2J\033[H", end="")  # ANSI escape codes
                
                # Display game info
                print(f"Frame: {frame_count}| char @TEST '{get_char_of_x_y(engine, player1.x, player1.y+1)}'")
                print("=" * 40)
                
                # Render the game
                engine.render()
                
                sleep(0.2)
                frame_count += 1
                
                # game logic
                if get_char_of_x_y(engine, player1.x, player1.y-1) == ' ':
                    player1.down()
                
                
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        
        # Wait for movement thread to finish
        movement_thread.join(timeout=1)


if __name__ == "__main__":
    main()