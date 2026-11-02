import pygame, json, os, random

pygame.init()
screen = pygame.display.set_mode((1000, 650))
pygame.display.set_caption("Monster Idle")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
BIG = pygame.font.SysFont("arial", 42, bold=True)
SAVE = "save.json"

def load():
    if os.path.exists(SAVE):
        try:
            with open(SAVE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"gold": 0, "damage": 1, "damage_cost": 10, "auto": 0, "auto_cost": 25, "level": 1}

s = load()
monster_hp = 20
monster_max = monster_hp
last_auto = pygame.time.get_ticks()

def save():
    with open(SAVE, "w", encoding="utf-8") as f:
        json.dump(s, f)

def new_monster():
    global monster_hp, monster_max
    s["level"] += 1
    monster_max = int(20 * (1.35 ** (s["level"] - 1)))
    monster_hp = monster_max

def hit(amount):
    global monster_hp
    monster_hp -= amount
    if monster_hp <= 0:
        reward = max(1, monster_max // 5)
        s["gold"] += reward
        new_monster()
        save()

attack_button = pygame.Rect(350, 420, 300, 100)
dmg_button = pygame.Rect(50, 520, 400, 80)
auto_button = pygame.Rect(550, 520, 400, 80)

running = True
while running:
    now = pygame.time.get_ticks()
    if s["auto"] > 0 and now - last_auto >= 1000:
        hit(s["auto"])
        last_auto = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            p = event.pos
            if attack_button.collidepoint(p):
                hit(s["damage"])
            elif dmg_button.collidepoint(p) and s["gold"] >= s["damage_cost"]:
                s["gold"] -= s["damage_cost"]
                s["damage"] += 1
                s["damage_cost"] = int(s["damage_cost"] * 1.7)
                save()
            elif auto_button.collidepoint(p) and s["gold"] >= s["auto_cost"]:
                s["gold"] -= s["auto_cost"]
                s["auto"] += 1
                s["auto_cost"] = int(s["auto_cost"] * 1.8)
                save()

    screen.fill((25, 28, 38))
    pygame.draw.rect(screen, (70, 80, 105), (250, 170, 500, 45))
    pygame.draw.rect(screen, (80, 210, 110), (250, 170, int(500 * monster_hp / monster_max), 45))

    screen.blit(BIG.render(f"MONSTER IDLE - Level {s['level']}", True, "white"), (250, 60))
    screen.blit(BIG.render(f"Monster HP: {monster_hp:,} / {monster_max:,}", True, "white"), (245, 240))
    screen.blit(FONT.render(f"Gold: {s['gold']:,}", True, (255, 220, 80)), (30, 25))
    screen.blit(FONT.render(f"Click Damage: {s['damage']:,}", True, "white"), (30, 65))
    screen.blit(FONT.render(f"Auto Damage/sec: {s['auto']:,}", True, "white"), (30, 100))

    pygame.draw.rect(screen, (80, 130, 220), attack_button, border_radius=12)
    screen.blit(BIG.render("ATTACK!", True, "white"), (405, 445))

    pygame.draw.rect(screen, (70, 150, 110), dmg_button, border_radius=12)
    screen.blit(FONT.render(f"Upgrade Damage +1  |  {s['damage_cost']:,} gold", True, "white"), (80, 548))

    pygame.draw.rect(screen, (150, 90, 190), auto_button, border_radius=12)
    screen.blit(FONT.render(f"Upgrade Auto +1/s  |  {s['auto_cost']:,} gold", True, "white"), (580, 548))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
