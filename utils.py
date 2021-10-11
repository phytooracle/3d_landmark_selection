import tifffile
import cv2
import gdal
import math

def load_ortho(path):
    img = tifffile.imread(path)
    img[:,0], img[:,2] = img[:,2], img[:,0]
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

def visualize_ortho(ortho):
    cv2.namedWindow("Ortho")
    cv2.resizeWindow("Ortho",200,100)
    cv2.imshow("Ortho",ortho)
    cv2.waitKey(0)