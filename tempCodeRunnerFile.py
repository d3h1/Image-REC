if file and allowed_files(file.filename):
                filename = file.filename
                file_path = os.path.join('static/images', filename)
                file.save(file_path)
                img = read_image(file_path)
                
                # We will now predict the class of an image
                with graph.as_default():
                    model1 = load_model('classification_model.h5')
                    class_prediction = model1.predict_classes(img)
                    print(class_prediction)
                    
                # We will map apparel category with numerical classes
                if class_prediction[0] == 0:
                    product = "TShirt/top"
                elif class_prediction[0] == 1:
                    product = "Trouser"
                elif class_prediction[0] == 2:
                    product = "Pullover"
                elif class_prediction[0] == 3:
                    product = "Dress"
                elif class_prediction[0] == 4:
                    product = "Coat"
                elif class_prediction[0] == 5:
                    product = "Sandal"
                elif class_prediction[0] == 6:
                    product = "Shirt"
                elif class_prediction[0] == 7:
                    product = "Sneaker"
                elif class_prediction[0] == 8:
                    product = "Bag"
                else:
                    product = "Ankle Boot"
                return render_template('predict.html', product = product, user_image = file_path)
            