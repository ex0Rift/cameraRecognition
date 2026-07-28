import cv2
import mediapipe as mp

# initialise mediapipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def main():
    # make the video capture device
    video_capture = cv2.VideoCapture(1)
    # spit out an error if the camera cannot be found 
    if not video_capture.isOpened():
        print("Could not open webcam.")
        return
    # confirm that the camera is open if successfull
    print('webcam is open. "q" to quit')

    # setup facedetection model and confidence for facial recognition
    with mp_face_detection.FaceDetection(
        model_selection= 0 , min_detection_confidence = 0.5
    ) as face_detection:
        # mainloop
        while True:
            # get frame
            ret, frame = video_capture.read()
            # error out if no frame
            if not ret:
                print('failed to grab frame.')
                break

            #convert frame to rgb for mediapipe
            frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result = face_detection.process(frame_rgb)

            # if any faces are seen draw the detection to the frame
            if result.detections:
                for detection in result.detections:
                    mp_drawing.draw_detection(frame, detection)

            # show the webcam
            cv2.imshow('webcam test',frame)

            #check for key press ' q ' if so break mainloop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # release and destroy windows after quitting 
    video_capture.release()
    cv2.destroyAllWindows()

# startpoint
if __name__ == "__main__":
    main()