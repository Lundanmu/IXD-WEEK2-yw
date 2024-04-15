# using ADC input to control servo movement
# NOTE: servo.py file should be saved to hardware first

import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import math
from servo import Servo  # import servo.py

title0 = None
label0 = None
color0= None
servo = None
adc1 = None

servo_timer = 0

rgb = None
rainbow_offset = 0

i2 = None

program_state = 'START'

def setup():
  global title0, label0, servo, adc1,rgb
  M5.begin()
  # display title ("title text", text offset, fg color, bg color, font):
  title0 = Widgets.Title("adc servo", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  color0 = Widgets.Title("RGB rainbow", 0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  # display label ("label text", x, y, layer number, fg color, bg color, font):
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # configure servo on pin 38:
  servo = Servo(pin=7)
  servo.move(90)  # stop the servo
  #servo.move(60)
  # initialize analog to digital converter on pin 1:
  adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  rgb = RGB(io=38, n=30, type="SK6812")
  rgb.fill_color(get_color(0, 250, 0))
  
# function to map input value range to output value range:
def map_value(in_val, in_min, in_max, out_min, out_max):
  out_val = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if out_val < out_min:
    out_val = out_min
  elif out_val > out_max:
    out_val = out_max
  return int(out_val)

def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

def hsb_to_color(h, s, v):
    h = float(h)/255.0
    s = float(s)/255.0
    v = float(v)/255.0
    
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]
    r = int(255 * r)
    g = int(255 * g)
    b = int(255 * b)
    rgb_color = (r << 16) | (g << 8) | b
    return rgb_color

def loop():
  global label0
  global program_state
  global servo_timer,rgb, rgb_timer, rainbow_offset
  
  M5.update()
  # read 12-bit ADC value (0 - 4095 range):
  adc1_val = adc1.read()
  
  # convert ADC value from 0-4095 range to 0-180 range:
  #servo_val = map_value(adc1_val, in_min=0, in_max=4095, out_min=70, out_max=110)
  #print('servo_val =', servo_val)
  # move servo using servo_val as input:
  #servo.move(servo_val)
  # display servo value on label0:
  #label0.setText(str(servo_val))
  
  if(program_state == 'START'):
    rgb.fill_color(get_color(250, 0, 0))
    if adc1_val > 2000:
      # update servo timer:
      servo_timer = time.ticks_ms()
      rgb_timer = time.ticks_ms()
      # move +1 step at a time from 70 to 110 degrees:
      program_state = 'STATE 1'
      print(program_state + "," + str(adc1_val))
      
      
  elif(program_state == 'STATE 1'):
    if adc1_val > 2000:
      rgb.fill_color(get_color(0, 250, 0))
      # current time is more than servo timer plus 5 seconds
      if(time.ticks_ms() > servo_timer + 3000):
        
        #print('move servo..')
        # start moving the servo:
        servo.move(105)
        #time.sleep_ms(100)
        # wait 2 seconds:
        time.sleep_ms(4200)
        # stop moving the servo:
        servo.move(90)
            
        program_state = 'STATE 3'
        print(program_state + "," + str(adc1_val))
        servo_timer = time.ticks_ms()
        rgb_timer = time.ticks_ms()
        
  elif(program_state == 'STATE 2'):
    rgb.fill_color(get_color(250, 0, 0))
    if adc1_val > 2000:
      rgb.fill_color(get_color(0, 250, 0))
      # current time is more than servo timer plus 5 seconds
      if(time.ticks_ms() > servo_timer + 3000):
        
        #print('move servo..')
        # start moving the servo:
        servo.move(105)
        #time.sleep_ms(100)
        # wait 2 seconds:
        time.sleep_ms(5400)
        # stop moving the servo:
        servo.move(90)
        time.sleep_ms(50)
        program_state = 'STATE 3'
            
        print(program_state + "," + str(adc1_val))
        servo_timer = time.ticks_ms()
        rgb_timer = time.ticks_ms()
        rgb.fill_color(get_color(250, 0, 0))
        
  elif(program_state == 'STATE 3'):
    rgb.fill_color(get_color(250, 0, 0))
    if adc1_val > 2000:
      for i2 in range(100):
        for i in range(30):
    # hue based on pixel index:
    #hue = map_value(i, 0, 30, 0, 255)
    # hue based on pixel index and rainbow offset:
          index = (i + rainbow_offset) % 30
          hue = map_value(index, 0, 30, 0, 255)
          color = hsb_to_color(hue, 255, 255)
          rgb.set_color(i, color)
        rainbow_offset += 1
        time.sleep_ms(50)
      program_state = 'STATE 4'
      
  elif(program_state == 'STATE 4'):
    if adc1_val < 2000:
      program_state = 'STATE 2'
    
  if(program_state == 'STATE 2') or (program_state == 'STATE 3')  or (program_state == 'STATE 1'):
    if adc1_val < 2000:
      #program_state = 'STATE 2'
      #print(program_state + "," +  str(adc1_val))
      servo_timer = time.ticks_ms()
      rgb_timer = time.ticks_ms()
      
  #else:
  #  servo.move(90)
  #  time.sleep(1)
  
  #print('light sensor =', adc1_val)
  print(program_state + "," +  str(adc1_val))
  time.sleep_ms(100)
  
  
if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
