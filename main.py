import cv2 , math
import mediapipe as mp

# create vector class for objects using x and y
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# initialise mediapipe
#
# face detection
mp_face_detection = mp.solutions.face_detection
# hand detection
mp_hands = mp.solutions.hands
# for drawing to the webcam
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#
# different modes of detection
# 0: facial , 1: hands
mode = 1

frameFail = False
camera = -1
ball = Vector(0,0)
force = Vector(20,20)
line_collision_cooldown = 10

def main():
    global camera , frameFail , ball , force , line_collision_cooldown
    #loops a total of 4 times to try 4 different camera options and tries to open them
    for i in range (0,4):
        # make the video capture device
        video_capture = cv2.VideoCapture(i)
        if video_capture.isOpened():
            # in case of frame failiour prevent opening the same camera twice
            if i != camera:
                # confirm that the camera is open if successfull
                print('webcam is open. "q" to quit')
                camera = i
                break
        else:
            # spit out an error if the camera cannot be found 
            print('camera not found, trying again...')
    if not video_capture.isOpened():
        #no camera could be found, quit
        print('No useable cameras! quitting...')
        return
    
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
                print('failed to grab frame. Trying a new camera...')
                frameFail = True
                break
            #flip the frame so it is more natural to look at
            frame = cv2.flip(frame,1)
            #convert frame to rgb for mediapipe
            frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result = detector.process(frame_rgb)

            # get frame dimentions for normalisation
            h , w , _ = frame.shape

            #logic for hands
            if mode == 1:
                if result.multi_hand_landmarks:
                    # only work if there are two or more hands on display
                    if len(result.multi_hand_landmarks) >= 2:
                        # get tip of each index finger
                        one_index = result.multi_hand_landmarks[0].landmark[8]
                        two_index = result.multi_hand_landmarks[1].landmark[8]
                        # normalise the coordinates to the screen
                        one_index_n = Vector(int(one_index.x * w), int(one_index.y * h))
                        two_index_n = Vector(int(two_index.x * w), int(two_index.y * h))
            #
            # logic for the ball
            #
            #move the ball by force
            ball.x += force.x
            ball.y += force.y
            #collisions with screen sides
            if ball.y >= h or ball.y <= 0:
                force.y = -force.y
            if ball.x >= w or ball.x <= 0:
                force.x = -force.x
            #Collision between the line drawn from index fingers and ball
            # line collision has a cooldown becuase the line moves alot from user movement
            if line_collision_cooldown == 0:
                #reset the cooldown
                line_collision_cooldown = 10
                # if hands exist
                if result.multi_hand_landmarks:
                    # only work if there are two or more hands on display
                    if len(result.multi_hand_landmarks) >= 2:
                        # calculate the individual distances and length
                        dx , dy = two_index_n.x - one_index_n.x , two_index_n.y - one_index_n.y
                        length_sq = dx**2 + dy**2
                        # project onto a line clamped by the segment to find the cloesest point to the ball
                        t = max(0, min(1, ((ball.x - one_index_n.x) * dx + (ball.y - one_index_n.y) * dy) / length_sq))
                        #get the cloesest point on the line from the ball
                        closest_x = one_index_n.x + t * dx
                        closest_y = one_index_n.y + t * dy
                        # calcualte the distace of the ball from the closest point on the line
                        distance = math.hypot(ball.x - closest_x, ball.y - closest_y)
                        # if the distance is shorter than minimum distance it counts as a hit
                        if (distance <= 25):
                            #This code only runs if the ball "hits" the line
                            if abs(two_index_n.y - one_index_n.y) < 100:
                                force.y = -force.y
                            elif abs(two_index_n.x - one_index_n.x) < 100:
                                force.x = -force.x
                            else:
                                force.y = -force.y
                                force.x = -force.x
            else:
                #itterate the cooldown
                line_collision_cooldown -= line_collision_cooldown
            #DRAWING
            #
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
                        # only does these drawings if both hands are detected
                        if len(result.multi_hand_landmarks) >= 2:
                            # draws the line between index fingers
                            cv2.line(frame, (one_index_n.x,one_index_n.y),(two_index_n.x,two_index_n.y),(255,0,0),2)
                        else:
                            # tell user both hands need to be on the screen
                            cv2.putText(frame,"Show BOTH Hands!",(10,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),3)
                    else:
                        # tell the user to show their hands
                        cv2.putText(frame,"Show Hands!",(10,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),3)
            # always tell the user that q can be pressed to quit the program
            cv2.putText(frame,"Press Q to quit",(w-260,h-25),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
            # draw the ball to the screen
            cv2.circle(frame,(ball.x,ball.y),40,(255,255,0),-1)

            # show the webcam
            cv2.imshow('webcam test',frame)

            #check for key press ' q ' if so break mainloop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    #if program quit because of frame error try another camera
    if frameFail:
        frameFail = False
        main()
    # release and destroy windows after quitting 
    video_capture.release()
    cv2.destroyAllWindows()

# startpoint
if __name__ == "__main__":
    main()