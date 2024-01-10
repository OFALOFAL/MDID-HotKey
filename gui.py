import pygame
import json

# GUI-related constants
window_size = [600, 250]
TOP_SEGMENT_HEIGHT = 50
TOP_SEGMENT_COLOR = (50, 50, 255)
BOTTOM_SEGMENT_COLOR = (255, 255, 255)
GREEN = (75, 205, 75)
BLUE = (50, 120, 200)
RED = (255, 50, 50)
WHITE = (255, 255, 255)
BLACK = (40, 45, 40)
YELLOW = (230, 200, 55)
LIGHTBLUE = (153, 186, 220)


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


def read_input(note):
    change_top_color(WHITE)

    reading_input = True
    actions = []

    while reading_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.display.quit()
                reading_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reading_input = False
                elif event.key == pygame.K_BACKSPACE:
                    try:
                        actions.pop()
                    except IndexError:
                        pass
                else:
                    key = pygame.key.name(event.key).upper()
                    actions.append(key)
                    if len(actions) == 15:
                        reading_input = False

        change_top_color(YELLOW)
        pygame.display.get_surface().fill(TOP_SEGMENT_COLOR)

        yoffset = 10
        fsize = 28
        font = pygame.font.Font(None, fsize)
        input_surface = font.render(f"Add hotkey to note: {note}", True, BLACK)
        pygame.display.get_surface().blit(input_surface, (10, yoffset))
        input_surface = font.render(f"ESC - stop recording input", True, BLACK)
        pygame.display.get_surface().blit(input_surface, (10, yoffset + fsize*2))
        input_surface = font.render(f"Set hotkey action (max length 15):", True, BLACK)
        pygame.display.get_surface().blit(input_surface, (10, yoffset + fsize*3))
        input_surface = font.render(f"{actions}", True, BLACK)
        pygame.display.get_surface().blit(input_surface, (10, yoffset + fsize*4))

        pygame.display.flip()

    return actions


def read_action(actions, note, window, recording_notes, filename):
    if note not in actions and note is not None and recording_notes:
        key_action = read_input(note)

        if key_action:
            actions[note] = key_action
            window_size[1] += 30
            new_window = pygame.display.set_mode(window_size)
            pygame.transform.scale(window, window_size, new_window)
            save_actions_to_json(actions, filename)
        return False
    return True


def delete_action(actions, note, window, filename):
    if note in actions and note is not None:
        try:
            actions.pop(note)
            window_size[1] -= 30
            new_window = pygame.display.set_mode(window_size)
            pygame.transform.scale(window, window_size, new_window)
            save_actions_to_json(actions, filename)
        except KeyError:
            pass
    else:
        pass


def change_top_color(new_color):
    global TOP_SEGMENT_COLOR
    TOP_SEGMENT_COLOR = new_color


def calculate_centered_x(text_width):
    return (window_size[0] - text_width) // 2


def draw_segments(window, communique, recording_notes, active):
    pygame.draw.rect(window, TOP_SEGMENT_COLOR, (0, 0, window_size[0], TOP_SEGMENT_HEIGHT))

    fsize = 50
    font = pygame.font.Font(None, fsize)
    text = font.render(str(communique), True, WHITE)
    window.blit(text, (10, 10))

    yoffset = 35
    fsize = 24
    font = pygame.font.Font(None, fsize)

    text = font.render("DELETE - remove a note", True, BLACK)
    text_width, text_height = font.size("DELETE - remove a note")
    window.blit(text, (calculate_centered_x(text_width), TOP_SEGMENT_HEIGHT + yoffset))

    info = 'playing' if recording_notes else 'recording'
    text = font.render(f"TAB - {info} mode", True, BLACK)
    text_width, text_height = font.size(f"TAB - {info} mode")
    window.blit(text, (calculate_centered_x(text_width), TOP_SEGMENT_HEIGHT + yoffset + fsize))

    info = 'disable' if active else 'enable'
    text = font.render(f"ESC - {info} hotkeys", True, BLACK)
    text_width, text_height = font.size(f"ESC - {info} hotkeys")
    window.blit(text, (calculate_centered_x(text_width), TOP_SEGMENT_HEIGHT + yoffset + fsize * 2))


def display_hotkeys(window, actions):
    # Display hotkey associations
    yoffset = 150
    fsize = 28
    font = pygame.font.Font(None, fsize)
    text = font.render('HOTKEYS:', True, BLACK)
    text_width, text_height = font.size('HOTKEYS:')
    window.blit(text, (calculate_centered_x(text_width), TOP_SEGMENT_HEIGHT + yoffset))
    for i, (key, action) in enumerate(actions.items()):
        text = font.render(f"{key}: {action}", True, BLACK)
        text_width, text_height = font.size(f"{key}: {action}")
        window.blit(text, (calculate_centered_x(text_width), TOP_SEGMENT_HEIGHT + yoffset + (i + 1) * 30))
