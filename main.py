"""
@author: Pratik Suhas Pawar
"""
import time
import image_processor
import cv2
import numpy as np
from mediapipe import solutions

# initializing the parameters
helicopter_blade = [(160, 160, 160), (64, 64, 64), (255, 255, 255), (10, 10, 10), (32, 32, 32)]
cam_index = 1
x, y = 150, 365
x_ini, y_ini = 150, 365
score = 20
shift_ = 0
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
hurdle_list = [100, 100, 100, 100, 100, 100, 100, 100, 100]
hand = solutions.hands.Hands()
prev_time = 0

# loading previous score
with open("score_", "r") as r:
    highest = r.read()
    r.close()


# drawing hurdles
def hurdles(image, hurdle_lst: list, shift_t: int, color=()) -> list:
    for ind, i in enumerate(hurdle_lst):
        cv2.rectangle(image, (ind * 80 - shift_t, 0), ((ind * 80) + 80 - shift_t, i), color, -1)  # rgb(115, 60, 60)
        cv2.rectangle(image, (ind * 80 - shift_t, i + 300), ((ind * 80) + 80 - shift_t, 480), color, -1)
    return image


# drawing helicopter
def helicopter(image, x_: int, y_: int) -> list:
    cv2.line(image, (x_, y_), (x_ - 25, y_ + 35), (40, 40, 40), 2)
    cv2.line(image, (x_, y_), (x_ + 25, y_ + 35), (40, 40, 40), 2)
    cv2.line(image, (x_ - 35, y_ + 35), (x_ + 35, y_ + 35), (40, 40, 40), 2)
    cv2.line(image, (x_ + 35, y_ + 35), (x_ + 40, y_ + 30), (40, 40, 40), 2)
    cv2.line(image, (x_, y_ - 10), (x_ - 100, y_ - 10), (68, 86, 223), 8)
    cv2.line(image, (x_ - 100, y_ - 25), (x_ - 100, y_ + 2), (213, 209, 204), 5)
    cv2.line(image, (x_, y_), (x_, y_ - 35), (213, 209, 204), 10)
    cv2.line(image, (x_ - 70, y_ - 40), (x_ + 70, y_ - 40),
             helicopter_blade[np.random.randint(0, len(helicopter_blade))], 3)
    cv2.line(image, (x_ - 120, y_ - 28), (x_ - 80, y_ - 28),
             helicopter_blade[np.random.randint(0, len(helicopter_blade))], 2)
    cv2.ellipse(image, (x_, y_), (50, 25), 0, 0, 360, (68, 86, 223), -1)
    cv2.rectangle(image, (x_ - 50, y_), (x_, y_ - 25), (68, 86, 223), -1)
    # cv2.line(img, (x, y - 24), (x, y), (93, 79, 51), 3)  # rgb(223, 223, 222)
    # cv2.line(img, (x, y), (x + 50, y), (93, 79, 51), 3)
    cv2.ellipse(image, (x_ + 23, y_ - 8), (10, 20), -70, 0, 360, (93, 79, 51), -1)
    cv2.rectangle(image, (x_ + 4, y_ - 10), (x_ + 32, y_ + 4), (93, 79, 51), -1)

    # cv2.circle(img, (x+5, y), 10, (93, 79, 51), -1)

    return image


