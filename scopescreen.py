import spidev
import time
import math
import random

class MCP4151:
    def __init__(self, busnumber, devicenumber, speed_MHz=60):
        assert busnumber in [0, 1]
        assert devicenumber in [0, 1]
        self.spi = spidev.SpiDev()
        self.spi.open(busnumber, devicenumber)
        self.speed_Hz = speed_MHz*1000000
        self.spi.max_speed_hz = speed_MHz*1000000
        
    def set_wiper(self, value):
        self.spi.xfer([0x00, value], self.speed_Hz, 0)

    def inc_wiper(self):
        self.spi.xfer([0b00000100], self.speed_Hz, 0)

    def dec_wiper(self):
        self.spi.xfer([0b00001000], self.speed_Hz, 0)

class ScopeScreen:
    def __init__(self, x_bus = 0, x_device = 1, y_bus = 0, y_device = 0):
        """ the y-poti is connected to channel 1,
            the x-poti is connected to channel 2 of the scope """  
        assert x_bus in [0, 1]
        assert x_device in [0, 1]
        assert y_bus in [0, 1]
        assert y_device in [0, 1]
        self.xpoti = MCP4151(x_bus, x_device)
        self.ypoti = MCP4151(y_bus, y_device)
        self.step = 1 # dont draw every point of lines
        self.startpoint = 0

    def point(self, x, y):
        """ draws a poin on screen. """
        self.xpoti.set_wiper(x)
        self.ypoti.set_wiper(y)

    def point_fast(self, x, y):
        """ its faster """
        self.xpoti.spi.xfer([0x00, x], self.xpoti.speed_Hz, 0)
        self.ypoti.spi.xfer([0x00, y], self.ypoti.speed_Hz, 0)

    def line(self, startpoint, endpoint):
        """ draws a line from startpoint (x1,y1) to endpoint (x2, y2).
            it is an implementation of the Bresenham's line algorithm:
            https://de.wikipedia.org/wiki/Bresenham-Algorithmus 
            self.step increases the step size between two point of the line """
        x1 = startpoint[0]
        y1 = startpoint[1]
        x2 = endpoint[0]
        y2 = endpoint[1]
        dx = x2-x1            # delta x
        dy = y2-y1            # delta y
        adx = abs(dx)         # absolute value of dx
        ady = abs(dy)         # absolute value of dy
        if dx == 0:
            sdx = 0           # sdx (signum of dx) = 0 for horizontal line
        else:
            sdx = int(dx/adx) # sdx = 1 for positive dx or sdx = -1 for negative dx
        if dy == 0:
            sdy = 0           # sdy (sginum of dy) = 0 for vertical line
        else:
            sdy = int(dy/ady) # sdy like sdx
        if adx > ady:                # x is fast direction
            pdx = int(sdx*self.step) # horizontal (parallel) step
            pdy = 0                  # vertical (parllel) step
            ddx = int(sdx*self.step) # x value of diagonal step
            ddy = int(sdy*self.step) # y value of diagonal step
            deltaslowdirection = int(ady/self.step) # number of slow steps
            deltafastdirection = int(adx/self.step) # number of fast steps
        else:                        # x is slow direction
            pdx = 0
            pdy = int(sdy*self.step)
            ddx = int(sdx*self.step)
            ddy = int(sdy*self.step)
            deltaslowdirection = int(adx/self.step)
            deltafastdirection = int(ady/self.step)
        x = x1
        y = y1
        self.point(x1,y1)
        error = deltafastdirection/2
        for i in range(deltafastdirection):
            error = error - deltaslowdirection
            if error < 0:     # take a diagonal step (in x- and y-direction)
                error = error + deltafastdirection
                x = x + ddx
                y = y + ddy
                self.xpoti.spi.xfer([0x00, x], self.xpoti.speed_Hz, 0)
                self.ypoti.spi.xfer([0x00, y], self.ypoti.speed_Hz, 0)
            else:             # take a parallel step (only in fast direction)  
                x = x + pdx
                y = y + pdy
                if pdx != 0:
                    self.xpoti.spi.xfer([0x00, x], self.xpoti.speed_Hz, 0)
                if pdy != 0:
                    self.ypoti.spi.xfer([0x00, y], self.ypoti.speed_Hz, 0)

    def figure(self, points):
        """ draws lines (edges) beteween the given points.
            points is a list of tuples. e.g.:
            [(x0,y0),(x1,y2), ..., (xn, yn)] """
        edges = len(points)-1    # number of edges
        for edge in range(edges):
            self.line(points[edge], points[edge+1])

    def square(self, a, sp=(0,0)):
        """ draws a square with edge length a. 
            sp is the startpoint (bottom left) """
        self.figure([sp,(sp[0],sp[1]+a),(sp[0]+a,sp[1]+a),(sp[0]+a,sp[1]),sp])

           
def main():
    screen = ScopeScreen()
    while(True):
        bird = [(10, 209),(68, 167),(139, 164),(166, 185),(185, 189),(201, 181),(204, 172),(223, 169),(202, 164),(201, 152),(190, 132),(173, 120),(129, 109),(130, 89),(140, 82),(127, 86),(126, 79),(119, 87),(107, 90),(121, 90),(124, 110),(83, 110),(86, 87),(95, 79),(81, 87),(80, 75),(76, 86),(61, 85),(78, 92),(77, 109),(53, 119),(54, 149),(10, 209)]
        screen.figure(bird)

if __name__ == "__main__":
   main()        
