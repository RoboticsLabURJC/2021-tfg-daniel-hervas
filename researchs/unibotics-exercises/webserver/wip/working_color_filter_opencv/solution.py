def execute(self):

    input_image = self.camera.getImage()
    if input_image is not None:
        self.set_color_image(input_image)  
        smooth_image = cv2.GaussianBlur(input_image,(5,5),0)
        HSV_smooth_image = cv2.cvtColor(smooth_image, cv2.COLOR_RGB2HSV)
        lower_boundary = np.array([110,155,0], dtype = "uint8")
        upper_boundary = np.array([179,255,255], dtype = "uint8")

        # PARA UN OBJETO AZUL
        lower_boundary2 = np.array([109,0,0], dtype = "uint8")
        upper_boundary2 = np.array([128,255,255], dtype = "uint8")
        # -------------------

        mask = cv2.inRange(HSV_smooth_image,lower_boundary,upper_boundary)
        mask2 = cv2.inRange(HSV_smooth_image,lower_boundary2,upper_boundary2)
        #self.camera.set_filtered_image(mask)
        input_image_copy = input_image

        mask_copy2 = np.copy(mask2)
        im2_2, contours2, hierarchy2 = cv2.findContours(mask_copy2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if contours2 != []:
            contour = sorted(contours2, key = cv2.contourArea, reverse = True)[0] 
            # Ordenamos los contornos por su area (de mayor a menor)
            x,y,w,h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(input_image_copy, (x,y), (x+w,y+h),(255,117,20),2)
            self.set_filtered_image(rectangle)

cf.setExecute(execute)
