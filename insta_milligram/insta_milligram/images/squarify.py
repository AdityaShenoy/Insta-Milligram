import django.core.files.uploadedfile as dcfu

import io

import PIL.Image as pi
import PIL.ImageFilter as pif


def squarify(img: dcfu.UploadedFile):
    orig_img = pi.open(img)  # type: ignore
    max_dim = max(orig_img.size)  # type: ignore
    canvas = pi.new("RGB", (max_dim, max_dim), color="white")  # type: ignore

    resized_img = orig_img.resize((max_dim, max_dim))  # type: ignore
    filtered_img = resized_img.filter(pif.GaussianBlur(100))  # type: ignore
    canvas.paste(filtered_img)  # type: ignore

    paste_x = (max_dim - orig_img.width) // 2
    paste_y = (max_dim - orig_img.height) // 2
    canvas.paste(orig_img, box=(paste_x, paste_y))  # type: ignore

    img_io = io.BytesIO()
    canvas.save(img_io, format="jpeg")  # type: ignore

    return dcfu.SimpleUploadedFile(img.name, img_io.getvalue())
