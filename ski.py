import pygame
import random
import sys
import os # Needed for high score file path

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 30  # Collision width
PLAYER_HEIGHT = 50 # Collision height
PLAYER_DRAW_WIDTH = 40 # Width of the drawing surface (includes skis)
PLAYER_DRAW_HEIGHT = 55 # Height of the drawing surface (includes skis/poles)
PLAYER_BODY_HEIGHT = 35
PLAYER_SKI_LENGTH = PLAYER_DRAW_WIDTH # Make skis fit drawing width
PLAYER_POLE_LENGTH = 30
PLAYER_SPEED = 7
OBSTACLE_WIDTH = 30 # Base width for trees
OBSTACLE_HEIGHT = 40 # Base height for trees
FLAG_POLE_WIDTH = 5
FLAG_TRIANGLE_WIDTH = 25 # Width of the flag triangle part
FLAG_IMAGE_WIDTH = FLAG_TRIANGLE_WIDTH + FLAG_POLE_WIDTH # Total width of flag image's surface
FLAG_HEIGHT = 30 # Height of the flag triangle + pole
INITIAL_SCROLL_SPEED = 4  # Initial speed obstacles move up
SPEED_INCREASE_PERCENT = 0.10 # Increase speed by 10%
GATE_PADDING = 25 # Minimum extra space on each side of the player within a gate
HIGH_SCORE_FILE = "horace_high_scores.txt"
NUM_HIGH_SCORES_DISPLAY = 3
NUM_HIGH_SCORES_STORE = 10 # Store more than displayed

# Game States
STATE_START_SCREEN = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)      # Flag color 1
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 200)     # Player Body
DARK_BLUE = (0, 0, 139)
GREEN = (0, 180, 0)    # Flag color 2 / Tree color 1
DARK_GREEN = (0, 100, 0) # Tree color 2
BROWN = (139, 69, 19)  # Tree trunk / Poles
GREY = (128, 128, 128) # Skis / Snow dots
SKY_BLUE = (135, 206, 235) # Background base
MOUNTAIN_COLOR_FAR = (160, 160, 180) # Distant mountains
MOUNTAIN_COLOR_NEAR = (130, 130, 150) # Closer hills
# SNOW_COLOR = (240, 240, 250) # Ground snow color - Removing solid fill
CLOUD_COLOR = (255, 255, 255, 160) # White clouds with alpha

# --- Utility Functions ---

def load_high_scores():
    """Loads high scores from the file."""
    scores = []
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            for line in f:
                try:
                    scores.append(int(line.strip()))
                except ValueError:
                    print(f"Warning: Skipping invalid score line: {line.strip()}")
        scores.sort(reverse=True)
        return scores[:NUM_HIGH_SCORES_STORE]
    except IOError as e:
        print(f"Error loading high scores: {e}")
        return []

