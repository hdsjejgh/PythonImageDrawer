from PIL import Image
import numpy as np
from time import sleep
import pyautogui
import os


def draw(filepath=None, scale = None):
    pyautogui.PAUSE = 0.001
    if filepath is None or scale is None:
        filepath, scale = getImageInfo()
    img = Image.open(filepath)
    imageArray = np.array(img)
    print("Drawing in 5 seconds... ")
    sleep(50)
    mousePos = pyautogui.position()
    for ridx, row in enumerate(imageArray):
        for pidx, pixel in enumerate(row):
            average = sum(color for color in pixel.tolist())/(255*3)
            if average<=0.5:
                pyautogui.moveTo(mousePos[0]+pidx*scale,mousePos[1]+ridx*scale,0)
                pyautogui.click()
                pass
    print("Drawing complete")

def getImageInfo(default=1):
    while not os.path.isfile(filepath:=input("Enter file path: ")):
        filepath = input("Enter file path: ")
    try:
        scale = int(input(f"Enter Input Scale (default: {default}): "))
    except:
        print(f"Invalid scale. Default ({default}) selected")
        scale = default
    return (filepath,scale)


if __name__ == '__main__':
    draw()