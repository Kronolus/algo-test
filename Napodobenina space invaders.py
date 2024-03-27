import pygame
import random
from pygame.locals import *
from time import time as timer

# Inicializace Pygame
pygame.init()

# Nastavení okna hry
window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("hra")

# Načtení obrázků
background = pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\hell.jpg"), (700, 500))
player_image = pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\stay12.jpg").convert_alpha(), (50, 50))
bullet_image = pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\střela.jpg").convert_alpha(), (10, 10))

# Načtení obrázků nepřátel
enemy_images = [
    pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\sugger danny.jpg"), (50, 50)),
    pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\shopaholic adel.jpg"), (50, 50)),
    pygame.transform.scale(pygame.image.load(r"C:\Users\matya\OneDrive\Obrázky\tary.jpg"), (50, 50))
]

# Pouští písničku
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load(r"C:\Users\matya\Music\y2mate.com - Living In A Nightmare feat R8eDR  INSTRUMENTAL  Blacklite District.wav")
pygame.mixer.music.play()

# Font pro text
font = pygame.font.Font(None, 36)

# Hráč
player_rect = player_image.get_rect(center=(350, 450))
speed = 3

# Náboje
bullets = []

# Nepřátelé
enemies = []

# Časovač pro vytváření nepřátel
enemy_timer = 0

# Skóre
prošli = 0
zásahy = 0

# Hlavní smyčka
run = True
while run:
    # Události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Střelba - přidání náboje
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet_rect = bullet_image.get_rect(center=player_rect.center)
            bullets.append(bullet_rect)

    # Přidání nových nepřátel
    if len(enemies) < 5 and pygame.time.get_ticks() - enemy_timer > 1000:
        num_enemies = random.randint(1, 3)  # Počet nových nepřátel (1 až 3)
        for _ in range(num_enemies):
            enemy_image = random.choice(enemy_images)
            enemy_rect = enemy_image.get_rect(center=(random.randint(0, 650), 0))
            enemies.append((enemy_image, enemy_rect))
        enemy_timer = pygame.time.get_ticks()

   
    # Pohyb nepřátel
    for enemy, enemy_rect in enemies:
        if enemy_rect.bottom < 500:
            enemy_rect.y += 1
            pygame.time.wait(2)
        
        else:
            prošli += 1
            enemies.remove((enemy, enemy_rect))

    # Pohyb nábojů a detekce kolize s nepřáteli
    for bullet_rect in bullets[:]:  # Používáme kopii seznamu pro iteraci, abychom mohli měnit původní seznam
        bullet_rect.y -= 5  # Pohyb náboje nahoru
        for enemy, enemy_rect in enemies[:]:  # Používáme kopii seznamu pro iteraci, abychom mohli měnit původní seznam
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet_rect)
                enemies.remove((enemy, enemy_rect))
                zásahy += 1

        # Odstranění nábojů, které opustí obrazovku
        if bullet_rect.bottom < 0:
            bullets.remove(bullet_rect)

    # Detekce konce hry
    if prošli >= 3:
        text = font.render("Prohrál jsi!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(350, 250))
        window.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)  # Zpoždění na 2 sekundy
        run = False
    elif zásahy >= 10:
        text = font.render("Vyhrál jsi!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(350, 250))
        window.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)  # Zpoždění na 2 sekundy
        run = False

    # Klávesové vstupy a kontrola hráče, aby neopustil obrazovku
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect.x -= speed
    if keys[K_RIGHT] and player_rect.right < 700:
        player_rect.x += speed

    # Vykreslení pozadí
    window.blit(background, (0, 0))

    # Vykreslení hráče
    window.blit(player_image, player_rect)

    # Vykreslení nepřátel
    for enemy, enemy_rect in enemies:
        window.blit(enemy, enemy_rect)

    # Vykreslení nábojů
    for bullet_rect in bullets:
        window.blit(bullet_image, bullet_rect)

    # Zobrazení skóre
    score_text = font.render("Prošli: " + str(prošli), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Zobrazení počtu nepřátel, které zbývá zabít
    remaining_enemies_text = font.render("Zbývá zničit: " + str(10 - zásahy), True, (255, 255, 255))
    window.blit(remaining_enemies_text, (10, 50))

    pygame.display.update()

pygame.quit()
