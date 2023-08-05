# pysimpletimers

This simple, yet useful module will help you to create simple timers that will execute a callback function at the right moment.

(https://github.com/Ilunawoo/pySimpleTimers)

Hope this will ever be useful to someone, it was fun to make.

The Timer object inherit from the threading.Thread object, but you don't need to think about that at all, everything is being taken care of internally.

<br>

A Timer object need 4 arguments when initialized, example below:

```py
my_timer = Timer(delay = 5, callback = my_func, args = (a_string, an_int, ....), loop = False)
```
  
- delay: int or float; represents the waiting time in seconds before executing the callback

- callback: function; your function 

- args: tuple; a tuple containing the args that will be used in your callback, is necessary even if your callback doesn't use args

- loop: bool; whether your timer will start over when it's finished or not

<br>

There are some useful funcs to use with these Timer objects and vars that can be modified:

## ----- functions -----

- timer_obj.start(): DOESN'T start a thread, this function override the original Thread.start() function, it only starts the timer, can be called MORE than one time, if the timer is already started, it will restart it from 0
  
- timer_obj.stop(): stops the timer but doesn't set its current time to 0
  
- timer_obj.quit(): stops the timer and KILL THE THREAD, after that the timer can't be restarted and is only useful to access its data

<br>

## ----- vars -----
 
- timer_obj.current_time: int or float, you should definitely not modify this, var containing the current time of the timer

The vars bellow can be modified even if the timer is already started but it can still cause errors, you should call the .stop() function before changing them (because the timer is a thread, it is possible, yet very unlikely, that you'll modify something at the same moment that it's being called, and then raise an error).

- sleep_time: int or float, the time that will be wait before checking if the delay has been exceded or not (need to be precise or not, at your convenience) NEED TO BE GREATER THAN 0

- timer_obj.delay: int or float, set at the timer's creation, duration of the timer (time waited before the execution of the callback)
  
- timer_obj.callback: function, set at the timer's creation, function called when the timer is completed

- self.args: tuple, set at the timer's creation, args of the callback function, need to be a tuple
  
- self.loop: bool, set at the timer's creation, True if the timer will repeats when it's completed
