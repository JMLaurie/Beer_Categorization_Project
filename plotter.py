from typing import Tuple, List, Union, Dict, cast
import svgwrite
import math
import numpy as np
import webbrowser
import plotter
import random

# Rounds pos to the nearest integer multiple of step
def snap(pos:float, step:float) -> float:
    return math.floor(pos / step + (step / 10.)) * step

# Finds a starting point and step size for tick marks from
# min_val to max_val, where the each tick mark will fall on a power of 10,
# and the total number of tick marks will be as close to target_count as possible.
def find_tick_spacing(target_count:int, min_val:float, max_val:float) -> Tuple[float, float]:
    sqrt_10 = math.sqrt(10.)
    min_ticks = target_count / sqrt_10
    max_ticks = target_count * sqrt_10
    range = max_val - min_val
    step = 1.
    while step * min_ticks > range:
        step /= 10
    while step * max_ticks < range:
        step *= 10
    return math.ceil(min_val / step) * step, step

# finds min and max in a nan-tolerant way
def get_min_and_max(vals:List[float]) -> Tuple[float, float]:
    min_val = np.nan
    max_val = np.nan
    for val in vals:
        if not np.isnan(val):
            min_val = min(val, min_val)
            max_val = max(val, max_val)
    return (min_val, max_val)


# A class for making SVG plots
class Plotter():
    def __init__(self, size:Tuple[int, int], bottom_left:Tuple[float, float], top_right:Tuple[float, float]) -> None:
        self.d = svgwrite.Drawing('untitled.svg', size=size, profile='full')
        self.size = size
        self.mins = bottom_left
        self.maxs = top_right

    # Projects a point onto the graph
    def _proj(self, x: Tuple[float,float]) -> Tuple[float,float]:
        return (
            (x[0] - self.mins[0]) / (self.maxs[0] - self.mins[0]) * self.size[0],
            self.size[1] - (x[1] - self.mins[1]) / (self.maxs[1] - self.mins[1]) * self.size[1],
        )

    # Draw a line
    def line(self, a:Tuple[float,float], b:Tuple[float,float], thickness:float=1., color:Tuple[int,int,int]=(0,0,0), absolute:bool=False) -> None:
        if not absolute:
            a = self._proj(a)
            b = self._proj(b)
        self.d.add(self.d.line(a, b, stroke_width=thickness, stroke=svgwrite.rgb(*color)))

    # Draw an arrow
    def arrow(self, a:Tuple[float,float], b:Tuple[float,float], thickness:float=1., color:Tuple[int,int,int]=(0,0,0), head_size:float=10., head_angle:float=0.785398163, absolute:bool=False) -> None:
        angle = math.atan2(a[1] - b[1], a[0] - b[0])
        ang1 = angle + head_angle / 2.
        ang2 = angle - head_angle / 2.
        self.line(a, b, thickness, color, absolute)
        self.line(b, (b[0] + head_size * math.cos(ang1), b[1] + head_size * math.sin(ang1)), thickness, color, absolute)
        self.line(b, (b[0] + head_size * math.cos(ang2), b[1] + head_size * math.sin(ang2)), thickness, color, absolute)

    # Draw an empty rectangle
    def rect_empty(self, a:Tuple[float,float], b:Tuple[float,float], thickness:float=1., color:Tuple[int,int,int]=(0,0,0), absolute:bool=False) -> None:
        self.line(a, (a[0], b[1]), thickness, color, absolute)
        self.line((a[0], b[1]), b, thickness, color, absolute)
        self.line(b, (b[0], a[1]), thickness, color, absolute)
        self.line((b[0], a[1]), a, thickness, color, absolute)

    # Draw a filled rectangle
    def rect(self, a:Tuple[float,float], b:Tuple[float,float], color:Tuple[int,int,int]=(0,0,0), absolute:bool=False) -> None:
        if not absolute:
            a = self._proj(a)
            b = self._proj(b)
        tl = (min(a[0], b[0]), min(a[1], b[1]))
        br = (max(a[0], b[0]), max(a[1], b[1]))
        wh = (br[0]-tl[0],br[1]-tl[1])
        self.d.add(self.d.rect(tl, wh, stroke='none', fill=svgwrite.rgb(*color)))

    # Draw a circle
    def circle(self, pos:Tuple[float,float], radius:float=1., color:Tuple[int,int,int]=(0,0,0), absolute:bool=False) -> None:
        if not absolute:
            pos = self._proj(pos)
        self.d.add(self.d.circle(pos, r=radius, fill=svgwrite.rgb(*color)))

    # Draw text
    def text(self, s:str, pos:Tuple[float,float], size:float=16, color:Tuple[int,int,int]=(0,0,0), absolute:bool=False) -> None:
        if not absolute:
            pos = self._proj(pos)
        if not np.isnan(pos[0]) and not np.isnan(pos[1]):
            self.d.add(self.d.text(s, insert=pos, fill=svgwrite.rgb(*color), style=f'font-size:{size}px; font-family:Arial'))

    # Draw vertical grid lines
    # If label_size is 0, no labels will be drawn
    def vert_lines(self, target_count:int=20, thickness:float=.1, color:Tuple[int,int,int]=(128,128,128), label_size:int=8) -> None:
        pos, step = find_tick_spacing(target_count, self.mins[0], self.maxs[0])
        while pos <= self.maxs[0]:
            pos = snap(pos, step)
            self.line((pos, self.mins[1]), (pos, self.maxs[1]), thickness, color)
            if label_size > 0:
                vpos = 0 if 0 >= self.mins[1] and 0 <= self.maxs[1] else self.mins[1]
                self.text(f'{pos:.6}', (pos, vpos), size=label_size, color=color)
            pos += step

    # Draw horizontal grid lines
    # If label_size is 0, no labels will be drawn
    def horiz_lines(self, target_count:int=20, thickness:float=.1, color:Tuple[int,int,int]=(128,128,128), label_size:int=8) -> None:
        pos, step = find_tick_spacing(target_count, self.mins[1], self.maxs[1])
        while pos <= self.maxs[1]:
            pos = snap(pos, step)
            self.line((self.mins[0], pos), (self.maxs[0], pos), thickness, color)
            if label_size > 0:
                hpos = 0 if 0 >= self.mins[0] and 0 <= self.maxs[0] else self.mins[0]
                self.text(f'{pos:.6}', (hpos, pos), size=label_size, color=color)
            pos += step

    # Draw a grid
    # If label_size is 0, no labels will be drawn
    def grid(self, target_count:int=20, thickness:float=.1, color:Tuple[int,int,int]=(128,128,128), label_size:int=8) -> None:
        self.vert_lines(target_count, thickness, color, label_size)
        self.horiz_lines(target_count, thickness, color, label_size)

    # Converts to a string in SVG format
    def tostr(self) -> str:
        return '<?xml version="1.0" encoding="utf-8" ?>\n' + str(self.d.tostring())

    # Generates an SVG file
    def tosvg(self, filename:str) -> None:
        with open(filename, 'w') as f:
            f.write(self.tostr())


