from settings import *
import random


class CharacterGenerator:
    def __init__(self):
        # classes
        self.classes = {
            "Warrior": {
                "name": "Warrior",
                "main_stats": ["STR"],
                "sprite_path": "warrior"
            },
            "Hunter": {
                "name": "Hunter",
                "main_stats": ["DEX"],
                "sprite_path": "hunter"
            },
            "Wizard": {
                "name": "Wizard",
                "main_stats": ["INT"],
                "sprite_path": "wizard"
            },
            "Assassin": {
                "name": "Assassin",
                "main_stats": ["LUC"],
                "sprite_path": "assassin"
            }
        }

    def generate_random_character(self):
        # random stats (20-25 total points)
        stats = self.generate_random_stats()

        # random class
        class_name = random.choice(list(self.classes.keys()))
        character_class = self.classes[class_name]

        # random HP
        base_hp = random.randint(3, 5) * 2

        character = {
            "class": character_class,
            "stats": stats,
            "HP": base_hp,
            "max_HP": base_hp,
            "roll_count": 10
        }

        return character

    def generate_random_stats(self):
        stats = {"str": 0, "dex": 0, "int": 0, "luc": 0}
        stat_names = list(stats.keys())

        total_points = random.randint(20, 25)

        # randomly distribute points
        for _ in range(total_points):
            random_stat = random.choice(stat_names)
            stats[random_stat] += 1

        return stats

    def calculate_combat_damage(self, character, base_damage=1):
        # calculate player damage
        main_stats = character["class"]["main_stats"]
        damage_bonus = 0

        for stat in main_stats:
            stat_value = character["stats"][stat.lower()]
            # 20% of stat value as bonus
            damage_bonus += stat_value * 0.2

        return int(base_damage + damage_bonus)


class CharacterPreviewPlayer:
    # character preview during character generation
    def __init__(self, position, character_data):
        # character data
        self.character_data = character_data
        self.class_info = character_data["class"]

        # load animations
        self.idle_frames = []
        self.run_frames = []
        self.load_animations()

        # surface and position
        self.current_frame = 0
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.old_position = self.position.copy()

        # movement and animation
        self.direction = pygame.math.Vector2()
        self.animation_speed = 0.15
        self.is_moving = False
        self.facing = "right"

    def load_animations(self):
        sprite_path = f'assets/sprites/player/{self.class_info["sprite_path"]}'

        # load idle and run animations
        for i in range(4):
            idle_img = pygame.image.load(f"{sprite_path}/idle{i}.png")
            run_img = pygame.image.load(f"{sprite_path}/run{i}.png")

            idle_img = pygame.transform.scale_by(idle_img, 2)
            run_img = pygame.transform.scale_by(run_img, 2)

            self.idle_frames.append(idle_img.convert_alpha())
            self.run_frames.append(run_img.convert_alpha())

        for i in range(len(self.idle_frames)):
            self.idle_frames[i] = self.trim_transparent_borders(self.idle_frames[i])
        for i in range(len(self.run_frames)):
            self.run_frames[i] = self.trim_transparent_borders(self.run_frames[i])

    def trim_transparent_borders(self, surface):
        # remove transparent borders from surface
        mask = pygame.mask.from_surface(surface)
        if mask.get_bounding_rects():
            bounds = mask.get_bounding_rects()[0]
            return surface.subsurface(bounds).copy()
        return surface

    def update_character_data(self, new_character_data):
        # update character data
        self.character_data = new_character_data
        self.class_info = new_character_data["class"]

        # reload animations
        self.idle_frames.clear()
        self.run_frames.clear()
        self.load_animations()

        # reset animation
        self.current_frame = 0
        self.image = self.idle_frames[0]

    def update(self):
        self.input()
        self.move()
        self.animate()

    def input(self):
        # key input to move character
        keys = pygame.key.get_pressed()

        self.direction.x = (int(keys[pygame.K_d]) - int(keys[pygame.K_a]))
        self.direction.y = (int(keys[pygame.K_s]) - int(keys[pygame.K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.is_moving = (self.direction.x != 0 or self.direction.y != 0)
        if self.direction.x > 0:
            self.facing = "right"
        elif self.direction.x < 0:
            self.facing = "left"

    def move(self):
        # move
        self.old_position = self.position.copy()
        self.position += self.direction * PLAYER_SPEED
        self.rect.center = self.position

    def revert_movement(self):
        # revert position
        self.position = self.old_position
        self.rect.center = self.position

    def animate(self):
        # animate character
        frames = self.run_frames if self.is_moving else self.idle_frames

        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        img = frames[int(self.current_frame)]
        if self.facing == "left":
            img = pygame.transform.flip(img, True, False)

        old_bottom = self.rect.bottom
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = self.position.x
        self.position = pygame.math.Vector2(self.rect.center)

    def draw(self, screen):
        # draw character
        screen.blit(self.image, self.rect)
