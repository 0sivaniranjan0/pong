import pygame
import random
import math

#  Initialize Pygame Modules 
# We initialize here so the font and sound modules are ready
pygame.font.init()
pygame.mixer.init()

# Game Constants 
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
BALL_RADIUS = 8
WINNING_SCORE = 10

# Asset Loading 
try:
    SCORE_FONT = pygame.font.Font('data/font/chilispepper.ttf', 36)
    icon = pygame.image.load("data/images/icon/ping-pong.png")
    hit_sound = pygame.mixer.Sound("data/sounds/Bounce.wav")
    score_sound = pygame.mixer.Sound("data/sounds/score.wav")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    print("Please ensure the 'data' folder is in the correct location.")
    
    SCORE_FONT = pygame.font.SysFont('Arial', 36) # Default system font
    icon = pygame.Surface((32, 32)) # Empty surface
    icon.fill((255, 0, 255))  # Magenta placeholder
    class DummySound:
        def play(self): pass
    hit_sound = DummySound()
    score_sound = DummySound()


# Game Classes 

class Paddle:
    """Represents a player's paddle."""
    COLOR = WHITE
    VEL = HEIGHT // 100  # Velocity scaled to screen height

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, window):
        """Draws the paddle on the window."""
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        """Moves the paddle up or down."""
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
        
        # Clamp paddle to screen
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def reset(self):
        """Resets the paddle to its original position."""
        self.y = self.original_y

class Ball:
    """Represents the game ball."""
    COLOR = WHITE
    VEL = 4
    ACC = 0.5  # Acceleration factor on hit

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.vel_x = self.VEL
        self.vel_y = 0
        self.color = self.COLOR

    def draw(self, window):
        """Draws the ball on the window."""
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        """Updates the ball's position based on its velocity."""
        self.x += self.vel_x
        self.y += self.vel_y

    def reset(self):
        """Resets the ball to the center and reverses its direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.vel_y = 0
        self.vel_x *= -1  # Reverse direction for the next serve
        self.color = self.COLOR


# Game Logic Functions 

def draw_game(window, paddles, ball, left_score, right_score, START):
    """Draws all game elements to the screen."""
    window.fill(BLACK)
    
    # Draw scores
    left_score_text = SCORE_FONT.render(str(left_score), True, WHITE)
    right_score_text = SCORE_FONT.render(str(right_score), True, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    # Draw paddles
    for paddle in paddles:
        paddle.draw(window)
         
    # Draw dashed center line
    for i in range(0, HEIGHT, HEIGHT // 19):
        if i % 2 == 0:
            pygame.draw.rect(window, WHITE, (WIDTH // 2 - 1, i, 2, HEIGHT // 30))

    # Draw ball
    ball.draw(window)
    
    if not START:
        start_text = SCORE_FONT.render("Press Space to Play", True, WHITE)
        window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))


    pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    """Moves paddles based on key presses."""
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

def handle_ball_collision(ball, left_paddle, right_paddle):
    """
    Handles ball collisions with walls and paddles.
    Returns 'left' or 'right' if a player scores, None otherwise.
    """
    # Top and bottom wall collision
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT:
        ball.vel_y = -ball.vel_y
        hit_sound.play()
    
    # Paddle collisions
    if ball.vel_x < 0:  # Ball moving left
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.vel_x = -ball.vel_x
                
                # Calculate bounce angle
                middle = left_paddle.y + left_paddle.height / 2
                difference_in_y = ball.y - middle
                reduction_factor = (left_paddle.height / 2) / ball.VEL
                vel_y = difference_in_y / reduction_factor
                ball.vel_y = vel_y + vel_y * ball.ACC
                
                hit_sound.play()
                new_color = tuple(random.randint(100, 255) for _ in range(3))
                ball.color = new_color

    else:  # Ball moving right
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.vel_x = -ball.vel_x

                # Calculate bounce angle
                middle = right_paddle.y + right_paddle.height / 2
                difference_in_y = ball.y - middle
                reduction_factor = (right_paddle.height / 2) / ball.VEL
                vel_y = difference_in_y / reduction_factor
                ball.vel_y = vel_y + vel_y * ball.ACC
                
                hit_sound.play()
                new_color = tuple(random.randint(100, 255) for _ in range(3))
                ball.color = new_color

    # Check for scoring
    if ball.x - ball.radius <= 0:  # Right player scores
        return "right"
    if ball.x + ball.radius >= WIDTH:  # Left player scores
        return "left"
    
    return None