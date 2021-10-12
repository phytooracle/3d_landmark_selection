import tifffile
import cv2
import gdal
import math
import os
import glob
import json
import numpy as np
import open3d as o3d
from pyproj import Proj,transform
proj_4326 = Proj(init='epsg:4326')
proj_2151 = Proj(init='epsg:2152')

def load_pcd(path):
    pcd = o3d.io.read_point_cloud(path,format="ply")
    return pcd

def utm_to_latlon(easting, northing):
    lon, lat = transform(proj_2151,proj_4326,easting,northing)
    return lon,lat

def latlon_to_utm(lon,lat):
    easting,northing = transform(proj_4326,proj_2151,lon,lat)
    return easting,northing

def load_ortho(path):
    img = tifffile.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img

def down_scale_ortho(ortho,scale):
    image = cv2.resize(ortho,(int(ortho.shape[1]*scale),int(ortho.shape[0]*scale)))
    return image

def read_tags(path):

    ds = gdal.Open(path)
    meta = gdal.Info(ds)
    lines = meta.splitlines()

    for line in lines:
        if 'Upper Left' in line:
            u_l = line.split()[2:4]
            u_l[0] = u_l[0].replace('(','').replace(',','')
            u_l[1] = u_l[1].replace(')','')
        if 'Lower Left' in line:
            l_l = line.split()[2:4]
            l_l[0] = l_l[0].replace('(','').replace(',','')
            l_l[1] = l_l[1].replace(')','')
        if 'Upper Right' in line: 
            u_r = line.split()[2:4]
            u_r[0] = u_r[0].replace('(','').replace(',','')
            u_r[1] = u_r[1].replace(')','')
        if 'Lower Right' in line:
            l_r = line.split()[2:4]
            l_r[0] = l_r[0].replace('(','').replace(',','')
            l_r[1] = l_r[1].replace(')','')
        if 'Center' in line:
            c = line.split()[1:3]
            c[0] = c[0].replace('(','').replace(',','')
            c[1] = c[1].replace(')','')

    upper_left = (float(u_l[0]),float(u_l[1]))
    lower_left = (float(l_l[0]),float(l_l[1]))
    upper_right = (float(u_r[0]),float(u_r[1]))
    lower_right = (float(l_r[0]),float(l_r[1]))
    center = (float(c[0]),float(c[1]))
    coord = {'UL':upper_left,'LL':lower_left,'UR':upper_right,'LR':lower_right,'C':center}
    
    return coord

def get_gps_distance(p1,p2):
    lon1,lat1 = p1
    lon2,lat2 = p2

    phi1 = math.radians(lat1)
    lambda1 = math.radians(lon1)
    phi2 = math.radians(lat2)
    lambda2 = math.radians(lon2)
    R = 6371e3

    a = math.sin((phi2-phi1)/2)**2+math.cos(phi1)*math.cos(phi2)*(math.sin((lambda2-lambda1)/2)**2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))

    return R*c

