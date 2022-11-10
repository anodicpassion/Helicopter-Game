import cv2


class Graphics:
    def draw_rect(self, pt1, pt2, text=None, font=cv2.FONT_ITALIC, rect=True, rect_color=(0, 255, 0), rect_thickness=2,
                  line=False, line_color=(0, 0, 255), line_thickness=5):
        if rect:
            cv2.rectangle(self, pt1, pt2, rect_color, rect_thickness)
        # cv2.GaussianBlur(img, (5, 5), 15)
        diagonal = (pt2[0] - pt1[0], pt2[1] - pt1[1])[0]
        if text is not None:
            cv2.rectangle(self, (pt1[0], pt2[1]), (pt2[0], pt2[1] + 50), rect_color, cv2.FILLED)
            cv2.putText(self, text, (pt1[0] + 20, pt2[1] + 35), font, 1, (255, 255, 255), 2)

        # print("diagonal length ", diagonal)

        point1 = pt1
        point2 = (pt2[0], pt1[1])
        point3 = pt2
        point4 = (pt1[0], pt2[1])

        dist_pt1_pt2 = point2[0] - point1[0]
        dist_pt1_pt4 = point4[1] - point1[1]

        if line:
            cv2.line(self, point1, (int(point1[0] + dist_pt1_pt2 * 0.25), point2[1]), line_color,
                     line_thickness)  # point1 to right
            cv2.line(self, point1, (point4[0], int(point1[1] + dist_pt1_pt4 * 0.25)), line_color,
                     line_thickness)  # point1 to bottom

            cv2.line(self, point2, (int(point2[0] - dist_pt1_pt2 * 0.25), point2[1]), line_color,
                     line_thickness)  # point2 to left
            cv2.line(self, point2, (point2[0], int(point2[1] + dist_pt1_pt4 * 0.25)), line_color,
                     line_thickness)  # point2 to bottom

            cv2.line(self, point3, (int(point3[0] - dist_pt1_pt2 * 0.25), point3[1]), line_color,
                     line_thickness)  # point3 to left
            cv2.line(self, point3, (point3[0], int(point3[1] - dist_pt1_pt4 * 0.25)), line_color,
                     line_thickness)  # point3 to top

            cv2.line(self, point4, (int(point4[0] + dist_pt1_pt2 * 0.25), point4[1]), line_color,
                     line_thickness)  # point4 to right
            cv2.line(self, point4, (point4[0], int(point4[1] - dist_pt1_pt4 * 0.25)), line_color,
                     line_thickness)  # point4 to top

        return self
