from flask import Flask, render_template, request
import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw
from qrcode.image.pil import PilImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form['url']
    logo = request.form['logo']

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)

    qr_eyes_img = qr.make_image(image_factory=StyledPilImage, eye_drawer=RoundedModuleDrawer(radius_ratio=1.2),
                                color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(216, 170, 0)))
    qr_img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                           color_mask=SolidFillColorMask(front_color=(46, 8, 5)), embeded_image_path=logo)

    def style_eyes(img):
        img_size = img.size[0]
        eye_size = 70 #default
        quiet_zone = 40 #default
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((40, 40, 110, 110), fill=255)
        draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255)
        draw.rectangle((40, img_size-110, 110, img_size-40), fill=255)
        draw.rectangle((img_size-110, img_size-110, img_size-40, img_size-40), fill=255)
        return mask

    mask = style_eyes(qr_img)
    final_img = Image.composite(qr_eyes_img, qr_img, mask)
    final_img.save('static/QR.png')

    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
