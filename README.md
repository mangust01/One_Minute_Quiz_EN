# One_Minute_Quiz_EN
Entry level GUI for a PC startup quiz.

It is useful application for learning new english words.
It should be added to windows startup folder.

You may build the *\*.exe* file from Python script (for example using the Pyinstaller) and add *\*.bat* file to *C:\Users\\\<NAME OF USER\>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup*.

Write the following to the *\*.bat* file:

`cd /d <FULL PATH TO YOUR *.EXE>`

`START <NAME OF YOUR *.EXE>.exe`

You also need to add near the *\*.exe* file the following:
1. Buttons images *1.svg*, *2.svg*, *3.svg*, *4.svg*, *5.svg*, *6.svg* 
2. Manually maintained your *Vocabulary.txt*
