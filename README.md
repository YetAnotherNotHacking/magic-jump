# MagicJump
A very basic datamoshing program for editting the raw bistreams of videos!
This allows for magic transition effects in your videos. 
# Features
This program has two main features, a datamosh transition and a datamosh melting effect.
# Installation
Download the latest release for your operating system from the Releases tab on GitHub.
## Transition
Deleting I-frames and making the decoder relay on P-frames to decode the image gives the image this very cool effect, see it below:
## Melting
A melting effect can be created by repeating P-frames after the last-iframe so that the decoder ends up distorting the image futher with bad motion data. The program is also able to do this.

# Other notes
Some other notes that might be helpful to someone using my program are:
 - The higher the quality value, the lower quality that the video will be
 - This program is only tested for Linux, if you run into issues with Windows or MacOS, please create an issue and I will resolve it quickly.
 - Star if you found this program helpful :D

# Demo
You are able to view a demo video on my Youtube Channel [here](https://www.youtube.com/watch?v=nCW5hlZGeOU)

### Siege
This program was created for the HackClub Siege hackathon, following this week's theme of magic!