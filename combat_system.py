from settings import *
import pygame


class SlashEffect(pygame.sprite.Sprite):
    def __init__(self, position, entity, direction, groups):
        super().__init__(groups)

        # load slash animation frames
        self.frames = []
        for i in range(4):
            img = pygame.image.load(f"assets/effects/slash/{i}.png")
            img = pygame.transform.scale_by(img, 0.1)
            img = pygame.transform.flip(img, direction, False)
            if entity == "enemy":
                img.fill((222, 0, 0, 30), special_flags=pygame.BLEND_MULT)
            self.frames.append(img.convert_alpha())

        # animation properties
        self.current_frame = 0
        self.animation_speed = 0.3
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        # advance animation
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.kill()  # remove when animation finishes
            return

        # update image
        self.image = self.frames[int(self.current_frame)]


class CombatSystem:
    def __init__(self):
        # combat state
        self.in_combat = False
        self.combat_player = None
        self.combat_enemy = None

        # turn management
        self.player_turn = True
        self.turn_timer = 0
        self.turn_delay = 60
        self.attack_delay = 30
        self.waiting_for_animation = False

        # damage values (hardcoded for now)
        self.player_damage = 2
        self.enemy_damage = 1

        # effects
        self.effects_group = pygame.sprite.Group()

    def start_combat(self, player, enemy):
        # start combat between player and enemy
        print(f"Starting combat")
        self.in_combat = True
        self.combat_player = player
        self.combat_enemy = enemy
        self.player_turn = True
        self.turn_timer = 0
        self.waiting_for_animation = False
        
        # make enemy face player
        enemy.face_target(player.rect.center)

    def update(self):
        # update combat state - called from main game loop
        if not self.in_combat:
            return

        # update effects
        self.effects_group.update()

        # handle turn timing
        if self.waiting_for_animation:
            self.turn_timer += 1
            if self.turn_timer >= self.attack_delay:
                self.waiting_for_animation = False
                self.turn_timer = 0
                # switch turns or check for combat end
                if self.player_turn:
                    # check if enemy died
                    if self.combat_enemy.HP <= 0:
                        self.end_combat(player_wins=True)
                        return
                    self.player_turn = False
                else:
                    # check if player died  
                    if self.combat_player.HP <= 0:
                        self.end_combat(player_wins=False)
                        return
                    self.player_turn = True
        else:
            self.turn_timer += 1
            if self.turn_timer >= self.turn_delay:
                self.execute_turn()
                self.turn_timer = 0

    def execute_turn(self):
        # execute the current turn
        if self.player_turn:
            self.player_attack()
        else:
            self.enemy_attack()
        self.waiting_for_animation = True

    def player_attack(self):
        # player attacks enemy
        self.combat_enemy.take_damage(self.player_damage)

        # create slash effect between player and enemy
        player_pos = self.combat_player.rect.center
        enemy_pos = self.combat_enemy.rect.center
        effect_pos = ((player_pos[0] + enemy_pos[0]) // 2,
                      (player_pos[1] + enemy_pos[1]) // 2)
        attack_direction = player_pos[0] >= enemy_pos[0]
        SlashEffect(effect_pos, "player", attack_direction, self.effects_group)

        if self.combat_enemy.HP <= 0:
            print("Enemy defeated!")

    def enemy_attack(self):
        # enemy attacks player
        self.combat_player.take_damage(self.enemy_damage)

        # create slash effect between enemy and player
        player_pos = self.combat_player.rect.center
        enemy_pos = self.combat_enemy.rect.center
        effect_pos = ((player_pos[0] + enemy_pos[0]) // 2,
                      (player_pos[1] + enemy_pos[1]) // 2)
        attack_direction = player_pos[0] < enemy_pos[0]
        SlashEffect(effect_pos, "enemy", attack_direction, self.effects_group)

        if self.combat_player.HP <= 0:
            print("Player defeated!")

    def end_combat(self, player_wins):
        # end combat
        self.in_combat = False

        if player_wins:
            print("Victory!")
            # remove defeated enemy from game
            self.combat_enemy.kill()
        else:
            print("Defeat!")

        # reset combat state
        self.combat_player = None
        self.combat_enemy = None
        self.player_turn = True
        self.turn_timer = 0
        self.waiting_for_animation = False

        # clear effects
        self.effects_group.empty()

    def draw_effects(self, screen, camera):
        # draw combat effects
        for effect in self.effects_group:
            effect_rect = camera.apply(effect.rect)
            screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            if effect_rect.colliderect(screen_rect):
                screen.blit(effect.image, effect_rect)
