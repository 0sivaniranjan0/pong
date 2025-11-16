import pygame
# Import all our game classes, constants, and functions from pong.py
from pong import *

def main():
    """Main game loop."""
    
    # Pygame Setup
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ping-Pong")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    #  Game State Variables
    left_score = 0
    right_score = 0
    bg_color = BLACK
    START = False  # Game starts paused
    running = True

    # Create Game Objects 
    left_paddle = Paddle(5, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 5 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddles = [left_paddle, right_paddle]
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Main Game Loop 
    while running:
        clock.tick(FPS)

        # Event Handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not START:
                    START = True

        # Game Logic 
        
        # Don't move anything if the game hasn't started
        if START:
            ball.move()
            score_side= handle_ball_collision(ball, left_paddle, right_paddle)
            
            if bg_color is None:
                bg_color = BLACK

            if score_side:
                START = False  # Pause the game
                ball.reset()
                if score_side == "left":
                    left_score += 1
                elif score_side == "right":
                    right_score += 1
                score_sound.play()

        # Paddle movement is always allowed
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        # Drawing 
        draw_game(WINDOW, paddles, ball, left_score, right_score, START)

        # Win Condition 
        win_text = ""
        if left_score >= WINNING_SCORE:
            win_text = "Left Player Wins!"
        elif right_score >= WINNING_SCORE:
            win_text = "Right Player Wins!"

        if win_text:
            START = False  # Stop the game
            text = SCORE_FONT.render(win_text, True, WHITE)
            WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)  # Show win message for 3 seconds
            
            # Reset game
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == "__main__":
    main()
