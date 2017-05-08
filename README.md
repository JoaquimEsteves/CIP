Instructions on how to install python:

	Install python2 on your computer https://www.python.org/downloads/release/python-2713/
	Don't forget t o add PYTHON to your path, (when installing, scroll down and check this option


Instructions for running the program:

	0) Inside the Main.py directory, open the terminal (shortcut: shift+right mouse click -> open command prompt)
	1) run in  terminal:python Main.py
	2) If any library is missing, use >pip install *MISSING_LIBRARY_HERE*
	3) Other stations connect to the hostname.
	4) When you run the main file it'll tell you what is the IP and port you'll have to connect  to.
	
General Organization of the Files (Alphabetical Order):
	
	protocols.py:
		- This is where the TCP, UDP class is stored.
	
	settings.py:
		- This is just a file with a bunch of constants
	
	utils.py:
		- Logger class, it just helps to keeps things nice and organized!
		
	Main.py:
		- Obviously the main section of code.
		
	clienc.m
		- Generic client code in MATLAB
