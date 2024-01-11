# MDID HotKey 
### Python program that allows to use midi input as hotkeys in Windows. 
  
Install requirements:
```
pip install -r requirements.txt
```
To run with window open MIDI HotKey.lnk or in cmd type:
```
python main.py
``` 
If you want to run in background open MIDI Hotkey - Background.lnk or in cmd type:
```
python no_gui.py
```

The program will exit after you hit C1 on your MIDI controller (even if run in background).  

---

### Delay  
Delay will differ depending on cable, device, os and your MIDI controller.  
Using Novation Launchkey Mini MK3 on Windows I got those results:
* Windowed version ~260 ms  
* Background version ~130 ms
