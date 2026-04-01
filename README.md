# deepfake-deduction-2026

Deepfake Detection System 

 Project Overview

This project is a Deepfake Detection System that analyzes uploaded videos and predicts whether they are REAL or FAKE using a deep learning model.

The system extracts frames from videos, detects faces, and uses a trained Xception-based CNN model to classify the video.


Features

- Video upload and analysis
- Face detection using MTCNN
- Deepfake prediction using Xception model
- Admin and user login system
- Email alert for fake videos
- User activity history (Admin dashboard)
- Clean and interactive Streamlit UI



 Technologies Used

- Python
- TensorFlow / Keras
- OpenCV
- MTCNN
- Streamlit
- SQLite



 How It Works

1. User uploads a video
2. Frames are extracted from the video
3. Faces are detected using MTCNN
4. Frames are passed to the trained model
5. Model outputs probability
6. Final result displayed as REAL or FAKE



 Model Details

- Architecture: Xception CNN
- Task: Binary Classification (Real vs Fake)
- Output: Probability score



 Project Structure

- app.py → Main Streamlit app
- model_utils.py → Model loading & prediction
- video_utils.py → Frame extraction & face detection
- db.py → Database operations
- email_utils.py → Email alert system



 Security Features

- Admin login system
- Email alert for fake detection
- Secure credentials using environment variables


 Future Improvements

- Face-only model prediction
- Real-time video detection
- Higher accuracy model training
- Deployment with scalable backend



 Conclusion

This system demonstrates how deep learning can be applied to detect manipulated videos and improve digital media security.