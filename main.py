import time
import image_processor
import cv2
import numpy as np
from mediapipe import solutions

helicopter_blade = [(160, 160, 160), (64, 64, 64), (255, 255, 255), (10, 10, 10), (32, 32, 32)]
cam_index = 0
x, y = 150, 365
x_ini, y_ini = 150, 365
score = 20
shift = 0
co_shift = 0
life = 3
take_off = 0
blank_image = np.zeros((480, 640, 3), np.uint8)
blank_image[:] = 191, 0, 249
blank_image[0:50, :] = 240, 0, 153
cam = cv2.VideoCapture(cam_index)
cam.set(3, 640)
cam.set(4, 480)
background = cv2.imread("background.jpg")
background = cv2.resize(background, (640, 480))
hrudle_list = [100, 100, 100, 100, 100, 100, 100, 100, 100]
hand = solutions.hands.Hands()
prev_time = 0
with open("data.xml", "r") as r:
    highest = r.read()
    r.close()

def hurdles(img, hurdle_list=[], shift=0, color=()):
    for id, i in enumerate(hurdle_list):
        cv2.rectangle(img, (id * 80 - shift, 0), ((id * 80) + 80 - shift, i), color, -1)  # rgb(115, 60, 60)
        cv2.rectangle(img, (id * 80 - shift, i + 300), ((id * 80) + 80 - shift, 480), color, -1)
    return img


def helicopter(img, x=200, y=200):
    cv2.line(img, (x, y), (x - 25, y + 35), (40, 40, 40), 2)
    cv2.line(img, (x, y), (x + 25, y + 35), (40, 40, 40), 2)
    cv2.line(img, (x - 35, y + 35), (x + 35, y + 35), (40, 40, 40), 2)
    cv2.line(img, (x + 35, y + 35), (x + 40, y + 30), (40, 40, 40), 2)
    cv2.line(img, (x, y-10), (x - 100, y-10), (68, 86,223), 8)
    cv2.line(img, (x - 100, y - 25), (x - 100, y + 2), (213, 209, 204), 5)
    cv2.line(img, (x, y), (x, y - 35), (213, 209, 204), 10)
    cv2.line(img, (x - 70, y - 40), (x + 70, y - 40), helicopter_blade[np.random.randint(0, len(helicopter_blade))], 3)
    cv2.line(img, (x - 120, y - 28), (x - 80, y - 28), helicopter_blade[np.random.randint(0, len(helicopter_blade))], 2)
    cv2.ellipse(img, (x, y), (50, 25), 0, 0, 360, (68, 86,223), -1)
    cv2.rectangle(img, (x - 50, y), (x, y - 25), (68, 86,223), -1)
    # cv2.line(img, (x, y - 24), (x, y), (93, 79, 51), 3)  # rgb(223, 223, 222)
    # cv2.line(img, (x, y), (x + 50, y), (93, 79, 51), 3)
    cv2.ellipse(img, (x+23, y-8), (10, 20), -70, 0, 360, (93, 79, 51), -1)
    cv2.rectangle(img, (x+4, y-10), (x+32, y+4), (93, 79, 51), -1)

    # cv2.circle(img, (x+5, y), 10, (93, 79, 51), -1)

    return img


# blank_image = hurdles(blank_image, score)

