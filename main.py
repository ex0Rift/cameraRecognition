import cv2

def main():
    video_capture = cv2.VideoCapture(1)

    if not video_capture.isOpened():
        print("Could not open webcam.")
        return

    print('webcam is open')

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print('failed to grab frame.')
            break

        cv2.imshow('webcam test',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()