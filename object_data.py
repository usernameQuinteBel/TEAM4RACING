import json

# Gegevens die je wilt opslaan uit objects.py
objects_data = {
    "screen_size": {
        "width": 288,
        "height": 512
    },
    "colors": {
        "blue": [53, 81, 92],
        "red": [255, 0, 0],
        "yellow": [255, 255, 0]
    },
    "lane_positions": [50, 95, 142, 190],
    "classes": {
        "Road": {
            "image_path": "Assets/road.png",
            "reset_position": {
                "x": 30,
                "y1": 0,
                "y2": -512
            }
        },
        "Player": {
            "image_size": {
                "width": 48,
                "height": 82
            }
        },
        "Obstacle": {
            "types": {
                "car": {
                    "image_size": {
                        "width": 48,
                        "height": 82
                    }
                },
                "barrel": {
                    "image_size": {
                        "width": 24,
                        "height": 36
                    }
                },
                "roadblock": {
                    "image_size": {
                        "width": 50,
                        "height": 25
                    }
                }
            }
        },
        "Nitro": {
            "image_path": "Assets/nitro.png",
            "image_size": {
                "width": 42,
                "height": 42
            }
        },
        "Tree": {
            "image_path": "Assets/trees/{type}.png"
        },
        "Fuel": {
            "image_path": "Assets/fuel.png"
        },
        "Coins": {
            "image_paths": [f'Assets/Coins/{i}.png' for i in range(1, 7)]
        },
        "Button": {
            "image_size": {
                "width": "variable",
                "height": "variable"
            }
        }
    }
}

# Schrijf de gegevens naar een JSON-bestand
with open('objects_data.json', 'w') as json_file:
    json.dump(objects_data, json_file, indent=4)

print("Data succesvol opgeslagen in objects_data.json")