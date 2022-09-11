import mlflow
import tensorflow as tf
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D,Dropout,Flatten,Conv2D,Input,MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.saved_model import signature_constants

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope


mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("ths-skin-cancer-experiment")


img_width,img_height = 128,128
model_input = (img_width,img_height,3)
img_size = (img_width,img_height)
batch_size = 32

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



def load_data_generator(data_path = r"E:\deep_learning\skin_cancer\dataset\dataset"):
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
        data_path+"/test",
        target_size = img_size,
        batch_size=batch_size,
        class_mode = "categorical"
    )

    return train_gen,test_gen



def train_model_search(train_gen : ImageDataGenerator,test_gen :ImageDataGenerator):
    from mlflow.models.signature import infer_signature
    def objective(params):
        with mlflow.start_run():  
            mlflow.set_tag("developer","tharhtet")
            mlflow.log_params(params)


            num_train = len(train_gen.filenames)
            num_test = len(test_gen.filenames)
            steps_per_epoch=int(num_train / batch_size)

            model = create_model(input_size= model_input,
                    kernel_size = params["kernel_size"],
                    num_filter=params["filter_size"],
                    num_conv_layer = params["conv_layers"],
                    num_output=3)
            
            model.compile(loss='categorical_crossentropy',
                        optimizer=Adam(lr=params["learning_rate"]),
                        metrics=['accuracy'])
            history = model.fit_generator(train_gen, steps_per_epoch=steps_per_epoch, epochs=epochs,
                            validation_data=test_gen,
                            validation_steps=int(num_test / batch_size))

            
            results = model.evaluate(test_gen , batch_size=batch_size)    
            mlflow.log_metric("val_loss", results[0])
            mlflow.log_metric("val_acc", results[1])

            test_img = None
            test_label = None
            for image,label in test_gen:
                test_img = image
                test_label = label
                break

            signature = infer_signature(test_img, model.predict(test_img))
            mlflow.keras.log_model(model, "scc_cnn", signature=signature) 

        return {'loss' :results[0],'status':STATUS_OK }


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
    "epochs" : scope.int(hp.quniform("epochs",2,10,1))
    }

    best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=5,
    trials=Trials()
    )

    return best_result


def train_best_model():




