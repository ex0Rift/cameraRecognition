import cv2
import mediapipe as mp

#
# initialise mediapipe
#
# face detection
mp_face_detection = mp.solutions.face_detection
# hand detection
mp_hands = mp.solutions.hands
# for drawing to the webcam
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# different modes of detection
# 0: facial , 1: hands
mode = 1

def main():
    # make the video capture device
    video_capture = cv2.VideoCapture(1)
    # spit out an error if the camera cannot be found 
    if not video_capture.isOpened():
        print("Could not open webcam.")
        return
    # confirm that the camera is open if successfull
    print('webcam is open. "q" to quit')

    # set up the detecting model depending on the mode
    match mode:
        case 0:
            detector = mp_face_detection.FaceDetection( model_selection= 0 , min_detection_confidence = 0.5)
        case 1:
            detector = mp_hands.Hands(model_complexity = 0 , max_num_hands = 2 , min_detection_confidence = 0.5 , min_tracking_confidence = 0.5)

    # mainloop
    with detector:
        while True:
            # get frame
            ret, frame = video_capture.read()
            # error out if no frame
            if not ret:
                print('failed to grab frame.')
                break

            #convert frame to rgb for mediapipe
            frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result = detector.process(frame_rgb)

            # draw according to which detection mode needing specific drawing requirments
            match mode:
                case 0:# if any faces are seen draw the detection to the frame
                    if result.detections:
                        for detection in result.detections:
                            mp_drawing.draw_detection(frame, detection)
                case 1:# if any hands are seen draw the detection to the frame
                    if result.multi_hand_landmarks:
                        for hand_landmarks in result.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())

            #logic

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