import ctypes
import os
import platform
from ctypes import get_errno
from typing import List, Optional, Tuple
import sys
if platform.system() != "Windows":
    import termios
    import tty
else:
    import msvcrt

class ITTEError(Exception):
    """Base exception class for iTTE errors."""
    def __init__(self, message):
        super().__init__(message)
        print(f"+{'='*10} ITTE Error {'='*10}+")
        print(f"Error: {message}")

class ITTEEngine:
    """Python interface for the iTTE engine."""
    
    def __init__(self):
        """Initialize the iTTE engine and load the required library."""
        self._lib = None
        self._game_ptr = None
        self._rows = 0
        self._cols = 0
        self._load_library()
        self._setup_functions()
        self._test_connection()

    def _load_library(self):
        """Load the appropriate library file based on the platform."""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lib_dir = os.path.join(parent_dir, "lib")
        
        try:
            if platform.system() == "Windows":
                dll_path = os.path.join(lib_dir, "iTTE.dll")
                if os.path.exists(lib_dir):
                    os.add_dll_directory(lib_dir)
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                kernel32.SetDllDirectoryW(lib_dir)
                self._lib = ctypes.CDLL(dll_path)
            else:
                dll_path = os.path.join(lib_dir, "iTTE.so")
                if os.path.exists(lib_dir):
                    os.environ['LD_LIBRARY_PATH'] = lib_dir + ":" + os.environ.get('LD_LIBRARY_PATH', '')
                self._lib = ctypes.CDLL(dll_path)

        except Exception as e:
            error_code = get_errno()
            raise ITTEError(f"Failed to load iTTE library: {e} (Error code: {error_code})")

    def _setup_functions(self):
        """Set up function signatures for the loaded library."""
        if not self._lib:
            raise ITTEError("Library not loaded")

        # Set up testbind_c
        self._lib.testbind_c.restype = None
        self._lib.testbind_c.argtypes = [ctypes.c_int]

        # Set up Init_c - now returns char** and takes int* for dimensions
        self._lib.Init_c.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
        self._lib.Init_c.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

        # Set up render_c - simplified, no longer needs game state pointer
        self._lib.render_c.restype = None
        self._lib.render_c.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),  # game_space_ptr (ignored)
            ctypes.c_int,  # row (ignored)
            ctypes.c_int   # col (ignored)
        ]

        # Set up AddObject_c - new function for adding objects
        self._lib.AddObject_c.restype = None
        self._lib.AddObject_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char]

        # Set up MoveObject_c - new function for moving objects
        self._lib.MoveObject_c.restype = None
        self._lib.MoveObject_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        
        # Set up RemoveObject_c - new function for removing objects
        self._lib.RemoveObject_c.restype = None
        self._lib.RemoveObject_c.argtypes = [ctypes.c_int]

        # Set up endscene_c
        self._lib.endscene_c.restype = None
        self._lib.endscene_c.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int]

        # Set up GetInput_c (deprecated but still available)
        self._lib.GetInput_c.restype = ctypes.c_char
        self._lib.GetInput_c.argtypes = []

    def _test_connection(self, value: int = 420):
        """Test if the connection to the library is working."""
        try:
            self._lib.testbind_c(value)
        except Exception as e:
            raise ITTEError(f"Failed to connect to iTTE: {e}")

    def initialize(self) -> Tuple[int, int]:
        """Initialize the game space and return its dimensions.
        
        Returns:
            Tuple[int, int]: The dimensions of the game space (rows, columns).
        """
        rows = ctypes.c_int()
        cols = ctypes.c_int()
        self._game_ptr = self._lib.Init_c(ctypes.byref(rows), ctypes.byref(cols))
        
        if not self._game_ptr:
            raise ITTEError("Failed to initialize game space")
        
        self._rows = rows.value
        self._cols = cols.value
        return self._rows, self._cols

    def get_game_state(self) -> List[List[str]]:
        """Get the current game state as a 2D list of characters.
        
        Note: This method is kept for compatibility but may not reflect 
        the actual rendered state with objects.
        
        Returns:
            List[List[str]]: The current game state.
        """
        if not self._game_ptr:
            raise ITTEError("Game not initialized")

        game = []
        for i in range(self._rows):
            row_list = []
            for j in range(self._cols):
                row_list.append(self._game_ptr[i][j].decode('ascii'))
            game.append(row_list)
        return game

    def render(self, game_state: Optional[List[List[str]]] = None) -> None:
        """Render the current game state.
        
        Args:
            game_state: Optional game state (ignored in new implementation).
                       The C++ engine now manages rendering internally.
        """
        if not self._lib:
            raise ITTEError("Library not loaded")

        # Create dummy parameters for compatibility - they're ignored by the C++ code
        dummy_ptr = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))()
        self._lib.render_c(dummy_ptr, 0, 0)

    def add_object(self, x: int, y: int, character: str) -> None:
        """Add a new object to the game world.
        
        Args:
            x: X coordinate of the object
            y: Y coordinate of the object
            character: Character to represent the object (single character)
        """
        if not self._lib:
            raise ITTEError("Library not loaded")
        
        if len(character) != 1:
            raise ValueError("Character must be a single character")
            
        char_byte = character.encode('ascii')[0]
        self._lib.AddObject_c(x, y, char_byte)

    def move_object(self, object_index: int, new_x: int, new_y: int) -> None:
        """Move an existing object to a new position.
        
        Args:
            object_index: Index of the object to move (0-based)
            new_x: New X coordinate
            new_y: New Y coordinate
        """
        if not self._lib:
            raise ITTEError("Library not loaded")
            
        self._lib.MoveObject_c(object_index, new_x, new_y)

    def remove_object(self, object_index: int) -> None:
        """Remove an object from the game world.
        
        Args:
            object_index: Index of the object to remove (0-based)
        """
        if not self._lib:
            raise ITTEError("Library not loaded")
            
        self._lib.RemoveObject_c(object_index)
    
    def get_input(self) -> str:
        """Get a single character of input from the user.
        
        Returns:
            str: The character entered by the user
        """
        if platform.system() == "Windows":
            while True:
                if msvcrt.kbhit():  # key is pressed
                    key = msvcrt.getwch()  # decode
                    return key
        else:
            filedescriptors = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
            key = sys.stdin.read(1)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
            return key

    def cleanup(self):
        """clean up resources."""
        if hasattr(self, '_game_ptr') and self._game_ptr and hasattr(self, '_lib'):
            self._lib.endscene_c(self._game_ptr, self._rows)
            self._game_ptr = None

    def __del__(self):
        self.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()