import random
import copy
import time
random.seed(109)

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1

        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('\nP1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i],
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i],
                        player_2_pits[-(i+1)], self.pits_per_player - i))

        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)

    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        if (pit >= 1 and pit <= self.pits_per_player):
            if self.current_player == 1:
                pit_index = pit - 1
            else:
                pit_index = self.pits_per_player + pit

            if self.board[pit_index] != 0:
                return True
        return False

    def all_valid_moves(self, sim_board, current_player):
        valid_moves = []

        if current_player == 1:
             for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                 if sim_board[i] > 0:  # If there are seeds in the pit
                     valid_moves.append(i + 1)

        elif current_player == 2:
            for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                if sim_board[i] > 0:  # If there are seeds in the pit
                   valid_moves.append(i - self.pits_per_player)  # Adjusting for Player 2's pits

        return valid_moves

    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """

        # write your code here
        valid_indexes = []
        if self.current_player == 1:
          for i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1, 1):
              if self.board[i] > 0: valid_indexes.append(i)

        elif self.current_player == 2:
          for i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1, 1):
              if self.board[i] > 0: valid_indexes.append(i)

        random_index = random.randint(0, len(valid_indexes) - 1)

        if self.current_player == 1:
          return valid_indexes[random_index] + 1
        else:
          return valid_indexes[random_index] - self.pits_per_player

    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        print(f"Player {self.current_player} chose pit: {pit}")

        if self.valid_move(pit):
            winner = self.winning_eval()
            if winner > 0:
                return winner

            else:
                self.moves.append((self.current_player, pit))

                if self.current_player == 2: pit = pit + self.p2_pits_index[0]

                num_stones = self.board[pit-1]
                self.board[pit-1] = 0

                i = pit
                while num_stones > 0:
                    if i > self.p2_mancala_index: i = 0
                    if self.current_player == 1 and i == self.p2_mancala_index:
                        i += 1
                        continue
                    elif self.current_player == 2 and i == self.p1_mancala_index:
                        i += 1
                        continue

                    if num_stones == 1 and self.board[i] == 0:
                      if self.current_player == 1 and i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1, 1):
                        opp_pit = self.p2_pits_index[1] - i
                        self.board[self.p1_mancala_index] += self.board[opp_pit] + 1
                        self.board[opp_pit] = 0
                      elif self.current_player == 2 and i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1, 1):
                        opp_pit = self.p2_pits_index[1] - i
                        self.board[self.p2_mancala_index] += self.board[opp_pit] + 1
                        self.board[opp_pit] = 0
                      else:
                        self.board[i] += 1
                    else:
                        self.board[i] += 1

                    num_stones -= 1
                    i += 1

        else:
            print("Invalid Move")
            return 0

        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

        return self.winning_eval()


    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        p1AllPitsEmpty, p2AllPitsEmpty = True, True

        # write your code here
        for i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1, 1):
            if self.board[i] > 0: p1AllPitsEmpty = False

        for i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1, 1):
            if self.board[i] > 0: p2AllPitsEmpty = False

        if p2AllPitsEmpty or p1AllPitsEmpty:
            if self.board[self.p1_mancala_index] > self.board[self.p2_mancala_index]:
                print("Player 1 Wins!")
                return 1
            elif self.board[self.p1_mancala_index] < self.board[self.p2_mancala_index]:
                print("Player 2 Wins!")
                return 2
            else:
                print("It's a Tie!")
                return 3

        return 0

    def play_simulation (self, pit, sim_board, sim_player):
        """
        This function simulates a single move made by a specific player using their selected pit. The sim_board is passed:
        """
        if sim_player == 2: pit += self.p2_pits_index[0]

        num_stones = sim_board[pit-1]

        sim_board[pit -1] = 0
        i = pit
        while num_stones > 0:
            if i > self.p2_mancala_index: i = 0
            if sim_player == 1 and i == self.p2_mancala_index:
                i += 1
                continue
            elif sim_player == 2 and i == self.p1_mancala_index:
                i += 1
                continue

            if num_stones == 1 and sim_board[i] == 0:
              if sim_player == 1 and i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1, 1):
                opp_pit = self.p2_pits_index[1] - i
                sim_board[self.p1_mancala_index] += sim_board[opp_pit] + 1
                sim_board[opp_pit] = 0
              elif sim_player == 2 and i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1, 1):
                opp_pit = self.p2_pits_index[1] - i
                sim_board[self.p2_mancala_index] += sim_board[opp_pit] + 1
                sim_board[opp_pit] = 0
              else:
                sim_board[i] += 1

            else:
                sim_board[i] += 1

            num_stones -= 1
            i += 1

        return sim_board

    def sim_winning_eval(self, sim_board):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        p1AllPitsEmpty, p2AllPitsEmpty = True, True

        # write your code here
        for i in range(self.p1_pits_index[0], self.p1_pits_index[1]+1, 1):
            if sim_board[i] > 0: p1AllPitsEmpty = False

        for i in range(self.p2_pits_index[0], self.p2_pits_index[1]+1, 1):
            if sim_board[i] > 0: p2AllPitsEmpty = False

        if p2AllPitsEmpty or p1AllPitsEmpty:
            if sim_board[self.p1_mancala_index] > sim_board[self.p2_mancala_index]:
                return 1
            elif sim_board[self.p1_mancala_index] < sim_board[self.p2_mancala_index]:
                return 2
            else:
                return 3

        return 0


    def utility(self, sim_board):
      """
      Calculates how good a state is, by taking the difference in mancala scores.
      """
      utility = sim_board[self.p1_mancala_index] - sim_board[self.p2_mancala_index]
      return utility

    def minimax_decision(self, state, depth):
      """
      kickstarts minimax, and returns the best move possible
      """
      (_, pit) = self.max_value(state, depth, self.current_player)
      return pit

    def min_value(self, state, depth, sim_player):
      """
      finds the min value for each action in a particular state
      """
      if self.sim_winning_eval(state) > 0 or depth <= 0:
        return (self.utility(state), -1)
      best_value = float('inf')
      best_action = None
      for action in self.all_valid_moves(state, sim_player):
        sim_board = copy.deepcopy(state)
        sim_board = self.play_simulation(action, sim_board, sim_player)
        next_player = 1 if sim_player == 2 else 2
        value, result = self.max_value(sim_board, depth - 1, next_player)

        if value < best_value:
          best_value = value
          best_action = action

      return (best_value, best_action)

    def max_value(self, state, depth, sim_player):
      """
      finds the max value for each action in a particular state
      """
      if self.sim_winning_eval(state) > 0 or depth <= 0:
        return (self.utility(state), -1)

      best_value = -float('inf')
      best_action = None
      for action in self.all_valid_moves(state, sim_player):
        sim_board = copy.deepcopy(state)
        sim_board = self.play_simulation(action, sim_board, sim_player)
        next_player = 2 if sim_player == 1 else 1
        value, result = self.min_value(sim_board, depth - 1, next_player)

        if value > best_value:
          best_value = value
          best_action = action

      return (best_value, best_action)

    def alpha_beta_decision(self, state, depth):
        """
        kickstarts alpha beta pruning, and returns the best move possible
        """
        alpha = float('-inf')
        beta = float('inf')
        (_, pit) = self.a_b_max_value(state, depth, self.current_player, alpha, beta)
        return pit


    def a_b_min_value(self, state, depth, sim_player, alpha, beta):
      """
      finds the min value for each action in a particular state, and prunes if necessary
      """
      if self.sim_winning_eval(state) > 0 or depth <= 0:
        return (self.utility(state), -1)
      best_value = float('inf')
      best_action = None
      for action in self.all_valid_moves(state, sim_player):
        sim_board = copy.deepcopy(state)

        # play action
        sim_board = self.play_simulation(action, sim_board, sim_player)
        next_player = 1 if sim_player == 2 else 2
        value, result = self.a_b_max_value(sim_board, depth - 1, next_player, alpha, beta)

        if value < best_value:
          best_value = value
          best_action = action

        #  if best value(beta) <= alphax, prune
        if best_value <= alpha:
          return (best_value, best_action)

        # otherwise keep going
        beta = min(beta, best_value)

      return (best_value, best_action)

    def a_b_max_value(self, state, depth, sim_player, alpha, beta):
      """
      finds the max value for each action in a particular state, and prunes if necessary
      """
      if self.sim_winning_eval(state) > 0 or depth <= 0:
        return (self.utility(state), -1)

      best_value = -float('inf')
      best_action = None
      for action in self.all_valid_moves(state, sim_player):
        sim_board = copy.deepcopy(state)
        sim_board = self.play_simulation(action, sim_board, sim_player)
        next_player = 2 if sim_player == 1 else 1
        value, result = self.a_b_min_value(sim_board, depth - 1, next_player, alpha, beta)

        if value > best_value:
          best_value = value
          best_action = action

        # if best value(alpha) >= beta, prune
        if best_value >= beta:
          return (best_value, best_action)

        # otherwise keep going
        alpha = max(alpha, best_value)

      return (best_value, best_action)


def playRandomGame(game_count):
  game = Mancala(6,4)

  turn_count = 0
  winner = 0
  while(winner < 1):
    print(f"Game #{game_count}, Turn #{turn_count}")
    # Random player
    random_play = game.random_move_generator()
    # Player 1
    winner = game.play(random_play)
    game.display_board()
    turn_count += 1

  return winner, turn_count

# Mancala part 2
game2 = Mancala(6,4)

game2.display_board()

game_count = 0
total_turn_count = 0
player_1_wins = 0
player_2_wins = 0
ties = 0

while (game_count < 100):
  winner, turns = playRandomGame(game_count)
  if winner == 1: player_1_wins += 1
  elif winner == 2: player_2_wins += 1
  else: ties += 1

  game_count += 1
  total_turn_count += turns

average_turns = total_turn_count / game_count
print(f"Player 1 wins: {player_1_wins}")
print(f"Player 2 wins: {player_2_wins}")
print(f"Ties: {ties}")
print(f"Average turns per game: {average_turns}")


def playMinimax(game_count, depth):
  game = Mancala(6,4)

  turn_count = 0
  winner = 0
  while(winner < 1):
    print(f"Game #{game_count}, Turn #{turn_count}")
    # Alternating player
    if turn_count % 2 == 0:
      sim_board = copy.deepcopy(game.board)
      move = game.minimax_decision(sim_board, depth)
    else:
      move = game.random_move_generator()
    winner = game.play(move)
    game.display_board()
    turn_count += 1

  return winner, turn_count

game_count = 0
total_turn_count = 0
player_1_wins = 0
player_2_wins = 0
ties = 0

start_time = time.time()

while (game_count < 100):
  winner, turns = playMinimax(game_count, 5)
  if winner == 1: player_1_wins += 1
  elif winner == 2: player_2_wins += 1
  else: ties += 1

  game_count += 1
  total_turn_count += turns


average_turns = total_turn_count / game_count
print(f"Player 1 wins: {player_1_wins}")
print(f"Player 2 wins: {player_2_wins}")
print(f"Ties: {ties}")
print(f"Average turns per game: {average_turns}")

end_time = time.time()

total_runtime = end_time - start_time
print(f"Total runtime: {total_runtime:.2f} seconds")


def playAlphaBeta(game_count, depth):
  game = Mancala(6,4)

  turn_count = 0
  winner = 0
  while(winner < 1):
    print(f"Game #{game_count}, Turn #{turn_count}")
    # Alternating player
    if turn_count % 2 == 0:
      sim_board = copy.deepcopy(game.board)
      move = game.alpha_beta_decision(sim_board, depth)
    else:
      move = game.random_move_generator()
    winner = game.play(move)
    game.display_board()
    turn_count += 1

  return winner, turn_count

game_count = 0
total_turn_count = 0
player_1_wins = 0
player_2_wins = 0
ties = 0

start_time = time.time()

while (game_count < 100):
  winner, turns = playAlphaBeta(game_count, 5)
  if winner == 1: player_1_wins += 1
  elif winner == 2: player_2_wins += 1
  else: ties += 1

  game_count += 1
  total_turn_count += turns


average_turns = total_turn_count / game_count
print(f"Player 1 wins: {player_1_wins}")
print(f"Player 2 wins: {player_2_wins}")
print(f"Ties: {ties}")
print(f"Average turns per game: {average_turns}")

end_time = time.time()

total_runtime = end_time - start_time
print(f"Total runtime: {total_runtime:.2f} seconds")


game_count = 0
total_turn_count = 0
player_1_wins = 0
player_2_wins = 0
ties = 0

start_time = time.time()

while (game_count < 100):
  winner, turns = playAlphaBeta(game_count, 10)
  if winner == 1: player_1_wins += 1
  elif winner == 2: player_2_wins += 1
  else: ties += 1

  game_count += 1
  total_turn_count += turns


average_turns = total_turn_count / game_count
print(f"Player 1 wins: {player_1_wins}")
print(f"Player 2 wins: {player_2_wins}")
print(f"Ties: {ties}")
print(f"Average turns per game: {average_turns}")

end_time = time.time()

total_runtime = end_time - start_time
print(f"Total runtime: {total_runtime:.2f} seconds")
