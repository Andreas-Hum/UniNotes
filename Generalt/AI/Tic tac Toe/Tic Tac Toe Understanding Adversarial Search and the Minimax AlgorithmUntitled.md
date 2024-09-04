## Author

**Andreas Hummelmose**  
_Computer Science Student, 5th Semester, Aalborg University_  
[LinkedIn: Andreas Hummelmose](https://www.google.com/url?q=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fandreas-hummelmose-77580a252%2F)

---

## **1. Introduction to Adversarial Search**

We’ll start by introducing the concept of adversarial search, which is a framework for solving problems where multiple agents compete against each other.
### **1.1 What is Adversarial Search?**

An adversarial search problem is characterized by a conflict of interests between two or more agents, typically modeled as a game. Each agent aims to maximize its own utility while minimizing that of the opponent.
### **1.2 Key Components of Adversarial Search**

- **Players**: Agents that make decisions in the game.
- **Actions**: The possible moves a player can make at each turn.
- **State**: A configuration of the game at a particular point in time.
- **Transition Model**: The function, which describes the result of applying an action to a state.
- **Utility Function**: A function that assigns a numerical value to the outcome of the game, reflecting the preferences of the player.
- **Initial State**: The starting configuration of the game.
- **Terminal State**: The state where the game ends (e.g., a win, loss, or draw).
### **1.3 Formal Definition**

We can define an adversarial search problem as a tuple (S,A,δ,P,U,s0,T), where:

- S: Set of all possible states.
- A: Set of all possible actions.
- δ:S×A→S: Transition function that describes the result of applying an action to a state.
- P:S→{Player 1,Player 2,…}: Function to determines whose turn it is.
- U:S→R: Utility function, assigning a value to terminal states.
- s0∈S: Initial state.
- T:S→bool: Function to determine if a state is terminal.
### **Example in Tic-Tac-Toe:**

In Tic-Tac-Toe:
- Players alternate turns marking the grid.
- The utility function could assign +1 for a win, -1 for a loss, and 0 for a draw.
- The initial state is an empty 3x3 grid.
- A terminal state occurs when one player wins or all cells are filled without a winner.

## **2. The Minimax Algorithm**

Here we introduce the Minimax algorithm, which is central to solving adversarial search problems.
### **2.1 What is the Minimax Algorithm?**

Minimax is a recursive decision-making algorithm used in two-player games. The core idea is to minimize the possible loss for a worst-case scenario, which effectively maximizes the minimum gain (hence the name "Minimax").
### **2.2 How Minimax Works**

The algorithm explores all possible moves in the game, constructing a game tree. Each node represents a game state, and each branch represents a possible move. The algorithm alternates between maximizing and minimizing players to determine the optimal move.
### **2.3 Key Concepts**

- **Maximizing Player**: The player who tries to maximize the utility.
- **Minimizing Player**: The opponent who tries to minimize the utility.
- **Utility Function**: A function that assigns a numerical value to the terminal states. For example, in Tic-Tac-Toe:
    - A win might be +1 for the maximizing player.
    - A loss might be -1 for the maximizing player.
    - A draw is typically 0.
### **Formal Pseudocode of Minimax:**

```
FUNCTION Minimax(state, depth, maximizingPlayer) -> INTEGER
	IF depth = 0 OR TerminalState(state) THEN
		RETURN Utility(state)
	END IF
	IF maximizingPlayer THEN
	    maxEval ← -∞
	    FOR each action IN Actions(state) DO
	        eval ← Minimax(Result(state, action), depth - 1, FALSE)
	        maxEval ← MAX(maxEval, eval)
	    END FOR
	    RETURN maxEval
	ELSE
	    minEval ← ∞
	    FOR each action IN Actions(state) DO
	        eval ← Minimax(Result(state, action), depth - 1, TRUE)
	        minEval ← MIN(minEval, eval)
	    END FOR
	    RETURN minEval
	END IF
END FUNCTION
```
### **Explanation:**

- **Terminal State Check**: The algorithm first checks if the game has reached a terminal state (end of the game) or if the search depth limit is reached.
- **Maximizing Player's Turn**: The algorithm selects the move that leads to the highest utility value.
- **Minimizing Player's Turn**: The algorithm selects the move that leads to the lowest utility value.

## **3. Implementing the Tic-Tac-Toe Game**

Now that we've covered the theory, let's start implementing the Tic-Tac-Toe game using Python. This implementation includes a human vs. AI mode, where the AI uses the Minimax algorithm with Alpha-Beta Pruning.
### **3.1 Tic-Tac-Toe Game Setup**

We'll start by defining the Tic-Tac-Toe game class, which manages the game state, handles player turns, and checks for a win or draw.

```python
import numpy as np

class TicTacToe:
    def __init__(self, players: int = 1) -> None:
        """Initialize the TicTacToe game.
        
        Args:
            players (int): Number of human players (0 for AI vs AI, 1 for human vs AI, 2 for human vs human).
        """
        self.turns = {
            1: "X",
            2: "O"
        }
        self.players = players
        self.ai = players < 2  # If less than 2 players, AI is involved

    def start(self) -> None:
        """Start a new game with the specified number of players."""
        self.board = TTTBoardGenerator.generate_board()
        self.turn = 1
        self.winner = None
        if self.ai:
            self.brain = TTTAI()  # Initialize AI if required
        self.game_loop()
```
### **3.2 Game Loop and Player Turns**

The `game_loop` function runs the main loop of the game, alternating turns between players (human or AI) until the game ends. It also checks for a win or tie after each turn.

```python
    def game_loop(self) -> None:
        """Main game loop that handles player and AI turns."""
        while True:
            current_turn = self.turn

            if self.players == 0:  # AI vs AI
                move = self.brain.choose_move(self.board, current_turn)
                self.update_board(move, current_turn)
            elif self.players == 1 and current_turn == 2:  # Human vs AI, AI's turn
                move = self.brain.choose_move(self.board, 2)
                self.update_board(move, 2)
            else:  # Human player's turn
                self.human_turn(current_turn)

            self.print_board()

            self.win_test(current_turn)
            if self.winner is not None:
                self.display_winner()
                break
            
            self.turn = 2 if current_turn == 1 else 1
```

### **3.3 Handling Human Turns**

The `human_turn` function processes the input from the human player, ensuring the move is valid before updating the board.

```python
    def human_turn(self, turn) -> None:
        """Handle human player's turn."""
        print(f"Player {turn}: Press 0-8")
        self.print_board()
        available = self.available_actions()
        while True:
            try:
                player_input = int(input())
                if player_input < 0 or player_input > 8 or player_input not in available:
                    print("Invalid move")
                else:
                    self.update_board(player_input, turn)
                    break
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")
```

### **3.4 Updating the Board**

The `update_board` function updates the game board based on the move made by a player (or AI).

```python
    def update_board(self, move, turn) -> None:
        """Update the board with the player's or AI's move."""
        row = move // 3
        col = move % 3
        self.board[row, col] = self.turns[turn]
```

### **3.5 Checking for Available Actions**

The `available_actions` function returns a list of available moves on the board.

```python
    def available_actions(self) -> list:
        """Return a list of available actions on the board."""
        return [i for i in range(9) if self.board[i // 3, i % 3] == ""]
```

### **3.6 Printing the Board**

The `print_board` function displays the current state of the board.

```python
    def print_board(self) -> None:
        """Print the current state of the board."""
        for i in range(3):
            print("".join("-" for _ in range(49)))
            row_display = [
                f"{i * 3 + j}" if self.board[i, j] == "" else self.board[i, j]
                for j in range(3)
            ]
	        print(f"|\t{row_display[0]}\t|\t{row_display[1]}\t|\t{row_display[2]}\t|")
        print("".join("-" for _ in range(49)))
```

### **3.7 Checking for a Win or Tie**

The `win_test` function checks if the game has ended in a win or a tie.

```python
    def win_test(self, turn) -> None:
        """Check if there's a winner or a tie."""
        if len(self.available_actions()) == 0:
            self.winner = 0  # Tie game
            return
        if self.check_diagonals() or self.check_rows_and_columns():
            self.winner = turn

    def check_diagonals(self) -> bool:
        """Check the diagonals for a win."""
        return (
            self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != "" or
            self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != ""
        )
    
    def check_rows_and_columns(self) -> bool:
        """Check all rows and columns for a win."""
        for i in range(3):
            if (
                self.board[i, 0] == self.board[i, 1] == self.board[i, 2] != "" or
                self.board[0, i] == self.board[1, i] == self.board[2, i] != ""
            ):
                return True
        return False

    def display_winner(self) -> None:
        """Display the result of the game."""
        if self.winner == 0:
            print("Tie")
        else:
            print(f"Player {self.winner} wins!!")
```

## **4. Implementing the AI with Minimax**

Now that we have the game mechanics, let's implement the AI using the Minimax algorithm with Alpha-Beta Pruning.
### **4.1 Initializing the AI**

The `TTTAI` class is responsible for determining the best move for the AI using the Minimax algorithm.

```python
class TTTAI:
    def __init__(self) -> None:
        """Initialize the Tic-Tac-Toe AI."""
        self.turns = {
            1: "X",
            2: "O"
        }
```

### **4.2 Choosing the Best Move**

The `choose_move` function uses the Minimax algorithm to select the best move for the AI.

```python
    def choose_move(self, state, turn) -> int:
        """Choose the best move for the current state and turn using Minimax with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            turn (int): The player's turn (1 or 2).

        Returns:
            int: The index of the best move.
        """
        if turn == 2:
            return self.minimax_decision(state, turn, float("inf"), False)
        else:
            return self.minimax_decision(state, turn, float("-inf"), True)
```

### **4.3 Minimax Decision-Making**

The `minimax_decision` function carries out the Minimax decision-making process with Alpha-Beta Pruning.

```python
    def minimax_decision(self, state, turn, best_value, is_maximizing) -> int:
        """Perform the Minimax decision-making process with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            turn (int): The player's turn (1 or 2).
            best_value (float): The initial best value to compare against.
            is_maximizing (bool): Flag to determine if maximizing or minimizing.

        Returns:
            int: The index of the best move.
        """
        best_move = None
        for action in self.available_actions(state):
            new_state = self.transition_model(state, action, turn)
            eval = self.minimax(new_state, not is_maximizing, float("-inf"), float("inf"))
            if is_maximizing and eval > best_value or not is_maximizing and eval < best_value:
                best_value = eval
                best_move = action
        return best_move
```

### **4.4 Minimax Algorithm with Alpha-Beta Pruning**

The `minimax` function implements the Minimax algorithm with Alpha-Beta Pruning.

```python
    def minimax(self, state, maximizingPlayer, alpha, beta) -> int:
        """Minimax algorithm with Alpha-Beta Pruning to optimize the search tree.
        
        Args:
            state (np.ndarray): The current state of the board.
            maximizingPlayer (bool): Flag to determine if maximizing or minimizing.
            alpha (float): The alpha value for pruning (highest value that the maximizer can guarantee).
            beta (float): The beta value for pruning (lowest value that the minimizer can guarantee).

        Returns:
            int: The evaluated value of the board.
        """
        if self.terminal(state):
            return self.utility(state)
        
        if maximizingPlayer:
            return self.maximize(state, alpha, beta)
        else:
            return self.minimize(state, alpha, beta)
```

### **4.5 Maximization and Minimization Functions**

The `maximize` and `minimize` functions perform the core logic of the Minimax algorithm, using Alpha-Beta Pruning to eliminate branches that do not need to be evaluated.

```python
    def maximize(self, state, alpha, beta) -> int:
        """Maximization step in the Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.

        Returns:
            int: The maximum evaluated value.
        """
        maxEval = float("-inf")
        for action in self.available_actions(state):
            eval = self.minimax(self.transition_model(state, action, 1), False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Pruning condition
                break
        return maxEval

    def minimize(self, state, alpha, beta) -> int:
        """Minimization step in the Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.

        Returns:
            int: The minimum evaluated value.
        """
        minEval = float("inf")
        for action in self.available_actions(state):
            eval = self.minimax(self.transition_model(state, action, 2), True, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Pruning condition
                break
        return minEval
```

### **4.6 Utility and Terminal Functions**

The `utility` function evaluates the board to determine the game outcome, and the `terminal` function checks if the current state is a terminal state.

```python
    def utility(self, state) -> int:
        """Evaluate the utility of the current state."""
        for line in [state[i, :] for i in range(3)] + [state[:, i] for i in range(3)] + [state.diagonal(), np.fliplr(state).diagonal()]:
            if np.all(line == 'X'):
                return 1
            elif np.all(line == 'O'):
                return -1
        return 0  # Draw or game not finished

    def terminal(self, state) -> bool:
        """Check if the state is terminal (win or tie)."""
        return len(self.available_actions(state)) == 0 or self.utility(state) != 0
```

### **4.7 Transition Model**

The `transition_model` function generates the next state based on the current state and action.

```python
    def transition_model(self, state, action, turn):
        """Generate the next state based on the current state and action."""
        new_state = np.copy(state)
        row = action // 3
        col = action % 3
        new_state[row, col] = self.turns[turn]
        return new_state
```

## **5. Board Generator**

The `TTTBoardGenerator` class provides a method to generate an empty Tic-Tac-Toe board.

```python
class TTTBoardGenerator:
    @staticmethod
    def generate_board() -> np.ndarray:
        """Generate an empty Tic-Tac-Toe board."""
        return np.full((3, 3), "", dtype=str)
```

## **6. Putting It All Together**

We integrate all the components to create a complete Tic-Tac-Toe game where the AI uses the Minimax algorithm with Alpha-Beta Pruning to make decisions.

```python
class TicTacToe:
    def __init__(self, players: int = 1) -> None:
        """Initialize the TicTacToe game.
        
        Args:
            players (int): Number of human players (0 for AI vs AI, 1 for human vs AI, 2 for human vs human).
        """
        self.turns = {
            1: "X",
            2: "O"
        }
        self.players = players
        self.ai = players < 2  # If less than 2 players, AI is involved

    def start(self) -> None:
        """Start a new game with the specified number of players."""
        self.board = TTTBoardGenerator.generate_board()
        self.turn = 1
        self.winner = None
        if self.ai:
            self.brain = TTTAI()  # Initialize AI if required
        self.game_loop()
    
    def game_loop(self) -> None:
        """Main game loop that handles player and AI turns."""
        while True:
            current_turn = self.turn

            if self.players == 0:  # AI vs AI
                move = self.brain.choose_move(self.board, current_turn)
                self.update_board(move, current_turn)
                self.print_board()
            elif self.players == 1 and current_turn == 2:  # Human vs AI, AI's turn
                print(f"AI turn")
                move = self.brain.choose_move(self.board, 2)
                self.update_board(move, 2)
                self.print_board()
            else:  # Human player's turn
                self.human_turn(current_turn)


            self.win_test(current_turn)
            if self.winner is not None:
                self.display_winner()
                break
            
            self.turn = 2 if current_turn == 1 else 1
    
    def human_turn(self, turn) -> None:
        """Handle human player's turn."""
        print(f"Player {turn}: Press 0-8")
        self.print_board()
        available = self.available_actions()
        while True:
            try:
                player_input = int(input())
                if player_input < 0 or player_input > 8 or player_input not in available:
                    print("Invalid move")
                else:
                    self.update_board(player_input, turn)
                    break
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")
    
    def update_board(self, move, turn) -> None:
        """Update the board with the player's or AI's move."""
        row = move // 3
        col = move % 3
        self.board[row, col] = self.turns[turn]

    def available_actions(self) -> list:
        """Return a list of available actions on the board."""
        return [i for i in range(9) if self.board[i // 3, i % 3] == ""]

    def print_board(self) -> None:
        """Print the current state of the board."""
        for i in range(3):
            print("".join("-" for _ in range(49)))
            row_display = [
                f"{i * 3 + j}" if self.board[i, j] == "" else self.board[i, j]
                for j in range(3)
            ]
            print(f"|\t{row_display[0]}\t|\t{row_display[1]}\t|\t{row_display[2]}\t|")
        print("".join("-" for _ in range(49)))

    def win_test(self, turn) -> None:
        """Check if there's a winner or a tie."""
        if len(self.available_actions()) == 0:
            self.winner = 0  # Tie game
            return
        if self.check_diagonals() or self.check_rows_and_columns():
            self.winner = turn

    def check_diagonals(self) -> bool:
        """Check the diagonals for a win."""
        return (
            self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != "" or
            self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != ""
        )
    
    def check_rows_and_columns(self) -> bool:
        """Check all rows and columns for a win."""
        for i in range(3):
            if (
                self.board[i, 0] == self.board[i, 1] == self.board[i, 2] != "" or
                self.board[0, i] == self.board[1, i] == self.board[2, i] != ""
            ):
                return True
        return False

    def display_winner(self) -> None:
        """Display the result of the game."""
        if self.winner == 0:
            print("Tie")
        else:
            print(f"Player {self.winner} wins!!")


class TTTAI:
    def __init__(self) -> None:
        """Initialize the Tic-Tac-Toe AI."""
        self.turns = {
            1: "X",
            2: "O"
        }

    def choose_move(self, state, turn) -> int:
        """Choose the best move for the current state and turn using Minimax with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            turn (int): The player's turn (1 or 2).

        Returns:
            int: The index of the best move.
        """
        if turn == 2:
            return self.minimax_decision(state, turn, float("inf"), False)
        else:
            return self.minimax_decision(state, turn, float("-inf"), True)

    def minimax_decision(self, state, turn, best_value, is_maximizing) -> int:
        """Perform the Minimax decision-making process with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            turn (int): The player's turn (1 or 2).
            best_value (float): The initial best value to compare against.
            is_maximizing (bool): Flag to determine if maximizing or minimizing.

        Returns:
            int: The index of the best move.
        """
        best_move = None
        for action in self.available_actions(state):
            new_state = self.transition_model(state, action, turn)
            eval = self.minimax(new_state, not is_maximizing, float("-inf"), float("inf"))
            if is_maximizing and eval > best_value or not is_maximizing and eval < best_value:
                best_value = eval
                best_move = action
        return best_move

    def minimax(self, state, maximizingPlayer, alpha, beta) -> int:
        """Minimax algorithm with Alpha-Beta Pruning to optimize the search tree.
        
        Args:
            state (np.ndarray): The current state of the board.
            maximizingPlayer (bool): Flag to determine if maximizing or minimizing.
            alpha (float): The alpha value for pruning (highest value that the maximizer can guarantee).
            beta (float): The beta value for pruning (lowest value that the minimizer can guarantee).

        Returns:
            int: The evaluated value of the board.
        """
        if self.terminal(state):
            return self.utility(state)
        
        if maximizingPlayer:
            return self.maximize(state, alpha, beta)
        else:
            return self.minimize(state, alpha, beta)

    def maximize(self, state, alpha, beta) -> int:
        """Maximization step in the Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.

        Returns:
            int: The maximum evaluated value.
        """
        maxEval = float("-inf")
        for action in self.available_actions(state):
            eval = self.minimax(self.transition_model(state, action, 1), False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Pruning condition
                break
        return maxEval

    def minimize(self, state, alpha, beta) -> int:
        """Minimization step in the Minimax algorithm with Alpha-Beta Pruning.
        
        Args:
            state (np.ndarray): The current state of the board.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.

        Returns:
            int: The minimum evaluated value.
        """
        minEval = float("inf")
        for action in self.available_actions(state):
            eval = self.minimax(self.transition_model(state, action, 2), True, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Pruning condition
                break
        return minEval

    def available_actions(self, state) -> list:
        """Return a list of available actions on the board."""
        return [i for i in range(9) if state[i // 3, i % 3] == ""]
    
    def transition_model(self, state, action, turn):
        """Generate the next state based on the current state and action."""
        new_state = np.copy(state)
        row = action // 3
        col = action % 3
        new_state[row, col] = self.turns[turn]
        return new_state
    
    def terminal(self, state) -> bool:
        """Check if the state is terminal (win or tie)."""
        return len(self.available_actions(state)) == 0 or self.utility(state) != 0
    
    def utility(self, state) -> int:
        """Evaluate the utility of the current state."""
        for line in [state[i, :] for i in range(3)] + [state[:, i] for i in range(3)] + [state.diagonal(), np.fliplr(state).diagonal()]:
            if np.all(line == 'X'):
                return 1
            elif np.all(line == 'O'):
                return -1
        return 0  # Draw or game not finished

```

## **7. Example Games and Testing**

We'll run some example games to verify that the AI works as expected.

### 7.1 **AI vs AI**

```python
# Example: AI vs AI Game
game = TicTacToe(players=0)
game.start()
```

#### output:

```plaintext
-------------------------
|	X	|	1	|	2	|
-------------------------
|	3	|	4	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
-------------------------
|	X	|	1	|	2	|
-------------------------
|	3	|	O	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	2	|
-------------------------
|	3	|	O	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	3	|	O	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	3	|	O	|	5	|
-------------------------
|	X	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	O	|	O	|	5	|
-------------------------
|	X	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	O	|	O	|	X	|
-------------------------
|	X	|	7	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	O	|	O	|	X	|
-------------------------
|	X	|	O	|	8	|
-------------------------
-------------------------
|	X	|	X	|	O	|
-------------------------
|	O	|	O	|	X	|
-------------------------
|	X	|	O	|	X	|
-------------------------
Tie
```

### 7.2 **Human vs AI**

```python
# Example: Human vs AI Game
game = TicTacToe(players=1)
game.start()
```

#### output:

```plaintext
Player 1: Press 0-8
-------------------------
|	0	|	1	|	2	|
-------------------------
|	3	|	4	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
4
AI turn
-------------------------
|	O	|	1	|	2	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
Player 1: Press 0-8
-------------------------
|	O	|	1	|	2	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	6	|	7	|	8	|
-------------------------
6
AI turn
-------------------------
|	O	|	1	|	O	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	X	|	7	|	8	|
-------------------------
Player 1: Press 0-8
-------------------------
|	O	|	1	|	O	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	X	|	7	|	8	|
-------------------------
1
AI turn
-------------------------
|	O	|	X	|	O	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	X	|	O	|	8	|
-------------------------
Player 1: Press 0-8
-------------------------
|	O	|	X	|	O	|
-------------------------
|	3	|	X	|	5	|
-------------------------
|	X	|	O	|	8	|
-------------------------
5
AI turn
-------------------------
|	O	|	X	|	O	|
-------------------------
|	O	|	X	|	X	|
-------------------------
|	X	|	O	|	8	|
-------------------------
Player 1: Press 0-8
-------------------------
|	O	|	X	|	O	|
-------------------------
|	O	|	X	|	X	|
-------------------------
|	X	|	O	|	8	|
-------------------------
8
Tie
```

## **8. Conclusion and Further Optimizations**

### **Conclusion**
In this notebook, we explored the fundamentals of adversarial search and implemented a Tic-Tac-Toe AI using the Minimax algorithm with Alpha-Beta Pruning. This AI is capable of playing optimally, either against another AI or a human player. We demonstrated how the Minimax algorithm systematically evaluates all possible moves to make decisions that maximize the chance of winning while minimizing potential losses. By incorporating Alpha-Beta Pruning, we significantly reduced the number of nodes that need to be evaluated, making the algorithm more efficient without sacrificing accuracy.

While the current implementation works well for a simple game like Tic-Tac-Toe, there are several areas where further optimizations and improvements can be made, especially if we aim to extend these techniques to more complex games or scenarios.

### **Further Optimizations**

1. **Advanced Heuristic Evaluation Functions:**
   - **Current Limitation:** The current Minimax implementation relies heavily on evaluating the game tree to its terminal states. While this is feasible in Tic-Tac-Toe due to the small state space, it becomes computationally expensive in more complex games (like Chess or Go).
   - **Optimization:** Implement an advanced heuristic evaluation function that can estimate the utility of non-terminal game states more effectively. For example, in Tic-Tac-Toe, instead of simply counting potential winning lines, the evaluation function could consider the number of "two-in-a-row" configurations, the potential to block the opponent, and even the control of the center square, which is strategically important. This allows the algorithm to cut off the search at a certain depth while still making informed decisions based on the heuristic value of the current state.

2. **Dynamic Depth Adjustment:**
   - **Current Limitation:** The Minimax algorithm in this implementation could be enhanced by dynamically adjusting the depth of the search based on the current game state. Currently, the depth of search is implicit, given the relatively shallow nature of Tic-Tac-Toe's game tree.
   - **Optimization:** Implement a dynamic depth adjustment where the algorithm can search deeper in critical positions (e.g., when the game is near its end or in positions where a decisive move can be made) and use shallower searches in less critical situations. This would improve the AI's decision-making speed without compromising the quality of its moves.

3. **Iterative Deepening Search:**
   - **Current Limitation:** Minimax as implemented explores the game tree to a fixed depth or until terminal states are reached. However, this approach can be rigid and may not be the most time-efficient method in time-constrained environments.
   - **Optimization:** Implement iterative deepening search, which combines depth-first search's memory efficiency with the breadth-first search's completeness. The algorithm performs a series of depth-limited searches, gradually increasing the depth until time runs out or the entire tree is searched. This ensures that the best possible move found within the available time is chosen, which is particularly useful in games where decision time is limited.

4. **Move Ordering for Enhanced Alpha-Beta Pruning:**
   - **Current Limitation:** The efficiency of Alpha-Beta Pruning depends on the order in which moves are evaluated. In the current implementation, moves are evaluated in the order they are generated, which may not be optimal for pruning.
   - **Optimization:** Implement move ordering, where the AI first evaluates the moves that are most likely to result in a favorable outcome. By ordering moves intelligently (e.g., evaluating captures or checks first in Chess), Alpha-Beta Pruning can prune more branches early, further reducing the number of nodes that need to be explored.

5. **Transposition Tables (Caching):**
   - **Current Limitation:** The AI may evaluate the same position multiple times if it arises through different sequences of moves (a situation common in more complex games).
   - **Optimization:** Implement transposition tables, which cache the results of previously evaluated positions. By storing and reusing the results of these evaluations, the algorithm avoids redundant calculations, speeding up the decision-making process. This is particularly beneficial in games with a large state space and where the same positions frequently recur.

6. **Learning-Based Enhancements:**
   - **Current Limitation:** The current AI does not learn from previous games. It plays each game independently, without adapting its strategy based on past experiences.
   - **Optimization:** Incorporate learning-based techniques, such as reinforcement learning, where the AI can improve its strategy over time by learning from the outcomes of previous games. For example, using Q-learning or deep reinforcement learning, the AI could develop more nuanced strategies and adapt its play style to exploit the weaknesses of specific opponents.

### **Application to More Complex Games**
While these optimizations are discussed in the context of Tic-Tac-Toe, they are especially relevant for more complex games, such as Chess, Go, or Checkers. In these games, the state space is exponentially larger, and making efficient use of computational resources becomes crucial. By integrating these optimizations, an AI could handle more complex decision-making processes and perform at a level closer to human or even superhuman capability.
