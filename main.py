from PIL import Image
import numpy as np
from time import sleep
import pyautogui
import os


def draw(filepath=None, scale = None, threshold=0.5, pause = 0.004):
    def getImageInfo(default=1):
        while not os.path.isfile(filepath := input("Enter file path: ").strip('"')):
            filepath = input("Enter file path: ").strip('"')
        try:
            scale = int(input(f"Enter Input Scale (default: {default}): "))
        except:
            print(f"Invalid scale. Default ({default}) selected")
            scale = default
        return (filepath, scale)
    pyautogui.PAUSE = pause
    if filepath is None or scale is None:
        filepath, scale = getImageInfo()

    img = Image.open(filepath)
    imageArray = np.array(img)
    print("Drawing in 3 seconds... ")
    sleep(3)
    mousePos = pyautogui.position()
    for ridx, row in enumerate(imageArray):
        width = len(row)
        first = None
        for pidx, pixel in enumerate(row):
            average = sum(color for color in pixel.tolist())/(255*3)
            if average<=threshold: #if black pixel
                if first is None:
                    first = (mousePos[0]+pidx*scale,mousePos[1]+ridx*scale,0)
                if pidx == width-1:#if last pixel in row, do the row
                    pyautogui.moveTo(first[0],first[1])
                    if (mousePos[0] + (pidx) * scale, mousePos[1] + (ridx) * scale) != first:
                        pyautogui.dragTo(mousePos[0] + (pidx) * scale, mousePos[1] + (ridx) * scale,0)
                        first = None
                    else:
                        pyautogui.click()
                        first = None
            else: #if white pixel
                if first is not None:
                    pyautogui.moveTo(first[0], first[1])
                    pyautogui.dragTo(mousePos[0]+(pidx-1)*scale,mousePos[1]+(ridx-1)*scale,0) #drags to previous pixel
                    first = None

                #pyautogui.moveTo(mousePos[0]+pidx*scale,mousePos[1]+ridx*scale,0)
                #pyautogui.click()
                pass
    print("Drawing complete")