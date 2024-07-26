import os
import cv2
import keras
import numpy as np
from sklearn.cluster import KMeans
from keras import Model
import shutil

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (250, 250)) 
            images.append(img)
            filenames.append(filename)
    return images, filenames

def extract_features(images):
    model = keras.applications.VGG16(weights='imagenet', include_top=False)
    model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
    features = []
    for img in images:
        img = np.expand_dims(img, axis=0)
        img = keras.applications.resnet50.preprocess_input(img)
        feature = model.predict(img)
        features.append(feature.flatten())
    return np.array(features)

folder_path = 'D:\\predict images\\segregate'
images, filenames = load_images_from_folder(folder_path)
features = extract_features(images)

kmeans = KMeans(n_clusters=2, random_state=0).fit(features)
labels = kmeans.labels_

folder_1 = 'D:\\predict images\\class1'
folder_2 = 'D:\\predict images\\class2'

os.makedirs(folder_1, exist_ok=True)
os.makedirs(folder_2, exist_ok=True)

for label, filename in zip(labels, filenames):
    src_path = os.path.join(folder_path, filename)
    if label == 0:
        dest_path = os.path.join(folder_1, filename)
    else:
        dest_path = os.path.join(folder_2, filename)
    shutil.move(src_path, dest_path)



