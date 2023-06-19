# py-modtime
Simple Python script to change exif and modtime of files in a folder.

I threw this together to work with some Google Takeout archives where it could walk through jpg's and update the modtime and exif data.

# Using

This package uses Nix and devenv, if you have devenv installed it's as simple as running `devenv shell` and then from there:

`python update_image_dates.py`

All of the dependencies are automatically managed / installed by Nix.

# Known Issues

- [ ] Exif data is being stripped

# Credits

[Mike Hindle, Unsplash](https://unsplash.com/photos/4PHsxHspavg)