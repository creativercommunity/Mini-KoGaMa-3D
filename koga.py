from aether import Engine, Scene, Entity, MeshFactory, Material, Camera, Sprite
from aether.scene.component import Transform, MeshRenderer
from PIL import Image, ImageDraw, ImageFont
import glfw
import math
import os

engine = Engine(1280, 720, "Mini KoGaMa Test")
engine.free_camera = False
engine.capture_mouse(True)
engine.draw_hud = True

scene = Scene("Main")

SPAWN_X, SPAWN_Y, SPAWN_Z = 0.0, 2.0, 6.0
camera = Camera(position=(0.0, 4.0, 11.0))
scene.set_main_camera(camera)

blocks = []

def set_pos(target, x, y, z):
    if hasattr(target, "set_position"):
        try:
            target.set_position((x, y, z))
            return
        except Exception:
            target.set_position(x, y, z)
            return
    target.position = (x, y, z)

def create_block(name, pos, scale, color, is_lava=False):
    block = Entity(name)
    block.add_component(Transform(position=pos, scale=scale))
    mat = Material()
    mat.albedo[:] = color
    block.add_component(MeshRenderer(mesh=MeshFactory.create_cube(), material=mat))
    scene.spawn(block)
    bx, by, bz = pos
    sx, sy, sz = scale
    blocks.append({
        "bx": bx, "by": by, "bz": bz,
        "sx": sx, "sy": sy, "sz": sz,
        "is_lava": is_lava
    })
    return block

create_block("Floor", (0, -0.5, 0), (24, 1, 24), (0.2, 0.8, 0.2))
create_block("Block1", (2, 0.5, 0), (1.5, 1, 1.5), (0.2, 0.2, 0.8))
create_block("Block2", (-2, 1.5, 2), (1.5, 1, 1.5), (0.2, 0.2, 0.8))
create_block("Block3", (0, 2.5, -2), (2.5, 0.5, 2.5), (0.9, 0.8, 0.1))
create_block("Lava", (2, 0.05, 3), (3, 0.1, 3), (1.0, 0.15, 0.0), is_lava=True)

SKIN = (0.76, 0.58, 0.42)
HAIR_BLUE = (0.14, 0.54, 0.90)
HAIR_LIGHT = (0.35, 0.72, 0.98)
RED = (0.78, 0.14, 0.16)
BLUE = (0.16, 0.52, 0.86)
WHITE = (0.96, 0.96, 0.98)
ORANGE = (0.90, 0.52, 0.10)
EYE_COLOR = (0.22, 0.14, 0.34)
DARK_SOCK = (0.15, 0.15, 0.18)

avatar_parts = []

def add_avatar_part(name, ox, oy, oz, sx, sy, sz, color, swing_group=0):
    ent = Entity(name)
    tr = Transform(position=(SPAWN_X + ox, SPAWN_Y + oy, SPAWN_Z + oz), scale=(sx, sy, sz))
    ent.add_component(tr)
    mat = Material()
    mat.albedo[:] = color
    ent.add_component(MeshRenderer(mesh=MeshFactory.create_cube(), material=mat))
    scene.spawn(ent)
    avatar_parts.append({"tr": tr, "ox": ox, "oy": oy, "oz": oz, "swing": swing_group})

