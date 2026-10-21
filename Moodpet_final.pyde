# MoodPet - Processing Python Mode (Python 2 / Jython)
# No external images, audio libraries, or extra files required.
# setup() runs once; draw() runs continuously.

DOGS = ["Pug", "Border Collie", "Pomeranian", "Shiba", "French Bulldog"]
screen = 0
selected_dog = 0
dog_name = ""
mood = "normal"
energy = 80
last_activity = 0
rest_start = 0
mood_start = 0
feed_until = 0
pressed_button = ""
button_until = 0
bg_r, bg_g, bg_b = 245.0, 240.0, 230.0


def setup():
    size(800, 600)
    frameRate(30)
    textAlign(CENTER, CENTER)


def draw():
    global bg_r, bg_g, bg_b, pressed_button
    if screen == 2:
        update_pet()
        palettes = {"normal": (245, 240, 230), "happy": (255, 239, 211),
                    "sad": (197, 209, 226), "excited": (255, 224, 193),
                    "tired": (214, 211, 217), "resting": (178, 189, 220)}
        target = palettes[mood]
        bg_r += (target[0] - bg_r) * 0.12
        bg_g += (target[1] - bg_g) * 0.12
        bg_b += (target[2] - bg_b) * 0.12
        background(int(bg_r), int(bg_g), int(bg_b))
        draw_play_screen()
    else:
        background(245, 240, 230)
        if screen == 0:
            draw_start_screen()
        else:
            draw_select_screen()
    if millis() > button_until:
        pressed_button = ""


def button(label, x, y, w, h, color_rgb):
    rectMode(CENTER)
    stroke(110, 100, 100, 90)
    strokeWeight(2)
    if pressed_button == label:
        fill(max(0, color_rgb[0] - 30), max(0, color_rgb[1] - 30), max(0, color_rgb[2] - 30))
    else:
        fill(*color_rgb)
    rect(x, y, w, h, 14)
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(21)
    text(label, x, y - 2)


def draw_start_screen():
    fill(65, 61, 72)
    textSize(52)
    text("MoodPet", 400, 150)
    textSize(20)
    text("Your virtual puppy friend", 400, 205)
    draw_dog(400, 340, 0.55, 2, "happy")
    button("Start", 400, 510, 210, 64, (116, 180, 140))


def draw_select_screen():
    fill(60)
    textSize(32)
    text("Choose Your Dog", 400, 62)
    for i in range(5):
        x = 100 + i * 150
        if i == selected_dog:
            noFill()
            stroke(95, 140, 215)
            strokeWeight(4)
            rectMode(CENTER)
            rect(x, 240, 136, 178, 15)
        draw_dog(x, 228, 0.40, i, "normal")
        fill(60)
        textSize(13)
        text(DOGS[i], x, 320)
    fill(70)
    textSize(19)
    text("Name your puppy:", 400, 391)
    rectMode(CENTER)
    fill(255)
    stroke(155)
    rect(400, 443, 400, 54, 9)
    fill(60)
    textSize(22)
    text(dog_name if dog_name else "Type a name here", 400, 442)
    button("Continue", 400, 525, 200, 55, (116, 180, 140))


def draw_dog(x, y, s, breed, state):
    # Drawn with Processing shapes so missing image files cannot crash the sketch.
    pushMatrix()
    translate(x, y)
    if state == "happy":
        translate(0, -abs(sin(frameCount * 0.18)) * 13)
    elif state == "excited":
        translate(0, -abs(sin(frameCount * 0.35)) * 24)
        rotate(sin(frameCount * 0.2) * 0.06)
    elif state == "sad":
        translate(0, 12)
    elif state == "resting":
        translate(0, 30)
        scale(1, 0.7)
    elif state == "tired":
        translate(0, 16)
    scale(s)
    coats = [(192, 151, 108), (235, 230, 222), (219, 153, 78),
             (212, 133, 67), (195, 184, 174)]
    coat = coats[breed]
    noStroke()
    fill(*coat)
    ellipse(0, 85, 155, 145)
    ellipse(-48, 143, 45, 30)
    ellipse(48, 143, 45, 30)
    # ears
    if breed == 0 or breed == 4:
        fill(coat[0] - 28, coat[1] - 22, coat[2] - 16)
        ellipse(-69, -42, 58, 95)
        ellipse(69, -42, 58, 95)
    else:
        fill(*coat)
        triangle(-78, -28, -66, -128, -12, -70)
        triangle(78, -28, 66, -128, 12, -70)
        fill(233, 166, 156)
        triangle(-66, -46, -61, -103, -32, -67)
        triangle(66, -46, 61, -103, 32, -67)
    fill(*coat)
    ellipse(0, -15, 170, 157)
    if breed == 1:
        fill(255)
        ellipse(0, -12, 53, 118)
    fill(255, 245, 225)
    ellipse(0, 28, 91, 66)
    fill(55, 45, 43)
    ellipse(-34, -27, 14, 19)
    ellipse(34, -27, 14, 19)
    ellipse(0, 15, 28, 20)
    stroke(65, 47, 48)
    strokeWeight(3)
    noFill()
    arc(0, 27, 34, 26, 0, PI)
    noStroke()
    if state == "happy" or state == "excited":
        fill(242, 145, 151)
        ellipse(-52, 3, 22, 13)
        ellipse(52, 3, 22, 13)
    popMatrix()


