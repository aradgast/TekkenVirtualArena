# Tekken Virtual Arena
Final project in DIP course - tekken virtual arena

How to play using the code??
1. install requirements from the requirement.txt file.
2. run the main.py file
3. in the terminal, you will ask to choose the number of players - one or two.
4. now, you can see to fill in the source for the first player.
each usb port gets a number, and for the built-in camera in your laptop choose "0".
5. after fill up the source, a live stream from the camera will appear. you will need to capture the background,
just press SPACE button when ready, and press 'y' if you are satisfied, if not, press 'n'
and repeat this process.
   (<ins>**note**</ins>: it will be better if there is no reflective surface in the frame. if needed, you can edit the exposure value if
needed by pressing '4' and '6'.)
6. then you will need to capture the player, ask the first player to stand in the center of the frame in a fight pose.
you can see the green bounding box that capture the player, if it captures the player from the top of his head to his fits,
press SPACE, and press 'y' if you are satisfied, if not, press 'n'
and repeat this process. you can adjust the threshold for the binary image by pressing "4" and "6".
7. now player one is all set, repeat 4-6 if choose two plater in section 3.
8. you can see a 5 seconds counter in the terminal, and after it get to zero, you can start <ins>**fighting**</ins>