# Quick Stage
##### A CS50 Harvard Final Project 2021, by Samuel Christofan Auditama
#### Video Demo:
#### Contact me: samuel.auditama@gmail.com

## Overview
Hi, my name is Samuel, I'm a 3D artist from Jakarta, Indonesia. I took CS50 because I wanted to have complimentary skills to my primary trade: 3D animation and motion graphics.
For the final project, I wrote this addon script for Blender. This is a python script which I wrote inside the python interpreter that comes with Blender and Blender API.
The goal of this project is to make tools that would greatly increase my work efficiency by automating the tedium of my field of work, so I can better focus my time and energy on the important things.

First, a quick summary of what this script does. Like the name, Quick Stage, the goal of this script is to let the user skip the mundane and tedious task of setting up a render. 
It does so by introducing these features:
- Render resolution & ratio changer.
- Spawning a camera with controller rig
- Spawning preset light setups.

A more detailed explanation below.
If you would like to know how the script works, you can take a peek inside the py file as I put in a generous amount of comment within it, so as to show you how it works.

## Installation
Installation is pretty simple, even if you have never used Blender before:

1.	Start Blender
2.	Go to edit, preference, addons, and click install
3.	Point it to the script
4.	Type in the search bar “Quick Stage”, a single entry will come out.
5.	And tick in the box to enable it. - You don't even need to restart Blender.

### Uninstall
If for whatever reason that you need to uninstall this script:

1. Go to edit, preference, addons.
2. Type in the search bar “Quick Stage”.
3. In the entry, click it to expand the dropdown
4. Press remove.

## Features
### Resolution & Ratio Changer

Straight up changes the resolution and ratio of your render. Just choose from the dropdown menu which rez and ratio you’d like your render to be, and click the respective buttons.
Skipping the hassle of typing in the resolution manually.
Side note, when you click change resolution, I’ve made it so that it dynamically takes into account the ratio you choose. So it automatically change it for you.

### Cam Rig

Spawn camera with controller rigs, it comes in Simple and Complex. The general principle is the same, instead of having to deal with the hassle of manual camera control, I’ve added the controller rig to make it easier to animate the camera.
This part of the script is heavily inspired by how camera objects in Autodesk Maya is set up. You have the option of making just a camera, or also make all this bells and whistle - which turns out to be quite helpful... and I sort of miss that feature while working in Blender. So ...why not make it exist in Blender?

#### Simple

Simple rig makes a camera and an 'empty' object. The camera is constrained to the 'empty', making it face the 'empty' object at all times - essentially turning it into a focus point. This allows you to easily adjust where your camera is pointing by using the focus point as a reference. This focus point also doubles as a Depth of Field focus.
Personally, this is the rig that i often used for most things. I would even go as far to suggest putting a second constraint on the camera, making it lock its position to a Spline Curve - so the camera movement is "on rail" like real camera would, and you are free to pan around using the focus point.

#### Complex
Complex camera controller is divided into multiple gimbal, constraints and empty object:
- Focus point: Similar as before, but now acts as a 'floor' for the rest of the rig to follow.
- Rotation object: The camera rotates around the focus point, and this rotation object is parented to the focus object.
- Zoom handle: Like the name - an object constraint to the camera and the camera to the object ... being only allowed to move a single axis which brings the camera further or closer from the focus.
- Camera itself.

##### Extra
There is also the option to have a light attached to the camera object, good for low light renders where you need a slight illumination where the camera is pointing.

### Light Setup

Inspired by the photography light setup that is posted by [Digital Camera World](https://www.digitalcameraworld.com/tutorials/cheat-sheet-pro-portrait-lighting-setups "Digitalcameraworld.com Lighting Guide Cheat Sheet."). This part of the script spawn in various light setups. These light setup closely follows the cheat sheet by DCW, but I’ve also rigged to simple controllers for when you need to adjust it to your scene.

##### Current light presets included
- Flat Light
- Clamshell
- Key Fill & Highlight
- High Key
- Loop with Rim Light
- Hard Key with Kickers
- Badger

Again, choose from the dropdown menu, and click the button.

# Closing
That’s all really, I plan on making the script free to download for everyone at a later date in Blender Market or other 3D marketplace. But first, i feel like there is some key features that I would like to implement before release (or post release).

- Stages... Ironically, despite the name, this script does not include stages/pedestal/display racks. I am somewhat conflicted about it too, if someone wants it, making a simple stage is pretty quick, thus I don’t see point of including one in the script. Then again, I could model a somewhat decent stage, upload it along the script, and the users could just drag and drop the file into their scene. But if I were to take the long road of coding in custom 3D geometry, I’ve actually watched some [youtube tutorials by Curtis Holt](https://youtu.be/mljWBuj0Gho) on how to make 3D objects by inputting Cartesian coordinates in python and assembling it vertex by vertex. 
- More light setups, I’ve only included a handful, and the cheat sheet from DCW still has a ton more!
- Batch rendering using multiple cameras and multiple intersecting timeline, sort of a far fetch (also frankly i haven't learn/research about it) - but it would be pretty neat - turning it from a simple quality of life improvement script into a full blown rendering management addon.



### Special Thanks

#### First, I’d like to thank all the CS50 staff for making learning possible in pandemic condition. Its been a journey, one that I would not imagine Id achieve went I started it – but here I am making scripts for 3D software.

also to all these people:

Author of Blender - Ton Roosendaal
For making an amazing software...for free!

Blender Foundation & Institute

Blender and Open Source community in large

Author of Python: Guido van Rossum

Curtis Holt and his YouTube tutorials on Blender Python API
https://youtu.be/XqX5wh4YeRw

Digital Camera World for their handy lighting guide
https://www.digitalcameraworld.com/tutorials/cheat-sheet-pro-portrait-lighting-setups

Darkfall studio, also for his tutorials
https://www.youtube.com/c/DarkfallBlender/about
https://darkfallblender.blogspot.com/

Blender Stack Exchange
https://blender.stackexchange.com/

CS50 Discord community and people

W3 School for help with python syntax
https://www.w3schools.com/python/

#### Last but not least, my fellow 3D artists friends that tested my script.
