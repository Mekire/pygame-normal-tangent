import os
import sys
import math
import pygame as pg


if sys.version_info[0] < 3:  range = xrange


class Control(object):
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        pg.init()
        self.screen = pg.display.set_mode((700,500))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.phase = 0
        self.scroll_speed = 45
        self.points = self.get_curve_points()

    def get_y(self,x):
        x += self.phase
        return 250 + 100*math.sin(x/100.0) + 50*math.cos(x/25.0)

    def get_derivative(self,x):
        x += self.phase
        return (1.0)*math.cos(x/100.0) - (2.0)*math.sin(x/25.0)

    def get_vectors(self,x,radius=100):
        y = self.get_y(x)
        tangent_slope = self.get_derivative(x)
        angle = math.atan(tangent_slope)
        x1 = radius*math.cos(angle)+x
        y1 = radius*math.sin(angle)+y
        tan = [(x,y),(x1,y1)]
        norm_slope = -1.0/tangent_slope
        angle = math.atan(norm_slope)
        if tangent_slope < 0:
            radius *= -1
        x2 = radius*math.cos(angle)+x
        y2 = radius*math.sin(angle)+y
        norm = [(x,y),(x2,y2)]
        return tan,norm

    def get_curve_points(self,per_x=5):
        points = []
        for x in range(0,self.screen_rect.width+1,per_x):
            points.append((x,self.get_y(x)))
        return points

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        while not self.done:
            delta = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.points = self.get_curve_points()
            tan,norm = self.get_vectors(pg.mouse.get_pos()[0])
            self.phase += self.scroll_speed*delta
            self.phase %= (2*math.pi*100)  #hardcoded wavelength
            self.screen.fill(pg.Color("black"))
            pg.draw.aalines(self.screen,pg.Color("white"),False,self.points)
            pg.draw.line(self.screen,pg.Color("red"),tan[0],tan[1],3)
            pg.draw.line(self.screen,pg.Color("blue"),norm[0],norm[1],3)
            pg.display.update()


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()