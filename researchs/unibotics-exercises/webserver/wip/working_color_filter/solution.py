def execute(self):

    # Get image
    input_image = self.camera.getImage()
    if input_image is None:
        # Can't get camera images, is there a video playing?
        return

    if input_image.any():

        # Filter image
        img_hsv = cv2.GaussianBlur(input_image, (11,11), 0)
        img_hsv = cv2.cvtColor(img_hsv, cv2.COLOR_RGB2HSV)

        lower_values = np.array([0,0,150],dtype=np.uint8)
        upper_values = np.array([40,200,255],dtype=np.uint8)

        threshold_img = cv2.inRange(img_hsv, lower_values, upper_values)

        # Get contours
        tmp_img = np.copy(threshold_img)       
        res  = cv2.findContours(tmp_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Force python 2.7 compatibility
        if len(res) == 2:
            contours = res[0]
        else:
            contours = res[1]

        # Draw best contour
        output_img = np.copy(input_image)
        best_contour = None
        best_area = -1
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            area = w*h
            if area > best_area:
                best_area = area
                best_contour = contour

        if best_contour is not None:
            x,y,w,h = cv2.boundingRect(best_contour)
            cv2.rectangle(output_img,(x,y), (x+w, y+h), (255,0,0),2)


        # Save images
        self.set_color_image(output_img)
        self.set_filtered_image(threshold_img)

cf.setExecute(execute)
