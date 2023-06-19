import os
import re
import sys
from datetime import datetime
from PIL import Image, ExifTags
from piexif import dump
import time

# pattern to match the three formats:
# 1. YYYY-MM-DD.jpg
# 2. YYYY_MM_DD(int).jpg
# 3. YYYYMMDD_HHMMSS_int.jpg
pattern = re.compile(
    r"(?P<year>\d{4})(?:[-_](?P<month>\d{2})[-_](?P<day>\d{2})|(?P<monthday>\d{4}))?(?:\((?P<count>\d+)\))?(_(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})_)?"
)


def update_image_dates(dir_path):
    if dir_path is None:
        print("No directory path provided.")
        sys.exit(1)

    # check if the path is a directory
    if not os.path.isdir(dir_path):
        print(f"Path {dir_path} is not a directory.")
        sys.exit(1)

    for filename in os.listdir(dir_path):
        path = os.path.join(dir_path, filename)
        if not os.path.isfile(path):
            print(f"Skipping {path} because it is not a file.")
            continue
        if path.endswith(".jpg"):
            update_image_date(path)


def update_image_date(filepath):
    match = pattern.search(os.path.basename(filepath))
    if match:
        (
            year,
            month,
            day,
            monthday,
            unknown1,
            unknown2,
            hour,
            minute,
            second,
            *extra,
        ) = match.groups()

        if len(extra) > 3:
            raise ValueError(f"Too many values in match.groups(): {extra}")

        if monthday is not None:
            month, day = monthday[:2], monthday[2:]

        if hour is None:
            hour = minute = second = "00"

        # create datetime object
        dt = datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )

        # open image
        img = Image.open(filepath)
        exif_dict = img._getexif()
        if exif_dict is not None:
            for tag, value in img._getexif().items():
                if tag in ExifTags.TAGS:
                    exif_dict[ExifTags.TAGS[tag]] = exif_dict.pop(tag)
        else:
            exif_dict = {}

        # update EXIF data
        dt = datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )
        fmtd = dt.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict["DateTimeOriginal"] = fmtd
        exif_dict["DateTimeDigitized"] = fmtd
        exif_dict["DateTime"] = fmtd

        print(
            f"Updating {filepath} to {year}-{month}-{day} {hour}:{minute}:{second} with EXIF data {exif_dict}"
        )

        # prepare EXIF data
        exif_bytes = dump(exif_dict)

        # save image with new EXIF data
        img.save(filepath, "jpeg", exif=exif_bytes)

        # change file modification time
        os.utime(filepath, (dt.timestamp(), dt.timestamp()))


if __name__ == "__main__":
    dir_path = input("Enter the directory path (eg. ~/Pictures): ")
    update_image_dates(dir_path)
