import numpy as np
import random
import pygame
import os
class HiderSeekerEnv:
    def __init__(self, grid_size=5, screen_width=500, screen_height=500):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))
        self.hider_pos = (0, 0)  # Hider starts at top-left corner
        self.seeker_pos = (4, 4)  # Seeker starts at bottom-right corner
        self.blockages = []
        self.place_blockages(4)  # Random blockages in the grid
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        # Initialize pygame for visualization
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hider-Seeker Game")

        # Calculate cell size for visualization
        self.cell_width = screen_width // grid_size
        self.cell_height = screen_height // grid_size

        # Load images for hider, seeker, and blockages
        self.hider_image = pygame.image.load('hider.png')  # Hider image
        self.seeker_image = pygame.image.load('seeker.png')  # Seeker image
        self.blockage_image = pygame.image.load('blockage.png')  # Blockage image

        # Scale images to fit in the grid cells
        self.hider_image = pygame.transform.scale(self.hider_image, (self.cell_width, self.cell_height))
        self.seeker_image = pygame.transform.scale(self.seeker_image, (self.cell_width, self.cell_height))
        self.blockage_image = pygame.transform.scale(self.blockage_image, (self.cell_width, self.cell_height))

    def reset(self):
        self.grid = np.zeros((self.grid_size, self.grid_size))
        self.hider_pos = (0, 0)  # Hider starts at top-left corner
        self.seeker_pos = (4, 4)  # Seeker starts at bottom-right corner
        self.place_blockages(4)
        return self.get_state()

    def place_blockages(self, num):
        self.blockages = [(1, 1), (3, 1), (3, 1), (3, 3)]  # Define blockage positions

    def move_hider(self):
        possible_moves = []
        for action in self.actions:
            new_pos = (self.hider_pos[0] + action[0], self.hider_pos[1] + action[1])
            if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and new_pos not in self.blockages:
                possible_moves.append(new_pos)
        
        if possible_moves:
            self.hider_pos = random.choice(possible_moves)

    def move_seeker(self, action):
        new_pos = (self.seeker_pos[0] + action[0], self.seeker_pos[1] + action[1])
        if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and new_pos not in self.blockages:
            self.seeker_pos = new_pos

    def get_state(self):
        return (self.hider_pos, self.seeker_pos)

    def get_reward(self):
        # Capture the Hider
        if self.seeker_pos == self.hider_pos:
            return 100  # Seeker captured the Hider
        
        # Collision with blockages
        if self.seeker_pos in self.blockages:
            return -10  # Blockage collision penalty

        # Calculate Manhattan distance to the Hider
        distance_old = self.calculate_distance(self.seeker_pos, self.hider_pos)
        progress_reward = -distance_old * 0.5  # Reward based on progress towards Hider

        # Penalty for each step to encourage efficiency
        step_penalty = -1

        reward = progress_reward + step_penalty
        return reward

    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def is_done(self):
        return self.seeker_pos == self.hider_pos

    def step(self, action):
        self.move_seeker(action)
        self.move_hider()
        reward = self.get_reward()
        done = self.is_done()
        return self.get_state(), reward, done

    def render(self):
        # Load and scale the background image
        background_image = pygame.image.load('background.jpeg')  # Replace with your image file
        background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))  # Scale it to fit the screen

        # Blit the background image onto the screen
        self.screen.blit(background_image, (0, 0))  # Position the image at (0, 0)

        # Draw the grid lines
        for x in range(self.grid_size + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (x * self.cell_width, 0), (x * self.cell_width, self.grid_size * self.cell_height))
            pygame.draw.line(self.screen, (0, 0, 0), (0, x * self.cell_height), (self.grid_size * self.cell_width, x * self.cell_height))

        # Draw the blockages (obstacles)
        for block in self.blockages:
            self.screen.blit(self.blockage_image, (block[1] * self.cell_width, block[0] * self.cell_height))

        # Draw the Hider
        self.screen.blit(self.hider_image, (self.hider_pos[1] * self.cell_width, self.hider_pos[0] * self.cell_height))

        # Draw the Seeker
        self.screen.blit(self.seeker_image, (self.seeker_pos[1] * self.cell_width, self.seeker_pos[0] * self.cell_height))

        # Update the display
        pygame.display.flip()

    def close(self):
        pygame.quit()


# import numpy as np
# import random
# import pygame
# import os


