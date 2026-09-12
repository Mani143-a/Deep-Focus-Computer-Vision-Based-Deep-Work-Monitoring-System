# DeepFocus

## Computer Vision Based Deep-Work Monitoring System

DeepFocus is a real-time computer vision system designed to monitor a user's
work session using a camera feed and estimate attention-related states such as
focused, distracted, drowsy, sleeping, and away from the desk.

The system combines facial landmarks, eye behavior, head-pose analysis,
temporal state estimation, rule-based reasoning, machine-learning inference,
reading-context detection, adaptive focus scoring, intelligent intervention,
session analytics, and runtime health monitoring.

---

## Key Features

- Real-time face and eye monitoring
- MediaPipe Face Landmarker integration
- Eye Aspect Ratio (EAR) based eye-state analysis
- Exponential moving average smoothing
- Temporal focus-state monitoring
- Blink and eye-closure tracking
- Drowsiness and sleeping detection
- Face-loss / away detection
- Head-pose estimation
- Rule-based distraction detection
- Reading-context detection
- Reading-aware distraction protection
- Machine-learning feature extraction
- ML inference engine
- ML + rule-based prediction fusion
- Adaptive focus scoring
- Intelligent intervention logic
- Audio intervention
- Runtime orchestration
- Runtime health monitoring
- Session logging
- Session analytics
- Session history
- Productivity insights
- Streamlit dashboard
- Formal benchmark evaluation
- Robustness evaluation
- Production preflight validation
- Final demo validation

---

# System Architecture

```text
                    Camera
                      │
                      ▼
             MediaPipe Face Landmarker
                      │
                      ▼
        ┌─────────────────────────────┐
        │ Facial / Temporal Features  │
        │                             │
        │ • EAR                       │
        │ • Eye closure               │
        │ • Blink rate                │
        │ • Head yaw                  │
        │ • Head pitch                │
        │ • Head roll                 │
        │ • Face visibility            │
        └──────────────┬──────────────┘
                       │
                       ▼
              Temporal State Monitor
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Distraction Logic    Reading Context
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
              ML Feature Builder
                       │
                       ▼
                 ML Inference
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        ML Prediction       Rule Evidence
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                ML + Rule Fusion
                       │
                       ▼
               Adaptive Focus Score
                       │
                       ▼
             Intelligent Intervention
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        Audio Feedback       Dashboard
              │                 │
              └────────┬────────┘
                       ▼
               Session Analytics
                       │
                       ▼
              History / Reports