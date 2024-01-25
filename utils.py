"""
This will import our settings file to this file
"""
import settings

#This is a function that will calculate the width and height for our interface
def width_prct(percentage):
    return settings.width/100 * percentage

def height_prct(percentage):
    return settings.height/100 * percentage