def get_mouse_position(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        gps = get_GPS_location([x,y],param['boundaries'],param['width'],param['height'])
        gps = latlon_to_utm(gps[0],gps[1])
        close_by_pcds = get_list_pcd_close_to_point(gps,param['meta_dict'])
        if len(close_by_pcds)>0:
            selected_3d_point = visualize_pcds(close_by_pcds,param['pcd_path'])
            if selected_3d_point is not None:
                apprx = transform_point_to_GPS((selected_3d_point[0],selected_3d_point[1],1))
                matched_point = {'correct_gps':gps,'3d_coord':selected_3d_point[:2],'approximate_gps':apprx}
                print(matched_point)
                param['list_points'].append(matched_point)
        
def get_GPS_location(point,boundaries,w,h):
    GPS_height = boundaries['UL'][1]-boundaries['LL'][1]
    GPS_width = boundaries['UR'][0]-boundaries['UL'][0]
    
    return point[0]*GPS_width/w+boundaries['UL'][0],boundaries['UL'][1]-point[1]*GPS_height/h

def draw_3d_boundaries_on_ortho(ortho,boundaries,meta_dict):
    UL = latlon_to_utm(*boundaries['UL'])
    UR = latlon_to_utm(*boundaries['UR'])
    LL = latlon_to_utm(*boundaries['LL'])
    LR = latlon_to_utm(*boundaries['LR'])

    gps_height = UL[1] - LL[1]
    gps_width = UR[0] - UL[0]
    height = ortho.shape[0]
    width = ortho.shape[1]
    
    up = LL[1]
    down = UL[1]
    left = UL[0]
    right = UR[0]

    for folder in meta_dict:
        gps = meta_dict[folder]['gps_boundaries']
        up = min(UL[1],max(up, gps['NW'][1]+0.5))
        down = max(LL[1],min(down, gps['SE'][1]-0.5))
        right = min(right, gps['NE'][0])
        left = max(left, gps['NW'][0])

    
    p1 = (int((left-UL[0])*width/gps_width),int((UL[1]-up)*height/gps_height))
    p2 = (int((right-left)*width/gps_width)+p1[0],int((up-down)*height/gps_height)+p1[1])
    
    overlay = ortho.copy()
    cv2.rectangle(ortho,p1,p2,(0,0,255),40)
    cv2.rectangle(overlay,p1,p2,(150,150,150),-1)
    ortho = cv2.addWeighted(overlay, 0.3, ortho, 0.7, 0)

    return ortho

def visualize_pcds(pcd_names,pcds_path):
    print(f":: Visualizing {len(pcd_names)} PCDs. ")
    pcd = o3d.geometry.PointCloud()
    points = []
    for folder in pcd_names:
        pcd_path = glob.glob(os.path.join(pcds_path,folder,"*.ply"))[0]
        points.append(np.array(load_pcd(pcd_path).points))
    pcd.points = o3d.utility.Vector3dVector(np.vstack(points))
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run() 
    vis.destroy_window()

    selected_index = vis.get_picked_points()
    if len(selected_index) == 1:
        return np.array(pcd.points)[selected_index[0]]

def visualize_ortho_get_point_pairs(ortho,boundaries,meta_dict,pcd_path):
    
    cv2.namedWindow("Ortho", cv2.WINDOW_GUI_EXPANDED)
    cv2.setWindowProperty("Name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
    cv2.resizeWindow("Ortho",500,1000)

    params = {'boundaries':boundaries,'width':ortho.shape[1],'height':ortho.shape[0],'list_points':[],'meta_dict':meta_dict,'pcd_path':pcd_path}
    
    cv2.setMouseCallback("Ortho",get_mouse_position,params)
    
    ortho = draw_3d_boundaries_on_ortho(ortho,boundaries,meta_dict)

    while True:
        cv2.imshow("Ortho",ortho)
        res = cv2.waitKey(0)
        print(params['list_points'])

        if res == 113:
            break
    
def transform_point_to_GPS(point):
    T = np.array([[9.92386804e-04,8.28480420e-06,4.08975523e+05],[7.04730386e-06,9.35075874e-04,3.65996863e+06]])
    transformed_point = np.matmul(T,point)
    return transformed_point

def transform_boundaries(boundaries):
    SW = [boundaries['mins'][0],boundaries['mins'][1],1]
    NE = [boundaries['maxs'][0],boundaries['maxs'][1],1]
    NW = [boundaries['mins'][0],boundaries['maxs'][1],1]
    SE = [boundaries['maxs'][0],boundaries['mins'][1],1]

    SW = transform_point_to_GPS(SW)
    NE = transform_point_to_GPS(NE)
    NW = transform_point_to_GPS(NW)
    SE = transform_point_to_GPS(SE)

    return {"SW":SW,"NE":NE,"NW":NW,"SE":SE}

def read_and_transform_all_pcd_boundaries(meta_path):
    pcd_GPS_boundaries = {}
    folders = os.listdir(meta_path)

    for folder in folders:
        meta_json_path = glob.glob(os.path.join(meta_path,folder,"*.json"))[0]
        with open(meta_json_path,"r") as f:
            metadata = json.load(f)
            metadata["gps_boundaries"] = transform_boundaries(metadata['boundaries'])
            pcd_GPS_boundaries[folder] = metadata

    return pcd_GPS_boundaries

def get_list_pcd_close_to_point(point,metadata_dict):
    folders = []
    for folder in metadata_dict:
        meta = metadata_dict[folder]
        if point[0]>meta['gps_boundaries']['SW'][0] and point[0]<meta['gps_boundaries']['NE'][0] and\
            point[1]>meta['gps_boundaries']['SW'][1] and point[1]<meta['gps_boundaries']['NE'][1]:
            folders.append(folder)

    return folders