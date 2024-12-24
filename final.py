import pygame
import random


# Color palette for the game
Beige = (245,245,220)  # Light color for chess board squares
Blue = (0, 119, 166)   # Darker color for chess board squares
Green = (191,255,0)    # Highlight color for white player's moves
Red = (210, 10, 46)    # Highlight color for black player's moves

# Screen and board configuration constants
width, height = 800, 900  # Total window size
ss = width//8  # Size of each chess square

# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ethan's Final Project") 



# Base Chess Piece class
class ChessPiece:
    def __init__(self, color, image):
        """
        Initialize a chess piece with its color and image
        :param color: Color of the piece (white/black)
        :param image: Path to the piece's image file
        """
        self.color = color
        # Load and scale the piece's image to fit a square
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (ss, ss))
        self.moved = False  # Track if the piece has moved (useful for special moves like castling)

# Specific piece classes inheriting from ChessPiece
class pawn(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)
class rook(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)
class bishop(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)
class knight(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)
class queen(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)
class king(ChessPiece): 
    def __init__(self, color, image):
        super().__init__(color, image)

# Initialize the chess board as a 2D list
game = [[0 for _ in range(8)] for _ in range(8)]

# Game flow variables
current_player = 'white'  # White starts first
clicked_piece = 0     # Currently selected chess piece
clicked_pos = 0       # Position of the selected piece
current_game_state = 0  # 0: Main menu, 1: Two-player game, 2: Bot game

def place_pieces():
    """
    Set up the initial chess board with all pieces in their starting positions
    """
    for col in range(8):
        game[1][col] = pawn('black', 'images/black pawn.png')
        game[6][col] = pawn('white', 'images/white pawn.png')
    game[0][0] = rook('black','images/black rook.png')
    game[0][7] = rook('black','images/black rook.png')
    game[7][0] = rook('white','images/white rook.png')
    game[7][7] = rook('white','images/white rook.png')
    game[0][1] = knight('black', 'images/black knight.png')
    game[0][6] = knight('black', 'images/black knight.png')
    game[7][1] = knight('white', 'images/white knight.png')
    game[7][6] = knight('white', 'images/white knight.png')
    game[0][2] = bishop('black', 'images/black bishop.png')
    game[0][5] = bishop('black', 'images/black bishop.png')
    game[7][2] = bishop('white', 'images/white bishop.png')
    game[7][5] = bishop('white', 'images/white bishop.png')
    game[0][3] = queen('black', 'images/black queen.png')
    game[7][3] = queen('white', 'images/white queen.png')
    game[0][4] = king('black', 'images/black king.png')
    game[7][4] = king('white', 'images/white king.png')

