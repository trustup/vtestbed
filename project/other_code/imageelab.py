from PIL import Image

#im = Image.open("/home/ubuntu/cyris/models/tankmodel/tankmodel.jpg")
#im.putalpha(128)


background = Image.open("/home/ubuntu/cyris/models/back.jpg")
foreground = Image.open("/home/ubuntu/cyris/models/tankmodel/tankmodel.png")
size = 1470, 700
foreground.thumbnail(size)
foreground.show()

background.paste(foreground, (0, 70))
background.show()
# new_im = Image.new('RGB', (444,222))
background.save('/home/ubuntu/PycharmProjects/prova.png')