import os
import time

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from entities import Character, GifAnimation
from groups import AllSprites
from support import all_character_import
from npc_behaviors import PathBehavior, WanderBehavior

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(base_dir)
TILE_SIZE = 32

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NGINX Game")
        self.clock = pygame.time.Clock()
        self.setup()

    def import_assets(self):
        self.overworld_frames = {
            'characters': all_character_import(base_dir, 'graphics', 'characters')
        }

        self.world_image_path = os.path.join(base_dir, 'graphics', 'map', 'world.png')
        try:
            self.world_image = pygame.image.load(self.world_image_path).convert_alpha()
        except pygame.error as e:
            print(f"Failed to load world image: {e}")

    def setup(self):
        self.all_sprites = AllSprites()
        self.import_assets()

        self.world_rect = self.world_image.get_rect()
        self.test_surface = pygame.Surface(self.world_rect.size)
        self.test_surface.blit(self.world_image, (0, 0))

        gif_path = os.path.join(base_dir, 'graphics', 'gifs', 'f5logo.gif')
        gif_size = (56, 56)  # Set your desired size
        gif_pos = (TILE_SIZE * 40, TILE_SIZE * 26)
        self.gif_animation = GifAnimation(gif_pos, gif_path, gif_size, self.all_sprites)

        alex_dialogs = [
            "Hi, I'm Alex! An Engineering Intern at F5/NGINX!",
            "Since a young age, I loved to tinker and mod software!",
            "I had a coding course when I was younger.",
            "I'm on the NGINX Ingress Controller Team.",
            "My biggest additions is on IP listener and Telemetry.",
            "Oh wait! I need to go to the conference room!"
        ]

        spencer_dialogs = [
            "My name Spencer and I'm an Intern at F5/NGINX",
            "I'm on the NGINX Agent Team.",
            "I've had the chance to work on some interesting projects.",
            "And this is how we navigate through F5 as interns!"
        ]

        stephen_dialogs = [
            "Hey, I'm Stephen, yet another engineering intern (there's dozens of us).",
            "Graduating this year from Munster Technological University?",
            "I have been passionate about tech from an early age.",
            "I am on the delivery engineering team",
            "I work under Sergey and my Mentor/Buddy Sean",
            "The rest of the team have been amazing to work with on my journey",
            "I'm late! The lads are waiting in the conference room"
        ]

        self.alex = Character((TILE_SIZE * 34, TILE_SIZE * 18), self.overworld_frames['characters']['alex'],
                              self.all_sprites, self.world_rect, alex_dialogs)
        self.spencer = Character((TILE_SIZE * 39, TILE_SIZE * 65), self.overworld_frames['characters']['spencer'],
                                 self.all_sprites, self.world_rect, spencer_dialogs)
        self.stephen = Character((TILE_SIZE * 7, TILE_SIZE * 95), self.overworld_frames['characters']['stephen'],
                                 self.all_sprites, self.world_rect, stephen_dialogs)

        # Define the path for each NPC
        npc_paths = {
            'npc1': [
                (TILE_SIZE * 10, TILE_SIZE * 40),
                (TILE_SIZE * 50, TILE_SIZE * 20),
                (TILE_SIZE * 42, TILE_SIZE * 26),
                (TILE_SIZE * 5, TILE_SIZE * 9)
            ],
            'npc2': [
                (TILE_SIZE * 20, TILE_SIZE * 20),
                (TILE_SIZE * 30, TILE_SIZE * 20),
                (TILE_SIZE * 30, TILE_SIZE * 30),
                (TILE_SIZE * 20, TILE_SIZE * 30)
            ],
            'npc3': [
                (TILE_SIZE * 12, TILE_SIZE * 33),
                (TILE_SIZE * 12, TILE_SIZE * 33),
                (TILE_SIZE * 12, TILE_SIZE * 33),
                (TILE_SIZE * 12, TILE_SIZE * 33),
                (TILE_SIZE * 12, TILE_SIZE * 34),
                (TILE_SIZE * 12, TILE_SIZE * 34),
                (TILE_SIZE * 12, TILE_SIZE * 34),
                (TILE_SIZE * 12, TILE_SIZE * 34),
                (TILE_SIZE * 12, TILE_SIZE * 34)

            ]
        }



        # Add NPCs with PathBehavior
        self.npc1 = Character((TILE_SIZE * 12, TILE_SIZE * 33), self.overworld_frames['characters']['npc1'],
                              self.all_sprites, self.world_rect, ["I'm NPC1!"])
        self.npc1.animation_speed = 2
        path_behavior1 = PathBehavior(npc_paths['npc3'])
        self.npc1.set_behavior(path_behavior1)

        self.npc2 = Character((TILE_SIZE * 20, TILE_SIZE * 20), self.overworld_frames['characters']['npc1'],
                              self.all_sprites, self.world_rect, ["I'm NPC2!"])
        path_behavior2 = PathBehavior(npc_paths['npc2'])
        self.npc2.set_behavior(path_behavior2)

        # Example for a new character with WanderBehavior
        new_character_path = [(TILE_SIZE * 10, TILE_SIZE * 10), (TILE_SIZE * 20, TILE_SIZE * 20)]
        self.new_character = Character((TILE_SIZE * 25, TILE_SIZE * 20),
                                       self.overworld_frames['characters']['npc1'],
                                       self.all_sprites, self.world_rect, "")
        wander_behavior = WanderBehavior(direction_change_interval=1.0)
        self.new_character.set_behavior(wander_behavior)

        self.current_character = self.alex
        self.alex.current_character = self.alex
        self.camera_target = self.alex

    def switch_character(self, new_character):
        if new_character == self.current_character:
            return

        if self.current_character:
            # Define the target location where the current character should move
            target_positions = {
                self.alex: (TILE_SIZE * 31, TILE_SIZE * 109),
                self.spencer: (TILE_SIZE * 29, TILE_SIZE * 110),
                self.stephen: (TILE_SIZE * 27, TILE_SIZE * 111)
            }

            target_position = target_positions.get(self.current_character, None)
            if target_position:
                self.current_character.move_to(target_position)
                self.facing_direction = 'down'

        # Switch the current character
        self.current_character = new_character
        self.camera_target = new_character
        self.all_sprites.set_camera(new_character.rect, self.world_rect)

        if self.current_character:
            if hasattr(self.current_character, 'team'):
                if new_character in self.current_character.team or not self.current_character.team:
                    self.current_character = new_character
                    new_character.current_character = new_character
                    if hasattr(new_character, 'rearrange_team'):
                        new_character.rearrange_team()
                    self.camera_target = new_character
                    self.all_sprites.set_camera(new_character.rect, self.world_rect)
                else:
                    print(f"{new_character} is not in the team of the current character.")
            else:
                self.current_character = new_character
                new_character.current_character = new_character
                self.camera_target = new_character
                self.all_sprites.set_camera(new_character.rect, self.world_rect)
        else:
            self.current_character = new_character
            new_character.current_character = new_character
            self.camera_target = new_character
            self.all_sprites.set_camera(new_character.rect, self.world_rect)

    def restart_game(self):
        self.setup()
        print("Game restarted.")

    def run(self):
        keypresses = {}
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        if key in keypresses and pygame.time.get_ticks() - keypresses[key] < 500:
                            self.current_character.stop_moving = not self.current_character.stop_moving
                        else:
                            keypresses[key] = pygame.time.get_ticks()
                            if key == pygame.K_1:
                                self.switch_character(self.alex)
                            elif key == pygame.K_2:
                                self.switch_character(self.spencer)
                            elif key == pygame.K_3:
                                self.switch_character(self.stephen)
                    elif key == pygame.K_e:
                        dialogue = self.current_character.interact()
                        if self.current_character.speech_bubble is None:
                            # Define the size of the speech bubble
                            bubble_width, bubble_height = 300, 100
                            self.current_character.speech_bubble = pygame.Surface((bubble_width, bubble_height),
                                                                                  pygame.SRCALPHA)

                            lime = (0, 255, 0)
                            white = (255, 255, 255)
                            draw_rounded_rect(self.current_character.speech_bubble, white,
                                              self.current_character.speech_bubble.get_rect(), 10, border_color=lime,
                                              border_width=5)

                            font = pygame.font.Font(None, 36)
                            max_text_width = bubble_width - 20  # Adjust according to your bubble size and padding

                            # Wrap the text to fit within the bubble
                            lines = wrap_text(dialogue, font, max_text_width)

                            # Render each line separately
                            y_offset = 10
                            for line in lines:
                                text = font.render(line, True, (0, 0, 0))
                                self.current_character.speech_bubble.blit(text, (10, y_offset))
                                y_offset += font.get_height()
                    elif key == pygame.K_RETURN:  # Handle Enter key for dialog cycling
                        if self.current_character.speech_bubble:
                            # Go to the next dialog
                            self.current_character.next_dialog()
                            dialogue = self.current_character.interact()

                            # Update the speech bubble with the new dialog
                            bubble_width, bubble_height = 300, 100
                            self.current_character.speech_bubble = pygame.Surface((bubble_width, bubble_height),
                                                                                  pygame.SRCALPHA)

                            lime = (0, 255, 0)
                            white = (255, 255, 255)
                            draw_rounded_rect(self.current_character.speech_bubble, white,
                                              self.current_character.speech_bubble.get_rect(), 10, border_color=lime,
                                              border_width=5)

                            font = pygame.font.Font(None, 36)
                            max_text_width = bubble_width - 20  # Adjust according to your bubble size and padding

                            # Wrap the text to fit within the bubble
                            lines = wrap_text(dialogue, font, max_text_width)

                            # Render each line separately
                            y_offset = 10
                            for line in lines:
                                text = font.render(line, True, (0, 0, 0))
                                self.current_character.speech_bubble.blit(text, (10, y_offset))
                                y_offset += font.get_height()
                    elif key == pygame.K_f:
                        for character in [self.alex, self.spencer, self.stephen]:
                            print_character_location(character)
                    elif key == pygame.K_r:
                        if self.current_character.speech_bubble:
                            self.current_character.speech_bubble = None
                            self.current_character.speech_bubble_start_time = None
                    elif key == pygame.K_ESCAPE:
                        self.restart_game()

            if self.current_character and not self.current_character.stop_moving:
                self.current_character.input()

            self.all_sprites.update(dt)
            if self.camera_target:
                self.all_sprites.set_camera(self.camera_target.rect, self.world_rect)

            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.test_surface, self.all_sprites.offset)
            self.all_sprites.draw(self.display_surface)

            if self.current_character.speech_bubble:
                # Update the position of the speech bubble to follow the player
                bubble_x = self.current_character.rect.centerx - self.current_character.speech_bubble.get_width() // 2
                bubble_y = self.current_character.rect.top - self.current_character.speech_bubble.get_height() - 10
                bubble_position = (bubble_x + self.all_sprites.offset.x, bubble_y + self.all_sprites.offset.y)

                # Draw the speech bubble
                self.display_surface.blit(self.current_character.speech_bubble, bubble_position)

            pygame.display.update()

