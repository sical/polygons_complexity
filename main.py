# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 10:50:24 2018

@author: thomas
"""
import glob
from complexity import complexity, to_table

if __name__ == "__main__":
    dir_shapes = ".\\shapes\\*.shp"
    dir_img = ".\\images\\*.png"
    shapes = glob.glob(dir_shapes)
    images = glob.glob(dir_img)
    coeff_ampl, coeff_conv = 0.8, 0.2
    
    #Export to latex
    filename = "complexity.tex"
    tablefmt = "latex_raw"
    str_img = "\includegraphics[width=1cm]{{figures/{}.png}}"
    
    gdf = complexity(shapes, images, coeff_ampl, coeff_conv, str_img)
    to_table(gdf, tablefmt, filename, str_img)
    
    #Export to html
    filename = "complexity.html"
    tablefmt = "html"
    str_img = '<img src=".//images//{}.png" style="width:10%;">'
    
    to_table(gdf, tablefmt, filename, str_img)