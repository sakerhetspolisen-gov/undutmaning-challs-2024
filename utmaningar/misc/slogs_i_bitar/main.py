#!/bin/env python3
from PIL import Image
from random import randint, random, seed

DEBUG_MODE = 0

# Hints:
# 1. Den gick i tusen bitar
# 2. röfrav edappat ud nim akurk?      -> ASCII encoded bytes are reversed (LSB it always 0 for flag text)

mask_img = 'bunny-ascii.png'  # 'stanford bunny white.png'  # 'bunny-ascii.png'
visible_img = 'pot.png'
BRIGHTNESS_THREASHOLD = 215  # 255 // 2 # 0 - 255
SCALE = 0.5  # 0.7
MASK_ERROR = 0.15  # 0.1
VISIBLE_ERROR = 0.4
RND_SEED = 532130
FLAG = "undut{Th3_La5t_b1t_W4s_7ricky_t0_f1Nd}"
EXTRA_CHALL = "ICAgICAvIFwKICAgIC8gXyBcCiAgIHwgLyBcIHwKICAgfHwgICB8fCBfX19fX19fCiAgIHx8ICAgfHwgfFwgICAgIFwKICAgfHwgICB8fCB8fFwgICAgIFwKICAgfHwgICB8fCB8fCBcICAgIHwKICAgfHwgICB8fCB8fCAgXF9fLwogICB8fCAgIHx8IHx8ICAgfHwKICAgIFxcXy8gXF8vIFxfLy8KICAgLyAgIF8gICAgIF8gICBcCiAgLyAgICAgICAgICAgICAgIFwKICB8ICAgIE8gICAgIE8gICAgfAogIHwgICBcICBfX18gIC8gICB8CiAvICAgICBcIFxfLyAvICAgICBcCi8gIC0tLS0tICB8ICAtLS0tLSAgXAp8ICAgICBcX18vfFxfXy8gICAgIHwKXCAgICAgICB8X3xffCAgICAgICAvCiBcX19fX18gICAgICAgX19fX18vCiAgICAgICBcICAgICAvCiAgICAgICB8ICAgICB8CgpLb20gdGlsbCBldmVudGV0IHDlIEhpc3Rvcmlza2EgTXVzZWV0IGkgQXByaWwKb2NoIGJlcuR0dGEgb20gZGluIHVuZC11cHBsZXZlbHNlIGb2ciBvc3MhClJlZ2lzdHJlcmEgZGlnIHDlOiBodHRwczovL3VuZHV0bWFuaW5nLnNlLw=="
# "ICAgICAvIFwKICAgIC8gXyBcCiAgIHwgLyBcIHwKICAgfHwgICB8fCBfX19fX19fCiAgIHx8ICAgfHwgfFwgICAgIFwKICAgfHwgICB8fCB8fFwgICAgIFwKICAgfHwgICB8fCB8fCBcICAgIHwKICAgfHwgICB8fCB8fCAgXF9fLwogICB8fCAgIHx8IHx8ICAgfHwKICAgIFxcXy8gXF8vIFxfLy8KICAgLyAgIF8gICAgIF8gICBcCiAgLyAgICAgICAgICAgICAgIFwKICB8ICAgIE8gICAgIE8gICAgfAogIHwgICBcICBfX18gIC8gICB8CiAvICAgICBcIFxfLyAvICAgICBcCi8gIC0tLS0tICB8ICAtLS0tLSAgXAp8ICAgICBcX18vfFxfXy8gICAgIHwKXCAgICAgICB8X3xffCAgICAgICAvCiBcX19fX18gICAgICAgX19fX18vCiAgICAgICBcICAgICAvCiAgICAgICB8ICAgICB8CgpLb20gdGlsbCBldmVudGV0IHDlIEFybeltdXNlZXQgaSBBcHJpbApvY2ggYmVy5HR0YSBvbSBkaW4gdXBwbGV2ZWxzZSBm9nIgb3NzIQpSZWdpc3RyZXJhIGRpZyBo5HI6IGh0dHBzOi8vdW5kdXRtYW5pbmcuc2Uv"
FLAG_TEXT = f"""Henrietta and Gerald had ran in circles for hours trying to pick up all the tiny
little pieces from the ground. "I'm sorry, I'm so sorry", cried Gerald as he
frantically searched the grass, "I didn't mean to break it". As the sun slowly
began to set, Henrietta took a last look under the table.
"Here it is!" she blurted out. This is such a nice suprise,
we didn't have to be so fright, the last bit was hidden in plain sight,
almost like playing tag, here's your flag:

    {FLAG}

Gerald helped Henrietta glue and put the pot together again the next morning.
After they matched up all pieces, some alpha numerical symbols emerged
wrapping around the clay pot.

     (################################)
     /                                \\
    /__________________________________\\
   |     _________________________      |
   |    /                         \\     |
   |   (  To Harald, from Mommy<3  )    |
   |    \\_________________________/     |
   |                                    |
   |{EXTRA_CHALL}|
   |                                    |
   \\------------------------------------/
    \\    O    O    O    O    O    O    /
     \\________________________________/
""".encode('ascii', 'replace')
PADDING = "THISISJUSTPADDINGPLEASEIGNORE".encode('ascii')


def noise(w, h):
    img = Image.new('L', (w, h))  # L for 8-bit grayscale mode
    for y in range(h):
        for x in range(w):
            color = randint(0, 255) if not DEBUG_MODE else 0
            img.putpixel((x, y), color)
    return img


def main():
    seed(RND_SEED)
    print("[#] Embedding:")
    print(FLAG_TEXT.decode('ascii'))
    print("[#] Loading...")
    mask = Image.open(mask_img)  # Template for byte positions
    mask = mask.resize(
        (int(mask.width * SCALE), int(mask.height * SCALE)), Image.NEAREST)
    w, h = (mask.width, mask.height)
    visible = Image.open(visible_img)  # Sample with noise when not in mask
    visible = visible.resize((w, h), Image.NEAREST)
    result = noise(w, h)
    idx = 0
    all_text_read = False
    for y in range(h):
        for x in range(w):
            p, _, _, _ = mask.getpixel((x, y))
            if p > BRIGHTNESS_THREASHOLD and random() > MASK_ERROR:
                if not all_text_read:
                    if idx < len(FLAG_TEXT):
                        # ascii value as int
                        b = FLAG_TEXT[idx]
                    else:
                        all_text_read = True
                        idx = 0
                if all_text_read:
                    b = PADDING[idx % len(PADDING)]  # ascii value as int
                # reverse bits and cast back to int
                rb = int(f'{b:08b}'[::-1], 2)
                assert rb & 1 == 0  # Make sure that the last bit is 0 for flag-text
                # rb = 0xff
                result.putpixel((x, y), rb)
                idx += 1
            else:
                cb = result.getpixel((x, y))
                # Select top most bits from visible image if not black
                vb, _, _, _ = visible.getpixel((x, y))
                if vb > 0 and random() > VISIBLE_ERROR:
                    nb = (vb & 0b11000000) | (cb & 0b00111111)
                else:
                    nb = cb
                nb = nb | 1  # set LSB to 1
                assert nb & 1 == 1  # Make sure that the last bit is 1 for junk data
                # b = 0x00
                result.putpixel((x, y), nb)

    print("[#]", "All flag text fit perfectly within the image, no problems!" if all_text_read else "THE TEXT DID NOT FIT!!!! Try generating again or change SCALE and ERROR")
    # result.show()
    result.save("result.png")


if __name__ == "__main__":
    main()
