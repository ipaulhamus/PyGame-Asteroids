# PyGame Asteroids

*What is this?* This project is an Asteroids game for the Raspberry Pi created using the PyGame engine. This game is controlled by an external joystick wired to the Pi through a breadboard, using the "Joystick" library to read inputs from the Joystick. The goal of the game is dodge the asteroids for as long as possible, with the player earning one point for every second they can pilot the ship without crashing. The game also makes use of some other breadboard components, including three LEDs. These LEDs are used to indicate the health of the ship, being green, yellow, or red.

This repository includes the code for the game, the assets the game uses, and an example of the game in action.

The game is built in a modular fashion, with functions such as "input_event", "do_keypress_event", "pause_check", and more being transportable to other PyGame projects. The game has three actors, being the Ship, Asteroid, and Comet. Each actor has it's own class with their own functions defining how they should be drawn on the screen and how much they should move each time a frame is rendered while they are in motion.

This project demonstrates a solid understanding of Python, writing modular programs, and working with IoT devices.
