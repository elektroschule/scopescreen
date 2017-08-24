import math
import pygame
import sys
import scopescreen


class Game:
    def __init__(self, scopescreen, width=300, height=200):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.scopescreen = scopescreen
        self.cam = Kamera(Punkt(x=0, y=0, z=-5))

        self.points = []
        self.kanten = []
        self.flaechen = []

        # computing center point
        self.cx = width / 2
        self.cy = height / 2

        # creating cube with 8 points
        #      3____2
        #     /|   /|
        #    / 0--/-1
        #  4/_/__/7/
        #   |/   |/
        #   5____6
        # creating points
        self.points.append(Punkt(-1, -1, -1))
        self.points.append(Punkt(1, -1, -1))
        self.points.append(Punkt(1, 1, -1))
        self.points.append(Punkt(-1, 1, -1))
        self.points.append(Punkt(-1, 1, 1))
        self.points.append(Punkt(-1, -1, 1))
        self.points.append(Punkt(1, -1, 1))
        self.points.append(Punkt(1, 1, 1))

        # creating edges
        self.kanten.append(Kante(self.points[0], self.points[1]))
        self.kanten.append(Kante(self.points[1], self.points[2]))
        self.kanten.append(Kante(self.points[2], self.points[3]))
        self.kanten.append(Kante(self.points[3], self.points[0]))
        self.kanten.append(Kante(self.points[4], self.points[5]))
        self.kanten.append(Kante(self.points[5], self.points[6]))
        self.kanten.append(Kante(self.points[6], self.points[7]))
        self.kanten.append(Kante(self.points[7], self.points[4]))
        self.kanten.append(Kante(self.points[0], self.points[5]))
        self.kanten.append(Kante(self.points[1], self.points[6]))
        self.kanten.append(Kante(self.points[2], self.points[7]))
        self.kanten.append(Kante(self.points[3], self.points[4]))

        # creating faces - Dreiecke
        #      3____2
        #     /|   /|
        #    / 0--/-1
        #  4/_/__/7/
        #   |/   |/
        #   5____6
        self.flaechen.append(Flaeche(self.points[0], self.points[1], self.points[2]))
        self.flaechen.append(Flaeche(self.points[0], self.points[2], self.points[3]))
        self.flaechen.append(Flaeche(self.points[0], self.points[1], self.points[6]))
        self.flaechen.append(Flaeche(self.points[0], self.points[5], self.points[6]))
        self.flaechen.append(Flaeche(self.points[0], self.points[3], self.points[4]))
        self.flaechen.append(Flaeche(self.points[0], self.points[4], self.points[5]))
        self.flaechen.append(Flaeche(self.points[7], self.points[2], self.points[3]))
        self.flaechen.append(Flaeche(self.points[7], self.points[3], self.points[4]))
        self.flaechen.append(Flaeche(self.points[7], self.points[2], self.points[1]))
        self.flaechen.append(Flaeche(self.points[7], self.points[1], self.points[6]))
        self.flaechen.append(Flaeche(self.points[7], self.points[4], self.points[5]))
        self.flaechen.append(Flaeche(self.points[7], self.points[5], self.points[6]))

    def key_down(self, key, dt=1):
        self.cam.update(dt, key)

    def repaint(self):
        self.screen.fill((0, 0, 0))

        flaechen_on_screen = []
        for fl in self.flaechen:
            fl_on_screen = Flaeche()
            fl_on_screen.punkte = []
            fl_on_screen.farbe = fl.farbe
            fl_on_screen.tiefe = 0
            for p in fl.punkte:
                x = p.x
                y = p.y
                z = p.z
                # rotate by camera angle
                p_ = Punkt.rotate2d(x, z, self.cam.roty)
                x = p_[0]
                z = p_[1]
                # move by camera location
                x -= self.cam.pos.x
                y -= self.cam.pos.y
                z -= self.cam.pos.z
                fl_on_screen.tiefe += x * x + y * y + z * z
                # perspective
                f = 0 if z == 0 else 200.0 / z
                x *= f
                y *= f
                fl_on_screen.punkte.append(Punkt(self.cx + x, self.cy + y, 0))

            flaechen_on_screen.append(fl_on_screen)

            # Flächen nach Abstand sortieren
            flaechen_on_screen = sorted(flaechen_on_screen,
                                        key=lambda f: f.tiefe)
            
            # Flächen in Sortierreihenfolge zeichnen
            for fl in flaechen_on_screen:
                fl.zeichne_auf_pygamescreen(self.screen)
                fl.zeichne_auf_scopescreen(self.scopescreen)


