# Yi Wang - Final Project
## Muisc Gotcha Machine

## Introduction   
This is a music gotcha machine to help users select music. While people want to play music in daily life, sometimes they don’t know what to listen to. So I want to make a fun music selector to help them make the decision. The way this device works is, everytime it rotates it will drop a ball off. When the ball rolls to the hole, the computer will play music. The initial idea is designing the machine connected to a website. The user will play the sound by inputting the number written on the ball to the website. While I was working on the progress, I found out there are too many unnecessary steps in this way, so I got rid of the website part, enabling users to play music as long as they make the machine rotate. 

Final Outcome

![IMG_0263](https://github.com/Lundanmu/adv-prototyping/assets/141177081/5035e814-19b6-4712-a900-05139c2daf1d)

Initial Idea

![未命名作品 8 1](https://github.com/Lundanmu/adv-prototyping/assets/141177081/b9e20ba4-fa0f-45d2-a6e1-ea35fe8ef08d)

Exploring different forms

![Group 7](https://github.com/Lundanmu/adv-prototyping/assets/141177081/02f6ac00-0661-44bd-9008-be096f36d9df)

## Implementation   
### Enclosure / Mechanical Design:
I used:
* Laser cut acrylic for the gotcha box
* 20 LB foam for the base and stand
  
Since this is a project highly based on the mechanical part, there are few things I was not sure about at the beginning stage, such as if the servo is strong enough to rotate the gotcha box. To make these questions figured out, I need to make a quick prototype. For the gotcha box, I get the acrylic pieces using laser cut, and table saw to make the 30° angle on the edge. The thickness of acrylic is 1/4’’ so it is easy for me to stick them together. 
For the base and the stand, I use a soft 6LB foam (pink) and 20 LB foam together (orange).

laser cut file for the gotcha box

![Group 11](https://github.com/Lundanmu/adv-prototyping/assets/141177081/90adbc9c-43c4-47a2-84e9-c222dbfc2e56)

Stick acrylic on a board to cut the 30° angle edge & make the central part thinner

![surface top](https://github.com/Lundanmu/adv-prototyping/assets/141177081/c518c44f-1715-409e-86d6-01b8130b1cdf)

Cut the first prototype out 

![first pp](https://github.com/Lundanmu/adv-prototyping/assets/141177081/c8de3dcb-bb42-44b8-a7d6-047d8e50f824)

From the first test, I am glad to find out the servo is able to move the gotcha machine. So I start to do the second, or the final prototype. I change all of the foam to 20LB because it is a stronger material. 

![box*stand](https://github.com/Lundanmu/adv-prototyping/assets/141177081/34d59631-c8f5-422a-9da1-8abe7fbc4c69)

### The Hardware Part:
I used:
* One M5Stack AtomS3 Lite Controller
* One M5Stack ATOMIC PortABC Extension Base
* One LED Strip Light
* One Light Sensor Unit
* One 360° Servo Unit
   
![harware](https://github.com/Lundanmu/adv-prototyping/assets/141177081/c44e187d-3c70-4692-8b0d-84177138f86b)

In order to make the light sensor be sensitive enough, I stick it to the back of the lid of the base. I hide all of the hardware inside the base, and the wire will come out through a hole.

![Group 8](https://github.com/Lundanmu/adv-prototyping/assets/141177081/aa9d1a45-6f5f-4de4-a3c9-1139ad3ec8e4)

![stuck](https://github.com/Lundanmu/adv-prototyping/assets/141177081/7aa766bc-5177-4a8f-bed6-617bc7daac42)

The round disk is sticked on the acrylic surface strongly. I need to insert the servo into the disk to make the gotcha box move.

![servo stucking](https://github.com/Lundanmu/adv-prototyping/assets/141177081/29f4d564-31a8-4069-8cdf-6223b98a6937)


### Firmware:
I used:
* MicroPython
  
[Code for Firmware](../final/final.py) 

I was mainly using a light sensor as my input. Its adc_value serves as the trigger to switch between different states. Here is the setup for the light sensor.

``` Python  
adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
```

Set the 'START' state, resetting all the timers and enable the LED Light turn on to red.

``` Python  
  if(program_state == 'START'):
    rgb.fill_color(get_color(250, 0, 0))
    if adc1_val > 1700:
      # update servo timer:
      servo_timer = time.ticks_ms()
      rgb_timer = time.ticks_ms()
      # move +1 step at a time from 70 to 110 degrees:
      program_state = 'STATE 1'
      print(program_state + "," + str(adc1_val))
```

In order to achieve the change between the rotating mode and sound mode, I set four states in the program after the user turns on the device. The first state is 'STATE 1'.When the user long presses the button, the program will enter 'STATE 2' to make the servo move 180°. The LED light will turn from red to green. So basically, this state serves as a switch.

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
After that, a ball will come off and rolls to the hole. When the ball rolls to the hole, the program will enter 'STATE 3', the music playing state. The LED light will turn to rainbow color and the computer will play sound.

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
When the users pick the ball up, the program will enter 'STATE 4', which allows it to go back to 'STATE 2'.

``` Python  
  elif(program_state == 'STATE 4'):
    if adc1_val < 800:
      program_state = 'STATE 2'
```

'STATE 2' is basically the same as 'STATE 1'. The only difference is when users long press the button, the servo moves 360° instead of 180°, because the opening now goes to the bottom after the first rotation.

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

Because this program needs the computer to play music, I need to use WebSerial PyScript. In Thonny, the program will print the state and send it to Visual Studio Code to play the voice.
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

## Project outcome  
The image

![IMG_0263](https://github.com/Lundanmu/adv-prototyping/assets/141177081/5035e814-19b6-4712-a900-05139c2daf1d)

![gotcha side](https://github.com/Lundanmu/adv-prototyping/assets/141177081/245a5449-ff27-4044-8a61-9bd8b79ff3c9)

Demo video

https://github.com/Lundanmu/adv-prototyping/assets/141177081/fbbf32de-41f7-4df9-8e31-99fe85fc539c
mklop0ljj
The change of light

https://github.com/Lundanmu/adv-prototyping/assets/141177081/2782515a-faf9-4e1d-bc82-74d4e04a179f

## Conclusion  
### What I have learned  
I learned a lot about how to combine the physical parts and coding together. There are a lot of things we need to consider to make the mechanical design work well and really express our idea. It is very interesting to see that using the same sensors and units can achieve so many different outputs based on your concept. Besides, my coding skills get really developed in this class. Before that, I could not imagine myself to deal with tricky state changes like what I have achieved in this project.

### Opportunities & Future Development 
There are still a couple of things I could explore in this project. For the mechanical part, the chances for the ball to fall off are not so stable, because it may get stuck at the opening or piled up to block it. I may fix it by drilling the opening bigger and making a door for that. 
For the coding part, initially I wanted the rainbow color to be blinking while playing the music. However I found out the waiting time for the blinking loop and the waiting time for the states will conflict, which means the state will stop changing if I applied the blinking effect. So I would like to explore this problem more if I have more time.

## Project references  

Links for Rainbow Color LED Light Effect:
https://genshin-impact.fandom.com/wiki/Freedom-Sworn
