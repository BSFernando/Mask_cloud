import modelo as md
import matplotlib.pyplot as plt
from PIL import Image

list_model = []
list_model_name = []

def criar(caminho, area1, model):
        linha = len(model) - model.count(0)
        cont = 1
        fig = plt.figure(figsize = (20,10))
        for item in model:
                if item == 0:
                        pass
                else:
                        fig1 = md.__img(caminho)
                        fig.add_subplot(linha,3,cont)
                        cont = cont + 1
                        plt.imshow(fig1)
                        if item == 1:
                                plt.title('Cloud', size = 8)  
                        elif item == 2:
                                plt.title('NDVI', size = 8)
                        else:
                                plt.title('Cloud&NDVI', size = 8)
                        plt.tick_params(labelbottom=False, labelright = False, labelleft=False, labeltop = False)
                        
                        fig.add_subplot(linha,3,cont)
                        cont = cont + 1
                        plt.imshow(md.cloud(caminho, item))
                        area = md.cloud(caminho, item)
                        numb = ((len(area[area==1])) * int(area1))
                        list_model.append(area)
                        list_model_name.append(item)
                        textstr = str(md.np.round(numb,2)) + ' km2'
                        plt.title('mask (' + textstr + ")", size = 8)
                        plt.tick_params(labelbottom=False, labelright = False, labelleft=False, labeltop = False)
                        
                        fig.add_subplot(linha,3,cont)
                        cont = cont + 1
                        fig1 = md.__img(caminho)
                        mask = md.cloud(caminho, item)
                        fig1[mask == 1] = md.np.array([1,0,1])
                        plt.imshow(fig1)
                        plt.title('Overlap', size = 8) 
                        plt.tick_params(labelbottom=False, labelright = False, labelleft=False, labeltop = False)
        return fig, list_model, list_model_name

	
