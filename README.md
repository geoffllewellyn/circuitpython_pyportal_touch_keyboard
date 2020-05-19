circuitpython_pyportal_touch_keyboard 
# Pyportal (Titano) On Screen Keyboard.

(currently sized for the Titano only.)

I made a fairly basic touch screen interface for typing in some text with the pyportal titano. 
It runs on the very edge of having enough memory or what ever. (im only intermediate skilled...)
Im not the best at this so it could use some major help from some much more skilled persons.

When I try to enlarge the buttons by 1 pixel vertically (JUST ONE!), I am getting a memory allocation error.
error is as follows: 
    MemoryError: memory allocation failed, allocating ~450-500 bytes.
    
Seems to happen in the button/rect drawing portion.

So there are some areas that are just blank spaces because of this. bummer.

anyway, Try it out! 
thanks!
-Geoff.

Usage:
  I have it set up to be used as a context managed package. (am i saying that right?)
  so in main:
  
      with TouchKeys() as kbd:
        result = kbd.show(splash)
        print(f'You typed: \'{result}\'')
        
  The show command will return the string you typed after you hit the return button on the keyboard.
  Splash is the main group you wish to run it on top of.
 
<img src="https://github.com/geoffllewellyn/circuitpython_pyportal_touch_keyboard/blob/master/titano_osk.jpg?raw=true" width=400"></img>
