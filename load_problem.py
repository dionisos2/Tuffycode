from classes import *

def load_problem(problem_path):
    # lord il faut que tu mettes tous ça dans les objets classes associés.
    # et par contre n’hésite pas à dire si il y a un problème.
    var = ["V","E","R","C","X"]
    with open(problem_path, "r+") as f:
        datas = f.readline()
        datas = list(map(lambda x:int(x), datas.split()))
        self.inputs = {var[i] : datas[i] for i in range(len(var))}
        self.taille_videos = list(map(lambda x:int(x), f.readline().split()))

    caches = [Cache(1)]
    endpoints = [EndPoint(1)]
    videos = [Video(1)]
    return(caches, endpoints, videos)
