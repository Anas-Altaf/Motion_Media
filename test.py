import cv2
import face_recognition

# Load the reference image and compute the embedding
ref_image = face_recognition.load_image_file("path_to_reference.jpg")
ref_embedding = face_recognition.face_encodings(ref_image)[0]

# Load the target image and find all faces
target_image = face_recognition.load_image_file("path_to_target.jpg")
face_locations = face_recognition.face_locations(target_image)
face_encodings = face_recognition.face_encodings(target_image, face_locations)

# Loop through detected faces and compare
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # Compute cosine similarity or use face_recognition.api.compare_faces
    matches = face_recognition.compare_faces([ref_embedding], face_encoding, tolerance=0.5)
    if matches[0]:
        # Draw a circle around the face (center and radius computed from bounding box)
        center = (int((left + right) / 2), int((top + bottom) / 2))
        radius = int((right - left) / 2)
        cv2.circle(target_image, center, radius, (0, 255, 0), 2)

# Save or display the result
cv2.imwrite("result.jpg", cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR))