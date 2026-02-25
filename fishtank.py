"""
AquariumGame: Interactive Fish Aquarium

Description:
This program simulates a virtual fish aquarium.

Features:
- Multiple fish swimming and chasing food.
- Click keyboard 0-9 to place different food types.
- Bubbles rising from bottom to top.
- Switch backgrounds with arrow keys.
- Adjustable fish speeds via GUI.

Designed for:
- Clients: Interactive and visual demo to showcase the aquarium.
- Software Engineers: Clear and extendable code to add fish behaviors, food types, or animations.

Note: Images for fish, food, and backgrounds should be placed in
the 'fish_drawings', 'food_images', and 'tank' folders respectively.
"""

# -------------------- Imports --------------------
import pygame
import random
import glob
import os
import tkinter as tk
from tkinter import messagebox
from drawing_interface import get_drawing_image, LAST_SAVED_NAME

# -------------------- Constants --------------------
FISH_SPEED_SCALE = 0.5  # for other software engineers: scales all fish speeds
BUBBLE_SPEED_RANGE = (0.6, 1.6)  # for other software engineers: min/max speed of bubbles
BUBBLE_DRIFT_RANGE = (-0.4, 0.4)
BUBBLE_RADIUS_RANGE = (3, 8)
FOOD_DISPLAY_SIZE = (50, 50)
FADE_SPEED = 8  # for other software engineers: controls how fast food fades after eaten

# -------------------- Classes --------------------
class Fish:
    """Represents a fish in the aquarium. # for client"""
    def __init__(self, img_path, w, h, scale=(120, 80), speed=2):
        self.image = pygame.transform.scale(
            pygame.image.load(img_path).convert_alpha(), scale
        )
        self.w, self.h = w, h
        self.speed = speed * FISH_SPEED_SCALE
        self.x = random.randint(50, w - 50)
        self.y = random.randint(50, h - 50)
        self.dx = random.choice([-self.speed, self.speed])
        self.dy = random.choice([-self.speed, self.speed])
        self.change_dir_counter = 0

    def _check_bounds(self):
        # for other software engineers: flip fish image horizontally when bouncing
        if self.x < 0 or self.x > self.w - self.image.get_width():
            self.dx = -self.dx
            self.image = pygame.transform.flip(self.image, True, False)
            self.x = max(0, min(self.x, self.w - self.image.get_width()))
            
        if self.y < 0 or self.y > self.h - self.image.get_height():
            self.dy = -self.dy
            self.y = max(0, min(self.y, self.h - self.image.get_height()))

    def update(self, food_list):
        # for client: fish will swim toward food if available, else random movement
        cx = self.x + self.image.get_width() // 2
        cy = self.y + self.image.get_height() // 2

        if food_list:
            closest = min(
                food_list,
                key=lambda f: (f.x - cx) ** 2 + (f.y - cy) ** 2
            )
            fx = closest.x + closest.surface.get_width() // 2
            fy = closest.y + closest.surface.get_height() // 2
            dx = fx - cx
            dy = fy - cy
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 0.01)

            eat_radius = min(self.image.get_width(), self.image.get_height()) * 0.35
            if dist < eat_radius:
                closest.start_fade()  # for client: fish eats the food
                return

            # for other software engineers: move fish toward food
            self.dx = self.speed * dx / dist
            self.dy = self.speed * dy / dist
        else:
            self.change_dir_counter += 1
            if self.change_dir_counter > 120:
                # for other software engineers: random swim direction
                self.dx = random.choice([-self.speed, self.speed])
                self.dy = random.choice([-self.speed, self.speed])
                self.change_dir_counter = 0

        self.x += self.dx
        self.y += self.dy
        self._check_bounds()

    def draw(self, screen):
        # for client: draws fish on the screen
        screen.blit(self.image, (self.x, self.y))


class Bubble:
    """Rising bubble animation. # for client"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(*BUBBLE_RADIUS_RANGE)
        self.speed = random.uniform(*BUBBLE_SPEED_RANGE)
        self.drift = random.uniform(*BUBBLE_DRIFT_RANGE)

    def update(self, screen_width, screen_height):
        # for other software engineers: moves bubble upwards with horizontal drift
        self.y -= self.speed
        self.x += self.drift
        return self.y + self.radius > 0 and -50 < self.x < screen_width + 50

    def draw(self, screen):
        # for client: draws bubble as a circle
        pygame.draw.circle(screen, (230, 240, 255), (int(self.x), int(self.y)), self.radius, 1)


class Food:
    """Food placed by user. # for client"""
    def __init__(self, pos, surface):
        self.x, self.y = pos
        self.surface = surface.copy()
        self.alpha = 255
        self.fading = False

    def start_fade(self):
        self.fading = True  # for client: starts fading after being eaten

    def update(self):
        if self.fading:
            self.alpha -= FADE_SPEED  # for other software engineers: fade effect
        return self.alpha > 0

    def draw(self, screen):
        temp_surface = self.surface.copy()
        if self.fading:
            temp_surface.set_alpha(max(self.alpha, 0))
        screen.blit(temp_surface, (self.x, self.y))


