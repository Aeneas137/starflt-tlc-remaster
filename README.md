# Starflight: The Lost Colony Remastered
A remaster of Starflight: The Lost Colony using Python, Pygame, and other tools to make modifications easier. The old codebase for TLC was started in 2006 with Visual C++ 2005 and a lot of libraries, and upgraded in 2010. It is difficult to set up the development environment for this project as a result of old dependencies. In addition to upgrading the art and gameplay, the new codebase will be more easily manageable. 

Why Python? Python is interpreted, while C++ is compiled and very fast. Isn't that a step backward? It is if your goal is framerate. This game does not require FPS-like framerates; it is a 2D game, a "space RPG" with only a few objects on the screen at a time. It will run fine with Python + Pygame and support libraries. Even the more demanding space combat module will run fine with Python.

It takes many hours to set up Visual C++ 2010 with all of the dependencies, even if you can find this version of the IDE today (normally a MSDN membership is req'd). Patches are required. Many updates are req'd and this process is time-heavy and error prone. Python takes only a few minutes to install and the libraries are installed with simple shell commands in a few seconds. Python is arguably easier to code than C++. 

But perhaps the most compelling reason to remaster the game is that the storyline was written in Lua code, which is a script language like Python, and a library is available called lupa to facilitate easy integration. We could rewrite the scripts for Python but this is not necessary: we can use Lua easily with lupa.

The old Allegro game engine in TLC works well but is difficult to deal with if any changes are needed. The game took a very long time to debug and finish because of Allegro. Granted, it was faster to adopt than DirectX, and cross-platform was a major consideration at the dawn of the project. This was a mistake. We should have used DirectX from the start. Going with Pygame eliminates the problem of updates. A python-based game will run on all kinds of different hardware. 

We need to start from scratch. There's no "upgrading from C++ to Python" here. The game will be rebuild from the ground up with Python.


