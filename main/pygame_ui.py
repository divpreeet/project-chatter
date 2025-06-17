import sys
import pygame
import threading
import queue
from main import main as m
import math
import time
import webbrowser

pygame.init()
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (23, 23, 23)
EYE_COLOR = (217, 217, 217)
TIP_COLOR = (180, 180, 180)
FPS = 60
ACCENT_COLOR = (214, 214, 214)
MENU_BG = (30, 32, 34)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chatter")
clock = pygame.time.Clock()
font = pygame.font.Font('Inter.ttf', 28)
caption_text = ""

tips = [
    'say "chatter what are you up to?" to start',
    'try asking chatter about itself',
    'you can say "chatter, tell me a joke"',
    'ask chatter to talk to you',
    'say "chatter, what can you do?" to learn more',
    'read the docs for more info!'
]
tip_font = pygame.font.Font('Inter.ttf', 18)
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

settings_open = False
settings_options = [
    {"label": "Default Input", "type": "cycle", "choices": ["Mic 1", "Mic 2"], "value": 0},
    {"label": "Default Output", "type": "cycle", "choices": ["Speaker 1", "Speaker 2"], "value": 0},
    {"label": "Stop Hints", "type": "toggle", "value": False},
    {"label": "Open Docs", "type": "button"},
    {"label": "Back", "type": "button"}
]
settings_sel = 0

def draw_settings(surface, options, selected):
    width, height = surface.get_size()
    menu_w, menu_h = 520, 420
    menu_x, menu_y =  (width - menu_w)//2, (height - menu_h)//2
    shadow = pygame.Surface((menu_w+16, menu_h+16), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0,0,0,80), shadow.get_rect(), border_radius=28)
    surface.blit(shadow, (menu_x-8, menu_y+12))
    menu_rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)
    pygame.draw.rect(surface, MENU_BG, menu_rect, border_radius=28)
    title_font = pygame.font.Font('Inter.ttf', 44)
    title_surface = title_font.render("Settings", True, ACCENT_COLOR)
    surface.blit(title_surface, (menu_x + 32, menu_y + 26))
    option_font = pygame.font.Font('Inter.ttf', 30)
    for i, opt in enumerate(options):
        if opt["type"] == "cycle":
            label = f'{opt["label"]}: {opt["choices"][opt["value"]]}'
        elif opt["type"] == "toggle":
            label = f'{opt["label"]}: {"On" if opt["value"] else "Off"}'
        else:
            label = opt["label"]
        color = ACCENT_COLOR if i == selected else EYE_COLOR
        bg_color = (40, 44, 48) if i == selected else MENU_BG
        item_rect = pygame.Rect(menu_x + 28, menu_y + 92 + i*60, menu_w - 56, 48)
        pygame.draw.rect(surface, bg_color, item_rect, border_radius=12)
        txt_surf = option_font.render(label, True, color)
        txt_rect = txt_surf.get_rect(midleft=(item_rect.x + 24, item_rect.centery))
        surface.blit(txt_surf, txt_rect)

def handle_settings(event, options, sel_idx):
    opt = options[sel_idx]
    if event.type == pygame.KEYDOWN:
        if opt["type"] == "cycle":
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                opt["value"] = (opt["value"] + 1) % len(opt["choices"])
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                opt["value"] = (opt["value"] - 1 ) % len(opt["choices"])
        elif opt["type"] == "toggle":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                opt["value"] = not opt["value"]
        elif opt["type"] == "button":
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if opt["label"] == "Open Docs":
                    webbrowser.open("https://github.com/divpreeet/project-chatter")
                elif opt["label"] == "Back":
                    return "close"
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_DOWN, pygame.K_s):
            return ("move", (sel_idx + 1) % len(options))
        elif event.key in (pygame.K_UP, pygame.K_w):
            return ("move", (sel_idx - 1) % len(options))
    return None

running = True
while running:
    if not settings_open:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    settings_open = True
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
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_open = False
                else:
                    result = handle_settings(event, settings_options, settings_sel)
                    if result == "close":
                        settings_open = False
                    elif isinstance(result, tuple) and result[0] == "move":
                        settings_sel = result[1]
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,128))
        screen.blit(overlay, (0,0))
        draw_settings(screen, settings_options, settings_sel)
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()
