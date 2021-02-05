import pickle
import numpy as np
from PIL import Image
import os

def escolha_model(model_choise):
    if model_choise == 1:
        with open(os.getcwd() + r'\model\logit_model_nuvem.pkl', 'rb') as file:
            model1 = pickle.load(file) 
            return model1
    elif model_choise == 2:
        with open(os.getcwd() + r'\model\logit_model_ndvi.pkl', 'rb') as file:
            model1 = pickle.load(file)
            return model1
    else:
        with open(os.getcwd() + r'\model\logit_model_ndvi.pkl', 'rb') as file0:
            model1 = pickle.load(file0)
        with open(os.getcwd() + r'\model\logit_model_nuvem.pkl', 'rb') as file1:
            model2 = pickle.load(file1) 
            return model1, model2


def __normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

def cloud(path, model):
    '''
    1 == cloud 
    '''
    rgb_1 = __img(path)
    rgb_2 = np.reshape(rgb_1, (rgb_1.shape[0] * rgb_1.shape[1], 3))
    if model == 1 or  model == 2:
        result = escolha_model(model).predict(rgb_2)
        final = np.reshape(result, (rgb_1.shape[0], rgb_1.shape[1]))
    else:
        model1, model2 = escolha_model(model)
        result1 = model1.predict(rgb_2)
        result2 = model2.predict(rgb_2)
        result3 = result1 + result2
        result3[result3 == 2] = 1
        final = np.reshape(result3, (rgb_1.shape[0], rgb_1.shape[1]))
    return final

def __img(caminho):
    img = Image.open(caminho).convert('RGB')
    rgb_1 = np.array(img)
    rgb_1 = __normalize(rgb_1)
    return rgb_1

	
