from json import load
from cv2 import boundingRect
from utils import *
from data import *
from config import Config

def main():

    #orth_path = '/home/ariyan/Desktop/LandmarkSelection/2020-03-01_ortho_10pct_cubic.tif'

    #season = 10
    conf = Config()
    #date = "2020-03-01"
    orth_path = conf.ortho.get_ortho_for_date(conf.args.scan)

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
