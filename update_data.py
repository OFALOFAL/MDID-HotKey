import json


def load_actions_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}


def save_actions_to_json(actions, filename):
    with open(filename, 'w') as file:
        json.dump(actions, file, indent=2)