add_avatar_part("Head", 0.0, 1.12, 0.0, 0.46, 0.42, 0.42, SKIN)
add_avatar_part("EyeL", -0.11, 1.11, -0.215, 0.09, 0.09, 0.02, EYE_COLOR)
add_avatar_part("EyeR", 0.11, 1.11, -0.215, 0.09, 0.09, 0.02, EYE_COLOR)
add_avatar_part("HairTop", 0.0, 1.36, 0.02, 0.54, 0.14, 0.50, HAIR_BLUE)
add_avatar_part("HairBack", 0.0, 1.14, 0.22, 0.56, 0.48, 0.14, HAIR_BLUE)
add_avatar_part("HairSideL", -0.28, 1.14, 0.02, 0.14, 0.46, 0.46, HAIR_BLUE)
add_avatar_part("HairSideR", 0.28, 1.14, 0.02, 0.14, 0.46, 0.46, HAIR_BLUE)
add_avatar_part("HairBangs", 0.0, 1.27, -0.21, 0.50, 0.13, 0.08, HAIR_LIGHT)
add_avatar_part("Ahoge", 0.02, 1.48, -0.02, 0.08, 0.16, 0.08, HAIR_LIGHT)
add_avatar_part("Neck", 0.0, 0.88, 0.0, 0.16, 0.10, 0.16, SKIN)
add_avatar_part("TorsoRed", -0.11, 0.72, 0.0, 0.22, 0.26, 0.24, RED)
add_avatar_part("TorsoBlue", 0.11, 0.72, 0.0, 0.22, 0.26, 0.24, BLUE)
add_avatar_part("ChestWhite", 0.0, 0.65, -0.02, 0.36, 0.14, 0.23, WHITE)
add_avatar_part("Bow", 0.0, 0.77, -0.13, 0.22, 0.08, 0.05, ORANGE)
add_avatar_part("Belly", 0.0, 0.54, 0.0, 0.32, 0.10, 0.20, SKIN)
add_avatar_part("SkirtRed", -0.12, 0.40, 0.0, 0.24, 0.20, 0.28, RED)
add_avatar_part("SkirtBlue", 0.12, 0.40, 0.0, 0.24, 0.20, 0.28, BLUE)
add_avatar_part("ArmL", -0.29, 0.64, 0.0, 0.11, 0.36, 0.11, SKIN, 1)
add_avatar_part("GloveL", -0.29, 0.44, 0.0, 0.12, 0.09, 0.12, WHITE, 1)
add_avatar_part("ArmR", 0.29, 0.64, 0.0, 0.11, 0.36, 0.11, SKIN, -1)
add_avatar_part("GloveR", 0.29, 0.44, 0.0, 0.12, 0.09, 0.12, WHITE, -1)
add_avatar_part("LegL", -0.11, 0.18, 0.0, 0.13, 0.26, 0.13, ORANGE, -1)
add_avatar_part("ShoeL", -0.11, 0.04, -0.03, 0.14, 0.08, 0.18, BLUE, -1)
add_avatar_part("LegR", 0.11, 0.18, 0.0, 0.13, 0.26, 0.13, DARK_SOCK, 1)
add_avatar_part("ShoeR", 0.11, 0.04, -0.03, 0.14, 0.08, 0.18, RED, 1)
CROSSHAIR_PATH = os.path.abspath("crosshair.png")
ch_img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
ch_draw = ImageDraw.Draw(ch_img)
ch_draw.ellipse((8, 8, 88, 88), outline=(30, 235, 30, 255), width=5)
ch_draw.ellipse((44, 44, 52, 52), fill=(30, 235, 30, 255))
ch_img.save(CROSSHAIR_PATH)

crosshair_sprite = Sprite.from_image(CROSSHAIR_PATH, x=0.0, y=0.0, width=76.0, height=76.0)
crosshair_sprite.visible = False
engine.renderer2d.add_sprite(crosshair_sprite)

CONTROLS_PATH = os.path.abspath("controls_hud.png")
CTRL_W, CTRL_H = 270, 165
CTRL_LINES = [
    "WASD - Move",
    "SPACE - Jump",
    "Q - 1st / 3rd Person",
    "F11 - Fullscreen",
    "ESC - Menu"
]

ctrl_img = Image.new("RGBA", (CTRL_W, CTRL_H), (0, 0, 0, 0))
c_draw = ImageDraw.Draw(ctrl_img)
c_draw.rounded_rectangle((0, 0, CTRL_W - 1, CTRL_H - 1), radius=10, fill=(20, 25, 35, 135))

try:
    ctrl_font = ImageFont.truetype("arialbd.ttf", 18)
