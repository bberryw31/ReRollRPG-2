from settings import *
import time


class CombatSystem:
    def __init__(self):
        # combat state
        self.in_combat = False
        self.combat_player = None
        self.combat_enemy = None

        # damage values (simple for now)
        self.player_damage = 2
        self.enemy_damage = 1

    def start_combat(self, player, enemy):
        """Start combat between player and enemy"""
        print(f"Starting combat!")
        self.in_combat = True
        self.combat_player = player
        self.combat_enemy = enemy

        # start the combat loop
        self.execute_combat()

    def execute_combat(self):
        """Execute the combat loop until one dies"""
        while self.in_combat:
            # player attacks first
            enemy_alive = self.player_attack()

            if not enemy_alive:
                self.end_combat(player_wins=True)
                break

            # small delay between attacks
            time.sleep(0.5)

            # enemy attacks back
            player_alive = self.enemy_attack()

            if not player_alive:
                self.end_combat(player_wins=False)
                break

            # small delay before next round
            time.sleep(0.5)

    def player_attack(self):
        """Player attacks enemy, returns True if enemy survives"""
        print(f"Player attacks for {self.player_damage} damage!")
        enemy_alive = self.combat_enemy.take_damage(self.player_damage)

        if not enemy_alive:
            print("Enemy defeated!")

        return enemy_alive

    def enemy_attack(self):
        """Enemy attacks player, returns True if player survives"""
        print(f"Enemy attacks for {self.enemy_damage} damage!")
        player_alive = self.combat_player.take_damage(self.enemy_damage)

        if not player_alive:
            print("Player defeated!")

        return player_alive

    def end_combat(self, player_wins):
        """End combat and clean up"""
        self.in_combat = False

        if player_wins:
            print("Victory!")
        else:
            print("Defeat!")

        # reset combat state
        self.combat_player = None
        self.combat_enemy = None
