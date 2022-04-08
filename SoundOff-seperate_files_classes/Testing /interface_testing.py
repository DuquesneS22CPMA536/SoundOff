# Using pyautogui to go through a simple run of using the app on Gabbie's computer to compare a file to all platforms, LUFS and peak
# all coordinates were found using an example program from https://pyautogui.readthedocs.io/en/latest/mouse.html
import pyautogui as gui, time
screenWidth, screenHeight = gui.size() # get screen size

# opening and maximizing SoundOff_Application folder in file explorer
gui.moveTo(33, 1058)
gui.click()
gui.typewrite('SoundOff_Application', interval=0.25)
gui.press('enter')
time.sleep(2)
gui.keyDown('alt')
gui.press(' ')
gui.press('x')
gui.keyUp('alt')

# opening and maximizing SoundOff
gui.moveTo(352, 261) # coordinates of SoundOff.exe when folder is maximized
gui.doubleClick()
time.sleep(10) # waiting 10 seconds for SoundOff window to open
gui.moveTo(470, 543) # switching active window to SoundOff window
gui.click()
time.sleep(2)
gui.keyDown('alt')
gui.press(' ')
gui.press('x')
gui.keyUp('alt')

# selecting a file
gui.moveTo(990, 389) # coordinates of "Select a file" button when SoundOff window is maximized
gui.click()
time.sleep(2)
gui.moveTo(100, 478) # coordinates of folder with file when file explorer is opened
gui.click()
time.sleep(2)
gui.moveTo(379, 287) # coordinates of file within folder when file explorer is opened
gui.doubleClick()
time.sleep(10) # waiting 10 seconds to calculate and display "Select Report" window

# selecting all platforms
gui.moveTo(96, 723) # coordinates of "Select All Platforms" button
gui.doubleClick()