except Exception:
    try:
        ctrl_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        ctrl_font = ImageFont.load_default()

cy = 14
for line in CTRL_LINES:
    c_draw.text((16, cy), line, font=ctrl_font, fill=(255, 255, 255, 255))
    cy += 28

ctrl_img.save(CONTROLS_PATH)

controls_sprite = Sprite.from_image(
    CONTROLS_PATH,
    x=-640.0 + CTRL_W / 2.0 + 18.0,
    y=360.0 - CTRL_H / 2.0 - 18.0,
    width=float(CTRL_W),
    height=float(CTRL_H)
)
controls_sprite.visible = True
engine.renderer2d.add_sprite(controls_sprite)

MENU_PATH = os.path.abspath("pause_menu.png")
MENU_W, MENU_H = 380, 520
MENU_LABELS = ["PLAY", "SETTINGS", "SHOP", "BOOST", "RESPAWN", "EXIT GAME"]
menu_btn_rects = []

menu_img = Image.new("RGBA", (MENU_W, MENU_H), (0, 0, 0, 0))
m_draw = ImageDraw.Draw(menu_img)
m_draw.rounded_rectangle((0, 0, MENU_W - 1, MENU_H - 1), radius=14, fill=(75, 115, 145, 155))

try:
    menu_font = ImageFont.truetype("arialbd.ttf", 22)
except Exception:
    try:
        menu_font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        menu_font = ImageFont.load_default()

btn_w = 336
btn_h = 62
btn_x = (MENU_W - btn_w) // 2
start_y = 22
gap = 18

for idx, label in enumerate(MENU_LABELS):
    by = start_y + idx * (btn_h + gap)
    m_draw.rectangle((btn_x, by + btn_h - 6, btn_x + btn_w, by + btn_h), fill=(155, 155, 150, 255))
    m_draw.rectangle((btn_x, by, btn_x + btn_w, by + btn_h - 6), fill=(235, 233, 224, 255))
    x_min, y_min, x_max, y_max = m_draw.textbbox((0, 0), label, font=menu_font)
    tw = x_max - x_min
    th = y_max - y_min
    tx = btn_x + (btn_w - tw) // 2
    ty = by + (btn_h - 6 - th) // 2 - 2
    m_draw.text((tx, ty), label, font=menu_font, fill=(52, 52, 52, 255))
    menu_btn_rects.append((label, btn_x, by, btn_x + btn_w, by + btn_h))

menu_img.save(MENU_PATH)

menu_sprite = Sprite.from_image(MENU_PATH, x=0.0, y=0.0, width=float(MENU_W), height=float(MENU_H))
menu_sprite.visible = False
engine.renderer2d.add_sprite(menu_sprite)

menu_open = False
was_mouse_down = False
force_exit = False
is_fullscreen = False
saved_win_rect = (100, 100, 1280, 720)
last_fb_size = (0, 0)

def toggle_fullscreen(win):
    global is_fullscreen, saved_win_rect
    if not win:
        return
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        wx, wy = glfw.get_window_pos(win)
        ww, wh = glfw.get_window_size(win)
        saved_win_rect = (wx, wy, ww, wh)
        mon = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(mon)
        glfw.set_window_monitor(win, mon, 0, 0, mode.size.width, mode.size.height, mode.refresh_rate)
    else:
        wx, wy, ww, wh = saved_win_rect
        glfw.set_window_monitor(win, None, wx, wy, ww, wh, 0)

def toggle_menu(state):
    global menu_open
    menu_open = state
    menu_sprite.visible = menu_open
    controls_sprite.visible = not menu_open
    engine.capture_mouse(not menu_open)
    if menu_open:
        crosshair_sprite.visible = False
    else:
        crosshair_sprite.visible = first_person

def intercept_quit(data=None):
    if force_exit:
        return
    engine._running = True
    toggle_menu(not menu_open)

engine.event_bus.subscribe("engine_quit", intercept_quit)

engine.load_scene(scene)

