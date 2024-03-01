import js as p5
from js import document

data_string = None
data_list = None

# load sound data and assign it to variable:
sound1 = p5.loadSound('quite.mp3') 
sound2 = p5.loadSound('noise.mp3') 
table = p5.loadImage('table2.png')

circle_color = p5.color(0, 0, 0)
circle_x = 150
x_position = p5.random(20,250)
x2_position = p5.random(20,250)
veg = ['🍅', '🥬', '🥕']
veg1 = veg[int(p5.random(3))]
veg2 = veg[int(p5.random(3))]
def setup():
  p5.createCanvas(300, 300)
  # change mode to draw rectangles from center:
  p5.rectMode(p5.CENTER)
  # change mode to draw images from center:
  p5.imageMode(p5.CENTER)
  # change stroke cap to square:
  p5.strokeCap(p5.SQUARE)
  



def draw():
  global circle_color, circle_x, x_position, x2_position, veg, veg1, veg2
  global table

  x2_position = p5.random(300)
  veg2 = veg[int(p5.random(3))]

  p5.background(255)
  global data_string, data_list


  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  # assign 1st item of data_list to sensor_val:
  imu_val = int(data_list[0])
  # assign 2nd item of data_list to sensor_val:
  button_val = int(data_list[1])


  if imu_val > 150:
    circle_color = p5.color(0,0,255)
    if(circle_x > 0):
      circle_x -= 3.5
    #p5.background(0,0,255)
      
    p5.textSize(18)
    p5.text('Left', 130, 65)
    sound1.play()
    p5.push()
    p5.scale(0.51)
    p5.image(table, 297, 315)
    p5.pop()
    
  if imu_val < 80:
    circle_color = p5.color(255,0,0)
    if(circle_x < 300):
      circle_x += 3.5
    #p5.background(255,0,0)
    p5.textSize(18)
    p5.text('Right', 130, 65)
    p5.push()
    p5.scale(0.51)
    p5.image(table, 297, 315)
    p5.pop()
    

  if (imu_val > 80) and (imu_val < 150) :
    p5.background(255,255,255)
    p5.textSize(16)
    p5.text('Eat some vegetables', 80, 65)
    p5.push()
    p5.scale(0.51)
    p5.image(table, 297, 315)
    p5.pop()

  if abs(circle_x - x_position) < 7:
    veg1 = veg2
    x_position =x2_position
  else:
    p5.fill(255,153,0)
    p5.text(veg1, x_position, 150)

  p5.noStroke()
  p5.fill(circle_color)
  p5.circle(circle_x, 150, 60)


