from json import load
from cv2 import boundingRect
from utils import *
from data import *

def main():

    # test functions here, not the finalized code...

    orth_path = '/home/ariyan/Desktop/LandmarkSelection/2020-03-01_ortho_10pct_cubic.tif'
    boundaries = read_tags(orth_path)
    print(get_gps_distance(boundaries['UL'],boundaries['UR']))
    print(get_gps_distance(boundaries['UL'],boundaries['LL']))
    ortho = load_ortho(orth_path)
    visualize_ortho_get_point_pairs(ortho,boundaries)

    # need to download these using phytooracle_data

    # get 3d scan date from user as input
    # download and untar merged_downsampled tar file from cyverse
    # download closest RGB 10% ortho
    # download preprocessing_metadata tar file from cyverse and untar
    

if __name__ == "__main__":
    main()