def save_high_scores(new_score, scores_list):
    """Adds a new score, sorts, keeps top N, and saves to file."""
    scores_list.append(new_score)
    scores_list.sort(reverse=True)
    scores_list = scores_list[:NUM_HIGH_SCORES_STORE]
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            for score in scores_list:
                f.write(f"{score}\n")
        return scores_list
    except IOError as e:
        print(f"Error saving high scores: {e}")
        return scores_list


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """Represents the player character (Horace) with skis and poles. Includes animation."""
    def __init__(self):
        super().__init__()
        self.image_straight = self._create_player_image("straight")
        self.image_left = self._create_player_image("left")
        self.image_right = self._create_player_image("right")
        self.image = self.image_straight
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed_x = 0
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def _create_player_image(self, direction):
        # (Drawing code remains the same as previous version)
        image = pygame.Surface([PLAYER_DRAW_WIDTH, PLAYER_DRAW_HEIGHT], pygame.SRCALPHA)
        body_width = PLAYER_WIDTH * 0.8
        body_x_offset = (PLAYER_DRAW_WIDTH - body_width) // 2
        body_rect = pygame.Rect(body_x_offset, 5, body_width, PLAYER_BODY_HEIGHT)
        pygame.draw.rect(image, BLUE, body_rect, border_radius=5)
        ski_y = PLAYER_BODY_HEIGHT
        ski_thickness = 4
        pole_thickness = 3
        pole_start_x = body_rect.centerx
        pole_start_y = body_rect.centery
        pole_end_y = PLAYER_DRAW_HEIGHT - 5
        if direction == "straight":
            pygame.draw.line(image, GREY, (0, ski_y), (PLAYER_DRAW_WIDTH, ski_y), ski_thickness)
            pygame.draw.line(image, GREY, (0, ski_y + 8), (PLAYER_DRAW_WIDTH, ski_y + 8), ski_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x - 15, pole_end_y), pole_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x + 15, pole_end_y), pole_thickness)
        elif direction == "left":
            pygame.draw.line(image, GREY, (0, ski_y - 2), (PLAYER_DRAW_WIDTH - 5, ski_y + 5), ski_thickness)
            pygame.draw.line(image, GREY, (5, ski_y + 6), (PLAYER_DRAW_WIDTH, ski_y + 13), ski_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x - 20, pole_end_y), pole_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x + 10, pole_end_y), pole_thickness)
        elif direction == "right":
            pygame.draw.line(image, GREY, (5, ski_y + 5), (PLAYER_DRAW_WIDTH, ski_y - 2), ski_thickness)
            pygame.draw.line(image, GREY, (0, ski_y + 13), (PLAYER_DRAW_WIDTH - 5, ski_y + 6), ski_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x - 10, pole_end_y), pole_thickness)
            pygame.draw.line(image, BROWN, (pole_start_x, pole_start_y), (pole_start_x + 20, pole_end_y), pole_thickness)
        return image

    def reset_position(self):
        """Resets player to starting position."""
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed_x = 0
        self.image = self.image_straight
        self.image_rect.center = self.rect.center

    def update(self):
        # (Update logic remains the same)
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        if keys[pygame.K_LEFT]: self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]: self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.speed_x < 0: self.image = self.image_left
        elif self.speed_x > 0: self.image = self.image_right
        else: self.image = self.image_straight
        self.image_rect.center = self.rect.center

    def draw(self, surface):
        surface.blit(self.image, self.image_rect)

