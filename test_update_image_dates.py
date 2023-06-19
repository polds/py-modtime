import os
import shutil
import tempfile
import unittest
from datetime import datetime
from PIL import Image
from update_image_dates import update_image_dates


class TestUpdateImageDates(unittest.TestCase):
    def setUp(self):
        # create temporary directory and files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_files = [
            "2022-01-01.jpg",
            "2022_01_02(1).jpg",
            "20220103_120000_1.jpg",
        ]
        for filename in self.temp_files:
            shutil.copyfile(
                "assets/unsplash.jpg", os.path.join(self.temp_dir.name, filename)
            )

        # check that there is a file in the temporary directory for each filename
        for filename in self.temp_files:
            if not os.path.isfile(os.path.join(self.temp_dir.name, filename)):
                raise ValueError(f"File {filename} was not created.")

    def tearDown(self):
        # delete temporary directory and files
        self.temp_dir.cleanup()

    def test_update_image_dates(self):
        # run the function on the temporary directory
        update_image_dates(os.path.abspath(self.temp_dir.name))

        # check that the modification times and EXIF data were updated correctly
        for filename in self.temp_files:
            if not os.path.isfile(os.path.join(self.temp_dir.name, filename)):
                raise ValueError(f"File {filename} was not created.")

            filepath = os.path.join(self.temp_dir.name, filename)
            img = Image.open(filepath)
            exif = img._getexif()
            if exif is None:
                raise ValueError(f"EXIF data not found in {filepath}")

            # TODO: figure out why the EXIF data is not being updated.
            print(f"Checking {filepath}")
            print(f"  EXIF data: {exif}")

            # check modification time
            mtime = os.path.getmtime(filepath)
            self.assertEqual(datetime.fromtimestamp(mtime), exif[306])

            # check EXIF data
            self.assertEqual(exif[36867], exif[36868])
            self.assertEqual(exif[36867], exif[306])
