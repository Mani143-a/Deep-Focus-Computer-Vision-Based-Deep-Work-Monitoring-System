import cv2

from app.camera.phone import PhoneStreamSource


STREAM_URL = "http://192.168.1.100:4747/video"


def main() -> None:
    source = PhoneStreamSource(STREAM_URL)

    print(f"Connecting to: {STREAM_URL}")

    if not source.connect():
        print("ERROR: Could not connect to DroidCam")
        return

    print("SUCCESS: DroidCam connected")

    try:
        while True:
            success, frame = source.read()

            if not success:
                print("ERROR: Failed to read frame")
                break

            cv2.imshow("DeepFocus - Phone Camera", frame)

            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        source.release()
        cv2.destroyAllWindows()
        print("Camera released")


if __name__ == "__main__":
    main()