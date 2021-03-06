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
            colour = (235, 125, 52) if is_white else (245, 231, 159)
            draw.rectangle((100 * x, 100 * y, (100 * x) + 100, (100 * y) + 100), fill=colour, outline=(255, 255, 255))

            if x == 4 and y == 0:
                white_king = Image.open('WhiteKing.png').resize((100, 100))

                im.paste(white_king, (400, 700), white_king)

            if x == 3 and y == 0:
                white_queen = Image.open('WhiteQueen.png').resize((100, 100))

                im.paste(white_queen, (300, 700), white_queen)

            if x in (2, 5) and y == 0:
                white_bishop = Image.open('WhiteBishop.png').resize((100, 100))

                im.paste(white_bishop, (100 * x, 700), white_bishop)

            if x in (1, 6) and y == 0:
                white_knight = Image.open('WhiteKnight.png').resize((100, 100))

                im.paste(white_knight, (100 * x, 700), white_knight)

            if x in (0, 7) and y == 0:
                white_rook = Image.open('WhiteRook.png').resize((100, 100))

                im.paste(white_rook, (100 * x, 700), white_rook)

            if y == 1:
                white_pawn = Image.open('WhitePawn.png').resize((100, 100))

                im.paste(white_pawn, (100 * x, 600), white_pawn)

    im.show()