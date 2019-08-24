# Layers
import face_recognition
from keras.layers import Dense, Activation, Flatten, Dropout
from keras import backend as K
import tensorflow as tf


#Networks
from keras.applications.resnet50 import ResNet50

# Other
from keras.models import Sequential, Model
from keras.models import load_model

# Utils
import numpy as np
import random, glob
import os, sys, csv
import cv2
import time, datetime
from keras.applications.resnet50 import preprocess_input
preprocessing_function = preprocess_input
from PIL import Image
import shutil

from keras.backend.tensorflow_backend import set_session


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.4)
#session = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))


global graph
graph = tf.get_default_graph()




WIDTH = 224
HEIGHT = 224
FC_LAYERS = [1024, 1024]
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(HEIGHT, WIDTH, 3))




def load_class_list(class_list_file):
    class_list = []
    with open(class_list_file, 'r') as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            class_list.append(row)
    class_list.sort()
    return class_list

def build_model(base_model, dropout, fc_layers, num_classes):
    for layer in base_model.layers:
        layer.trainable = False
    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        x = Dense(fc, activation='relu')(x) # New FC layer, random init
        x = Dropout(dropout)(x)
    predictions = Dense(num_classes, activation='softmax')(x) # New softmax layer
    finetune_model = Model(inputs=base_model.input, outputs=predictions)
    return finetune_model

class_list_file =  "./checkpoints/" + "ResNet50_dataset_class_list.txt"
class_list = load_class_list(class_list_file)
model = build_model(base_model, dropout=1e-3, fc_layers=FC_LAYERS, num_classes=len(class_list))
model.load_weights("./checkpoints/" + "ResNet50_model_weights.h5")
#model._make_predict_function()
#finetune_model.summary()


def predict(path, model1):
    predictingimages=os.listdir(path)
    #print(predictingimages)
    if predictingimages == []:
        print("No Frames To Work With")
    else:
        smokingimages = []
        predictingimages=sorted(predictingimages)
        for img in predictingimages:
            print("Finding Face in Image..")
            frame = face_recognition.load_image_file(path+"/"+img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame, model=model1)
            print(face_locations)
            if len(face_locations) > 0:
                #os.mkdir(path+"/crop")
                #print("Directory Created...")
                for j in range(len(face_locations)):
                    coord = face_locations[j]
                    height, width, channels = frame.shape
                    y1 = np.maximum(0,coord[0]-15)
                    y2 = np.minimum(height, coord[2]+15)
                    x1 = np.maximum(0,coord[3]-15)
                    x2 = np.minimum(width,coord[1]+15)
                    y_h = y2 - y1
                    x_w = x2 - x1
                    if y_h >= 50 and x_w >= 50:
                        crop_img = frame[y1:y2, x1:x2]
                        # cv2.imwrite(path+"/crop/"+str(j)+".."+img, crop_img)
                        # print("image transferred")
                    else:
                        print("file skipped, size too small...")
                    # print("Crop Directory:",os.listdir(path+"/crop/"))
                    # for crop_file in os.listdir(path+"/crop/"):
                    # print("entering crop directory...", crop_img)
                    #image = cv2.imread(path+ "/crop/"+ crop_file,-1)
                    #save_image = image
                    image = np.float32(cv2.resize(crop_img, (HEIGHT, WIDTH)))
                    image = preprocessing_function(image.reshape(1, HEIGHT, WIDTH, 3))
                    with graph.as_default():
                        out = model.predict(image)
                    confidence = out[0]
                    class_prediction = list(out[0]).index(max(out[0]))
                    class_name = class_list[class_prediction]
                    print("Predicted class = ", class_name)
                    print("", confidence, img, class_name)
                    ''' [1,0] -> Not_Smoking and [0,1] -> Smoking'''
                    if confidence[1] > confidence[0]:
                        print("", confidence, img, class_name)
                        smokingimages.append(img)
                        #shutil.copy(path+"/"+img, "temp/")
                    # print("Run time = ", run_time)
                    # if class_name == "smoking":
                    #     cv2.imwrite("Predictions/smoking/" + img + ".png", save_image)
                    # else:
                    #     cv2.imwrite("Predictions/not_smoking/" + img + ".png", save_image)
                # shutil.rmtree(path+"/crop")

            else:
                #os.remove(path+"/"+img)
                pass

        # for img in os.listdir(path):
        #     print("entering crop directory...", img)
        #     image = cv2.imread(path+ "/"+ img,-1)
        #     #save_image = image
        #     image = np.float32(cv2.resize(image, (HEIGHT, WIDTH)))
        #     image = preprocessing_function(image.reshape(1, HEIGHT, WIDTH, 3))
        #     with graph.as_default():
        #         out = model.predict(image)
        #     confidence = out[0]
        #     class_prediction = list(out[0]).index(max(out[0]))
        #     class_name = class_list[class_prediction]
        #     #print("Predicted class = ", class_name)
        #     #print("", confidence, img, class_name)
        #     ''' [1,0] -> Not_Smoking and [0,1] -> Smoking'''
        #     if confidence[1] - confidence[0] > 0.1:
        #         print("", confidence, img, class_name)
        #         smokingimages.append(img)
        #         shutil.copy(path+"/"+img, "temp/")
    print("Smoking Images:",smokingimages)   
    return smokingimages      
#predict("full")