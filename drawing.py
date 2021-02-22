from PIL import Image, ImageDraw


def draw_square(is_white):
    im = Image.new('RGB', (500, 300), (128, 128, 128))
    draw = ImageDraw.Draw(im)

    colour = "white" if is_white else "black"
    draw.rectangle((200, 100, 300, 200), fill=colour, outline=(255, 255, 255))

    # write to stdout
    im.show()


def draw_board():
    im = Image.new('RGB', (900, 900), (128, 128, 128))
    draw = ImageDraw.Draw(im)

    for y in range(7, -1, -1):
        for x in range(0, 8):
            is_white = ((x + y) % 2 == 0)
            colour = "white" if is_white else "black"
            draw.rectangle((100 * x, 100 * y, (100 * x) + 100, (100 * y) + 100), fill=colour, outline=(255, 255, 255))

    im.show()