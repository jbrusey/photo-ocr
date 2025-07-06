import cv2
import pytesseract
import re
import csv
from pathlib import Path

downloads = Path("~/Downloads").expanduser()
output_csv = downloads / "server_paths.csv"

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["server_path"])

    for file in downloads.glob("IMG_*"):
        img = cv2.imread(str(file))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(thresh)

        for line in text.splitlines():
            if "Server path:" in line:
                m = re.search(r"Server path:\s*(.*)", line)
                if m:
                    server_path = m.group(1).strip()
                    print(f"Found: {server_path}")
                    writer.writerow([server_path])
