from re import S
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


@task
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


@task
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


@task
def load_data_generator(data_path = r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered"):
    _datagen = ImageDataGenerator(
        rescale=1/255,
		width_shift_range=0.1,
		height_shift_range=0.1,
		horizontal_flip=True)

    train_gen = _datagen.flow_from_directory(
        data_path+"/train",
        target_size = img_size,
        batch_size=batch_size,
        class_mode = "categorical"
    )

    test_gen = _datagen.flow_from_directory(
        data_path+"/validation",
        target_size = img_size,
        batch_size=batch_size,
        class_mode = "categorical"
    )

    return train_gen,test_gen


@task
def train_model_search(train_gen : ImageDataGenerator,test_gen :ImageDataGenerator):
    

    def objective(params):
        with mlflow.start_run():
            print("####train_model_search####")  
            mlflow.set_tag("developer","tharhtet")
            mlflow.log_params(params)
            
            
            epochs = params["epochs"]
            num_train = len(train_gen.filenames)
            num_test = len(test_gen.filenames)
            steps_per_epoch=int(num_train / batch_size)

            model = create_model(input_size= model_input,
                    kernel_size = params["kernel_size"],
                    num_filter=params["filter_size"],
                    num_conv_layer = params["conv_layers"],
                    num_output=2)
            
            model.compile(loss='categorical_crossentropy',
                        optimizer=Adam(lr=params["learning_rate"]),
                        metrics=['accuracy'])

        

            lr_callback = LearningRateScheduler(lr_schedule)
            history = model.fit_generator(train_gen, steps_per_epoch=steps_per_epoch, epochs=epochs,
                                validation_data=test_gen,
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
            

            test_img = None
            for image,label in test_gen:
                test_img = image
                break

            signature = infer_signature(test_img, model.predict(test_img))
            mlflow.keras.log_model(model, "scc_cnn", signature=signature)

        
            
        return {'loss' :final_valLoss,'status':STATUS_OK }

        


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

    best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=1,
    trials=Trials()
    )

    return best_result

@task
def train_best_model(best_model_config:dict,train_gen : ImageDataGenerator,test_gen :ImageDataGenerator):

    """
    best_model_config ={
        'conv_layers': 3.0,
        'epochs': 10.0,
        'filter_size': 1,
        'kernel_size': 2,
        'learning_rate': 0.9057050345989054
    """
    epochs = int(best_model_config["epochs"])
    num_train = len(train_gen.filenames)
    num_test = len(test_gen.filenames)
    steps_per_epoch=int(num_train / batch_size)

    model = create_model(input_size= model_input,
            kernel_size = best_model_config["kernel_size"],
            num_filter=best_model_config["filter_size"],
            num_conv_layer = int(best_model_config["conv_layers"]),
            num_output=2)
    
    model.compile(loss='categorical_crossentropy',
                optimizer=Adam(lr=best_model_config["learning_rate"]),
                metrics=['accuracy'])

    

    lr_callback = LearningRateScheduler(lr_schedule)
    history = model.fit_generator(train_gen, steps_per_epoch=steps_per_epoch, epochs=epochs,
                        validation_data=test_gen,
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
    

    test_img = None
    test_label = None
    for image,label in test_gen:
        test_img = image
        test_label = label
        break

    signature = infer_signature(test_img, model.predict(test_img))
    mlflow.keras.log_model(model, "scc_cnn", signature=signature)





@flow
def main():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("ths-cat-and-dog-experiment")
    
    train_gen, val_gen = load_data_generator(data_path =  r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered")
    print("OK Na Sa")
    best_model = train_model_search(train_gen=train_gen,test_gen=val_gen)
    train_best_model(best_model_config=best_model,train_gen=train_gen,test_gen=val_gen)


main()