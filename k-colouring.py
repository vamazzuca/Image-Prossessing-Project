# -----------------------
# Name: Vittorio Mazzuca
# Program: k-colouring.py
# -----------------------


from cImage import *
import cluster
import sys

"""
.

NOTE - Do not modify cluster.py or cImage.py
"""

def create_centroids(k, image, image_window):
    # This function asks the user to select k pixels with distinct RGB
    # values from the image and store them as centroids. Note that the
    # way you store these centroids is completely up to you. You can store
    # the pixel objects, store their (R,G,B) tuple values, etc.
    # Let the user click on k points of the image, store them as
    # centroids, and print x and y coordinates of them in k lines. If a
    # selected point has the same RGB values as one of the previous ones,
    # don't accept it and wait for another one. You can display a message
    # and ask the user to input another pixel.
    
    print("Select {} centoids by clicking on the image".format(k))
    centroids = []
    previous = None
    
    for i in range(1, k + 1):
        click = image_window.getMouse()
        pixel = image.getPixel(click[0], click[1])
        while tuple(pixel) == previous:
            print("That colour has already been picked, pick another")
            click = image_window.getMouse()
            pixel = image.getPixel(click[0], click[1])
        print("Centroid {}: {}".format(i, click))
        previous = tuple(pixel)
        centroids.append(tuple(pixel))
            
    return centroids

def create_data_file(image):
    # This function creates a dictionary with image pixels as the values
    # and returns the dataFile dictionary. Note that the data structure 
    # you use to store points is up to you (I used dictionary)
    data_dict = {}
    
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            coords = (x, y)
            data_dict[coords] = tuple(image.getPixel(x, y))
    
    return data_dict


def create_new_image(clusters, centroids, width, height):
    # This function creates a new image (You can check Chapter 6, page 192
    # of your textbook to get a hint) where each pixel has the colour
    # value of its centroid (use the round() function for each
    # RGB value) and returns the new image.
    # Hint: The size of the new image should be the same as the old one.
    # So you can use width and height arguments to create such an image
    # with the same size.
    empty_im = EmptyImage(width, height)
    for i in range(len(clusters)):
        for coords in clusters[i]:
            pixel = Pixel(round(centroids[i][0]), round(centroids[i][1]), 
                          round(centroids[i][2]))
            empty_im.setPixel(coords[0], coords[1], pixel)
            
    
    return empty_im

def compute_distance(clusters, centroids, data_file, image):
    # This function computes the total distance and returns its value
    # which has been rounded to 2 digits beyond the decimal point in form
    # of a string.
    # The total distance is defined as the sum of all distances between
    # points and their centroids.
    # NOTE: you should round the total result to two digits of precision
    # beyond the decimal point.
    total = 0
    
    for i in range(len(clusters)):
        for coords in clusters[i]:
            pixel = image.getPixel(coords[0], coords[1])
            distance = cluster.euclidD(centroids[i], pixel)
            total += distance
   
    return total

def display_image(imagename):
    # This function opens the image whose name is imagename and
    # displays it in a window which is the same size as the image
    # It also returns the image object as well as the window object.
    
    img = FileImage(imagename)
    win = ImageWin("Display", img.getWidth(), img.getHeight())
    img.draw(win)

    return img, win


def readCommandLineArgs():
    # Process the command line arguments. These arguments are the name
    # of the original image and the number of clusters (k). Consider 6
    # as the default value of k. The user will enter them after the name
    # of your program file in command line
    k = 6
    iterations = 5
    inputFile = sys.argv[1]
    if len(sys.argv) == 3:
    	k = int(sys.argv[2])
    if len(sys.argv) == 4:
        k = int(sys.argv[2])
    	iterations = int(sys.argv[3])

    return inputFile, k, iterations


def main():
    # TODO read and Process the command line arguments.
    (image_name, num_clusters, iterations) = readCommandLineArgs()

    # TODO Read in the original image and display it. Note that when you
    # displayed the image in display_image function, you should return the
    # image object as well as the window object you created in
    # display_image function.
    
    image, image_window = display_image(image_name)

    # TODO Get width and height of the original image.

    width = image.getWidth()
    height = image.getHeight()

    # TODO Let the user click on k points of the image, store them as
    # centroids, and print x and y coordinates of them in k lines. If a
    # selected point has the same RGB values as one of the previous ones,
    # don't accept it and wait for another one.
    
    centroids = create_centroids(num_clusters, image, image_window)
    
    # TODO Create data_file which is a dictionary with pixel indexes and also
    # the the pixels as the values of the dictionary.
    
    data_file = create_data_file(image)

    new_image = image
    counter = 0
    passes = 1
    print("\nStarting clustering process")
    while counter < iterations:
        # TODO Partition the color values in the image. That is, each pixel is
        # grouped in the cluster whose centroid it is closest to. 
        # Hint: use cluster.py

        clusters = cluster.assignPointsToClusters(centroids, data_file)

        # TODO Create a new image where each pixel has the colour value of its
        # centroid.
        
        new_image = create_new_image(clusters, centroids, width, height)
        
        # TODO Display the new image.
        new_image.draw(image_window)

        # TODO Print the total distance rounded to two digits of precision
        # beyond the decimal point. Also NOTE that we are passing the
        # original image to computeDistance as the argument (NOT the
        # new_image we created previously)

        distance = compute_distance(clusters, centroids, data_file, image)
        print("Total distance at pass {}: {:.2f}".format(passes, distance))

        # TODO Compute new centroids based on the clusters. 
        # Hint: use cluster.py
        
        centroids = cluster.updateCentroids(clusters, centroids, data_file)

        counter += 1
        passes += 1
    #TODO save image to new file k_colours.gif
    image_window._close()
    new_image.save("k_colours.gif")

    


if __name__ == "__main__":
    main()
