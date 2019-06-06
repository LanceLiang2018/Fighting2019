from PIL import Image, ImageDraw, ImageFont
import numpy as np


def load_img():
    return Image.open('im.jpg')  # .resize((1024, 1024))


def add_text(im: Image):
    size = 360
    # font = ImageFont.truetype('NotoSansCJK-Thin', size=size)
    font = ImageFont.truetype('MSYHMONO', size=size)
    draw = ImageDraw.Draw(im)
    # 居中显示
    rect = draw.textsize(font=font, text='高考')
    pos = [(im.size[0] - rect[0]) // 2, (im.size[1] - rect[1] * 2) // 2]
    # print(rect)
    draw.text((pos[0], pos[1]), font=font, text='高考')
    draw.text((pos[0], pos[1] + size), font=font, text='必胜')
    font2 = ImageFont.truetype('font.ttf', size=size//2)
    rect2 = draw.textsize(font=font2, text='2019')
    draw.text(((im.size[0] - rect2[0]) // 2, pos[1] - rect2[1] - 32), font=font2, text='2019')
    font3 = ImageFont.truetype('MSYHMONO', size=size//2)
    rect2 = draw.textsize(font=font3, text='玉武加油')
    draw.text(((im.size[0] - rect2[0]) // 2, pos[1] + 2 * rect2[1] + size), font=font3, text='玉武加油')


def to_hex(im: Image):
    im2 = im.copy()  # 变暗的图像
    im2.point(lambda i: i // 2)
    # im2.show()
    im3 = im.copy()  # 变亮的图像
    im3.point(lambda i: max(int(i * 2.6), 255))
    # im3.show()
    size = 1024 // 32
    draw = ImageDraw.Draw(im2)
    font = ImageFont.truetype('font.ttf', size=size)
    rect = draw.textsize(font=font, text='FF')
    gray = im3.convert("L")
    print('字体', rect)
    for y in range(0, 1024, rect[1]):
        for x in range(0, 1024, rect[0]):
            crop_g = gray.crop((x, y, x + rect[0], y + rect[1]))

            crop3s = im3.crop((x, y, x + rect[0], y + rect[1])).split()
            # data3 = np.array(crop3s)
            data3 = []
            for s in crop3s:
                data3.append(np.array(s))
            val3 = []
            for d in range(3):
                val3.append(int(data3[d].sum() // data3[d].size))
            # val3 = [B, G, R]
            # val3 = list(map(lambda i: 255 - i, val3))

            data = np.array(crop_g)
            val = int(data.sum() // data.size)
            # draw.ink = val3[0] + val3[1] * 1 >> 8 + val3[2] * 1 >> 16
            draw.text((x, y), font=font, text='%02X' % val,
                      fill=int('%02X%02X%02X' % (val3[2], val3[1], val3[0]), 16))

    im.paste(im2)


if __name__ == '__main__':
    image = load_img()
    add_text(image)
    to_hex(image)
    add_text(image)
    # image.show()
    image.save('result.jpg')
