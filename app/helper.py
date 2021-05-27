from app import jdatetime
from datetime import datetime
import imghdr
from PIL import Image, ExifTags


def convertGregorianToJalali(dateTime: datetime):
    if dateTime is not None:
        jalaliDate = jdatetime.date.fromgregorian(date=dateTime)
        return jalaliDate
    else:
        return


def covertJalaliToGeregorain(date, time):
    if date is not '' and time is not None:
        splitted = date.split('/')
        j = jdatetime.datetime(int(splitted[0]), int(splitted[1]), int(splitted[2]))
        date = jdatetime.date.togregorian(j)
        dbDateTime = datetime(date.year, date.month, date.day, time.hour, time.minute)
        return dbDateTime
    else:
        return


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def resizePic(filename):
    try:
        image = Image.open(filename)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation': break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

        # image.save(filename)
        new_image = image.resize((1080, 1920))
        new_image.save(filename)
        print(image.size)  # Output: (1920, 1280)
        print(new_image.size)  # Output: (400, 400)

    except:
        print('resize error')
