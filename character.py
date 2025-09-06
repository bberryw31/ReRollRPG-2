from settings import *


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
        base_hp = random.randint(5, 10)

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
