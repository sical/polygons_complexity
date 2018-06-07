# Measures of polygon's complexity
## Intro
In order to measure the complexity of polygons, we studied a paper and a QGIS plugin (*not working in QGIS LTR 2.18**) based on this paper:
  *   Brinkhoff, Thomas, Hans-Peter Kriegel, Ralf Schneider, et Alexander Braun., [*Measuring the Complexity of Polygonal Objects*](https://www.google.fr/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiar5SdlrzbAhVFPxQKHY-MCsMQFggtMAA&url=http%3A%2F%2Fciteseerx.ist.psu.edu%2Fviewdoc%2Fdownload%3Fdoi%3D10.1.1.73.1045%26rep%3Drep1%26type%3Dpdf&usg=AOvVaw1J5RsuN2NBeZbzNHkbouF_).
  * [QGIS plugin](https://github.com/pondrejk/PolygonComplexity) by [Peter Ondrejka](https://github.com/pondrejk)

We develop functions to measure the complexity and functions to export results as statistical tables (*with possibility to chose the export format: html, latex, ...*) included in the *complexity* module.

## Calculation
Find parameters to quantify/qualify the complexity of a polygon:
* Number of polygon
* Area
* Perimeter
* Number of vertices or edges
* Centroid
* Frequency of vibration (*normalized notches*) (**see paper**):
"*Measure the vibration of polygon’s boundary. “Notches describe the non-convex parts of a polygon. The maximum number of notches that occur on a polygon pol depend on its number of vertices*." Notches are vertex where an interior angle larger than ![pi](./math_formulas/pi.gif):

  > ![notches](./math_formulas/notches.gif)

* "*The fewer notches that occur, the smoother the boundary is. If notchesnorm is 0, the polygon is convex. Similar to low values of notches norm, high values indicate a smooth boundary*"
* Amplitude (*ampl*) of  polygon (*pol*) vibration (**see paper**):
"*The frequency of the vibration makes no statement with respect to the intensity of the vibration. In order to quantify this amplitude, we investigate the increase of the boundary of the polygon compared to the boundary of its convex hull*":

  > ![amplitude](./math_formulas/amplitude.gif)

* Deviation from convex hull (**see paper**):
"*The two parameters introduced before describe the local vibration of a spatial object. The global shape of a spatial object is however another aspect that intuitively influences the rating of the complexity of the spatial object. In order to obtain a measure for this type of global complexity, we use the convex hull of the polygon again*":

  > ![deviation](./math_formulas/deviation.gif)

* Complexity (**see paper**):
  > ![complexity](./math_formulas/complexity.gif)

## Structure of directory
If you git clone the project, you will have everything you need.
If you want to make changes, you have to keep the following instructions in mind.
In order to use the *complexity* functions, you have to have a directory with:
  * main.py (*configuration*)
  * complexity.py (*main module*)
  * subdirectory **images** (*images files with a specific name that matches with shape name*)
  * subdirectory **shapes** (*shapefiles with a specific name that matches with image name*):
    * example for shapes directory: ![shape](./screenshots/shape_dir.png)
    * example for images directory: ![img](./screenshots/img_dir.png)

## Export to table format
We use the *tabulate* Python module to generate table with these potential formats (*see [tabulate doc](https://pypi.org/project/tabulate/) for more information*):
* "plain"
* "simple"
* "grid"
* "fancy_grid"
* "pipe"
* "orgtbl"
* "jira"
* "presto"
* "psql"
* "rst"
* "mediawiki"
* "moinmoin"
* "youtrack"
* "html"
* "latex"
* "latex_raw"
* "latex_booktabs"
* "textile"

For example, we use these parameters to get a latex table with links to images (*see main.py file*):
```
import glob
from complexity import complexity, to_table

if __name__ == "__main__":
    dir_shapes = ".\\shapes\\*.shp"
    dir_img = ".\\images\\*.png"
    shapes = glob.glob(dir_shapes)
    images = glob.glob(dir_img)
    coeff_ampl, coeff_conv = 0.8, 0.2
    filename = "complexity.tex"
    tablefmt = "latex_raw"
    str_img = "\includegraphics[width=1cm]{{figures/{}}}"

    gdf = complexity(shapes, images, coeff_ampl, coeff_conv, str_img)
    to_table(gdf, tablefmt, filename)
```
> for *str_img* parameter, you'll need to check the format and string that matches your needs. In the example, it is set for latex table format.
