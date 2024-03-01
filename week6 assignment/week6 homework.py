# read and print IMU X, button values
# this example can be used with WebSerial Pyscript Template


import os, sys, io
import M5
from M5 import *
from hardware import *
import time

title0 = None
label0 = None
pin41 = None

def setup():
  global label0, pin41
  M5.begin()
  # initialize dispaly title and label:
  title0 = Widgets.Title("IMU, button", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # initialize pin 41 (screen button on AtomS3 board) as input:
  pin41 = Pin(41, mode=Pin.IN)

# function to map input value range to output value range:
def map_value(in_val, in_min, in_max, out_min, out_max):
  out_val = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if out_val < out_min:
    out_val = out_min
  elif out_val > out_max:
    out_val = out_max
  return int(out_val)

def loop():
  global label0
  M5.update()
  
  # read button value:
  button_value = pin41.value()
  
  # read the IMU accelerometer values:
  imu_val = Imu.getAccel()

  # map the IMU X value from -1.0 - 1.0 to 0 - 255 range:
  imu_x_val_8bit = map_value(imu_val[0], -1.0, 1.0, 0, 255)
  #print(imu_x_val_8bit)
  
  # print imu_x_val_8bit, button_value:
  print(str(imu_x_val_8bit) + ',' + str(button_value))
  
  # display imu_x_val_8bit, button values on display label:
  label0.setText(str(imu_x_val_8bit) + ',' + str(button_value))
  time.sleep_ms(500)

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