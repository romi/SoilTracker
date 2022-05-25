import matplotlib.pyplot as plt
import numpy as np

import odrive
from odrive_utils import *
from odrive.enums import *

terrainProfile = [
    [0, 6, 12, 18, 25, 26, 27, 28, 29, 30, 32, 34, 35, 40, 45, 46, 47, 49, 50, 51, 52, 53, 54, 60, 67],
    [2, 2, 2, 2, 2, 3.5, 4, 4.5, 5.5, 6, 7, 8, 8.5, 8.5, 8.5, 8, 7, 5, 4, 3.5, 3, 2.5, 1.5, 1.5, 1.5]
]

def grabData(path, velAnalysis):
    try:
        xIndex = np.loadtxt(path+"xIndex.txt")
        tStart = np.loadtxt(path+"tStart.txt")
        t_start = tStart
    except Exception:
        xIndex = None
        t_start = 1.652712032335355282e+09


    currentXAxis = DataContainer()
    currentXAxis.t = np.loadtxt(path+"currentXAxis_time.txt")
    currentXAxis.raw = np.loadtxt(path+"currentXAxis_raw.txt")
    currentXAxis.filtered = np.loadtxt(path+"currentXAxis_filtered.txt")
    currentXAxis.t_start = t_start

    currentZAxis = DataContainer()
    currentZAxis.t = np.loadtxt(path+"currentZAxis_time.txt")
    currentZAxis.raw = np.loadtxt(path+"currentZAxis_raw.txt")
    currentZAxis.filtered = np.loadtxt(path+"currentZAxis_filtered.txt")
    currentZAxis.t_start = t_start

    currentWAxis = DataContainer()
    currentWAxis.t = np.loadtxt(path+"currentWAxis_time.txt")
    currentWAxis.raw = np.loadtxt(path+"currentWAxis_raw.txt")
    currentWAxis.filtered = np.loadtxt(path+"currentWAxis_filtered.txt")
    currentWAxis.t_start = t_start

    if velAnalysis:
        velWAxis = DataContainer()
        velWAxis.t = np.loadtxt(path+"velWAxis_time.txt")
        velWAxis.raw = np.loadtxt(path+"velWAxis_raw.txt")
        velWAxis.filtered = np.loadtxt(path+"velWAxis_filtered.txt")
        velWAxis.t_start = t_start

        velXAxis = DataContainer()
        velXAxis.t = np.loadtxt(path+"velXAxis_time.txt")
        velXAxis.raw = np.loadtxt(path+"velXAxis_raw.txt")
        velXAxis.filtered = np.loadtxt(path+"velXAxis_filtered.txt")
        velXAxis.t_start = t_start
    else:
        velXAxis, velWAxis = None, None

    return currentXAxis, currentZAxis, currentWAxis, velXAxis, velWAxis, xIndex

def interpolation(terrain, xIndex):
    terrainResized = [xIndex, []]
    for i, elt in enumerate(xIndex):
        foundMatch = False
        for j in range(len(terrain[0])-1):
            if terrain[0][j] <= elt and elt <= terrain[0][j+1] and not foundMatch:
                terrainInterpolated = terrain[1][j] + ((terrain[1][j+1] - terrain[1][j]) / (terrain[0][j+1] - terrain[0][j])) * (elt - terrain[0][j]) # it's magic at this point
                terrainResized[1].append(terrainInterpolated)
                foundMatch = True
    return terrainResized

def dashboard(currentXAxis, currentZAxis, currentWAxis, velXAxis, velWAxis, xIndex, choice):
    global terrainProfile
    # Dashboard1 : I(x) & v(x)
    if choice == 1:
        plt.subplot(311)
        plt.plot(xIndex, velXAxis.raw, label="Vitesse AxeX v(x)")
        plt.plot(xIndex, velWAxis.raw, label="Vitesse AxeW w(x)")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)

        plt.subplot(312)
        plt.plot(xIndex, currentXAxis.filtered, label="Courant AxeX I(x)")
        plt.plot(xIndex, currentZAxis.filtered, label="Courant AxeZ I(x)")
        plt.plot(xIndex, currentWAxis.filtered, label="Courant AxeW I(x)")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=3, mode="expand", borderaxespad=0.)

        plt.subplot(313)
        plt.title("Profondeur terrain P(x)")
        plt.plot(xIndex, interpolation(terrainProfile, xIndex)[1], color="black")

    if choice == 2:
        plt.subplot(131)
        plt.scatter(interpolation(terrainProfile, xIndex)[1], currentXAxis.filtered, s=1, marker="x")
        plt.xlabel("P (cm)")
        plt.ylabel("I (A)")
        plt.title("Courant consommé en fonction de la profondeur sur l'axe X")

        plt.subplot(132)
        plt.scatter(interpolation(terrainProfile, xIndex)[1], currentZAxis.filtered, s=1, marker="x")
        plt.xlabel("P (cm)")
        plt.ylabel("I (A)")
        plt.title("Courant consommé en fonction de la profondeur sur l'axe Z")

        plt.subplot(133)
        plt.scatter(interpolation(terrainProfile, xIndex)[1], currentWAxis.filtered, s=1, marker="x")
        plt.xlabel("P (cm)")
        plt.ylabel("I (A)")
        plt.title("Courant consommé en fonction de la profondeur sur l'axe W")

    return plt.show()
