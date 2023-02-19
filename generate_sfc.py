import math
import numpy as np
import pandas as pd


def nextPoint(x, y, angle):
    a = math.pi * angle / 180
    x2 = (int)(round(x + (math.cos(a))))
    y2 = (int)(round(y + (math.sin(a))))
    return x2, y2


def expand(axiom, rules, level):
    for l in range(0, level):
        a2 = ""
        for c in axiom:
            if c in rules:
                a2 += rules[c]
            else:
                if c == "F":
                    a2 += chr(ord("0") + level - l - 1)
                else:
                    a2 += c
        axiom = a2
        # print(axiom)
    return axiom


def draw_lsystem(axiom, rules, angle, direction, iterations, add_padding):
    xp = [1]
    yp = [1]
    # direction = 135
    for c in expand(axiom, rules, iterations):
        if c == "F":
            xn, yn = nextPoint(xp[-1], yp[-1], direction)
            xp.append(xn)
            yp.append(yn)
        elif c == "+":
            direction = direction - angle
            if direction < 0:
                direction = 360 + direction
        elif c == "-":
            direction = (direction + angle) % 360
        elif c in ["L", "R", "X"]:
            pass
        else:
            for i in range((ord(c) - ord("0") + 2) if add_padding else 1):
                xn, yn = nextPoint(
                    xp[-1],
                    yp[-1],
                    direction,
                )
                xp.append(xn)
                yp.append(yn)

    xp = np.array(xp)
    xp = (xp - np.min(xp)) / (np.max(xp) - np.min(xp))
    yp = np.array(yp)
    yp = (yp - np.min(yp)) / (np.max(yp) - np.min(yp))
    return xp, yp


def get_sfc(level: int, add_padding: bool, sfc_type: str = "hilbert"):
    # L-System Definition
    s_axiom = {"sierpinski_square": "F+XF+F+XF", "moore": "LFL+F+LFL", "hilbert": "-L"}
    s_rules = {
        "sierpinski_square": {"X": "XF-F+F-XF+F+XF-F+F-X"},
        "moore": {
            "L": "-RF+LFL+FR-",
            "R": "+LF-RFR-FL+",
        },
        "hilbert": {"L": "+RF-LFL-FR+", "R": "-LF+RFR+FL-"},
    }
    s_angle = {"sierpinski_square": 90, "moore": 90, "hilbert": 270}
    c_angle = {"sierpinski_square": 135, "moore": 90, "hilbert": 90}
    return draw_lsystem(
        s_axiom[sfc_type],
        s_rules[sfc_type],
        s_angle[sfc_type],
        c_angle[sfc_type],
        level,
        add_padding,
    )


# def get_moore
