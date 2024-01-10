import rtmidi


def get_message(midi):
    if midi.isNoteOn():
        return 1, (midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        return 0, (midi.getMidiNoteName(midi.getNoteNumber()), None)
    elif midi.isController():
        return 2, (midi.getControllerNumber(), midi.getControllerValue())


def open_midi_device(port=0):
    midiin = rtmidi.RtMidiIn()
    ports = range(midiin.getPortCount())

    if ports:
        for i in ports:
            print(midiin.getPortName(i))

        midiin.openPort(port)
    return midiin


def get_midi_message(midiin, key_pressed):
    note = None
    velocity = 0

    data = midiin.getMessage(250)
    if data:
        try:
            state, message = get_message(data)
        except TypeError:
            return key_pressed, note, velocity, -1

        if state == 1:
            key_pressed = True
            note = message[0]
            velocity = message[1]
        elif state == 0:
            key_pressed = False

        return key_pressed, note, velocity, state

    return key_pressed, note, velocity, -1
