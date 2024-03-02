# Pong with Hand Gesture Tracking

## A cross-platform project written in Python - Pygame!

This repository contains the code for a Pong video game developed in Python. The unique aspect of this game is the control mechanism - the player uses hand gestures captured by the laptop's webcam to move the paddle. This project integrates computer vision techniques with real-time game mechanics.

## Key Features
- Game Interface: A classic Pong game with a bouncing ball and a player-controlled paddle.
- Control Mechanism: The player's hand position in the webcam feed 
  determines the paddle's vertical movement.
- Difficulty Level: The game starts slow and gradually increases ball speed 
  with successful hits.
- Score System: Players earn points for hitting the ball and lose points for 
  missing it.

## Game Modes:
### Solo Mode (2D):
Single hand controls the paddle vertically based on hand position in the webcam feed.
Players score points for hitting the ball and lose points for missing it.
### Two Player Mode (2D):
Player on the left side of the screen controls the left paddle based on 
their hand's vertical position.
Player on the right hand controls the right paddle based on their hand 
vertical position.
Players score points when their opponent misses the ball.
### Solo Mode (3D): (Most difficult to master)
Single hand controls the paddle.
Vertical hand movement controls the paddle up and down (like 2D mode).
Forward and backward hand movement controls the paddle moving in and out of the screen (depth).

## What else?
### Movement that Feels Natural: Beyond Button Presses
Traditionally, Pong games relied on button presses to control the paddle. 
While effective, this approach doesn't translate well to real-world 
interactions.  Imagine hitting a real ping pong ball - you wouldn't 
repeatedly tap or long press a button!

This game takes a different approach. By using hand tracking, your movements in the air directly translate to the paddle's movement on screen. This intuitive control scheme feels more natural, especially when playing the 3D version where depth adds another layer of realism. 
It's like you're truly pushing the paddle through the air to hit the ball!

### Immerse Yourself in the Game: Sound and Visual Cues
The game provides immediate feedback through engaging sound effects and subtle visual changes to keep you in the zone:

#### Sound Effects: 
A satisfying sound rings out when your paddle makes contact with the ball, keeping you informed of your successful hits. Additionally, a distinct sound effect plays when you miss a shot, letting you know it's time to refocus.

#### Level Up with Color: 
As the game progresses and the difficulty ramps up, the ball subtly transforms its color. It starts as a fiery red, and as you conquer each level, it transitions through the color spectrum like a mini-rainbow, giving you a visual cue of your growing mastery.


## Watch the demonstration!




## Technical features
### More real-world like due to added physics: 
The paddle's impact transfers horizontal momentum to the ball upon contact. 
This interaction, however, isn't frictionless. 
The brief moment of impact also introduces an impulsive frictional force that 
acts in the opposite direction of the ball's movement relative to the paddle. 
Imagine it like a tiny braking effect. This frictional force can be 
approximated as a step change in the ball's vertical velocity. 
That's the secret sauce! By strategically using the paddle's movement, skilled players can exploit this friction to slow down the ball's bounce, giving them more control over the game.
### Decoupled update and refresh
The game logic and element updates run at a much higher rate than both the screen's refresh rate and the webcam's capture frequency. 
This clever design ensures the ball can travel at high speeds without ever appearing to teleport past the paddle or walls. 
In the background, interpolation steps seamlessly track the precise movements of all elements, creating a smooth and responsive gameplay experience.

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues (Work in progress)

### Missing Settings Menu: 
We're currently working on adding a settings menu 
where you can customize your gameplay experience. This will allow you to adjust hand speed sensitivity, toggle sound effects, and choose a game background – all to your liking!

### Full-Screen Scaling: 
While the game can be played in full-screen mode, the 
game elements themselves (paddle, ball, etc.) don't currently scale up to match the larger window. We're working on a fix to ensure everything remains crisp and visible at any screen size. 

These and other updates are coming soon!