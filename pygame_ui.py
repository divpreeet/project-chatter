import sys
import pygame
import threading
import queue
from main import main as m

pygame.init()

WIDTH = 1280
HEIGHT = 720
BG_COLOR = (23, 23, 23)
FPS = 60
EYE_COLOR = (217, 217, 217)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Eyes(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.color = color
        self.state = "idle"

    def draw(self, surface):
        if self.state == "listening":
            blur_radius = 16
            
            shadow_offset = (0, 10)
            shadow_color = (0, 0, 0)
            
            shadow_surf = pygame.Surface((self.rect.width + blur_radius * 2, self.rect.height + blur_radius * 2), pygame.SRCALPHA)
            shadow_rect = pygame.Rect(blur_radius, blur_radius, self.rect.width, self.rect.height)
        
            pygame.draw.rect(shadow_surf, shadow_color + (180,), shadow_rect, border_radius=18)
        
            shadow_surf = pygame.transform.smoothscale(shadow_surf, (self.rect.width // 2, self.rect.height // 2))
            shadow_surf = pygame.transform.smoothscale(shadow_surf, (self.rect.width + blur_radius * 2, self.rect.height + blur_radius * 2))
        
            surface.blit(shadow_surf, (self.rect.x - blur_radius + shadow_offset[0], self.rect.y - blur_radius + shadow_offset[1]))
        
            pygame.draw.rect(surface, self.color, self.rect, border_radius=18)

        elif self.state == "idle":
            pygame.draw.rect(surface, BG_COLOR, self.rect, border_radius=18)
            y = self.rect.centery
            x1 = self.rect.left + 40
            x2 = self.rect.right - 40
            pygame.draw.line(surface, self.color, (x1, y), (x2, y), 6)


# eye group
eye1 = Eyes((168, 237, 352, 247), EYE_COLOR)
eye2 = Eyes((760, 237, 352, 247), EYE_COLOR)
eyes_group = pygame.sprite.Group()
eyes_group.add(eye1, eye2)

# setup states
ui_queue = queue.Queue()
ai_thread = threading.Thread(target=m, args=(ui_queue,), daemon=True)
ai_thread.start()

for i in eyes_group:
    i.state = "idle"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         new_state = "listening" if i.state == "idle" else "idle"
        #         for i in eyes_group:
        #             i.state = new_state

        try:
            while True:
                msg = ui_queue.get_nowait()
                if "state" in msg:
                    for i in eyes_group:
                        i.state = msg["state"]
        except queue.Empty:
            pass

    screen.fill(BG_COLOR)
    for i in eyes_group:
        i.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
