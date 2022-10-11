import os
import numpy as np
import mlflow
from mlflow.models.signature import infer_signature

import tensorflow as tf
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D,Dropout,Flatten,Conv2D,Input,MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.saved_model import signature_constants
from tensorflow.keras.callbacks import LearningRateScheduler

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope
from prefect import flow,task
from prefect.task_runners import SequentialTaskRunner
#prefect orion start


img_width,img_height = 128,128
model_input = (img_width,img_height,3)
img_size = (img_width,img_height)
batch_size = 32
epochs = 0



def lr_schedule(epoch,lr):
    # Learning Rate Schedule

    lr = lr
    total_epochs = epochs

    check_1 = int(total_epochs * 0.9)
    check_2 = int(total_epochs * 0.8)
    check_3 = int(total_epochs * 0.6)
    check_4 = int(total_epochs * 0.4)

    if epoch > check_1:
        lr *= 1e-4 #0.00001
    elif epoch > check_2:
        lr *= 1e-3 #0.0001
    elif epoch > check_3:
        lr *= 1e-2
    elif epoch > check_4:
        lr *= 1e-1

    mlflow.log_metric("learning_rate", lr)
    
    return lr



def create_model(input_size,kernel_size,num_filter,num_conv_layer,num_output):
    model = Sequential(Conv2D(num_filter,kernel_size = kernel_size,padding='same',activation = 'relu',input_shape =input_size ))
    for i in range(num_conv_layer):
        model.add(Conv2D(num_filter,kernel_size = kernel_size,padding='same',activation = 'relu'))
        model.add(Conv2D(num_filter,kernel_size = kernel_size,padding='same',activation = 'relu'))

        model.add(MaxPooling2D(2, 2))
        num_filter= num_filter+num_filter
    model.add(Flatten())
    model.add(Dense(units = num_output,activation = "softmax"))
    return model





def image_read(img_path,img_size = (128,128)):
    import cv2
    image = cv2.imread(img_path)
    resized_img = cv2.resize(image,img_size)
    return resized_img 




@task
def load_data_generator(data_path = r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered"):
    train_imgs,train_label= [],[]
    test_imgs,test_label = [],[]

    for foldername in os.listdir(data_path+"\\train"):
        
        for filename in os.listdir(data_path+"\\train\\"+foldername):
            if filename.strip() == "cats":
                train_label.append(0)
            else:
                train_label.append(1)

            read_path = data_path+"\\train\\"+foldername+"\\"+filename
            train_imgs.append(image_read(img_path=read_path))
        
    for foldername in os.listdir(data_path+"\\validation"):
        for filename in os.listdir(data_path+"\\validation\\"+foldername):
            if filename.strip() == "cats":
                test_label.append(0)
            else:
                test_label.append(1)
        
            read_path = data_path+"\\validation\\"+foldername+"\\"+filename
            test_imgs.append(image_read(img_path=read_path))

    train_imgs,train_label = np.array(train_imgs),np.array(train_label)
    test_imgs,test_label = np.array(test_imgs),np.array(test_label)

    print("Train images : ",train_imgs.shape)
    print("Train Label : ",train_label.shape)

    print("Test images : ",test_imgs.shape)
    print("Test Label : ",test_label.shape)
    
    return train_imgs,train_label,test_imgs,test_label


@task
def train_model_search(train_imgs,train_label,test_imgs,test_label):
    
    conv_layers = 2
    filters_size = [16,32,64]
    kernel_sizes= [(3,3),(5,5),(7,7)]
    learning_rate = 0.001
    epochs =3
    
    search_space = {
    "conv_layers" : scope.int(hp.quniform("conv_layers",2,4,1)),
    "filter_size" : scope.int(hp.choice("filter_size",filters_size)),
    "kernel_size" : hp.choice("kernel_size",kernel_sizes),
    "learning_rate" : hp.loguniform("learning_rate",-3,0),
    "epochs" : scope.int(hp.quniform("epochs",2,5,1))
    }

    def objective(params):
        with mlflow.start_run():
            print("####train_model_search####")  
            mlflow.set_tag("developer","tharhtet")
            mlflow.log_params(params)

            epochs = params["epochs"]
            num_train = len(train_imgs)
            num_test = len(test_imgs)
            steps_per_epoch=int(num_train / batch_size)

            model = create_model(input_size= model_input,
                    kernel_size = params["kernel_size"],
                    num_filter=params["filter_size"],
                    num_conv_layer = params["conv_layers"],
                    num_output=2)
             
            model.compile(loss='sparse_categorical_crossentropy',
                        optimizer=Adam(lr=params["learning_rate"]),
                        metrics=['accuracy'])

            lr_callback = LearningRateScheduler(lr_schedule)
            history = model.fit(x = train_imgs,y=train_label, steps_per_epoch=steps_per_epoch, epochs=epochs,
                                validation_data=(test_imgs,test_label),
                                validation_steps=int(num_test / batch_size), callbacks=[ lr_callback])

            train_acc = history.history['accuracy']
            val_acc = history.history['val_accuracy']
            train_loss = history.history['loss']
            val_loss = history.history['val_loss']
            final_valLoss = 0
            for t_acc,t_loss,v_acc,v_loss in zip(train_acc,train_loss,val_acc,val_loss):
                mlflow.log_metric("train_accuracy", t_acc)
                mlflow.log_metric("train_loss", t_loss)
                mlflow.log_metric("val_accuracy", v_acc)
                mlflow.log_metric("val_loss", v_loss)
                final_valLoss = v_loss
            #results[0]=val_loss, results[1] = val_acc
            

            test_img = np.array([test_imgs[0]])
            signature = infer_signature(test_img, model.predict(test_img,batch_size=1))
            mlflow.keras.log_model(model, "scc_cnn", signature=signature)

        return {'loss' :final_valLoss,'status':STATUS_OK }




    best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=1,
    trials=Trials()
    )

    return best_result

