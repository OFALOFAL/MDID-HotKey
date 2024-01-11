import midi_read
import keyboard
import ctypes
import update_data

myappid = 'OFAL.MIDI-HotKey.main.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def read_action(actions, note, recording_notes, last_note):
    return not (note not in actions and note is not None and recording_notes) and last_note is not None


def hold_keys(keys):
    for key in keys:
        if '[' in key and len(key) > 1:
            keyboard.press(key[1])
        else:
            keyboard.press(key)


def release_keys(keys):
    for key in keys:
        if '[' in key and len(key) > 1:
            keyboard.release(key[1])
        else:
            keyboard.release(key)


def main():
    actions_json = 'actions.json'
    actions = update_data.load_actions_from_json(actions_json)

    # Init midi device
    midiin = midi_read.open_midi_device()

    key_pressed = False
    note = last_note = None

    while note != 'C1':
        # Update Midi
        key_pressed, note, _, _ = midi_read.get_midi_message(midiin, key_pressed)
        if note is not None:
            last_note = note
        if key_pressed:
            if read_action(actions, note, False, last_note):
                try:
                    hold_keys(actions[last_note])
                    release_keys(actions[last_note])
                except KeyError:
                    pass
    print('Exit')

main()
