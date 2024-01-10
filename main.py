import imutils
import cv2

redLower = (0, 84, 50)
redUpper = (131, 255, 255)

camera = cv2.VideoCapture(0)

prev_direction = None

while True:
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if cnts:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            epsilon = 0.04 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            vertices = len(approx)

            if prev_direction is not None:
                print("Stop")

            if prev_direction is None:
                print("Center")
            else:
                # Compare current and previous positions to determine direction
                dx = center[0] - prev_center[0]
                dy = center[1] - prev_center[1]

                if abs(dx) > abs(dy):
                    if dx > 0:
                        print("Right")
                    else:
                        print("Left")
                else:
                    if dy > 0:
                        print("Down")
                    else:
                        print("Up")

        # Update previous center and direction
        prev_center = center
        prev_direction = None if vertices == 4 else "Up"  # Assuming the object is square

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