@task
def train_best_model(best_model_config:dict,train_imgs,train_label,test_imgs,test_label):
    filters_size = [16,32,64]
    kernel_sizes= [(3,3),(5,5),(7,7)]
    """
    best_model_config ={
        'conv_layers': 3.0,
        'epochs': 10.0,
        'filter_size': 1,
        'kernel_size': 2,
        'learning_rate': 0.9057050345989054
    """
    epochs = int(best_model_config["epochs"])
    num_train = len(train_imgs)
    num_test = len(test_imgs)
    steps_per_epoch=int(num_train / batch_size)

    model = create_model(input_size= model_input,
            kernel_size = kernel_sizes[best_model_config["kernel_size"]],
            num_filter=filters_size[best_model_config["filter_size"]],
            num_conv_layer = int(best_model_config["conv_layers"]),
            num_output=2)
    
    model.compile(loss='sparse_categorical_crossentropy',
                optimizer=Adam(lr=best_model_config["learning_rate"]),
                metrics=['accuracy'])

    

    lr_callback = LearningRateScheduler(lr_schedule)
    history = model.fit(x = train_imgs,y=train_label, steps_per_epoch=steps_per_epoch, epochs=epochs,
                        validation_data=(test_imgs,test_label),
                        validation_steps=int(num_test / batch_size))

    train_acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']
    final_valLoss = 0
    for t_acc,t_loss,v_acc,v_loss in zip(train_acc,train_loss,val_acc,val_loss):
        mlflow.log_metric("train_accuracy", t_acc)
        mlflow.log_metric("train_loss", t_loss)
        mlflow.log_metric("val_accuracy", v_acc)
        mlflow.log_metric("val_loss", v_loss)
        final_valLoss = v_loss
    #results[0]=val_loss, results[1] = val_acc
    

    test_img = np.array([test_imgs[0]])
    signature = infer_signature(test_img, model.predict(test_img,batch_size=1))
    mlflow.keras.log_model(model, "best_cnn_model", signature=signature)










@flow
def prefect_proj():
    mlflow.set_tracking_uri("sqlite:///mlflow_ths.db")
    mlflow.set_experiment("ths-cat-and-dog-new-exp")
    train_imgs,train_label,test_imgs,test_label = load_data_generator(data_path =  r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered")
    best_model_config = train_model_search(train_imgs,train_label,test_imgs,test_label)
    train_best_model(best_model_config,train_imgs,train_label,test_imgs,test_label)


prefect_proj()
