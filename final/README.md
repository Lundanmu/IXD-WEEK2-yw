# Yi Wang - Final Project
## Muisc Gotcha machine

## Introduction   
This is a music gotcha machine to help users select music. While people want to play music in daily life, sometimes they don’t know what to listen to. So I want to make a fun music selector to help them make the decision. The way this device works is, everytime it rotates will drop a ball off. When the ball rolls to the hole, the computer will play a music. The initial idea is designing the machine connected to a website. The user will play the sound by inputing the number written on the ball to the website. While I was working on the progress, I found out there are too many unneccesary steps in this way, so I get rid of the website part, enabling user to play music as long as they make the machine rotate. 

![IMG_0263](https://github.com/Lundanmu/adv-prototyping/assets/141177081/5035e814-19b6-4712-a900-05139c2daf1d)

Final Outcome

![未命名作品 8 1](https://github.com/Lundanmu/adv-prototyping/assets/141177081/b9e20ba4-fa0f-45d2-a6e1-ea35fe8ef08d)

Initial Idea

![Group 7](https://github.com/Lundanmu/adv-prototyping/assets/141177081/02f6ac00-0661-44bd-9008-be096f36d9df)

Exploring different forms

## Implementation   
### Enclosure / Mechanical Design:
I used:
* Laser cut arylic for the gotcha box
* 20LB foam for the base and stand
  
Since this is a project highly based on the mechanical part, there are few things I did not sure about at the beginning stage, such as if servo is strong enough to rotate the gotcha box. To make these questions figure out, I need to make a quick prototype. For the gotcha box, I got the acrylic pieces using laser cut, and table saw to make the 30° angle on the edge. The thickness of acrylic is 1/4’’ so it is easy for me to stuck them together. 
For the base and the stand, I used a soft 6LB foam (pink) and 20LB foam together (orange).

![process gotcha2](https://github.com/Lundanmu/adv-prototyping/assets/141177081/f535feef-bf1a-4a86-ad4e-0a442ebe83f0)

laser cut file for the gotcha box

![Group 9](https://github.com/Lundanmu/adv-prototyping/assets/141177081/b73aa09f-c69a-4094-80ed-a43ea680ea27)

Stick acrylic on a board to cut the 30° angle edge & First prototype

From the first test, I was glad to find out the servo is able to move the gotcha machine. So I started to do the second, or the final prototype. I changed all of the foam to 20LB because it was a stronger material. 

![Group 8](https://github.com/Lundanmu/adv-prototyping/assets/141177081/043788ba-87f8-42cd-81c7-4643aa532f1d)

### The Hardware Part:
I used:
* One M5Stack AtomS3 Lite Controller
* One M5Stack ATOMIC PortABC Extension Base
* One LED Strip Light
* One Light Sensor Unit

`[https://github.com/Lundanmu/adv-prototyping/blob/main/final/main.py](./)`  

In order to make the light sensor be sensitive enough, I stick it to the back of the lid of the base. I hide all of the hardware inside the base, and the wire will come out through a hole.

![Group 8](https://github.com/Lundanmu/adv-prototyping/assets/141177081/aa9d1a45-6f5f-4de4-a3c9-1139ad3ec8e4)

### Firmware:
I used:
* MicroPython
  
[Code for Firmware](../final/final.py) 

Light sensor setup:

``` Python  
adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
```
In order to achieve the change between the rotating mode and sound mode, I set four states in the program. The first state is 'STATE 1'.When the user long press the button, the program will enter 'STATE 2' to make the servo moves 180° degree. The LED light will turn from red to green.

``` Python  
  elif(program_state == 'STATE 1'):
    if adc1_val > 1700:
      rgb.fill_color(get_color(0, 250, 0))
      if(time.ticks_ms() > servo_timer + 3000):
        servo.move(105)
        time.sleep_ms(1700)
        servo.move(90)
            
        program_state = 'STATE 3'
        print(program_state + "," + str(adc1_val))
        servo_timer = time.ticks_ms()
        rgb_timer = time.ticks_ms()
```
After that, a ball will come off and rolls to the hole. When the ball rolls to the hole, the program will enter 'STATE 3', the music playing stage. The LED light will turn to rainbow and the computer will play sound.

``` Python  
elif(program_state == 'STATE 3'):
    rgb.fill_color(get_color(250, 0, 0))
    if adc1_val > 1000:
      if(time.ticks_ms() > rainbow_timer + 50):
        rainbow_timer = time.ticks_ms()
        for i in range(30):
            # hue based on pixel index:
            #hue = map_value(i, 0, 30, 0, 255)
            # hue based on pixel index and rainbow offset:
            index = (i + rainbow_offset) % 30
            hue = map_value(index, 0, 30, 0, 255)
            color = hsb_to_color(hue, 255, 255)
            rgb.set_color(i, color)
        rainbow_offset += 1
        program_state = 'STATE 4'
```
When the user pick the ball off, the program will enter 'STATE 4', which allows it to go back to 'STATE 2'.

``` Python  
  elif(program_state == 'STATE 4'):
    if adc1_val < 800:
      program_state = 'STATE 2'
```

'STATE 2' is basically the same as 'STATE 1'. The only difference is when the user long press the button, the servo moves 360° instead of 180°, because the opening now goes to the bottom after the first rotation.

``` Python  
if adc1_val > 1700:
      rgb.fill_color(get_color(0, 250, 0))
      # current time is more than servo timer plus 3 seconds
      if(time.ticks_ms() > servo_timer + 3000):
        
        servo.move(105)
        time.sleep_ms(1700)
        servo.move(90)
            
        program_state = 'STATE 3'
        print(program_state + "," + str(adc1_val))
        servo_timer = time.ticks_ms()
        rgb_timer = time.ticks_ms()
```
### Software & Integrations:
I used:
* Python syntax
  
[Code for Software](../final/main.py) 

Because this program needs the computer to play music, so I need to use WebSerial PyScript. In Thonny, the program will print the state and send it to Visual Studio Code to play the voice.
``` Python  
  if (program_state == "STATE 4"):
    if(sensor_val > 1000):
      if(voice.isPlaying() == False):
        voice.play()
    #program_state = "STATE 2"

  else: 
    voice.stop()
```
I also made the sound play randomly by using random() from p5.libraty.
``` Python  
sound1 = p5.loadSound('quite.mp3') 
sound2 = p5.loadSound('moon.mp3') 
sound3 = p5.loadSound('tides.mp3') 
sound4 = p5.loadSound('stars.mp3') 
sound5 = p5.loadSound('funky.mp3') 
soundall = [sound1, sound2, sound3, sound4, sound5]
voice = soundall[int(p5.random(5))]
```

### The showcases of the gotcha machine:

https://github.com/Lundanmu/adv-prototyping/assets/141177081/fbbf32de-41f7-4df9-8e31-99fe85fc539c

The whole demo

https://github.com/Lundanmu/adv-prototyping/assets/141177081/2782515a-faf9-4e1d-bc82-74d4e04a179f

The change of light

## Project outcome  

From this project, not only did I learn how to write programs better, but I also did I enhanced my skill of designing and making hand-made stuff. For the programming part, I now have the ability to know micro python better, to understand how different devices connect together, and how those devices are able to connect to the Internet. It is really important for me to understand all of those things before I push my interactive design to the next level. For the hand-making part, this is my first time making a "Real-Sword", from the first version to the final outcome, I understood how could I make a real hand-made prototype and get through troubles. Meanwhile, improving my hand-made skill is also beneficial for me to do my own physical interaction projects in the future.

## Conclusion  

This term is the first term I really got a feeling of how to learn and write codes, before finishing the final project, I never thought I can push those three ideas so far. Because of this, I think this project really gives me the opportunity to do a design that combines physical and digital interactions together. And moreover, I also feel happy that I could create something real for the game I love and make them work!

## Project references  

Links for Rainbow Color LED Light Effect:
https://genshin-impact.fandom.com/wiki/Freedom-Sworn
