# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 12:54:44 2018

@author: thomas
"""
import os
import math, random
from shapely.geometry import Polygon
import geopandas as gpd

def generatePolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts, path_shp, path_img, crs):
    """
    Start with the centre of the polygon at ctrX, ctrY, 
    then creates the polygon by sampling points on a circle around the centre. 
    Randon noise is added by varying the angular spacing between sequential points,
    and by varying the radial distance of each point from the centre.

    Params:
    ctrX, ctrY - coordinates of the "centre" of the polygon
    aveRadius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.
    irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]
    spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]
    numVerts - self-explanatory
    
    Source: https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon, Mike Ounsworth
    Modified by thom leysens

    Returns a list of vertices, in CCW order.
    """
    name = "r={}_i={}_s={}_v={}".format(aveRadius, irregularity, spikeyness, numVerts)
    crs = {"init": crs}
    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius
    
    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp
    
    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2*math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k
    
    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append((x,y))
    
        angle = angle + angleSteps[i]
        
    #Create polygon and GeoDataframe
    poly = Polygon(points)
    dict_gdf = {
            "name":[name],
            "aveRadius":[aveRadius],
            "irregularity":[irregularity],
            "spikeyness":[spikeyness],
            "numVerts":[numVerts],
            "geometry":[poly]
            }
    
    gdf = gpd.GeoDataFrame(dict_gdf, crs=crs) 
    gdf.set_geometry("geometry")
    
    img = name + ".png"
    name = name + ".shp"
    name = os.path.join(path_shp, name)
    img = os.path.join(path_img, img)

    fig = gdf.plot(legend=False, color="white", edgecolor="black", linewidth=7)

    fig.axes.get_yaxis().set_visible(False)
    fig.axes.get_xaxis().set_visible(False)
    fig = fig.get_figure()
    fig.savefig(img)
    gdf.to_file(name)
    
    return gdf

def clip(x, min, max):
    """
    Source: https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon, Mike Ounsworth
    """
    if( min > max ):  
        return x    
    elif( x < min ):  
        return min
    elif( x > max ):  
        return max
    else:             
        return x 