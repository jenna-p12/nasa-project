from ursina import *
import time

class Stopwatch(Entity):
    def __init__(user, **kwargs):
        super().__init__(**kwargs)
        user.timeElapsed = 0  
        user.running = False
        user.textEntity = Text(text="000:00:00.00", color=color.white, font='VeraMono.ttf', position=(-0.35, -.16), origin=(0, 0))
        user.lastTime = time.time()


    def update(user):
        if user.running:
           
            user.timeElapsed += time.dt


            hours = int(user.timeElapsed // 3600)
            minutes = int((user.timeElapsed % 3600) // 60)
            seconds = int(user.timeElapsed % 60)
            milliseconds = int((user.timeElapsed % 1) * 1000)  


            clockappFormat = f"{hours:03}:{minutes:02}:{seconds:02}.{milliseconds:02}"


            user.textEntity.text = clockappFormat


    def start(user):
        user.running = True


    def stop(user):
        user.running = False


    def reset(user):
        user.timeElapsed = 0
        user.textEntity.text = "000:00:00.00"


app = Ursina()


stopwatch = Stopwatch()


def start_stopwatch():
    stopwatch.start()


def stop_stopwatch():
    stopwatch.stop()


def reset_stopwatch():
    stopwatch.reset()


startButton = Button(text="Start", color = color.green, position=(-0.15, -0.15), scale=(.04, .04), on_click=start_stopwatch)
stopButton = Button(text="Stop", color = color.red, position=(-0.15, -0.2), scale=(0.04, 0.04), on_click=stop_stopwatch)
resetButton = Button(text="Reset", color = color.blue, position=(-0.15, -0.25), scale=(0.04, 0.04), on_click=reset_stopwatch)


startButton.text_entity.scale = (14, 14)
stopButton.text_entity.scale = (14, 14)
resetButton.text_entity.scale = (14, 14)

def on_circle_click():
    print("collapse")

circle = Entity(model='circle', color=color.red, scale=(.9, .8, .8), position=(.09,-3.2), collider = "box")

def update():
    if circle.hovered and held_keys['left mouse']:
        on_circle_click()

pit = Entity(model='quad', texture='drawing.png', scale = (14.6,8), position = (0, -.08))
app.run()



