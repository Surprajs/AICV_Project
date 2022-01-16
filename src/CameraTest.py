import pygame
import cv2


class Capture(object):
    def __init__(self):
        self.size = (640, 480)
        self.camera = cv2.VideoCapture(0)
        self.display = pygame.display.set_mode(self.size, 0)
        # self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_frame(self):
        ret, frame = self.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # resized = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
        # color = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        surf = pygame.surfarray.make_surface(frame)
        self.display.blit(surf, (0, 0))
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    self.vid.release()
                    going = False

            self.get_frame()


c1 = Capture()
c1.main()
