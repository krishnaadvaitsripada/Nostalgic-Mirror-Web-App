# Nostalgic Mirror (UofTHacks 11)

DevPost: https://devpost.com/software/nostalgic-mirror

### Inspiration
Our inspiration originated from the aspiration to offer users a time-travel experience, enabling them to journey into their past. Recognizing the innate human inclination to cherish and revisit cherished memories, we came up with the idea of designing a magical mirror. This mirror serves as a portal to the past, inviting users to relive those precious moments in a nostalgic manner.

### What it does
A virtual mirror software with a webcam that waits for people to walk in front of it, then show them nostalgic memories of them together from their uploaded photo albums through a web app. It uses facial recognition to identify people standing in front of the mirror, then search for their faces on their uploaded albums.

### How we built it
- **Mirror:** Python, pygame, OpenCV and DeepFace libraries
- **Frontend:** Crafted using HTML, CSS, and React.js.
- **Backend:** Developed with Flask (Python).
- **Database:** Utilized MongoDB.

### Challenges we ran into
- **Facial Recognition:** Faced challenges in achieving accurate facial recognition using OpenCV, encountering low accuracy and requiring extensive troubleshooting.
- **API Endpoint Connectivity:** Encountered difficulties in connecting API endpoints within the backend.
- **Integration Complexity:** Navigated challenges in seamlessly integrating frontend, backend, and the Computer Vision aspect.

### Accomplishments that we're proud of
Successfully achieved the development of a visually appealing website, showcasing a reasonably accurate facial recognition algorithm.

### What we learned
Through collaborative efforts, we gained valuable experience in utilizing Flask, MongoDB, and integrating REST APIs, marking our initial exposure to these technologies.
