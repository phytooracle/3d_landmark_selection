import tifffile
import cv2
import gdal
import math

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
        param['list_points'].append(gps)
        

def get_GPS_location(point,boundaries,w,h):
    GPS_height = boundaries['UL'][1]-boundaries['LL'][1]
    GPS_width = boundaries['UR'][0]-boundaries['UL'][0]
    
    return point[0]*GPS_width/w+boundaries['UL'][0],boundaries['UL'][1]-point[1]*GPS_height/h

def visualize_ortho_get_point_pairs(ortho,boundaries):
    
    cv2.namedWindow("Ortho", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
    
    params = {'boundaries':boundaries,'width':ortho.shape[1],'height':ortho.shape[0],'list_points':[]}
    
    cv2.setMouseCallback("Ortho",get_mouse_position,params)
    
    while True:
        cv2.imshow("Ortho",ortho)
        res = cv2.waitKey(0)
        print(params['list_points'])

        if res == 113:
            break
    

    