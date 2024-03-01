import os, sys, io
import M5
from M5 import *
import time

title0 = None
label0 = None
label1 = None
label2 = None

imu_val = None

def setup():
  global title0, label0, label1, label2

  M5.begin()
  title0 = Widgets.Title("IMU test", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label1 = Widgets.Label("--", 3, 40, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label2 = Widgets.Label("--", 3, 60, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)


def loop():
  global title0, label0, label1, label2
  global imu_val
  M5.update()
  
  # read the IMU accelerometer values:
  imu_val = Imu.getAccel()
  
  # print all IMU values (X, Y, Z):
  print(imu_val)
  # print the first IMU value (X) only:
  #print('acc x:', imu_val[0])
  
  # format each IMU value with 2 points precision:
  imu_str = 'acc x: {:0.2f}'.format(imu_val[0])
  label0.setText(imu_str)
  imu_str = 'acc y: {:0.2f}'.format(imu_val[1])
  label1.setText(imu_str)
  imu_str = 'acc z: {:0.2f}'.format(imu_val[2])
  label2.setText(imu_str)
  
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
