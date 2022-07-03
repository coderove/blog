# 图片验证码生成
import random

from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO

str_all = string.digits + string.ascii_letters


# 随机颜色
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 随机验证码
def random_code(size=(200, 40), length=4, point_num=100, line_num=15):
    width, height = size
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font='static/custom/font/Viafont.ttf', size=32)
    valid_code = ''
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 10), random_char, (0, 0, 0), font=font)
        valid_code += random_char

    #  随机点
    for i in range(point_num):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), random_color())
    #  随机先线
    for i in range(line_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    # 创建一个内存句柄
    f = BytesIO()
    # 保存图片到内存
    img.save(f, 'PNG')
    # 读取
    data = f.getvalue()
    return (data, valid_code)


if __name__ == '__main__':
    random_code()
