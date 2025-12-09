"""
Falling Tic-Tac-Toe (Connect Four Variant)
Author: Adam Trepáč
Description: A console-based game where players drop symbols into columns. 
The first to align 4 symbols (horizontally, vertically, or diagonally) wins.
Includes a simple AI opponent.
"""

from random import randint
from typing import List, Optional

def create_board(rows: int, cols: int) -> List[List[str]]:
    """Initializes an empty game board filled with spaces."""
    board = []
    for _ in range(rows):
        row = [' ' for _ in range(cols)]
        board.append(row)
    return board

def show_board(state: List[List[str]]) -> None:
    """Prints the current state of the game board to the console."""
    # Print the rows
    for row in state:
        for char in row:
            print(f" {char} ", end='')
        print()
    
    # Print the separator line
    width = len(state[0])
    print("---" * width)
    
    # Print column numbers
    for i in range(width):
        print(f" {i} ", end='')
    print()

def get_ai_move(state: List[List[str]], symbol: str) -> int:
    """
    Simple AI Strategy: Returns a random valid column index.
    """
    cols = len(state[0])
    # Try to find a random valid column
    while True:
        col = randint(0, cols - 1)
        if is_valid_move(col, state):
            return col

def is_valid_move(col: int, state: List[List[str]]) -> bool:
    """Checks if a move can be made in the selected column."""
    if col < 0 or col >= len(state[0]):
        return False
    # If the top row is empty, there is space to drop a piece
    return state[0][col] == ' '

def update_board(col: int, state: List[List[str]], symbol: str) -> List[List[str]]:
    """Drops the symbol into the lowest available spot in the column."""
    # Start from the bottom row and go up
    for i in range(len(state) - 1, -1, -1):
        if state[i][col] == ' ':
            state[i][col] = symbol
            return state
    return state

def check_win(state: List[List[str]], symbol: str) -> bool:
    """Checks board for 4 connected symbols (Horizontal, Vertical, Diagonal)."""
    rows = len(state)
    cols = len(state[0])

    # 1. Check Horizontal (Rows)
    for r in range(rows):
        count = 0
        for c in range(cols):
            if state[r][c] == symbol:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

    # 2. Check Vertical (Columns)
    for c in range(cols):
        count = 0
        for r in range(rows):
            if state[r][c] == symbol:
                count += 1
            else:
                count = 0
            if count == 4:
                return True

    # 3. Check Diagonal (Top-Left to Bottom-Right)
    # Iterate through all possible starting points for a diagonal of 4
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(state[r + i][c + i] == symbol for i in range(4)):
                return True

    # 4. Check Diagonal (Bottom-Left to Top-Right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(state[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(state: List[List[str]]) -> bool:
    """Returns True if the board is full (no spaces left)."""
    for row in state:
        if ' ' in row:
            return False
    return True

def play_game(rows: int = 6, cols: int = 7, human_starts: bool = True) -> None:
    """Main game loop."""
    state = create_board(rows, cols)
    print(f"Starting Game! Board Size: {rows}x{cols}")
    show_board(state)
    
    # Define players: (Symbol, is_human)
    players = [('X', True), ('O', False)] if human_starts else [('O', False), ('X', True)]
    
    turn = 0
    while True:
        symbol, is_human = players[turn % 2]
        print(f"\nTurn: {'Player' if is_human else 'Computer'} ({symbol})")
        
        col = -1
        if is_human:
            while True:
                try:
                    user_input = input(f"Choose column (0-{cols - 1}): ")
                    col = int(user_input)
                    if is_valid_move(col, state):
                        break
                    print("Invalid move or column full. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            # AI Logic
            col = get_ai_move(state, symbol)
            print(f"Computer chose column {col}")

        # Execute Move
        state = update_board(col, state, symbol)
        show_board(state)

        # Check Win/Draw
        if check_win(state, symbol):
            print(f"\nGame Over! {'Player' if is_human else 'Computer'} ({symbol}) WINS!")
            break
        
        if check_draw(state):
            print("\nGame Over! It's a DRAW.")
            break
            
        turn += 1

if __name__ == '__main__':
    # Standard board size is usually 6x7 for this type of game
    play_game(rows=6, cols=7)