# -------------------- Fish Speed GUI --------------------
def choose_fish_speeds_gui(fish_images_with_names):
    """GUI to set individual fish speeds. # for client"""
    speeds = []

    def confirm():
        nonlocal speeds
        speeds = []
        for idx, entry in enumerate(entries):
            val = entry.get()
            if not val.isdigit() or not (1 <= int(val) <= 5):
                messagebox.showerror("Invalid input",
                                     f"{fish_images_with_names[idx][0]} speed must be 1~5.")
                return
            speeds.append(int(val))
        root.destroy()

    root = tk.Tk()
    root.title("Set Fish Speeds")
    root.resizable(False, False)
    entries = []

    for name, _ in fish_images_with_names:
        frame = tk.Frame(root)
        frame.pack(pady=5, fill="x")
        tk.Label(frame, text=f"{name} speed (1~5):").pack(anchor="w", padx=5)
        entry = tk.Entry(frame)
        entry.insert(0, "2")
        entry.pack(anchor="w", padx=5)
        entries.append(entry)

    tk.Button(root, text="Confirm", command=confirm).pack(pady=10)
    root.mainloop()
    return speeds


# -------------------- Aquarium Game --------------------
class AquariumGame:
    """Main aquarium game engine. # for other software engineers"""
    def __init__(self, width=900, height=600, bg_folder="tank", food_folder="food_images"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Fish Aquarium")

        # Load backgrounds
        self.backgrounds = []
        for ext in ["*.jpg", "*.png"]:
            self.backgrounds.extend(
                sorted(glob.glob(os.path.join(bg_folder, ext)))
            )
        self.backgrounds = [
            pygame.transform.scale(pygame.image.load(p).convert(), (width, height))
            for p in self.backgrounds
        ]
        self.current_bg_index = 0

        # Load food images
        self.food_surfaces = [
            pygame.transform.scale(pygame.image.load(p).convert_alpha(), FOOD_DISPLAY_SIZE)
            for p in sorted(glob.glob(os.path.join(food_folder, "*.png")))
        ]
        print(f"Loaded {len(self.food_surfaces)} food PNGs")

        self.fish_list = []
        self.food_list = []
        self.bubbles = []
        self.bubble_timer = 0
        self.running = True

    def add_fish(self, image_path, speed=2):
        self.fish_list.append(Fish(image_path, self.width, self.height, speed=speed))

    def add_fishes(self, image_list, speeds=None):
        if speeds and len(speeds) == len(image_list):
            for img, sp in zip(image_list, speeds):
                self.add_fish(img, speed=sp)
        else:
            for img in image_list:
                self.add_fish(img)

    def handle_events(self, selected_food_index):
        """Handle mouse and keyboard events. # for other software engineers"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                surface = self.food_surfaces[selected_food_index[0] % len(self.food_surfaces)]
                self.food_list.append(Food(event.pos, surface))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.current_bg_index = (self.current_bg_index + 1) % len(self.backgrounds)
                elif event.key == pygame.K_LEFT:
                    self.current_bg_index = (self.current_bg_index - 1) % len(self.backgrounds)
                elif event.unicode.isdigit():
                    idx = int(event.unicode)
                    if 0 <= idx < len(self.food_surfaces):
                        selected_food_index[0] = idx

    def update(self):
        """Update all game elements: fish, food, bubbles. # for other software engineers"""
        self.bubble_timer += 1
        if self.bubble_timer >= 12:
            for _ in range(random.randint(1, 3)):
                x = random.randint(20, self.width - 20)
                y = self.height - 10
                self.bubbles.append(Bubble(x, y))
            self.bubble_timer = 0

        self.bubbles = [b for b in self.bubbles if b.update(self.width, self.height)]
        self.food_list = [f for f in self.food_list if f.update()]
        for fish in self.fish_list:
            fish.update(self.food_list)

    def draw(self):
        """Draw all game elements. # for client"""
        if self.backgrounds:
            self.screen.blit(self.backgrounds[self.current_bg_index], (0, 0))
        else:
            self.screen.fill((0, 100, 150))

        for b in self.bubbles:
            b.draw(self.screen)
        for f in self.food_list:
            f.draw(self.screen)
        for fish in self.fish_list:
            fish.draw(self.screen)

    def run(self, selected_food_index):
        """Main loop. # for client"""
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events(selected_food_index)
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


# -------------------- Launcher --------------------
def aquarium(fish_images=None, fish_speeds=None,
             fish_folder="fish_drawings", bg_folder="tank", food_folder="food_images"):
    """Launcher function. # for client"""
    if fish_images is None:
        fish_images = sorted(
            [os.path.join(fish_folder, f) for f in os.listdir(fish_folder) if f.endswith(".png")],
            key=os.path.getctime
        )
    if not fish_images:
        print("No fish drawn yet!")
        return

    if fish_speeds is None or len(fish_speeds) != len(fish_images):
        fish_speeds = [2] * len(fish_images)

    game = AquariumGame(bg_folder=bg_folder, food_folder=food_folder)
    game.add_fishes(fish_images, fish_speeds)
    game.run([0])

if __name__ == "__main__":
    fishtank()
