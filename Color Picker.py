import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import math
import random

# random not important
def update_scale(event):
    red_var.set(int(red_var.get()))
    green_var.set(int(green_var.get()))
    blue_var.set(int(blue_var.get()))


def validate(p):
    if p.isdigit() and 0 <= int(p) <= 255:
        return True
    elif p == "":
        return True
    else:
        return False


def update_color():
    try:
        brightness_var.set(100)
        r = red_var.get()
        g = green_var.get()
        b = blue_var.get()
        brightness_ = brightness_var.get() / 100
        if r != '' and g != '' and b != '':
            color = f"#{r:02x}{g:02x}{b:02x}"
            bright_color = adjust_brightness(color, brightness_)
            color_result_canvas.create_rectangle(0, 0, 50, 200, fill=bright_color, outline="")
            result_text.set(bright_color)
    except:
        pass


def update_bri():
  try:
    r = red_var.get()
    g = green_var.get()
    b = blue_var.get()
    brightness_ = brightness_var.get() / 100
    if r != '' and g != '' and b != '':
      color = f"#{r:02x}{g:02x}{b:02x}"
      bright_color = adjust_brightness(color, brightness_)
      color_result_canvas.create_rectangle(0, 0, 50, 200, fill=bright_color, outline="")
      result_text.set(bright_color)
  except:
    pass


def random_color():
    red_var.set(random.randint(0, 255))
    green_var.set(random.randint(0, 255))
    blue_var.set(random.randint(0, 255))
    update_color()

def adjust_brightness(hex_color, brightness):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)

    return f"#{r:02x}{g:02x}{b:02x}"


def create_color_circle(size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    center = size // 2
    radius = size // 2
    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= radius:
                angle = math.atan2(dy, dx)
                hue = (angle + math.pi) / (2 * math.pi)
                saturation = distance / radius
                r, g, b = hsv_to_rgb(hue, saturation, 1)
                draw.point((x, y), (int(r * 255), int(g * 255), int(b * 255), 255))
            else:
                draw.point((x, y), (0, 0, 0, 0))
    return ImageTk.PhotoImage(image)


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i %= 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def on_circle_click(event):
    x, y = event.x - 150, event.y - 125
    if x**2 + (y - 20)**2 <= 125**2:
        r, g, b = hsv_to_rgb((math.atan2(y, x) + math.pi) / (2 * math.pi), min(1, math.sqrt(x * x + y * y) / 150), 1)
        red_var.set(int(r * 255))
        green_var.set(int(g * 255))
        blue_var.set(int(b * 255))
        update_color()


app = tk.Tk()
app.geometry('400x550')
app.title('Color Picker')
app.resizable(width=False, height=False)

# Create color circle image
color_circle_image = create_color_circle(250)
color_circle_canvas = tk.Canvas(app, width=400)
color_circle_canvas.create_image(150, 130, image=color_circle_image)
color_circle_canvas.bind("<Button-1>", on_circle_click)
color_circle_canvas.place(x=0, y=0)

# # Color result canvas
color_result_canvas = tk.Canvas(app, width=50, height=200, background='#efefef')
color_result_canvas.place(x=320, y=30)
#
# # Mode dropdown
mode = ttk.Combobox(app, values=["RGB", "HSV"], state="readonly")
mode.set("RGB")
mode.place(x=30, y=350)
#
# # Result color hex value entry
result_text = tk.StringVar(value='#000000')
result_entry = ttk.Entry(app, textvariable=result_text, font=('Arial', 16), width=10)
result_entry.place(x=270, y=400)


red_var = tk.IntVar(value=0)
red_label = ttk.Label(app, text="Red", foreground='red')
red_label.place(x=30, y=380)
red_entry = ttk.Entry(app, textvariable=red_var, validate='key', validatecommand=(app.register(validate), '%P'),
                      width=6)
red_entry.place(x=60, y=380)
red_slider = ttk.Scale(app, from_=0, to=255, orient='horizontal', variable=red_var, command=lambda event: update_color())
red_slider.place(x=120, y=380)
red_slider.bind("<ButtonRelease-1>", update_scale)

green_var = tk.IntVar(value=0)
green_label = ttk.Label(app, text="Green", foreground='green')
green_label.place(x=30, y=420)
green_entry = ttk.Entry(app, textvariable=green_var, validate='key',
                        validatecommand=(app.register(validate), '%P'), width=6)
green_entry.place(x=60, y=420)
green_slider = ttk.Scale(app, from_=0, to=255, orient='horizontal', variable=green_var, command=lambda event: update_color())
green_slider.place(x=120, y=420)
green_slider.bind("<ButtonRelease-1>", update_scale)

#
blue_var = tk.IntVar(value=0)
blue_label = ttk.Label(app, text="Blue", foreground='blue')
blue_label.place(x=30, y=460)
blue_entry = ttk.Entry(app, textvariable=blue_var, validate='key', validatecommand=(app.register(validate), '%P'),
                       width=5)
blue_entry.place(x=60, y=460)
blue_slider = ttk.Scale(app, from_=0, to=255, orient='horizontal', variable=blue_var, command=lambda event: update_color())
blue_slider.place(x=120, y=460)
blue_slider.bind("<ButtonRelease-1>", update_scale)

# Brightness slider
brightness_var = tk.IntVar(value=100)
brightness_label = ttk.Label(app, text="Brightness")
brightness_label.place(x=70, y=300)
brightness_slider = ttk.Scale(app, from_=0, to=100, orient='horizontal', variable=brightness_var, length=200, command=lambda event: update_bri())
brightness_slider.place(x=150, y=300)

random_color_btn = ttk.Button(master=app, text='Random Color', command=random_color)
random_color_btn.place(x=150, y=500)

random_color()
app.mainloop()