# class HiderSeekerEnv:
#     def __init__(self, grid_size=5, screen_width=500, screen_height=500):
#         self.grid_size = grid_size
#         self.grid = np.zeros((grid_size, grid_size))
#         self.hider_pos = (0, 0)  # Hider starts at top-left corner
#         self.seeker_pos = (4, 4)  # Seeker starts at bottom-right corner
#         self.blockages = []
#         self.place_blockages(4)  # Random blockages in the grid
#         self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
#         # Initialize pygame for visualization
#         pygame.init()
#         self.screen = pygame.display.set_mode((screen_width, screen_height))
#         pygame.display.set_caption("Hider-Seeker Game")

#         # Calculate cell size for visualization
#         self.cell_width = screen_width // grid_size
#         self.cell_height = screen_height // grid_size

#         # Load images for hider, seeker, and blockages
#         self.hider_image = pygame.image.load('hider.png')  # Hider image (e.g., red circle or avatar)
#         self.seeker_image = pygame.image.load('seeker.png')  # Seeker image (e.g., blue circle or avatar)
#         self.blockage_image = pygame.image.load('blockage.png')  # Blockage image (e.g., obstacle)

#         # Scale images to fit in the grid cells
#         self.hider_image = pygame.transform.scale(self.hider_image, (self.cell_width, self.cell_height))
#         self.seeker_image = pygame.transform.scale(self.seeker_image, (self.cell_width, self.cell_height))
#         self.blockage_image = pygame.transform.scale(self.blockage_image, (self.cell_width, self.cell_height))

#     def reset(self):
#         self.grid = np.zeros((self.grid_size, self.grid_size))
#         self.hider_pos = (0, 0)  # Hider starts at top-left corner
#         self.seeker_pos = (4, 4)  # Seeker starts at bottom-right corner
#         self.place_blockages(4)
#         return self.get_state()

#     def place_blockages(self, num):
#         self.blockages = [(1, 1), (3, 1), (3, 1), (3, 3)]  # Define blockage positions
#         # Add more blockages if needed

#     def move_hider(self):
#         possible_moves = []
#         for action in self.actions:
#             new_pos = (self.hider_pos[0] + action[0], self.hider_pos[1] + action[1])
#             if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and new_pos not in self.blockages:
#                 possible_moves.append(new_pos)
        
#         if possible_moves:
#             self.hider_pos = random.choice(possible_moves)

#     def move_seeker(self, action):
#         new_pos = (self.seeker_pos[0] + action[0], self.seeker_pos[1] + action[1])
#         if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and new_pos not in self.blockages:
#             self.seeker_pos = new_pos

#     def get_state(self):
#         return (self.hider_pos, self.seeker_pos)

#     def get_reward(self):
#     # Capture the Hider
#         if self.seeker_pos == self.hider_pos:
#             return 50  # Seeker captured the Hider
#         elif self.seeker_pos in self.blockages:
#             return -5   # Blockage collision penalty

#         distance = self.calculate_distance(self.seeker_pos, self.hider_pos)
#         reward = -distance  # Encourage getting closer to the Hider



#         return reward

#     def calculate_distance(self, pos1, pos2):
#         return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#     def is_done(self):
#         return self.seeker_pos == self.hider_pos

#     def step(self, action):
#         self.move_seeker(action)
#         self.move_hider()
#         reward = self.get_reward()
#         done = self.is_done()
#         return self.get_state(), reward, done

#     def render(self):
#         # Load and scale the background image
#         background_image = pygame.image.load('background.jpeg')  # Replace with your image file
#         background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))  # Scale it to fit the screen

#         # Blit the background image onto the screen
#         self.screen.blit(background_image, (0, 0))  # Position the image at (0, 0)

#         # Draw the grid lines
#         for x in range(self.grid_size + 1):
#             pygame.draw.line(self.screen, (0, 0, 0), (x * self.cell_width, 0), (x * self.cell_width, self.grid_size * self.cell_height))
#             pygame.draw.line(self.screen, (0, 0, 0), (0, x * self.cell_height), (self.grid_size * self.cell_width, x * self.cell_height))

#         # Draw the blockages (obstacles)
#         for block in self.blockages:
#             self.screen.blit(self.blockage_image, (block[1] * self.cell_width, block[0] * self.cell_height))

#         # Draw the Hider
#         self.screen.blit(self.hider_image, (self.hider_pos[1] * self.cell_width, self.hider_pos[0] * self.cell_height))

#         # Draw the Seeker
#         self.screen.blit(self.seeker_image, (self.seeker_pos[1] * self.cell_width, self.seeker_pos[0] * self.cell_height))

#         # Update the display
#         pygame.display.flip()

#     def close(self):
#         pygame.quit()

