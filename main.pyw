import pygame
import sys
import gui
import midi_read
import keyboard

import ctypes
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def hold_keys(keys):
    for key in keys:
        keyboard.press(key)


def release_keys(keys):
    for key in keys:
        keyboard.release(key)


def main():
    actions_json = 'actions.json'
    actions = gui.load_actions_from_json(actions_json)

    # Initialize Pygame
    pygame.init()
    gui.window_size[1] += len(actions) * 30

    # Create Pygame window
    window = pygame.display.set_mode(gui.window_size)
    pygame.display.set_caption("Midi Hotkeys")
    icon = pygame.image.load('MIDI.png')
    pygame.display.set_icon(icon)

    # Init midi device
    midiin = midi_read.open_midi_device()

    key_pressed = False
    note = last_note = None
    delete_note = False
    recording_notes = False
    active = True

    communique = 'PLAY'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                midiin.closePort()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    delete_note = True
                    if delete_note:
                        communique = 'DELETE'
                elif event.key == pygame.K_ESCAPE:
                    active = not active
                    if not active:
                        communique = 'DISABLED'
                    elif recording_notes:
                        communique = 'RECORD'
                    else:
                        communique = 'PLAY NOTES'
                elif event.key == pygame.K_TAB:
                    recording_notes = not recording_notes
                    if recording_notes:
                        communique = 'RECORD'
                    else:
                        communique = 'PLAY'
                elif event.key == pygame.K_ESCAPE and delete_note:
                    delete_note = False
        # Clear the screen
        window.fill(gui.WHITE)

        # Update Midi
        key_pressed, note, _, _ = midi_read.get_midi_message(midiin, key_pressed)
        if note is not None:
            last_note = note
        if active:
            if delete_note:
                gui.change_top_color(gui.RED)
                if key_pressed:
                    gui.delete_action(actions, note, window, actions_json)
                    delete_note = False
            else:
                if key_pressed:
                    if delete_note:
                        gui.delete_action(actions, note, actions_json)
                    else:
                        if last_note in actions:
                            gui.change_top_color(gui.GREEN)
                        else:
                            gui.change_top_color(gui.YELLOW)
                        if gui.read_action(actions, note, window, recording_notes, actions_json) and last_note is not None:
                            try:
                                hold_keys(actions[last_note])
                                release_keys(actions[last_note])
                            except KeyError:
                                pass
                else:
                    if recording_notes:
                        gui.change_top_color(gui.BLUE)
                    else:
                        gui.change_top_color(gui.LIGHTBLUE)
        else:
            gui.change_top_color(gui.BLACK)

        # Draw segments with the current top and bottom segment colors
        gui.draw_segments(window, communique, recording_notes, active)

        # Display hotkey associations
        gui.display_hotkeys(window, actions)

        # Update the display
        pygame.display.flip()


main()
