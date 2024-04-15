import js as p5
from js import document

data_string = None
data_list = None

# load sound data and assign it to variable:
sound1 = p5.loadSound('quite.mp3') 
sound2 = p5.loadSound('moon.mp3') 
sound5 = p5.loadSound('funky.mp3') 
soundall = [sound1, sound2, sound5]
voice = soundall[int(p5.random(3))]


def setup():
  p5.createCanvas(300, 300)

def draw():
  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')
  # assign 1st item of data_list to sensor_val:
  program_state = data_list[0]
  # assign 2nd item of data_list to sensor_val:
  sensor_val = int(data_list[1])

  if (program_state == "STATE 4"):
    voice.play()

  else: 
    voice.stop()