class Punkt:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

        """
        Rotating a point by rad.

                   ^                                                            
                   #                                                    
                   #                  P(x'|y')                         
                   #                 ##                                 
                   #                ##.                                 
                   #               ## .                                 
                   #              ##  .                                 
                   #             ##   .                                 
                   #            ##    .                                 
                   #        r  ##     .            p(x|y)                
                   #          #       .           ##                    
                   #         ##..     .        ####.                    
                   #        ##   .    .      ###   .                    
                   #       ##     .   .  ####      .                    
                   #      ##   b  .   .###         .                    
                   #     ##       . ###            .                    
                   #    ##      ####  .            .                    
                   #   ##     ### .   .            .                    
                   #  ##  ####     .  .            .                    
                   # ######      a .  .            .                    
                   # ###           .  .            .                    
                   ##################################################>
        
        r = Abstand von p bzw. p' zum Ursprung
        a = Winkel zwischen x-Achse und p
        b = Drehwinkel
        y/r = sin a => y = r sin a            _=y__           _=x_
        x/r = cos a => x = r cos a           /     \         /     \
        y'/r = sin(a+b) => y' = r sin(a+b) = r sin a cos b + r cos a sin b = y cos b + x sin b
        x'/r = cos(a+b) => x' = r cos(a+b) = r cos a cos b - r sin a sin b = x cos b - y sin b
        ergo: x'= x cos b - y sin b und y' = y cos b + x sin b
        """
    @staticmethod
    def rotate2d(x, y, rad):
        s = math.sin(rad)
        c = math.cos(rad)

        p2 = Punkt()
        p2.x = x * c - y * s
        p2.y = y * c + x * s
        return [p2.x, p2.y]


class Kante:
    def __init__(self, s, t):
        self.src = s
        self.tgt = t


class Flaeche:
    def __init__(self, p1=Punkt(), p2=Punkt(), p3=Punkt(),
                 farbe=(255, 0, 0)):
        assert isinstance(farbe, tuple), farbe

        self.punkte = [p1, p2, p3]
        self.farbe = farbe
        self.tiefe = 0

    def zeichne_auf_pygamescreen(self, pygame_screen, line_thickness=5):
        pts = []

        for p in self.punkte:
            pts.append([int(p.x), int(p.y)])

        pygame.draw.polygon(pygame_screen, self.farbe, pts, line_thickness)

    def zeichne_auf_scopescreen(self, scope_scr: scopescreen.ScopeScreen):
        pts = []

        for p in self.punkte:
            pts.append((int(p.x), int(p.y)))
        pts.append((self.punkte[0].x, self.punkte[0].y)) # append the first point again

        scope_scr.figure(pts)


class Kamera:
    def __init__(self, pos):
        self.pos = pos
        # rotx = 0
        self.roty = 0

    def update(self, dt, taste):
        # s = dt * 5

        if (taste == pygame.K_w):
            self.pos.z += dt
        elif (taste == pygame.K_a):
            self.pos.x -= dt

        elif (taste == pygame.K_s):
            self.pos.z -= dt

        elif (taste == pygame.K_d):
            self.pos.x += dt

        elif(taste == pygame.K_q):
            self.pos.y -= dt

        elif(taste == pygame.K_e):
            self.pos.y += dt

        elif(taste == pygame.K_y):
            self.roty -= 0.1

        elif (taste == pygame.K_c):
            self.roty += 0.1


def main():
    # init scopescreen with defaults
    sc = scopescreen.ScopeScreen(x_bus=0, x_device=1, y_bus=0, y_device=0)
    sc.step = 3
    screen = Game(sc, width=256, height=256)

    # start game loop
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # limit runtime to 60 fps
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                screen.key_down(event.key)

        # update screen
        screen.repaint()

        # flip the buffer
        pygame.display.flip()


if __name__ == "__main__":
    main()
