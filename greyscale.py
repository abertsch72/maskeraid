# MAKE SURE THE WORKING DIRECTORY IS THE MASKERAID FOLDER!!!!!!!!!


from PIL import Image, ImageOps
import os
print(os.path.abspath(os.getcwd()))
currPath = os.path.abspath(os.getcwd())
counter = 1000
for filename in os.listdir((currPath+ r"\data set")):
    print(filename)
    fullpath = currPath + r"\data set" + r"\{name}".format(name=filename)
    og_image = Image.open(fullpath)
    #og_image.show()
    gray_image = ImageOps.grayscale(og_image)
    gray_image.save(currPath + r"\final versions\i{num}.png".format(num=counter))
    counter += 1
    #gray_image.show()

# applying grayscale method

#gray_image.save(currPath + r"\final versions\1.png")