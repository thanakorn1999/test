import bz2
from cProfile import label
from contextlib import nullcontext
import csv
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


def list_to_pandas(datas,columns_name):
    d ={}
    for index,col in enumerate(columns_name):
        d[columns_name[index]] =datas[index]
    df = pd.DataFrame(d)
    return df


def find_distance (x ,y ,x2,y2 ):
    distances_x_y=[]
    for index,_ in enumerate(x2):
        distance = math.sqrt( ((x-x2[index])**2)+((y-y2[index])**2) )
        distances_x_y.append([round(distance,5),round(x2[index],5),round(y2[index],5)])
    return distances_x_y


def check_within_x_meters(distances,x):
    list_focus =[]
    for distance in distances:
        if x>distance[0]:
            list_focus.append(distance)
    return len(list_focus)


def radius_in_x_percent(coordinates_distance_x_y,x_percent=100):
    coordinates_distance_x_y = coordinates_distance_x_y[0]
    coordinates_distance_x_y = sorted(coordinates_distance_x_y,key=lambda l:l[0], reverse=False)

    for index,data in enumerate(coordinates_distance_x_y):
        coordinates_distance_x_y[index][0] =data[0]/2

    len_list = len(coordinates_distance_x_y)
    n=int(len_list/100*x_percent)
    coordinates_distance_x_y = coordinates_distance_x_y[0:n]
    return coordinates_distance_x_y


def fine_k_centroids(x,y):
    x_center = np.sum(x)/len(x)
    y_center = np.sum(y)/len(y)
    return [x_center,y_center]


def get_xy_from_distances_x_y(distances_x_y):
    Y,X=[],[]
    distances=[]
    for list_disxy in distances_x_y:
        if list_disxy ==[]:
            continue
        for dis,x,y in list_disxy :
            X.append(x)
            Y.append(y)
            distances.append(dis)
    return X,Y,distances


def count_n_pandas(centroids):
    pass
    count_n_5_meters,count_n_10_meters=0,0

    for i,data in enumerate(centroids["n_within_5_meters"]):
        count_n_5_meters  += centroids["n_within_5_meters"][i]
        count_n_10_meters += centroids["n_within_10_meters"][i]


    return count_n_5_meters,count_n_10_meters



def calculate(centroids,coordinates):
    plot =False
    if plot == True:
        plt.scatter(coordinates['X'],coordinates['Y'], label='Point (X;Y)' , color ='pink')
        plt.scatter(centroids['X'],centroids['Y'], label='Point (X;Y)' , color ='k')
        plt.xlabel('X')
        plt.xlabel('Y')
        plt.title('test')
        plt.legend()
        plt.show()

    centroids['coordinates_distance_x_y'] = centroids.apply(lambda row : find_distance(row['X'],row['Y'], coordinates["X"],coordinates["Y"]), axis = 1)

    # 1.	How many coordinates are within 5 meters of at least one of the centroids?
    # 2.	How many coordinates are within 10 meters of at least one of the centroids?
    centroids['n_within_5_meters']  = centroids.apply(lambda row : check_within_x_meters(row['coordinates_distance_x_y'], 5), axis = 1)
    centroids['n_within_10_meters'] = centroids.apply(lambda row : check_within_x_meters(row['coordinates_distance_x_y'], 10), axis = 1)
    count_n_5_meters,count_n_10_meters = count_n_pandas(centroids)
    print("")
    print("coordinates are within 5 meters :",count_n_5_meters)
    print("coordinates are within 10 meters :", count_n_10_meters)

    # 3.	What is the minimum radius R such that 80 percent of the coordinates are within R meters of at least one of K centroids?
    k_centroids = fine_k_centroids(coordinates["X"],coordinates["Y"])
    k_centroids = list_to_pandas([[k_centroids[0]],[k_centroids[1]]],["X","Y"])
    k_centroids['coordinates_distance_x_y']  = k_centroids.apply(lambda row : find_distance(row['X'],row['Y'], coordinates["X"],coordinates["Y"]), axis = 1)

    radius_xy_within_80_percent =radius_in_x_percent(k_centroids['coordinates_distance_x_y'],80)
    radius_xy_min_of_80 = radius_xy_within_80_percent[0]
    print("")
    print("x,y :",radius_xy_min_of_80[1],radius_xy_min_of_80[2])
    print("radius :",radius_xy_min_of_80[0])

    # 4.	Bonus: What is the maximum radius R such that the number of coordinates within a distance strictly less than R of any centroid is at most 1000?
    # find max(coordinates.radius)<(centroid.radius)
    k_centroids['centroids_distance_x_y']  = k_centroids.apply(lambda row : find_distance(row['X'],row['Y'], centroids["X"],centroids["Y"]), axis = 1)

    centroids_radius_xy    = radius_in_x_percent(k_centroids['centroids_distance_x_y'])
    coordinates_radius_xy  = radius_in_x_percent(k_centroids['coordinates_distance_x_y'])

    min_r_centroids = centroids_radius_xy[0][0]

    print("")
    print("min_radius_centroids :",min_r_centroids)
    rcd_less_than_rct =[]

    for radius_cd,x,y in coordinates_radius_xy:
        if min_r_centroids>radius_cd:
            rcd_less_than_rct.append(radius_cd)
        else:
            break

    print("radius_max_coordinates < min_radius_centroids :",rcd_less_than_rct[-1])
    return str(count_n_5_meters) ,str(count_n_10_meters) ,str(radius_xy_min_of_80[0]) ,str(rcd_less_than_rct[-1])
    

centroids_path="centroids.csv.bz2"
coordinates_path="coordinates.csv.bz2"


# for test
centroids =pd.read_csv(centroids_path,nrows = 100 )
coordinates =pd.read_csv(coordinates_path,nrows = 100  )

n_5_meters ,n_10_meters ,radius_min_of_80 ,rcdmax_less_than_minrct = calculate(centroids,coordinates)