def pixel_to_tile(pixel_pos, tile_size):
    return pixel_pos // tile_size

def print_character_location(character):
    # Get the pixel position of the character's center
    x_pixel, y_pixel = character.rect.center
    # Convert pixel position to tile coordinates
    x_tile = pixel_to_tile(x_pixel, TILE_SIZE)
    y_tile = pixel_to_tile(y_pixel, TILE_SIZE)
    # Print the location in TILE_SIZE * X format
    print(f"Character's Location: TILE_SIZE * {x_tile}, TILE_SIZE * {y_tile}")

def wrap_text(text, font, max_width):
    """Wrap text into multiple lines that fit within max_width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word exceeds the max width
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            # If it exceeds, save the current line and start a new one
            lines.append(current_line.strip())
            current_line = word + " "

    # Add the last line
    if current_line:
        lines.append(current_line.strip())

    return lines

def draw_rounded_rect(surface, color, rect, radius, border_color=None, border_width=0):
    """Draws a rounded rectangle with optional border."""
    rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)

    # Draw the filled rounded rectangle
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=radius)

    if border_color and border_width > 0:
        pygame.draw.rect(shape_surf, border_color, shape_surf.get_rect(), border_radius=radius, width=border_width)

    surface.blit(shape_surf, rect.topleft)

if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.display.update()