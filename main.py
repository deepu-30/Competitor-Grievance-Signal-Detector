import argparse
from signals.competitor_grievance import run_detector
from utils.output import save_json, save_sqlite

def main():
    parser = argparse.ArgumentParser(
        description="Competitor Grievance Signal Detector"
    )
    parser.add_argument(
        "--output",
        choices=["json", "sqlite", "both"],
        default="json",
        help="Output format (default: json)"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("  Competitor Grievance Signal Detector")
    print("=" * 50)

    signals = run_detector()

    print(f"\n📊 Total signals detected: {len(signals)}")

    if args.output in ("json", "both"):
        save_json(signals)
    if args.output in ("sqlite", "both"):
        save_sqlite(signals)

    print("\nDone! Check the /outputs folder.")

if __name__ == "__main__":
    main()