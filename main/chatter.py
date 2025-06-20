import sys
import os
import json
import pygame
import threading
import queue
from main import main as m
import math
import time

# adding customization w config

DEFAULT_CONF = {
    "bg_color": [23, 23, 23],
    "eye_color": [217, 217, 217],
    "tip_color": [180, 180, 180],
    "fonts": {
        "caption": "Inter.ttf",
        "caption_size": 28,
        "tip_size": 18
    },
    "tip_interval": 20
}

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.exists(config_path):
    try:
        with open(config_path, "r") as file:
            user_conf = json.load(file)
    except json.JSONDecodeError:
        print("config is not properly formed, using default config")
        user_conf = {}
else:
    user_conf = {}

def merge(dflt, user):
    for key, val in user.items():
        if isinstance(val, dict) and key in dflt:
            merge(dflt[key], val)
        else:
            dflt[key] = val

merge(DEFAULT_CONF, user_conf)
cfg = DEFAULT_CONF

BG_COLOR  = tuple(cfg["bg_color"])
EYE_COLOR = tuple(cfg["eye_color"])
TIP_COLOR = tuple(cfg["tip_color"])
TIP_INTERVAL = cfg["tip_interval"]

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chatter")
clock = pygame.time.Clock()
font = pygame.font.Font(cfg["fonts"]["caption"], cfg["fonts"]["caption_size"])
caption_text = ""

tips = [
    'say "chatter what are you up to?" to start',
    'try asking chatter about itself',
    'you can say "chatter, tell me a joke"',
    'ask chatter to talk to you',
    'say "chatter, what can you do?" to learn more',
    'read the docs for more info!'
]
tip_font = pygame.font.Font(cfg["fonts"]["caption"], cfg["fonts"]["tip_size"])
current_tip = 0
last_tip = time.time()
tip_change = 20

class Eyes(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.color = color
        self.state = "idle"

    def draw(self, surface):
        blur_radius = 16
        shadow_offset = (0, 10)
        shadow_color = (0, 0, 0)
        if self.state in ("thinking", "listening", "speaking"):
            if self.state == "thinking":
                t = pygame.time.get_ticks() / 500
                pulse = 0.8 + 0.2 * math.sin(t * math.pi)
                pulse_color = tuple(
                    min(255, int(c * pulse + 255 * (1 - pulse))) for c in self.color
                )
            else:
                pulse_color = self.color
            shadow_surf = pygame.Surface(
                (self.rect.width + blur_radius * 2, self.rect.height + blur_radius * 2),
                pygame.SRCALPHA
            )
            shadow_rect = pygame.Rect(blur_radius, blur_radius, self.rect.width, self.rect.height)
            pygame.draw.rect(shadow_surf, shadow_color + (180,), shadow_rect, border_radius=18)
            shadow_surf = pygame.transform.smoothscale(
                shadow_surf,
                (self.rect.width // 2, self.rect.height // 2)
            )
            shadow_surf = pygame.transform.smoothscale(
                shadow_surf,
                (self.rect.width + blur_radius * 2, self.rect.height + blur_radius * 2)
            )
            surface.blit(
                shadow_surf,
                (self.rect.x - blur_radius + shadow_offset[0], self.rect.y - blur_radius + shadow_offset[1])
            )
            pygame.draw.rect(surface, pulse_color, self.rect, border_radius=18)
        else:
            pygame.draw.rect(surface, BG_COLOR, self.rect, border_radius=18)
            y = self.rect.centery
            x1 = self.rect.left + 40
            x2 = self.rect.right - 40
            pygame.draw.line(surface, self.color, (x1, y), (x2, y), 6)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current = ""
    for w in words:
        test = current + w + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current.rstrip())
            current = w + " "
    if current:
        lines.append(current.rstrip())
    return lines

def write_text(surface, text, font, color, y_pos, max_width=1000, line_spacing=5):
    if not text:
        return
    lines = wrap_text(text, font, max_width)
    total_h = len(lines) * (font.get_height() + line_spacing)
    y = y_pos - total_h // 2
    for line in lines:
        surf = font.render(line, True, color)
        rect = surf.get_rect(center=(surface.get_width()//2, y + font.get_height()//2))
        surface.blit(surf, rect)
        y += font.get_height() + line_spacing

def get_eye_rects(width, height):
    left_eye = pygame.Rect(int(width * 168 / 1280), int(height * 237 / 720), int(width * 352 / 1280), int(height * 247 / 720))
    right_eye = pygame.Rect(int(width * 760 / 1280), int(height * 237 / 720), int(width * 352 / 1280), int(height * 247 / 720))
    return left_eye, right_eye

eye1 = Eyes((168, 237, 352, 247), EYE_COLOR)
eye2 = Eyes((760, 237, 352, 247), EYE_COLOR)
eyes = pygame.sprite.Group(eye1, eye2)

ui_queue = queue.Queue()
threading.Thread(target=m, args=(ui_queue,), daemon=True).start()

running = True
while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        elif events.type == pygame.VIDEORESIZE:
            new_w = max(events.w, WIDTH)
            new_h = max(events.h, HEIGHT)
            screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)

            left_eye, right_eye = get_eye_rects(new_w, new_h)
            eye1.rect = left_eye
            eye2.rect = right_eye

    width = screen.get_width()
    height = screen.get_height()

    t = pygame.time.get_ticks() / 1000
    pulse = 0.25 + 0.25 * math.sin(t * 2 * math.pi)
    alpha = int(128 + 127 * pulse)

    if time.time() - last_tip > tip_change:
        current_tip = (current_tip + 1) % len(tips)
        last_tip = time.time()

    tip_text = tips[current_tip]
    tip_surface = tip_font.render(tip_text, True, TIP_COLOR)
    tip_rect = tip_surface.get_rect(center=(width//2, height - 40))
    tip_surface.set_alpha(alpha)

    try:
        while True:
            msg = ui_queue.get_nowait()
            if "state" in msg:
                if msg["state"] == "goodbye":
                    running = False
                    break
                for e in eyes:
                    e.state = msg["state"]
            if "text" in msg:
                caption_text = msg["text"]
    except queue.Empty:
        pass
    screen.fill(BG_COLOR)
    write_text(screen, caption_text, font, EYE_COLOR, 125, max_width=WIDTH - 100)
    for e in eyes:
        e.draw(screen)

    screen.blit(tip_surface, tip_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()