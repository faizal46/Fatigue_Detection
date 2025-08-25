from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def mouth_aspect_ratio(mouth):
	A = distance.euclidean(mouth[13], mouth[19])  # 14-20 in 1-based indexing
	B = distance.euclidean(mouth[14], mouth[18])  # 15-19
	C = distance.euclidean(mouth[15], mouth[17])  # 16-18
	D = distance.euclidean(mouth[12], mouth[16])  # 13-17 (horizontal)
	mar = (A + B + C) / (3.0 * D)
	return mar

# EAR & MAR Thresholds and frame checks
EAR_THRESH = 0.3
EAR_CONSEC_FRAMES = 10
MAR_THRESH = 0.6  # Adjusted threshold for yawning
MAR_CONSEC_FRAMES = 15

# Initialize counters
eye_flag = 0
mouth_flag = 0


# Dlib detector and shape predictor
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("C:\\Users\\Admin\\OneDrive\\Desktop\\shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["mouth"]

# Start video stream
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
	ret, frame = cap.read()
	if not ret:
		break

	frame = imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)

	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)

		# Eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0

		# Mouth
		mouth = shape[mStart:mEnd]
		mar = mouth_aspect_ratio(mouth)

		# Print EAR and MAR
		print(f"EAR: {ear:.2f} | MAR: {mar:.2f}")

		# Draw eye and mouth contours
		cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (255, 0, 0), 1)

		# Drowsiness by eyes
		if ear < EAR_THRESH:
			eye_flag += 1
			if eye_flag >= EAR_CONSEC_FRAMES:
				cv2.putText(frame, "ALERT! Drowsiness Detected", (10, 30),
				            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		else:
			eye_flag = 0

		# Yawning detection
		if mar > MAR_THRESH:
			mouth_flag += 1
			if mouth_flag >= MAR_CONSEC_FRAMES:
				cv2.putText(frame, "YAWNING DETECTED", (10, 60),
				            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
		else:
			mouth_flag = 0

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
