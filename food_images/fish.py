from PIL import Image, ImageDraw, ImageFont
import os

emoji_dict = {
    "1": "🍤",
    "2": "🥨",
    "3": "🐟",
    "4": "🥐",
    "5": "🥦",
    "6": "🍺",
    "7": "🍇",
    "8": "🍙",
    "9": "🍟",
    "0": "🍕"
}

output_folder = "emoji_pngs_safe"
os.makedirs(output_folder, exist_ok=True)

font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"

size = 256 
max_font_size = 200 

for key, emoji in emoji_dict.items():
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_size = max_font_size
    while font_size > 10:
        try:
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), emoji, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if w <= size and h <= size:
                break
        except OSError:
            pass
        font_size -= 2

    bbox = draw.textbbox((0, 0), emoji, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]

    draw.text((x, y), emoji, font=font, embedded_color=True)

    output_path = os.path.join(output_folder, f"{key}_{emoji}.png")
    img.save(output_path)
    print(f"Saved {output_path}")