def draw_play_screen():
    fill(65)
    textSize(36)
    text(dog_name, 400, 65)
    draw_dog(290, 237, 1.3, selected_dog, mood)
    if mood == "resting":
        fill(75, 83, 140)
        textSize(35)
        text("Zzz", 460, 164)
    elif mood == "happy":
        fill(233, 91, 111)
        textSize(36)
        text("<3", 450, 164)
    elif mood == "sad":
        fill(70, 100, 170)
        textSize(34)
        text("...", 450, 164)
    elif mood == "excited":
        fill(240, 170, 50)
        textSize(38)
        text("* *", 450, 164)
    if millis() < feed_until:
        fill(170, 113, 56)
        ellipse(445, 295, 48, 30)
        fill(255)
        textSize(16)
        text("Yum!", 448, 336)
    rectMode(CENTER)
    fill(255, 250, 245)
    stroke(204, 193, 182)
    rect(400, 402, 465, 68, 12)
    fill(65)
    textSize(19)
    text("Mood: " + mood.capitalize(), 290, 400)
    noStroke()
    fill(216)
    rect(493, 402, 150, 23, 6)
    fill(104, 182, 121)
    rectMode(CORNER)
    rect(418, 390, 150 * energy / 100.0, 23, 6)
    fill(55)
    textSize(13)
    text(str(energy) + "%", 493, 401)
    colors = [(127, 184, 153), (228, 169, 110), (116, 161, 217), (162, 149, 184)]
    for i, label in enumerate(["Pet", "Feed", "Play", "Rest"]):
        button(label, 145 + 170 * i, 507, 145, 62, colors[i])
    fill(90)
    textSize(14)
    text("Pet to cheer up  |  Feed for energy  |  Play to have fun  |  Rest to recharge", 400, 568)


def change_mood(new_mood):
    global mood, mood_start, rest_start
    if mood != new_mood:
        mood = new_mood
        mood_start = millis()
        if mood == "resting":
            rest_start = millis()


def update_pet():
    global energy, last_activity
    now = millis()
    if mood == "resting":
        if frameCount % 6 == 0:
            energy = min(100, energy + 1)
        if now - rest_start >= 4000 and energy >= 70:
            change_mood("normal")
            last_activity = now
    else:
        if now - last_activity >= 60000:
            change_mood("resting")
        elif now - last_activity >= 30000:
            change_mood("sad")
        elif mood in ("happy", "excited") and now - mood_start > 5500:
            change_mood("normal" if energy > 20 else "tired")
        if energy <= 20 and mood != "sad":
            change_mood("tired")


def inside(x, y, cx, cy, w, h):
    return abs(x - cx) <= w / 2 and abs(y - cy) <= h / 2


def mousePressed():
    global screen, selected_dog, energy, last_activity
    global feed_until, pressed_button, button_until
    if screen == 0:
        if inside(mouseX, mouseY, 400, 510, 210, 64):
            screen = 1
    elif screen == 1:
        for i in range(5):
            if inside(mouseX, mouseY, 100 + i * 150, 240, 136, 178):
                selected_dog = i
                return
        if inside(mouseX, mouseY, 400, 525, 200, 55):
            start_play()
    else:
        labels = ["Pet", "Feed", "Play", "Rest"]
        for i in range(4):
            if inside(mouseX, mouseY, 145 + i * 170, 507, 145, 62):
                pressed_button = labels[i]
                button_until = millis() + 200
                last_activity = millis()
                if i == 0:
                    change_mood("happy")
                elif i == 1:
                    energy = min(100, energy + 15)
                    feed_until = millis() + 1700
                    change_mood("happy")
                elif i == 2:
                    energy = max(0, energy - 20)
                    change_mood("excited" if energy > 20 else "tired")
                else:
                    change_mood("resting")
                return


def start_play():
    global screen, dog_name, last_activity, energy
    if not dog_name.strip():
        dog_name = DOGS[selected_dog]
    screen = 2
    energy = 80
    last_activity = millis()
    change_mood("normal")


def keyPressed():
    global dog_name
    if screen != 1:
        return
    if key == ENTER or key == RETURN:
        start_play()
    elif key == BACKSPACE:
        dog_name = dog_name[:-1]
    elif key != CODED and len(dog_name) < 18:
        if ord(key) >= 32:
            dog_name += key