px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
vel_y = 0.0
on_ground = False
cam_yaw = -90.0
cam_pitch = 15.0
player_yaw = 0.0
target_yaw = 0.0
walk_time = 0.0
CAM_DIST = 5.5
first_person = False

GRAVITY = -22.0
JUMP_FORCE = 8.5
MOVE_SPEED = 6.0
HALF_W = 0.3
HEIGHT = 1.5

def check_collision(x, y, z):
    for b in blocks:
        hx = b["sx"] / 2.0
        hy = b["sy"] / 2.0
        hz = b["sz"] / 2.0
        if (abs(x - b["bx"]) < hx + HALF_W and
            abs(z - b["bz"]) < hz + HALF_W and
            y < b["by"] + hy and
            y + HEIGHT > b["by"] - hy):
            return b
    return None

def update_avatar_transform(x, y, z, yaw_deg, visible, walk_phase):
    if not visible:
        for p in avatar_parts:
            p["tr"].set_position(x, -100.0, z)
        return
    rad = math.radians(yaw_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    swing = math.sin(walk_phase) * 0.08
    for p in avatar_parts:
        ox = p["ox"]
        oy = p["oy"]
        oz = p["oz"] + swing * p["swing"]
        rx = ox * cos_a + oz * sin_a
        rz = -ox * sin_a + oz * cos_a
        p["tr"].set_position(x + rx, y + oy, z + rz)
        p["tr"].set_rotation(0.0, yaw_deg, 0.0)

def update_game(dt):
    global px, py, pz, vel_y, on_ground, cam_yaw, cam_pitch, player_yaw, target_yaw, walk_time, first_person
    global was_mouse_down, force_exit, last_fb_size

    inp = engine.input
    win = glfw.get_current_context()

    if win:
        fb_w, fb_h = glfw.get_framebuffer_size(win)
        if fb_w > 0 and fb_h > 0 and (fb_w, fb_h) != last_fb_size:
            last_fb_size = (fb_w, fb_h)
            engine._on_window_resize({"width": fb_w, "height": fb_h})
            menu_sprite.x = 0.0
            menu_sprite.y = 0.0
            crosshair_sprite.x = 0.0
            crosshair_sprite.y = 0.0
            controls_sprite.x = -fb_w / 2.0 + CTRL_W / 2.0 + 18.0
            controls_sprite.y = fb_h / 2.0 - CTRL_H / 2.0 - 18.0

        if inp.get_key_down(glfw.KEY_F11):
            toggle_fullscreen(win)

    if menu_open and win:
        mouse_down = glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        if mouse_down and not was_mouse_down:
            mx, my = glfw.get_cursor_pos(win)
            w_w, w_h = glfw.get_window_size(win)
            fb_w, fb_h = glfw.get_framebuffer_size(win)
            sx = fb_w / float(w_w) if w_w > 0 else 1.0
            sy = fb_h / float(w_h) if w_h > 0 else 1.0
            pmx = mx * sx
            pmy = my * sy
            left = (fb_w - MENU_W) / 2.0
            top = (fb_h - MENU_H) / 2.0
            lx = pmx - left
            ly = pmy - top
            for label, x1, y1, x2, y2 in menu_btn_rects:
                if x1 <= lx <= x2 and y1 <= ly <= y2:
                    if label == "PLAY":
                        toggle_menu(False)
                    elif label == "RESPAWN":
                        px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
                        vel_y = 0.0
                        toggle_menu(False)
                    elif label == "EXIT GAME":
                        force_exit = True
                        engine._running = False
                    else:
                        print(f"[Menu] {label} clicked")
                    break
        was_mouse_down = mouse_down
    else:
        was_mouse_down = False

    if not menu_open:
        if inp.get_key_down(glfw.KEY_Q):
            first_person = not first_person
            crosshair_sprite.visible = first_person
            if first_person:
                cam_pitch = max(-75.0, min(75.0, cam_pitch))
            else:
                cam_pitch = max(-20.0, min(75.0, cam_pitch))

        cam_yaw += inp.mouse_dx * 0.15
        if first_person:
            cam_pitch = max(-80.0, min(80.0, cam_pitch + inp.mouse_dy * 0.15))
        else:
            cam_pitch = max(-20.0, min(75.0, cam_pitch + inp.mouse_dy * 0.15))

    rad_yaw = math.radians(cam_yaw)
    forward_x = math.cos(rad_yaw)
    forward_z = math.sin(rad_yaw)
    right_x = -forward_z
    right_z = forward_x

    move_x, move_z = 0.0, 0.0
    if not menu_open:
        if inp.get_key(glfw.KEY_W):
            move_x += forward_x
            move_z += forward_z
        if inp.get_key(glfw.KEY_S):
            move_x -= forward_x
            move_z -= forward_z
        if inp.get_key(glfw.KEY_D):
            move_x += right_x
            move_z += right_z
        if inp.get_key(glfw.KEY_A):
            move_x -= right_x
            move_z -= right_z

    length = math.hypot(move_x, move_z)
    if length > 0:
        move_x = (move_x / length) * MOVE_SPEED * dt
        move_z = (move_z / length) * MOVE_SPEED * dt
        target_yaw = math.degrees(math.atan2(-move_x, -move_z))
        if on_ground:
            walk_time += dt * 14.0
    else:
        walk_time = 0.0

    diff = (target_yaw - player_yaw + 180.0) % 360.0 - 180.0
    player_yaw += diff * min(1.0, dt * 15.0)

    px += move_x
    hit = check_collision(px, py, pz)
    if hit:
        if hit["is_lava"]:
            px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
            vel_y = 0.0
        else:
            px -= move_x

    pz += move_z
    hit = check_collision(px, py, pz)
    if hit:
        if hit["is_lava"]:
            px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
            vel_y = 0.0
        else:
            pz -= move_z

    vel_y += GRAVITY * dt
    py += vel_y * dt
    on_ground = False

    hit = check_collision(px, py, pz)
    if hit:
        if hit["is_lava"]:
            px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
            vel_y = 0.0
        else:
            if vel_y <= 0:
                py = hit["by"] + hit["sy"] / 2.0
                on_ground = True
            else:
                py = hit["by"] - hit["sy"] / 2.0 - HEIGHT
            vel_y = 0.0

    if py < -10.0:
        px, py, pz = SPAWN_X, SPAWN_Y, SPAWN_Z
        vel_y = 0.0

    if not menu_open and inp.get_key(glfw.KEY_SPACE) and on_ground:
        vel_y = JUMP_FORCE
        on_ground = False

    rad_pitch = math.radians(cam_pitch)

    if first_person:
        update_avatar_transform(px, py, pz, player_yaw, False, 0.0)

        eye_x, eye_y, eye_z = px, py + 1.25, pz
        dir_x = math.cos(rad_yaw) * math.cos(rad_pitch)
        dir_y = -math.sin(rad_pitch)
        dir_z = math.sin(rad_yaw) * math.cos(rad_pitch)

        set_pos(camera, eye_x, eye_y, eye_z)
        try:
            camera.look_at((eye_x + dir_x, eye_y + dir_y, eye_z + dir_z))
        except Exception:
            camera.look_at(eye_x + dir_x, eye_y + dir_y, eye_z + dir_z)
    else:
        update_avatar_transform(px, py, pz, player_yaw, True, walk_time)

        tx, ty, tz = px, py + 1.1, pz
        cam_x = tx - math.cos(rad_yaw) * math.cos(rad_pitch) * CAM_DIST
        cam_y = ty + math.sin(rad_pitch) * CAM_DIST
        cam_z = tz - math.sin(rad_yaw) * math.cos(rad_pitch) * CAM_DIST

        set_pos(camera, cam_x, cam_y, cam_z)
        try:
            camera.look_at((tx, ty, tz))
        except Exception:
            camera.look_at(tx, ty, tz)


engine.on_update(update_game)
engine.run()