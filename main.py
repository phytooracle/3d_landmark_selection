from json import load
from cv2 import boundingRect
from utils import *
from data import *
from config import Config

def main():

    #orth_path = '/home/ariyan/Desktop/LandmarkSelection/2020-03-01_ortho_10pct_cubic.tif'

    season = 10
    conf = Config(season)
    date = "2020-03-01"
    orth_path = conf.ortho.get_ortho_for_date(date)

    boundaries = read_tags(orth_path)
    print(get_gps_distance(boundaries['UL'],boundaries['UR']))
    print(get_gps_distance(boundaries['UL'],boundaries['LL']))
    ortho = load_ortho(orth_path)
    visualize_ortho(ortho)

if __name__ == "__main__":
    main()
