import json

# Gegevens die je wilt opslaan uit main.py
main_data = {
    "screen_size": {
        "width": 288,
        "height": 512
    },
    "colors": {
        "white": [255, 255, 255],
        "blue": [30, 144, 255],
        "red": [255, 0, 0],
        "green": [0, 255, 0],
        "black": [0, 0, 20]
    },
    "lane_positions": [50, 95, 142, 190],
    "sounds": {
        "car_crash": 'Sounds/car-crash_A_minor.wav',
        "click": 'Sounds/click.mp3',
        "fuel": 'Sounds/fuel.wav',
        "start": 'Sounds/start.mp3',
        "restart": 'Sounds/restart.mp3',
        "coin": 'Sounds/coin.mp3',
        "background_music": 'Sounds/song1.mp3'
    },
    "images": {
        "background": 'Assets/bg.png',
        "home": 'home.png',
        "play_button": 'Assets/buttons/play.png',
        "end_image": 'Assets/end.jpg',
        "game_over_image": 'Assets/game_over.png',
        "coin_image": 'Assets/coins/1.png',
        "dodge_image": 'Assets/car_dodge.png',
        "left_arrow": 'Assets/buttons/arrow.png',
        "right_arrow": 'Assets/buttons/arrow.png',
        "home_button": 'Assets/buttons/home.png',
        "replay_button": 'Assets/buttons/replay.png',
        "sound_off_button": 'Assets/buttons/soundOff.png',
        "sound_on_button": 'Assets/buttons/soundOn.png',
        "vosk_off_button": 'Assets/buttons/voiceOff.png',
        "vosk_on_button": 'Assets/buttons/voiceOn.png'
    }
}

# Schrijf de gegevens naar een JSON-bestand
with open('main_data.json', 'w') as json_file:
    json.dump(main_data, json_file, indent=4)

print("Data succesvol opgeslagen in main_data.json")