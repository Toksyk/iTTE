import ctypes
import os
import platform
from ctypes import get_last_error
from typing import List, Optional, Tuple

class ITTEError(Exception):
    """Base exception class for iTTE errors."""
    print(f"+{'='*10} ITTE Error {'='*10}+")
    pass

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
                os.add_dll_directory(lib_dir)
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                kernel32.SetDllDirectoryW(lib_dir)
                self._lib = ctypes.CDLL(dll_path)
            else:
                dll_path = os.path.join(lib_dir, "iTTE.so")
                os.environ['LD_LIBRARY_PATH'] = lib_dir
                self._lib = ctypes.CDLL(dll_path)
        except Exception as e:
            error_code = get_last_error()
            raise ITTEError(f"Failed to load iTTE library: {e} (Error code: {error_code})")

    def _setup_functions(self):
        """Set up function signatures for the loaded library."""
        if not self._lib:
            raise ITTEError("Library not loaded")

        # Set up testbind_c
        self._lib.testbind_c.restype = None
        self._lib.testbind_c.argtypes = [ctypes.c_int]

        # Set up Init_c
        self._lib.Init_c.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
        self._lib.Init_c.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

        # Set up render_c
        self._lib.render_c.restype = None
        self._lib.render_c.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set up endscene_c
        self._lib.endscene_c.restype = None
        self._lib.endscene_c.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int]

    def _test_connection(self,value: int = 420):
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

    def render(self, game_state: List[List[str]]) -> None:
        """Render the given game state.
        
        Args:
            game_state: A 2D list of characters representing the game state.
        """
        if not self._lib:
            raise ITTEError("Library not loaded")

        rows = len(game_state)
        if rows == 0:
            raise ValueError("Empty game state")
        cols = len(game_state[0])

        c_char = ctypes.c_char * cols
        c_char_ptr = ctypes.POINTER(c_char)
        c_rows = (c_char_ptr * rows)()

        for i in range(rows):
            char_row = c_char(*[ord(c) for c in game_state[i]])
            c_rows[i] = ctypes.cast(char_row, c_char_ptr)

        self._lib.render_c(
            ctypes.cast(c_rows, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
            rows,
            cols
        )

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        if hasattr(self, '_game_ptr') and self._game_ptr and hasattr(self, '_lib'):
            self._lib.endscene_c(self._game_ptr, self._rows)