# --- Obstacle Class (Trees) ---
class Obstacle(pygame.sprite.Sprite):
    """Represents obstacles (trees) with varied graphics."""
    def __init__(self, x, y, speed):
        # (Init code remains the same)
        super().__init__()
        self.speed_y = speed
        tree_type = random.choice(['pine1', 'pine2'])
        self.image = pygame.Surface([OBSTACLE_WIDTH, OBSTACLE_HEIGHT], pygame.SRCALPHA)
        trunk_height = 10
        trunk_width = 8
        foliage_height = OBSTACLE_HEIGHT - trunk_height
        trunk_rect = pygame.Rect((OBSTACLE_WIDTH - trunk_width) // 2, foliage_height, trunk_width, trunk_height)
        pygame.draw.rect(self.image, BROWN, trunk_rect)
        if tree_type == 'pine1':
            color = GREEN
            points = [(OBSTACLE_WIDTH // 2, 0), (0, foliage_height), (OBSTACLE_WIDTH, foliage_height)]
            pygame.draw.polygon(self.image, color, points)
        elif tree_type == 'pine2':
            color = DARK_GREEN
            points = [(OBSTACLE_WIDTH // 2, 5), (0, foliage_height), (OBSTACLE_WIDTH, foliage_height)]
            pygame.draw.polygon(self.image, color, points)
            points_top = [(OBSTACLE_WIDTH // 2, 0), (OBSTACLE_WIDTH * 0.25, 10), (OBSTACLE_WIDTH * 0.75, 10)]
            pygame.draw.polygon(self.image, color, points_top)
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self, current_speed):
        """Move the obstacle up the screen based on current game speed."""
        self.speed_y = current_speed
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Flag Class ---
class Flag(pygame.sprite.Sprite):
    """Represents flags (poles with triangles) to ski between."""
    def __init__(self, x, y, color, speed, is_left):
        # (Init code remains the same)
        super().__init__()
        self.speed_y = speed
        self.passed = False
        self.is_left = is_left
        self.image = pygame.Surface([FLAG_IMAGE_WIDTH, FLAG_HEIGHT], pygame.SRCALPHA)
        pole_x = FLAG_TRIANGLE_WIDTH if is_left else 0
        pole_rect = pygame.Rect(pole_x, 0, FLAG_POLE_WIDTH, FLAG_HEIGHT)
        pygame.draw.rect(self.image, BLACK, pole_rect)
        triangle_base_y = 5
        triangle_height = FLAG_HEIGHT - 10
        triangle_tip_x = 0 if is_left else FLAG_IMAGE_WIDTH
        triangle_base_x = pole_x + (FLAG_POLE_WIDTH // 2)
        triangle_points = [(triangle_base_x, triangle_base_y), (triangle_base_x, triangle_base_y + triangle_height), (triangle_tip_x, triangle_base_y + triangle_height // 2)]
        pygame.draw.polygon(self.image, color, triangle_points)
        self.rect = self.image.get_rect()
        if is_left: self.rect.topleft = (x - FLAG_TRIANGLE_WIDTH, y)
        else: self.rect.topright = (x + FLAG_TRIANGLE_WIDTH, y)

    def update(self, current_speed):
        """Move the flag up the screen based on current game speed."""
        self.speed_y = current_speed
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Parallax Background Layer ---
class ParallaxLayer:
    """Represents a single layer for parallax scrolling."""
    def __init__(self, image, speed_factor):
        self.image = image
        self.speed_factor = speed_factor
        self.height = self.image.get_height()
        # Ensure height is at least screen height for proper tiling
        if self.height < SCREEN_HEIGHT:
             print(f"Warning: Parallax image height ({self.height}) is less than screen height ({SCREEN_HEIGHT}). May cause gaps.")
             # Optionally resize or tile the image here if needed, but for now just warn.
        self.y1 = 0
        self.y2 = -self.height # Position second image directly above the first

    def update(self, scroll_speed):
        """Updates the layer's position."""
        move_speed = scroll_speed * self.speed_factor
        self.y1 += move_speed
        self.y2 += move_speed

        # If an image has scrolled completely below the screen bottom, reset its position above the other one
        if self.y1 >= self.height:
            self.y1 = self.y2 - self.height
        if self.y2 >= self.height:
            self.y2 = self.y1 - self.height

        # Also handle scrolling up (less common but possible if speed reverses)
        if self.y1 <= -self.height:
             self.y1 = self.y2 + self.height
        if self.y2 <= -self.height:
             self.y2 = self.y1 + self.height


    def draw(self, surface):
        """Draws the layer (two copies for seamless scrolling)."""
        surface.blit(self.image, (0, int(self.y1)))
        surface.blit(self.image, (0, int(self.y2)))

# --- Game Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horace Skis Again! - Clouds!")
clock = pygame.time.Clock()
# Fonts
title_font = pygame.font.Font(None, 80)
score_font = pygame.font.Font(None, 36)
info_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 74)
restart_font = pygame.font.Font(None, 50)

# --- Create Parallax Background Layers ---
# Layer 1: Distant Mountains (slowest)
bg_layer1_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_layer1_surf.fill(SKY_BLUE) # Base sky
pygame.draw.polygon(bg_layer1_surf, MOUNTAIN_COLOR_FAR, [(0, 400), (200, 150), (450, 300), (600, 100), (SCREEN_WIDTH, 350), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
parallax_layer1 = ParallaxLayer(bg_layer1_surf, 0.1)

# Layer 2: Closer Hills (medium speed)
bg_layer2_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Transparent surface
pygame.draw.polygon(bg_layer2_surf, MOUNTAIN_COLOR_NEAR, [(0, 500), (150, 300), (350, 450), (550, 250), (700, 480), (SCREEN_WIDTH, 400), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
parallax_layer2 = ParallaxLayer(bg_layer2_surf, 0.3)

# Layer 3: Snow Ground Texture (fastest - same speed as obstacles)
# *** MODIFIED: Use transparent surface with dots ***
bg_layer3_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# bg_layer3_surf.fill(SNOW_COLOR) # Remove solid fill
# Draw some random dots for texture
for _ in range(200): # Adjust number of dots for density
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    radius = random.randint(1, 2)
    pygame.draw.circle(bg_layer3_surf, GREY, (x, y), radius)
parallax_layer3 = ParallaxLayer(bg_layer3_surf, 1.0) # Scrolls at base speed

# *** NEW: Layer 4: Clouds (Foreground) ***
bg_layer4_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
# Draw some random cloud shapes (overlapping circles)
for _ in range(15): # Number of cloud puffs
    center_x = random.randint(0, SCREEN_WIDTH)
    center_y = random.randint(0, SCREEN_HEIGHT // 2) # Clouds higher up
    base_radius = random.randint(20, 50)
    # Draw a few overlapping circles for one cloud puff
    for i in range(random.randint(3, 6)):
        offset_x = random.randint(-base_radius // 2, base_radius // 2)
        offset_y = random.randint(-base_radius // 2, base_radius // 2)
        radius = random.randint(base_radius // 2, base_radius)
        pygame.draw.circle(bg_layer4_surf, CLOUD_COLOR, (center_x + offset_x, center_y + offset_y), radius)
parallax_layer4_clouds = ParallaxLayer(bg_layer4_surf, 1.2) # Faster than ground speed

# Order layers for drawing (back to front, clouds separate for foreground)
background_parallax_layers = [parallax_layer1, parallax_layer2, parallax_layer3]
foreground_parallax_layers = [parallax_layer4_clouds]


# --- Sprite Groups ---
all_game_sprites = pygame.sprite.Group() # Sprites active during gameplay (player, obstacles, flags)
obstacles = pygame.sprite.Group()
flags = pygame.sprite.Group()

# Create the player (will be added to group when game starts)
player = Player()

# --- Game Variables ---
game_state = STATE_START_SCREEN
score = 0
last_score = None # Initialize last_score
high_scores = load_high_scores()
current_scroll_speed = INITIAL_SCROLL_SPEED
next_speed_increase_threshold = 100 # Score needed for next speed increase
last_obstacle_spawn_time = 0
obstacle_spawn_delay = 800

# --- Function to Reset Game ---
def reset_game():
    """Resets game variables and sprites for a new game."""
    global score, current_scroll_speed, next_speed_increase_threshold, last_obstacle_spawn_time
    score = 0
    current_scroll_speed = INITIAL_SCROLL_SPEED
    next_speed_increase_threshold = 100
    last_obstacle_spawn_time = pygame.time.get_ticks() # Reset spawn timer
    all_game_sprites.empty()
    obstacles.empty()
    flags.empty()
    player.reset_position()
    all_game_sprites.add(player)

# --- Function to Draw Start Screen ---
def draw_start_screen(surface, scores, last):
    # (Drawing code remains the same)
    surface.fill(SKY_BLUE)
    title_text = title_font.render("Horace Skis Again!", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.2))
    surface.blit(title_text, title_rect)
    instr1 = info_font.render("Use Left/Right Arrows to Steer", True, DARK_BLUE)
    instr2 = info_font.render("Ski Between Flags (Green/Red) for Points", True, DARK_BLUE)
    instr3 = info_font.render("Avoid the Trees!", True, DARK_RED)
    instr4 = info_font.render("Press ENTER to Start", True, BLACK)
    surface.blit(instr1, instr1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.4)))
    surface.blit(instr2, instr2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.45)))
    surface.blit(instr3, instr3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.5)))
    surface.blit(instr4, instr4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.85)))
    hs_title = score_font.render("High Scores:", True, BLACK)
    surface.blit(hs_title, hs_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.6)))
    y_offset = SCREEN_HEIGHT * 0.65
    for i, sc in enumerate(scores[:NUM_HIGH_SCORES_DISPLAY]):
        hs_text = info_font.render(f"{i+1}. {sc}", True, BLACK)
        surface.blit(hs_text, hs_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30)))
    if last is not None:
        last_text = info_font.render(f"Last Score: {last}", True, BLACK)
        surface.blit(last_text, last_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.78)))


# --- Function to Draw Game Over Screen ---
def draw_game_over_screen(surface, current_score):
    # (Drawing code remains the same)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, DARK_RED)
    score_text = score_font.render(f"Final Score: {current_score}", True, WHITE)
    restart_text = restart_font.render("Press 'R' to Restart", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    surface.blit(game_over_text, game_over_rect)
    surface.blit(score_text, score_rect)
    surface.blit(restart_text, restart_rect)


# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == STATE_START_SCREEN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = STATE_PLAYING
            elif game_state == STATE_PLAYING:
                pass # Player handles keys in update
            elif game_state == STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    # Reset last_score when going back to start screen *after* a game over
                    # last_score = 0 # Or keep it to show on start screen? Keep it.
                    game_state = STATE_START_SCREEN


    # --- Game Logic ---
    if game_state == STATE_PLAYING:
        # Spawn obstacles
        # (Spawning logic remains the same)
        now = pygame.time.get_ticks()
        if now - last_obstacle_spawn_time > obstacle_spawn_delay:
            last_obstacle_spawn_time = now
            spawn_type = random.random()
            if spawn_type < 0.45: # Tree
                tree_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
                tree = Obstacle(tree_x, -OBSTACLE_HEIGHT, current_scroll_speed)
                obstacles.add(tree)
                all_game_sprites.add(tree)
            elif spawn_type < 0.9: # Flag pair
                min_actual_gap = PLAYER_WIDTH + 2 * GATE_PADDING
                max_actual_gap = 350
                actual_gap = random.randint(min_actual_gap, max_actual_gap)
                min_center = FLAG_IMAGE_WIDTH + actual_gap // 2
                max_center = SCREEN_WIDTH - FLAG_IMAGE_WIDTH - actual_gap // 2
                if min_center < max_center:
                    gap_center_x = random.randint(min_center, max_center)
                    left_flag_inner_x = gap_center_x - actual_gap // 2
                    right_flag_inner_x = gap_center_x + actual_gap // 2
                    left_flag = Flag(left_flag_inner_x, -FLAG_HEIGHT, GREEN, current_scroll_speed, is_left=True)
                    right_flag = Flag(right_flag_inner_x, -FLAG_HEIGHT, DARK_RED, current_scroll_speed, is_left=False)
                    flags.add(left_flag, right_flag)
                    all_game_sprites.add(left_flag, right_flag)

        # Update Player
        player.update()

        # Update Obstacles and Flags
        obstacles.update(current_scroll_speed)
        flags.update(current_scroll_speed)

        # Update Parallax Backgrounds (including clouds)
        for layer in background_parallax_layers:
            layer.update(current_scroll_speed)
        for layer in foreground_parallax_layers:
            layer.update(current_scroll_speed) # Clouds scroll based on game speed too

        # --- Collision Detection ---
        # (Collision logic remains the same)
        # Trees
        tree_hits = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_rect_ratio(0.8))
        if tree_hits:
            print("Hit a tree! Game Over.")
            last_score = score
            high_scores = save_high_scores(score, high_scores)
            game_state = STATE_GAME_OVER
        # Flags
        processed_flags = set()
        for flag in flags:
            if flag in processed_flags or game_state == STATE_GAME_OVER: continue
            if not flag.passed and player.rect.centery > flag.rect.top and player.rect.centery < flag.rect.bottom:
                 pair_flag = None
                 potential_pairs = [f for f in flags if f != flag and abs(f.rect.y - flag.rect.y) < 5 and f not in processed_flags]
                 if potential_pairs:
                     pair_flag = potential_pairs[0]
                     processed_flags.add(flag); processed_flags.add(pair_flag)
                     left_f = flag if flag.is_left else pair_flag
                     right_f = pair_flag if flag.is_left else flag
                     if player.rect.left > left_f.rect.right and player.rect.right < right_f.rect.left:
                         score += 10
                         flag.passed = True; pair_flag.passed = True
                     else:
                         print("Missed the gate! Game Over.")
                         last_score = score
                         high_scores = save_high_scores(score, high_scores)
                         game_state = STATE_GAME_OVER

        # --- Speed Increase ---
        # (Speed logic remains the same)
        if score >= next_speed_increase_threshold:
            current_scroll_speed *= (1.0 + SPEED_INCREASE_PERCENT)
            next_speed_increase_threshold += 100
            print(f"Score {score}: Speed increased to {current_scroll_speed:.2f}")


    # --- Drawing ---
    # Draw based on game state
    if game_state == STATE_START_SCREEN:
        draw_start_screen(screen, high_scores, last_score) # Pass last_score

    elif game_state == STATE_PLAYING or game_state == STATE_GAME_OVER:
        # --- Draw Scene ---
        # 1. Background Parallax Layers (Back to Front)
        for layer in background_parallax_layers:
            layer.draw(screen)

        # 2. Game Sprites (Obstacles, Flags)
        obstacles.draw(screen)
        flags.draw(screen)

        # 3. Player
        player.draw(screen)

        # 4. Foreground Parallax Layers (Clouds)
        for layer in foreground_parallax_layers:
            layer.draw(screen)
        # --- End Scene ---

        # Draw Score UI (only when playing)
        if game_state == STATE_PLAYING:
            score_text = score_font.render(f"Score: {score}", True, BLACK)
            # Add a small background rect for score visibility
            score_bg_rect = pygame.Rect(5, 5, score_text.get_width() + 10, score_text.get_height() + 6)
            pygame.draw.rect(screen, WHITE, score_bg_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, score_bg_rect, width=1, border_radius=5) # Outline
            screen.blit(score_text, (10, 8)) # Position text inside bg rect

        # Draw Game Over Screen (if applicable, drawn over everything else)
        if game_state == STATE_GAME_OVER:
            draw_game_over_screen(screen, last_score)

    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)

# --- Quit Pygame ---
pygame.quit()
sys.exit()