# defining last stage of game
def game_over(image: list, x: int, y: int, highest_score: int, curr_score: int, life_: int) -> tuple:
    w = x + 80
    h = y + 55
    x = x - 130
    y = y - 60
    image = image_processor.Graphics.draw_rect(image, (x, y), (w, h), rect=False, line=True, line_thickness=2)

    cv2.imshow("Helicopter", image)
    cv2.waitKey(1000)
    if life_ > 0:
        life_ = life_ - 1
        return 320, 240, curr_score, 0, [100, 100, 100, 100, 100, 100, 100, 100,
                                         100], highest_score, 0, life_, 0, 150, 365
    if int(curr_score) > int(highest_score):
        highest_score = int(curr_score)
        with open("score_", "w") as w:
            w.write(str(highest_score))
            w.close()
    cv2.putText(image, "Game Over", (110, 120), cv2.FONT_ITALIC, 2.5, (255, 255, 255), 3)
    cv2.putText(image, "Better luck next time...!", (135, 200), cv2.FONT_ITALIC, 1, (0, 0, 255), 1)

    cv2.putText(image, "Escape 2 Exit | Enter 2 Play Again", (40, 240), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
    cv2.imshow("Helicopter", image)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        cam.release()
        exit()
    if cv2.waitKey(0) == 13:
        with open("score_", "r") as r:
            highest_score = r.read()
            r.close()
        x, y, score, prev_time, hrudle_list, shift, life_, take_off, x_ini, y_ini = 320, 240, 0, 0, [100, 100, 100, 100,
                                                                                                     100, 100, 100, 100,
                                                                                                     100], 0, 3, 0, 150, 365
        return x, y, score, prev_time, hrudle_list, int(highest_score), shift, life_, take_off, x_ini, y_ini


# main driver code
def main() -> None:
    global prev_time, score, hurdle_list, shift_, take_off, highest, life, x_ini, y_ini, x, y, blank_image
    blank_img = blank_image
    while True:
        _, img = cam.read()
        img = cv2.flip(img, 1)
        # img = cv2.resize(img, dsize=None, fx=640, fy=480)
        if time.time() - prev_time > 1 and x > 400 and score < 10:
            curve = hurdle_list[-1] + np.random.randint(-100, 100)
            if curve < -200:
                continue
            if curve > 300:
                continue
            hurdle_list.pop(0)
            hurdle_list.insert(8, curve)
            prev_time = time.time()
            shift_ = 0
            # co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)

        if time.time() - prev_time > 0.5 and x > 400 and 20 > score > 10:
            curve = hurdle_list[-1] + np.random.randint(-100, 100)
            if curve < -200:
                continue
            if curve > 300:
                continue
            hurdle_list.pop(0)
            hurdle_list.insert(8, curve)
            prev_time = time.time()
            shift_ = 0
            # co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)

        if time.time() - prev_time > 0.3 and x > 400 and 60 > score > 20:

            curve = hurdle_list[-1] + np.random.randint(-100, 100)
            if curve < -200:
                continue
            if curve > 300:
                continue
            hurdle_list.pop(0)
            hurdle_list.insert(8, curve)
            prev_time = time.time()
            shift_ = 0
            # co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)

        if time.time() - prev_time > 0.2 and x > 400 and 100 > score > 60:

            curve = hurdle_list[-1] + np.random.randint(-180, 180)
            if curve < -200:
                continue
            if curve > 300:
                continue
            hurdle_list.pop(0)
            hurdle_list.insert(8, curve)
            prev_time = time.time()
            shift_ = 0
            # co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)

        if time.time() - prev_time > 0.1 and x > 400 and 200 > score > 100:

            curve = hurdle_list[-1] + np.random.randint(-180, 180)
            if curve < -200:
                continue
            if curve > 300:
                continue
            hurdle_list.pop(0)
            hurdle_list.insert(8, curve)
            prev_time = time.time()
            shift_ = 0
            # co_shift = int(((1 - (score / 50)) - (time.time() - prev_time)) * 10)

        # print(int(((1 - (score / 50)) - (time.time() - prev_time))*10))
        if x > 400:
            if 0 < score < 10:
                shift_ = shift_ + 7
            elif 10 < score < 20:
                shift_ = shift_ + 11
            elif 20 < score < 60:
                shift_ = shift_ + 13
            elif 60 < score < 100:
                shift_ = shift_ + 15
            elif 100 < score < 200:
                shift_ = shift_ + 20
            score = score + 0.1
        # print(hrudle_list)
        # blank_image[:] = 191, 0, 249
        # blank_img = []
        if score < 50:
            blank_img[:] = img
        else:
            blank_img[:] = background
        if score > 50:
            blank_img = hurdles(blank_img, hurdle_list, shift_, (115, 88, 87))
        else:
            blank_img = hurdles(blank_img, hurdle_list, shift_, (60, 50, 50))
        # blank_image[0:50, :] = 49, 7, 0
        header = "Score: " + str(int(score)) + " | " + str(highest) + "                        " + "Life: " + str(
            life) + " | " + "3"
        cv2.putText(blank_img, header, (10, 34), cv2.FONT_ITALIC, 0.8, (200, 200, 200), 1)
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

        blank_img = helicopter(blank_img, x, y)

        if 0 - shift_ < x < 80 - shift_ and y - 35 < hurdle_list[0]:
            print("game over parameters 1:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 0 - shift_ < x < 80 - shift_ and y + 25 > hurdle_list[0] + 300:
            print("game over parameters 9:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 80 - shift_ < x < 160 - shift_ and y - 35 < hurdle_list[1]:
            print("game over parameters 2:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 80 - shift_ < x < 160 - shift_ and y + 25 > hurdle_list[1] + 300:
            print("game over parameters 10:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 160 - shift_ < x < 240 - shift_ and y - 35 < hurdle_list[2]:
            print("game over parameters 3:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 160 - shift_ < x < 240 - shift_ and y + 25 > hurdle_list[2] + 300:
            print("game over parameters 11:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 240 - shift_ < x < 320 - shift_ and y - 35 < hurdle_list[3]:
            print("game over parameters 4:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 240 - shift_ < x < 320 - shift_ and y + 25 > hurdle_list[3] + 300:
            print("game over parameters 12:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 320 - shift_ < x < 400 - shift_ and y - 35 < hurdle_list[4]:
            print("game over parameters 5:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 320 - shift_ < x < 400 - shift_ and y + 25 > hurdle_list[4] + 300:
            print("game over parameters 6:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 400 - shift_ < x < 480 - shift_ and y - 35 < hurdle_list[5]:
            print("game over parameters 7:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 400 - shift_ < x < 480 - shift_ and y + 25 > hurdle_list[5] + 300:
            print("game over parameters 8:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 480 - shift_ < x < 560 - shift_ and y - 35 < hurdle_list[6]:
            print("game over parameters 7:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 480 - shift_ < x < 560 - shift_ and y + 25 > hurdle_list[6] + 300:
            print("game over parameters 8:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 560 - shift_ < x < 640 - shift_ and y - 35 < hurdle_list[7]:
            print("game over parameters 7:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue
        if 560 - shift_ < x < 640 - shift_ and y + 25 > hurdle_list[7] + 300:
            print("game over parameters 8:", x, y, hurdle_list)
            x, y, score, prev_time, hurdle_list, highest, shift_, life, take_off, x_ini, y_ini = game_over(blank_img,
                                                                                                           x, y,
                                                                                                           highest,
                                                                                                           score,
                                                                                                           life)
            continue

        cv2.imshow("Helicopter", blank_img)
        # blank_image = hurdles(blank_image, score)

        if cv2.waitKey(1) == 27:
            break


if __name__ == "__main__":
    main()