def draw_game():
    """
    Draw the main menu screen with game mode selection
    :return: Rectangles for two-player and bot mode buttons
    """
    screen.fill((0,0,0))
    
    # Load and scale king images for decoration
    image1 = pygame.image.load('images/black king.png')
    image1 = pygame.transform.scale(image1, (ss, ss))
    
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 60)
    button_font = pygame.font.SysFont('Arial', 40)
    
    # Render game title
    title = title_font.render("Ethan's Chess", True, (255,255,255))
    title_rect = title.get_rect(center=(width//2, 200))
    screen.blit(title, title_rect)
    
    # Draw decorative kings
    screen.blit(image1, (20, 200))
    screen.blit(image1, (width - ss - 20, 200))
    
    # Create Two-Player Button
    button_rect1 = pygame.Rect(width // 2 - 100, 400, 200, 100)
    pygame.draw.rect(screen, Blue, button_rect1)
    two_player_text = button_font.render("Two-Player", True, (0, 0, 0))
    text_rect1 = two_player_text.get_rect(center=button_rect1.center)
    screen.blit(two_player_text, text_rect1)
    
    # Create Easy Bot Button
    button_rect2 = pygame.Rect(width // 2 - 100, 600, 200, 100)
    pygame.draw.rect(screen, Blue, button_rect2)
    bot_text = button_font.render("Easy Bot", True, (0, 0, 0))
    text_rect2 = bot_text.get_rect(center=button_rect2.center)
    screen.blit(bot_text, text_rect2)
    
    return button_rect1, button_rect2

def draw_board():
    """
    Draw the chess board and game UI elements
    Highlights selected piece and shows valid moves
    """
    global current_game_state
    screen.fill((0,0,0))
    
    # Load game logo king
    image1 = pygame.image.load('images/black king.png')
    image1 = pygame.transform.scale(image1, (ss, ss))
    
    # Draw bottom UI bar
    pygame.draw.rect(screen, (255, 255, 255), (0, 800, 800, 400))
    font = pygame.font.SysFont('Arial', 60)
    title = font.render("Ethan's Chess", True, (0, 0, 0))
    screen.blit(title, (250, 812))
    screen.blit(image1 ,(20, 800))
    screen.blit(image1 ,(700, 800))

    # Draw chess board squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = Beige
            else:
                color = Blue
            pygame.draw.rect(screen, color, (col * ss, row * ss, ss, ss))

    # Highlight selected piece
    if clicked_pos:
        if current_game_state == 1:
            # Use different colors for white and black players
            if current_player == 'white':
                pygame.draw.rect(screen, Green, (clicked_pos[1] * ss, clicked_pos[0] * ss, ss, ss))
            elif current_player == 'black':
                pygame.draw.rect(screen, Red, (clicked_pos[1] * ss, clicked_pos[0] * ss, ss, ss))
    
    # Draw dots for valid moves of the selected piece
    if clicked_piece:
        if current_game_state == 1:
            # Different colored dots for each player
            if current_player == 'black':
                valid_moves = all_moves(clicked_piece, clicked_pos[0], clicked_pos[1])
                for move in valid_moves:
                    move_row, move_col = move
                    pygame.draw.circle(screen, Red, (move_col * ss + ss // 2, move_row * ss + ss // 2), 10)

            elif current_player == 'white':
                valid_moves = all_moves(clicked_piece, clicked_pos[0], clicked_pos[1])
                for move in valid_moves:
                    move_row, move_col = move
                    pygame.draw.circle(screen, Green, (move_col * ss + ss // 2, move_row * ss + ss // 2), 10)

    # Display checkmate message if enemy king is in check
    if is_enemy_king_in_check():
        font = pygame.font.SysFont('Arial', 60)
        text = font.render(f'Checkmate, {current_player.capitalize()} wins!', True, (255, 0, 0))  # Red color
        screen.blit(text, (100, 400))
        
        font_small = pygame.font.SysFont('Arial', 30)
        restart_text = font_small.render('Press ESC to Quit', True, (0, 255, 0))  # Green color
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 60))

def draw_piece():
    """
    Draw all chess pieces on the board
    """
    for row in range(8):
        for col in range(8):
            piece = game[row][col]
            if piece:
                screen.blit(piece.image,(col*ss, row*ss))

def all_moves(piece, row, col):
    """
    Determine valid moves for a specific piece
    :param piece: The chess piece to check moves for
    :param row: Current row of the piece
    :param col: Current column of the piece
    :return: List of valid move coordinates
    """
    moves = []

    def add_line_moves(directions):
        """
        Add moves in straight lines (used for rooks, bishops, and queens)
        """
        for row_change, col_change in directions:
            r, c = row + row_change, col + col_change
            while 0 <= r < 8 and 0 <= c < 8:
                if game[r][c] == 0 :
                    moves.append((r, c))
                elif game[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += row_change
                c += col_change

    def add_single_moves(deltas):
        """
        Add moves for pieces that move only one square (used for kings and knights)
        """
        for row_change, col_change in deltas:
            r, c = row + row_change, col + col_change
            if 0 <= r < 8 and 0 <= c < 8:
                if game[r][c] == 0 or game[r][c].color != piece.color:
                    moves.append((r, c))

    if isinstance(piece, pawn):
        # Pawn forward move
        direction = -1 if piece.color == 'white' else 1
        if 0 <= row + direction < 8 and game[row + direction][col] == 0:
            moves.append((row + direction, col))
            # Initial double move
            if not piece.moved and game[row + 2 * direction][col] == 0:
                moves.append((row + 2 * direction, col))

        # Pawn captures
        for col_change in [-1, 1]:
            r, c = row + direction, col + col_change
            if 0 <= r < 8 and 0 <= c < 8 and game[r][c] and game[r][c].color != piece.color:
                moves.append((r, c))

    elif isinstance(piece, rook):
        add_line_moves([(1, 0), (-1, 0), (0, 1), (0, -1)])

    elif isinstance(piece, bishop):
        add_line_moves([(1, 1), (1, -1), (-1, 1), (-1, -1)])

    elif isinstance(piece, queen):
        add_line_moves([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])

    elif isinstance(piece, knight):
        add_single_moves([(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)])

    elif isinstance(piece, king):
        add_single_moves([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])

    return moves

def is_enemy_king_in_check():
    """
    Check if the enemy king is in check (can be captured in the next move)
    :return: Boolean indicating if the enemy king is in check
    """
    # Find the enemy king's position
    if current_player == 'white':
        enemy_color = 'black' 
    else:
        enemy_color = 'white'
    enemy_king_pos = None

    for r in range(8):
        for c in range(8):
            piece = game[r][c]
            if piece and piece.color == enemy_color and isinstance(piece, king):
                enemy_king_pos = (r, c)
                break
        if enemy_king_pos:
            break

    if not enemy_king_pos:
        return False  # No enemy king found (should never happen)

    # Check if any of the current player's pieces can attack the enemy king
    for r in range(8):
        for c in range(8):
            piece = game[r][c]
            if piece and piece.color == current_player:
                if enemy_king_pos in all_moves(piece, r, c):
                    return True
    return False



def player_click(pos):
    global current_game_state
    """
    Handle mouse click events for different game states and piece interactions.
    
    Manages:
    - Main menu game mode selection
    - Piece selection and movement
    - Turn-based gameplay rules
    
    :param pos: Mouse click position (x, y coordinates)
    """
    global clicked_piece, clicked_pos, current_player, current_game_state

    # Handle main menu state
    if current_game_state == 0:
        _handle_menu_selection(pos)
        return

    # Convert screen coordinates to board coordinates
    col, row = pos[0] // ss, pos[1] // ss

    # First click - piece selection
    if clicked_piece == 0:
        _select_piece(row, col)
    else:
        # Second click - move piece or reset selection
        _handle_piece_movement(row, col)

def _handle_menu_selection(pos):
    global current_game_state
    """
    Handle game mode selection in main menu.
    
    :param pos: Mouse click position
    """
    button_rect1, button_rect2 = draw_game()
    
    if button_rect1.collidepoint(pos):
        # Two-Player mode
        place_pieces()
        
        current_game_state = 1
    
    elif button_rect2.collidepoint(pos):
        # Easy Bot mode
        place_pieces()
        
        current_game_state = 2

def _select_piece(row, col):
    """
    Select a piece for movement.
    
    :param row: Row of selected piece
    :param col: Column of selected piece
    """
    global clicked_piece, clicked_pos
    piece = game[row][col]
    
    # Only allow selecting pieces of the current player
    if piece and piece.color == current_player:
        clicked_piece = piece
        clicked_pos = (row, col)

def _handle_piece_movement(row, col):
    """
    Handle piece movement and turn switching.
    
    :param row: Destination row
    :param col: Destination column
    """
    global clicked_piece, clicked_pos, current_player
    
    # Check if the move is valid
    if (row, col) in all_moves(clicked_piece, clicked_pos[0], clicked_pos[1]):
        # Execute the move
        game[row][col] = clicked_piece
        game[clicked_pos[0]][clicked_pos[1]] = 0
        clicked_piece.moved = True

        # Switch player turns
        current_player = 'black' if current_player == 'white' else 'white'

    # Reset piece selection
    clicked_piece = 0
    clicked_pos = 0


def bot_move():
    """
    Implement bot's move strategy in single-player mode.
    
    Strategy:
    - Find all pieces of the current player (bot)
    - Filter to only pieces with valid moves
    - Randomly select a piece and a valid move
    - Execute the move
    - Handle pawn promotion
    - Switch turns
    """
    global current_player, clicked_piece, clicked_pos

    # Find all the bot's pieces with valid moves
    bot_pieces = []
    for row in range(8):
        for col in range(8):
            piece = game[row][col]
            if piece and piece.color == current_player:
                valid_moves = all_moves(piece, row, col)
                if valid_moves:  # Only include pieces that have valid moves
                    bot_pieces.append((piece, (row, col), valid_moves))

    # If no valid moves, return (game should handle end state)
    if not bot_pieces:
        return  # No valid moves for the bot (should trigger game end logic)

    # Randomly select a piece and a valid move
    clicked_piece, clicked_pos, valid_moves = random.choice(bot_pieces)
    target_move = random.choice(valid_moves)

    # Execute the move
    game[target_move[0]][target_move[1]] = clicked_piece
    game[clicked_pos[0]][clicked_pos[1]] = 0
    clicked_piece.moved = True

    # Check for pawn promotion
    if isinstance(clicked_piece, pawn) and (target_move[0] == 0 or target_move[0] == 7):
        game[target_move[0]][target_move[1]] = queen(clicked_piece.color, f'images/{clicked_piece.color} queen.png')

    # Switch turns
    if current_player == 'white':
        current_player = 'black' 
    else: 
        current_player ='white'


def run_game():

    """
    Main game loop that handles:
    - Event processing (quit, mouse clicks, key presses)
    - Game state management
    - Drawing game elements
    - Bot move execution
    - Display updates
    
    Game states:
    - 0: Main menu
    - 1: Two-player mode
    - 2: Single-player (bot) mode
    """

    # Initialize Pygame
    pygame.init()

    global current_game_state

    while True:
        # Process pygame events
        for mode in pygame.event.get():
            if mode.type == pygame.QUIT:
                pygame.quit()
            
            elif mode.type == pygame.MOUSEBUTTONDOWN:
                player_click(pygame.mouse.get_pos())
            
            elif mode.type == pygame.KEYDOWN:
                # Allow restarting or quitting from game over state
                if is_enemy_king_in_check():
                    if mode.key == pygame.K_ESCAPE:
                        current_game_state = 0

        # Render game based on current state
        if current_game_state == 0:
            # Main menu
            draw_game()
        elif current_game_state == 2:  # Single-player mode
            draw_board()
            draw_piece()
            if current_player == 'black':  # Bot's turn
                bot_move()
        else:
            # Two-player mode
            draw_board()
            draw_piece()

        # Update display
        pygame.display.flip()

run_game()