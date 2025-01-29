from PIL import Image #To get the image
import numpy as np #To represent image in array
from time import sleep #To wait before beginning to draw
import pyautogui #To move mouse
import os #To verify image file


def draw(filepath=None, scale = 1, threshold=0.5, pause = 0.004):
    """
    Draws image
    :param filepath: Path of file
    :param scale: How many pixels to jump each time (Defaults to 1)
    :param threshold: Brightness level needed to constitute image as white (not draw it) (defaults to 0.5)
    :param pause: Pause in seconds between movements (lower value move quicker, but can cause problems with the windows input buffer) (defaults to 0.004)
    """
    def getImageInfo(default=1): #gets image info
        while not os.path.isfile(filepath := input("Enter file path: ").strip('"')):
            filepath = input("Enter file path: ").strip('"')
        try:
            scale = int(input("Enter scale: "))
        except:
            print(f"Invalid scale. Setting to default ({default})")
            scale=default
        return (filepath, scale)
    pyautogui.PAUSE = pause
    if filepath is None: #gets image info from console if not provided
        filepath, scale = getImageInfo(scale)


    img = Image.open(filepath)
    imageArray = np.array(img) #represents image as 3d array [rows,pixels,RGB]
    print("Drawing in 3 seconds... ")
    sleep(3) #gives user time to switch to drawing application
    mousePos = pyautogui.position() #sets top left mouse position
    for ridx, row in enumerate(imageArray): #iterates over rows
        width = len(row) #width of row
        first = None #first black pixel's position in sequence of black pixels (used for dragging across large lines of black)
        for pidx, pixel in enumerate(row): #iterates over pixels in row
            average = sum(color for color in pixel.tolist())/(255*len(pixel)) #gets brightness value
            if average<=threshold: #if black pixel
                if first is None: #if it is the first black pixel in row, or previous was white
                    first = (mousePos[0]+pidx*scale,mousePos[1]+ridx*scale,0)
                if pidx == width-1:#if last pixel in row, draw from first black pixel in series to last pixel
                    pyautogui.moveTo(first[0],first[1])
                    if (mousePos[0] + (pidx) * scale, mousePos[1] + (ridx) * scale) != first: #if the first pixel isnt the last pixel
                        pyautogui.dragTo(mousePos[0] + (pidx) * scale, mousePos[1] + (ridx) * scale,0) #drag
                        first = None
                    else:
                        pyautogui.click() #if first and last pixel are the same, just click
                        first = None
            else: #if white pixel
                if first is not None: #if white pixel is ending a series of black pixels
                    pyautogui.moveTo(first[0], first[1])
                    pyautogui.dragTo(mousePos[0]+(pidx-1)*scale,mousePos[1]+(ridx-1)*scale,0) #drags to previous pixel
                    first = None
    print("Drawing complete")