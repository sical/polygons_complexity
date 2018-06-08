# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 17:16:22 2018

@author: thomas
"""

from generate_polygons import generatePolygon
import json
import itertools


if __name__ == "__main__":
    params = "./params/params.json"
    params = json.load(open(params))
    lon = params["lon"]
    lat = params["lat"]
    epsg = params["epsg"]
    radius = params["radius"]
    irregularity = params["irregularity"]
    spikeyness = params["spikeyness"]
    vertices = params["vertices"]
    path_shp = params["path_shp"]
    path_img = params["path_img"]
    iteration = params["iteration"]
    
    l_spikeyness = [spikeyness*i for i in range(1,iteration)]
    l_irregularity = [irregularity*i for i in range(1,iteration)]
    l_vertices = [vertices//vertices*i for i in range(3,iteration)]
    
    l = [l_spikeyness, l_irregularity, l_vertices]
    
    possibilities = list(itertools.product(*l))
    
    for x in possibilities:
        irregularity,spikeyness,vertices = x[0], x[1], x[2]
        generatePolygon(lon,lat,radius,irregularity,spikeyness,vertices,path_shp, path_img, epsg)