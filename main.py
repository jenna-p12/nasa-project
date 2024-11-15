from ursina import *
import time

class Stopwatch(Entity):
    def __init__(user, **kwargs):
        super().__init__(**kwargs)
        user.timeElapsed = 0  
        user.running = False
        user.textEntity = Text(text="00:00:00.000", position=(0, -0.1), origin=(0, 0))
        user.lastTime = time.time() 

    def update(user):
        if user.running:
           
            user.timeElapsed += time.dt  

           
            hours = int(user.timeElapsed // 3600)
            minutes = int((user.timeElapsed % 3600) // 60)
            seconds = int(user.timeElapsed % 60)
            milliseconds = int((user.timeElapsed % 1) * 1000)  

            clockappFormat = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

            user.textEntity.text = clockappFormat

    def start(user):
        user.running = True

    def stop(user):
        user.running = False

    def reset(user):
        user.timeElapsed = 0
        user.textEntity.text = "00:00:00.000"

app = Ursina()

stopwatch = Stopwatch()

def start_stopwatch():
    stopwatch.start()

def stop_stopwatch():
    stopwatch.stop()

def reset_stopwatch():
    stopwatch.reset()

startButton = Button(text="Start", position=(-0.08, -0.2), scale=(.05, .05), on_click=start_stopwatch)
stopButton = Button(text="Stop", position=(0.0, -0.2), scale=(0.05, 0.05), on_click=stop_stopwatch)
resetButton = Button(text="Reset", position=(0.08, -0.2), scale=(0.05, 0.05), on_click=reset_stopwatch)

startButton.text_entity.scale = (14, 14)
stopButton.text_entity.scale = (14, 14)
resetButton.text_entity.scale = (14, 14)

app.run()
