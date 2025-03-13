import pygame
import random
import os
import sys
import threading
import json
from vosk import Model, KaldiRecognizer
import pyaudio
from objects import Road, Player, Nitro, Tree, Button, Obstacle, Coins, Fuel
import math




# Initialize Pygame
pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 30

lane_pos = [50, 95, 142, 190]

# COLORS **********************************************************************
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# FONTS ***********************************************************************
font = pygame.font.SysFont('cursive', 32)
select_car = font.render('Select Car', True, WHITE)

# IMAGES **********************************************************************
bg = pygame.image.load('Assets/bg.png')
home_img = pygame.image.load('home.png')
home_img = pygame.transform.scale(home_img, (WIDTH, HEIGHT))
play_img = pygame.image.load('Assets/buttons/play.png')
end_img = pygame.image.load('Assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('Assets/coins/1.png')
dodge_img = pygame.image.load('Assets/car_dodge.png')

left_arrow = pygame.image.load('Assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

home_btn_img = pygame.image.load('Assets/buttons/home.png')
replay_img = pygame.image.load('Assets/buttons/replay.png')
sound_off_img = pygame.image.load("Assets/buttons/soundOff.png")
sound_on_img = pygame.image.load("Assets/buttons/soundOn.png")
vosk_off_img = pygame.image.load("Assets/buttons/voiceOff.png")
vosk_on_img = pygame.image.load("Assets/buttons/voiceOn.png")
car_crash_fx = pygame.mixer.Sound('Sounds/car-crash_A_minor.wav')
car_crash_fx.set_volume(1.0)


cars = []
car_type = 0
for i in range(1, 9):
    img = pygame.image.load(f'Assets/cars/{i}.png')
    img = pygame.transform.scale(img, (59, 101))
    cars.append(img)

nitro_frames = []
nitro_counter = 0
for i in range(6):
    img = pygame.image.load(f'Assets/nitro/{i}.gif')
    img = pygame.transform.flip(img, False, True)
    img = pygame.transform.scale(img, (18, 36))
    nitro_frames.append(img)

# Load the background image for the car selection page
car_bg_img = pygame.image.load('Assets/car_selection_bg.png')  # Replace with your image path
car_bg_img = pygame.transform.scale(car_bg_img, (WIDTH, HEIGHT))  # Scale it to fit the screen

# FUNCTIONS *******************************************************************
def center(image):
    return (WIDTH // 2) - image.get_width() // 2

# BUTTONS *********************************************************************
play_btn = Button(play_img, (100, 34), center(play_img) + 10, HEIGHT - 80)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH - 60, 180)

home_btn = Button(home_btn_img, (24, 24), WIDTH // 4 - 18, HEIGHT - 80)
replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT - 86)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT - 80)
vosk_btn = Button(vosk_on_img, (24, 24), WIDTH - 50, 10)  # Vosk toggle button in the top right corner
pause_btn = Button(pygame.image.load("Assets/buttons/pause.png"), (24, 24), WIDTH - 50, 50)  # Pause button

# SOUNDS **********************************************************************
click_fx = pygame.mixer.Sound('Sounds/click.mp3')
fuel_fx = pygame.mixer.Sound('Sounds/fuel.wav')
start_fx = pygame.mixer.Sound('Sounds/start.mp3')
restart_fx = pygame.mixer.Sound('Sounds/restart.mp3')
coin_fx = pygame.mixer.Sound('Sounds/coin.mp3')

pygame.mixer.music.load('Sounds/song1.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.6)

# OBJECTS *********************************************************************
road = Road()
nitro = Nitro(WIDTH - 80, HEIGHT - 80)
p = Player(100, HEIGHT - 120, car_type)

tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# VARIABLES *******************************************************************
home_page = True
car_page = False
game_page = False
over_page = False
paused = False  # New variable to track pause state

current_lane_index = 1  # Start in the middle lane
nitro_on = False
sound_on = True
vosk_on = True  # Vosk recognition state

counter = 0
counter_inc = 1
speed = 0.5
dodged = 0
coins = 0
cfuel = 100

# Add a variable to track distance traveled in meters
distance_traveled = 0

# Speed increment settings
speed_increment = 0.0001  # Speed increase per meter traveled
max_speed = 10  # Maximum speed limit

endx, enddx = 0, 0.5
gameovery = -50

# Vosk Speech Recognition Setup
model = Model("model")  # Path to the Vosk model
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Global variable to store the recognized command
voice_command = None

def listen_for_commands():
    global voice_command
    while True:
        data = stream.read(4000, exception_on_overflow=False)  # Reduce buffer size
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())  # Full recognition
        else:
            result = json.loads(recognizer.PartialResult())  # Partial recognition (faster)

        recognized_text = result.get("text", "")
        print("Vosk hears:", recognized_text)  # Debugging output

        words = recognized_text.split()

        # Move left if any word contains 'l'
        if any("l" in word for word in words):
            voice_command = "links"
        # Move right if any word contains 'r'
        elif any("r" in word for word in words):
            voice_command = "rechts"
        else:
            voice_command = None  # Reset if no valid command

# Start the speech recognition thread
listener_thread = threading.Thread(target=listen_for_commands)
listener_thread.daemon = True
listener_thread.start()

running = True
while running:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_LEFT:
                if current_lane_index > 0:
                    current_lane_index -= 1
                    p.rect.x = lane_pos[current_lane_index]

            if event.key == pygame.K_RIGHT:
                if current_lane_index < len(lane_pos) - 1:
                    current_lane_index += 1
                    p.rect.x = lane_pos[current_lane_index]

            if event.key == pygame.K_UP:
                nitro_on = True

            if event.key == pygame.K_p:  # Pause the game
                paused = not paused

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                nitro_on = False
                speed = 1
                counter_inc = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if nitro.rect.collidepoint((x, y)):
                nitro_on = True

        if event.type == pygame.MOUSEBUTTONUP:
            nitro_on = False
            speed = 3
            counter_inc = 1

    # Handle voice commands
    if vosk_on:  # Only process voice commands if Vosk is on
        if voice_command == "links" and current_lane_index > 0:  # Replace "left" with "links"
            current_lane_index -= 1
            p.rect.x = lane_pos[current_lane_index]
            voice_command = None  # Reset the command after processing

        if voice_command == "rechts" and current_lane_index < len(lane_pos) - 1:  # Replace "right" with "rechts"
            current_lane_index += 1
            p.rect.x = lane_pos[current_lane_index]
            voice_command = None  # Reset the command after processing

    if home_page:
        win.blit(home_img, (0, 0))
        counter += 1
        if counter % 60 == 0:
            home_page = False
            car_page = True

    if car_page:
        win.blit(car_bg_img, (0, 0))  # Draw the background image

        win.blit(select_car, (center(select_car), 80))

        win.blit(cars[car_type], (WIDTH // 2 - 30, 150))
        if la_btn.draw(win):
            car_type -= 1
            click_fx.play()
            if car_type < 0:
                car_type = len(cars) - 1

        if ra_btn.draw(win):
            car_type += 1
            click_fx.play()
            if car_type >= len(cars):
                car_type = 0

        if play_btn.draw(win):
            car_page = False
            game_page = True

            start_fx.play()

            p = Player(100, HEIGHT - 120, car_type)
            counter = 0

        if vosk_btn.draw(win):  # Toggle Vosk recognition
            vosk_on = not vosk_on
            if vosk_on:
                vosk_btn.update_image(vosk_on_img)
            else:
                vosk_btn.update_image(vosk_off_img)

    if over_page:
        win.blit(end_img, (endx, 0))
        endx += enddx
        if endx >= 10 or endx <= -10:
            enddx *= -1

        win.blit(game_over_img, (center(game_over_img), gameovery))
        if gameovery < 16:
            gameovery += 1

        num_coin_img = font.render(f'{coins}', True, WHITE)
        num_dodge_img = font.render(f'{dodged}', True, WHITE)

        win.blit(coin_img, (80, 240))
        win.blit(dodge_img, (50, 280))
        win.blit(num_coin_img, (180, 250))
        win.blit(num_dodge_img, (180, 300))

        if home_btn.draw(win):
            over_page = False
            home_page = True

            coins = 0
            dodged = 0
            counter = 0
            nitro.gas = 0
            cfuel = 100
            distance_traveled = 0  # Reset distance

            endx, enddx = 0, 0.5
            gameovery = -50

        if replay_btn.draw(win):
            over_page = False
            game_page = True

            coins = 0
            dodged = 0
            counter = 0
            nitro.gas = 0
            cfuel = 100
            distance_traveled = 0  # Reset distance

            endx, enddx = 0, 0.5
            gameovery = -50

            restart_fx.play()

        if sound_btn.draw(win):
            sound_on = not sound_on

            if sound_on:
                sound_btn.update_image(sound_on_img)
                pygame.mixer.music.play(loops=-1)
            else:
                sound_btn.update_image(sound_off_img)
                pygame.mixer.music.stop()

    if game_page and not paused:  # Only update game if not paused
        win.blit(bg, (0, 0))
        road.update(speed)
        road.draw(win)

        counter += counter_inc
        distance_traveled += speed  # Increment distance traveled by speed

        # Increase speed over time
        speed += speed_increment * (distance_traveled / 100)  # Increase speed based on distance
        if speed > max_speed:  # Cap the speed to a maximum value
            speed = max_speed

        if counter % 60 == 0:
            tree = Tree(random.choice([-5, WIDTH - 35]), -20)
            tree_group.add(tree)

        if counter % 270 == 0:
            type = random.choices([1, 2], weights=[6, 4], k=1)[0]
            x = random.choice(lane_pos) + 10
            if type == 1:
                count = random.randint(1, 3)
                for i in range(count):
                    coin = Coins(x, -100 - (25 * i))
                    coin_group.add(coin)
            elif type == 2:
                fuel = Fuel(x, -100)
                fuel_group.add(fuel)
        elif counter % 90 == 0:
            obs = random.choices([1, 2, 3], weights=[6, 2, 2], k=1)[0]
            obstacle = Obstacle(obs)
            obstacle_group.add(obstacle)

        if nitro_on and nitro.gas > 0:
            x, y = p.rect.centerx - 8, p.rect.bottom - 10
            win.blit(nitro_frames[nitro_counter], (x, y))
            nitro_counter = (nitro_counter + 1) % len(nitro_frames)

            speed = 10
            if counter_inc == 1:
                counter = 0
                counter_inc = 5

        if nitro.gas <= 0:
            speed = 3
            counter_inc = 1

        nitro.update(nitro_on)
        nitro.draw(win)
        obstacle_group.update(speed)
        obstacle_group.draw(win)
        tree_group.update(speed)
        tree_group.draw(win)
        coin_group.update(speed)
        coin_group.draw(win)
        fuel_group.update(speed)
        fuel_group.draw(win)

        p.update(False, False)  # No need to pass move_left and move_right
        p.draw(win)

        if cfuel > 0:
            pygame.draw.rect(win, GREEN, (20, 20, cfuel, 15), border_radius=5)
        pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
        cfuel -= 0.05

        # COLLISION DETECTION & KILLS
        for obstacle in obstacle_group:
            if obstacle.rect.y >= HEIGHT:
                if obstacle.type == 1:
                    dodged += 1
                obstacle.kill()

            if pygame.sprite.collide_mask(p, obstacle):
                pygame.draw.rect(win, RED, p.rect, 1)
                speed = 0
                car_crash_fx.play()  # Play crash sound

                game_page = False
                over_page = True

                tree_group.empty()
                coin_group.empty()
                fuel_group.empty()
                obstacle_group.empty()


        if pygame.sprite.spritecollide(p, coin_group, True):
            coins += 1
            coin_fx.play()

        if pygame.sprite.spritecollide(p, fuel_group, True):
            cfuel += 25
            fuel_fx.play()
            if cfuel >= 100:
                cfuel = 100

        # Check if fuel is empty
        if cfuel <= 0:
            speed = 0  # Stop the speed
            game_page = False
            over_page = True  # Go to the game over page

    # Draw the border
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()