# Makes a histogram plot
def plot_histogram(vals:List[float]) -> Plotter:
    # Divide the data into buckets
    min_val, max_val = get_min_and_max(vals)
    buckets = max(2, int(1.2 * math.sqrt(len(vals))))
    bucket_width = (max_val - min_val) / buckets
    counts = [0] * buckets
    for v in vals:
        bucket = max(0, min(buckets - 1, int((v - min_val) // bucket_width)))
        counts[bucket] += 1
    biggest = max(counts)

    # Plot the histogram
    plotter = Plotter((400, 400), (min_val, 0), (max_val, biggest * 3 // 2))
    plotter.rect(plotter.mins, plotter.maxs, (255, 255, 255))
    for i in range(buckets):
        plotter.rect((min_val + i * bucket_width, 0), (min_val + ((i + .98) * bucket_width), counts[i]), (0, 0, 128))
    plotter.grid(8, thickness=0.5, color=(128,128,128), label_size=16)
    return plotter

# Makes a categorical distribution plot
def plot_categorical(vals:List[str]) -> Plotter:
    cat:Dict[str,int] = {}
    for v in vals:
        if v in cat:
            cat[v] += 1
        else:
            cat[v] = 1
    width = max([cat[v] for v in cat]) * 1.2
    plotter = Plotter((400, 400), (0, 0), (width, len(cat)))
    plotter.rect(plotter.mins, plotter.maxs, (255, 255, 255))
    plotter.grid(8, thickness=0.5, color=(128,128,128), label_size=16)
    i = 0
    for v in cat:
        plotter.rect((0, i), (cat[v], i + 0.7), (0, 128, 0))
        plotter.text(v, (0, i), size=24, color=(255, 128, 0))
        i += 1
    return plotter

# Draws a bunch of points with an auto-computed radius and jitter
def plot_float_float_pairs(pairs:List[Tuple[float,float]]) -> Plotter:
    a_min, a_max = get_min_and_max([x[0] for x in pairs])
    b_min, b_max = get_min_and_max([x[1] for x in pairs])
    h_margin = .15 * (a_max - a_min)
    v_margin = .15 * (b_max - b_min)
    mins = (a_min - h_margin, b_min - v_margin)
    maxs = (a_max + h_margin, b_max + v_margin)
    plotter = Plotter((400, 400), mins, maxs)
    plotter.rect(mins, maxs, (255, 255, 255))
    plotter.grid(8, thickness=0.5, color=(128,128,128), label_size=16)
    radius = 30. / math.sqrt(len(pairs))
    jitter_x = 0.02 * (plotter.maxs[0] - plotter.mins[0])
    jitter_y = 0.02 * (plotter.maxs[1] - plotter.mins[1])
    for i in range(len(pairs)):
        p = pairs[i]
        plotter.circle((p[0] + random.gauss(0., jitter_x), p[1] + random.gauss(0., jitter_y)), radius, (0,0,128))
    return plotter

def plot_float_str_pairs(pairs:List[Tuple[float,str]]) -> Plotter:
    # Enumerate all the strings
    str_enumerator:Dict[str,int] = {}
    for pair in pairs:
        if not pair[1] in str_enumerator:
            str_enumerator[pair[1]] = len(str_enumerator)
    if len(str_enumerator) < 20:
        # Plot the points
        new_pairs = [(pair[0], float(str_enumerator[pair[1]])) for pair in pairs]
        plotter = plot_float_float_pairs(new_pairs)

        # Draw some labels
        for s in str_enumerator:
            plotter.text(s, (plotter.mins[0], str_enumerator[s]), size=24, color=(0,128,0))
        return plotter
    else:
        plotter = Plotter((400, 400), (0, 0), (1, 1))
        plotter.text('too many values', (0, 0), size=24, color=(128,0,0))
        return plotter

def plot_str_str_pairs(pairs:List[Tuple[str, str]]) -> Plotter:
    # Enumerate and count all the strings and co-occurrences
    enum_a:Dict[str,int] = {}
    enum_b:Dict[str,int] = {}
    for pair in pairs:
        if not pair[0] in enum_a:
            enum_a[pair[0]] = len(enum_a)
        if not pair[1] in enum_b:
            enum_b[pair[1]] = len(enum_b)
    if len(enum_a) < 20 and len(enum_b) < 20:
        # Plot the points
        new_pairs = [(float(enum_a[pair[0]]), float(enum_b[pair[1]])) for pair in pairs]
        plotter = plot_float_float_pairs(new_pairs)

        # Draw some labels
        for x in enum_a:
            plotter.text(x, (enum_a[x], 0), size=24, color=(0,128,0))
        for y in enum_b:
            plotter.text(y, (0, enum_b[y]), size=24, color=(0,128,0))
        return plotter
    else:
        plotter = Plotter((400, 400), (0, 0), (1, 1))
        plotter.text('too many values', (0, 0), size=24, color=(128,0,0))
        return plotter




if __name__ == "__main__": # If this file is being executed (as opposed to being imported)...
    p = Plotter(size=(500, 500), bottom_left=(-200., -200.), top_right=(600., 600.))
    p.grid()
    p.arrow((-200., 0.), (600., 0.), color=(128, 64, 64))
    p.arrow((0., -200.), (0., 600.), color=(128, 64, 64))
    p.circle((400., 200.), radius=5., color=(0, 0, 128))
    p.rect((100., 100.), (200., 200.), color=(0, 128, 0))
    p.line((200, 100), (400, 200), thickness=4., color=(0, 0, 128))
    p.text("Label", (200, 200))
    p.tosvg('test.svg')
    webbrowser.open(f'test.svg', new=2)