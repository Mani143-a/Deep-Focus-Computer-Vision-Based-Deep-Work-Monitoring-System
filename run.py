import argparse
import logging
import sys

from app.camera import (
    PhoneStreamSource,
    VideoFileSource,
    WebcamSource,
)
from app.camera.base import VideoSource
from app.main import DeepFocusApp


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def build_source(args: argparse.Namespace) -> VideoSource:
    if args.source == "webcam":
        return WebcamSource(
            camera_index=args.camera_index,
            width=args.width,
            height=args.height,
        )

    if args.source == "phone":
        if not args.url:
            raise ValueError(
                "--url is required when using --source phone"
            )

        return PhoneStreamSource(args.url)

    if args.source == "video":
        if not args.file:
            raise ValueError(
                "--file is required when using --source video"
            )

        return VideoFileSource(args.file)

    raise ValueError(f"Unsupported source: {args.source}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DeepFocus Stage 1 video pipeline"
    )

    parser.add_argument(
        "--source",
        choices=["webcam", "phone", "video"],
        default="webcam",
        help="Video source.",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Webcam device index.",
    )

    parser.add_argument(
        "--url",
        type=str,
        help="Phone MJPEG/HTTP stream URL.",
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to video file.",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Requested webcam width.",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Requested webcam height.",
    )

    return parser.parse_args()


def main() -> int:
    configure_logging()

    try:
        args = parse_args()
        source = build_source(args)

        app = DeepFocusApp(source)
        app.run()

        return 0

    except KeyboardInterrupt:
        logging.info("Interrupted by user.")
        return 0

    except Exception as exc:
        logging.exception("DeepFocus failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())