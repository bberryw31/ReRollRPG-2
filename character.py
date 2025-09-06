class CharacterGenerator:
    def __init__(self):
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