def game_over(img, x, y, highest = 0, curr_score = 0, life=0):

    w = x + 80
    h = y + 55
    x = x - 130
    y = y - 60
    img = image_processor.Graphics.draw_rect(img, (x, y), (w, h), rect=False, line=True, line_thickness=2)

    cv2.imshow("Helicopter", img)
    cv2.waitKey(1000)
    if life > 0:
        life = life - 1
        return 320, 240, curr_score, 0, [100, 100, 100, 100, 100, 100, 100, 100, 100], highest, 0, life, 0, 150, 365
    if int(curr_score) > int(highest):
        highest = int(curr_score)
        with open("data.xml", "w") as w:
            w.write(str(highest))
            w.close()
    cv2.putText(img, "Game Over", (110, 120), cv2.FONT_ITALIC, 2.5, (255, 255, 255), 3)
    cv2.putText(img, "Better luck next time...!", (135, 200), cv2.FONT_ITALIC, 1, (0, 0, 255), 1)

    cv2.putText(img, "Escape 2 Exit | Enter 2 Play Again", (40, 240), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
    cv2.imshow("Helicopter", img)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        cam.release()
        exit()
    if cv2.waitKey(0) == 13:
        with open("data.xml", "r") as r:
            highest_score = r.read()
            r.close()
        x, y, score, prev_time, hrudle_list, shift, life, take_off, x_ini, y_ini = 320, 240, 0, 0, [100, 100, 100, 100, 100, 100, 100, 100, 100], 0, 3, 0, 150, 365
        return x, y, score, prev_time, hrudle_list, int(highest_score), shift, life, take_off, x_ini, y_ini


while True:
    _, img = cam.read()
    img = cv2.flip(img, 1)
    if time.time() - prev_time > 1 and x > 400 and score < 10:
        curv = hrudle_list[-1] + np.random.randint(-100, 100)
        if curv < -200:
            continue
        if curv > 300:
            continue
        hrudle_list.pop(0)
        hrudle_list.insert(8, curv)
        prev_time = time.time()
        shift = 0
        co_shift = int(((1 - (score / 50)) - (time.time() - prev_time))*10)
        # print()

    if time.time() - prev_time > 0.5 and x > 400 and 20 > score > 10:
        curv = hrudle_list[-1] + np.random.randint(-100, 100)
        if curv < -200:
            continue
        if curv > 300:
            continue
        hrudle_list.pop(0)
        hrudle_list.insert(8, curv)
        prev_time = time.time()
        shift = 0
        co_shift = int(((1 - (score / 50)) - (time.time() - prev_time))*10)
        # print()

    if time.time() - prev_time > 0.3 and x > 400 and 60 > score > 20:

        curv = hrudle_list[-1] + np.random.randint(-100, 100)
        if curv < -200:
            continue
        if curv > 300:
            continue
        hrudle_list.pop(0)
        hrudle_list.insert(8, curv)
        prev_time = time.time()
        shift = 0
        co_shift = int(((1 - (score / 50)) - (time.time() - prev_time))*10)
        # print()

    if time.time() - prev_time > 0.2 and x > 400 and 100 > score > 60:

        curv = hrudle_list[-1] + np.random.randint(-180, 180)
        if curv < -200:
            continue
        if curv > 300:
            continue
        hrudle_list.pop(0)
        hrudle_list.insert(8, curv)
        prev_time = time.time()
        shift = 0
        co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)
        # print()

    if time.time() - prev_time > 0.1 and x > 400 and 200 > score > 100:

        curv = hrudle_list[-1] + np.random.randint(-180, 180)
        if curv < -200:
            continue
        if curv > 300:
            continue
        hrudle_list.pop(0)
        hrudle_list.insert(8, curv)
        prev_time = time.time()
        shift = 0
        co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)
        # print()

    # print(int(((1 - (score / 50)) - (time.time() - prev_time))*10))
    if x > 400:
        if 0 < score < 10:
            shift = shift + 7
        elif 10 < score < 20:
            shift = shift + 11
        elif 20 < score < 60:
            shift = shift + 13
        elif 60 < score < 100:
            shift = shift + 15
        elif 100 < score < 200:
            shift = shift + 20
        score = score + 0.1
    # print(hrudle_list)
    # blank_image[:] = 191, 0, 249
    if score < 50:
        blank_image[:] = img
    else: blank_image[:] = background
    if score > 50:
        blank_image = hurdles(blank_image, hrudle_list, shift, (115, 88, 87))
    else: blank_image = hurdles(blank_image, hrudle_list, shift, (60, 50, 50))
    # blank_image[0:50, :] = 49, 7, 0
    header = "Score: " + str(int(score)) + " | " + str(highest) + "                        " + "Life: " + str(life) + " | " + "3"
    cv2.putText(blank_image, header , (10, 34), cv2.FONT_ITALIC, 0.8, (200, 200, 200), 1)  # rgb(255, 133, 179)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pos = hand.process(img_rgb)
    if pos.multi_hand_landmarks:
        for id_finger in pos.multi_hand_landmarks:
            for id, loc in enumerate(id_finger.landmark):
                if id == 8:
                    x, y = int(loc.x * 640), int(loc.y * 480)
                    cv2.drawMarker(img, (x, y), (0, 0, 255), markerSize=50, thickness=5)

    img_resize = cv2.resize(img, (160, 120))
    # blank_image[360:, 0:160] = img_resize
    # print("take off", take_off, x_ini, y_ini)
    if take_off < 1000:
        if x_ini < x and take_off > 70:
            x_ini = x_ini + 10
        if y_ini > y and take_off > 70:
            y_ini = y_ini - 10

        if x_ini > x and take_off > 70:
            x_ini = x_ini - 10
        if y_ini < y and take_off > 70:
            y_ini = y_ini + 10
        print(x_ini, y_ini, x, y)
        if x_ini == x and y_ini == y:
            take_off = 2000
        take_off = take_off + 1
        x, y = x_ini, y_ini
        # blank_image = helicopter(blank_image, x_ini, y_ini)

    blank_image = helicopter(blank_image, x, y)


    if 0 - shift < x < 80 - shift and y - 35 < hrudle_list[0]:
        print("game over parameters 1:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 0 -shift < x < 80 -shift and y + 25 > hrudle_list[0] + 300:
        print("game over parameters 9:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 80 -shift < x < 160 -shift and y - 35 < hrudle_list[1]:
        print("game over parameters 2:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 80 -shift < x < 160 -shift and y + 25 > hrudle_list[1] + 300:
        print("game over parameters 10:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 160 -shift < x < 240 -shift and y - 35 < hrudle_list[2]:
        print("game over parameters 3:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 160 -shift < x < 240 -shift and y + 25 > hrudle_list[2] + 300:
        print("game over parameters 11:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 240 -shift < x < 320 -shift and y - 35 < hrudle_list[3]:
        print("game over parameters 4:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 240 -shift < x < 320 -shift and y + 25 > hrudle_list[3] + 300:
        print("game over parameters 12:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 320 -shift < x < 400 -shift and y - 35 < hrudle_list[4]:
        print("game over parameters 5:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 320 -shift < x < 400 -shift and y + 25 > hrudle_list[4] + 300:
        print("game over parameters 6:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 400 -shift < x < 480 -shift and y - 35 < hrudle_list[5]:
        print("game over parameters 7:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 400 -shift < x < 480 -shift and y + 25 > hrudle_list[5] + 300:
        print("game over parameters 8:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 480 -shift < x < 560 -shift and y - 35 < hrudle_list[6]:
        print("game over parameters 7:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 480 -shift < x < 560 -shift and y + 25 > hrudle_list[6] + 300:
        print("game over parameters 8:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 560 -shift < x < 640 -shift and y - 35 < hrudle_list[7]:
        print("game over parameters 7:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue
    if 560 -shift < x < 640 -shift and y + 25 > hrudle_list[7] + 300:
        print("game over parameters 8:", x, y, hrudle_list)
        x, y, score, prev_time, hrudle_list, highest, shift, life, take_off, x_ini, y_ini = game_over(blank_image, x, y, highest, score, life)
        continue


    cv2.imshow("Helicopter", blank_image)
    # blank_image = hurdles(blank_image, score)

    if cv2.waitKey(1) == 27:
        break
