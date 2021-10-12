import pdb
from json import load
from cv2 import boundingRect
from utils import *
from data import *
from config import Config

def main():

    conf = Config() # This contains command line arguments, and phytooracle_data classes.

    #orth_path = '/home/ariyan/Desktop/LandmarkSelection/2020-03-01_ortho_10pct_cubic.tif'
    #down_sampled_merged_path = "/home/ariyan/Desktop/LandmarkSelection/2020-02-29_merged_downsampled_preprocessed/merged_downsampled"
    #meta_path = "/home/ariyan/Desktop/LandmarkSelection/2020-02-29_metadata/metadata"
    transformation_path = "/home/ariyan/Desktop/LandmarkSelection/season_10_lettuce_yr_2020/level_1/scanner3DTop/2020-03-01/preprocessing/transfromation.json"

    valid_ortho_dates = conf.ortho.get_dates()

    if conf.args.scan not in valid_ortho_dates:
        print(f"Didn't find {conf.args.scan} in the current season ortho scan dates.")
        from phytooracle_data import find_nearest_date
        nearest_date = find_nearest_date(valid_ortho_dates, conf.args.scan)
        rgb_date = nearest_date.strftime("%Y-%m-%d")
        print(f"  ... We will use this date instead: {conf.args.scan}")
    else:
        rgb_date = conf.args.scan
    
    orth_path = conf.ortho.get_ortho_for_date(rgb_date)
    meta_path = conf.three_dee.get_preprocessed_metadata_for_date(conf.args.scan)
    down_sampled_merged_path = conf.three_dee.get_preprocessed_downsampled_merged_for_date(conf.args.scan)

    meta_dict = read_and_transform_all_pcd_boundaries(meta_path)
    boundaries = read_tags(orth_path)
    ortho = load_ortho(orth_path)
    ortho = down_scale_ortho(ortho,0.3)
    list_matched_points = visualize_ortho_get_point_pairs(ortho,boundaries,meta_dict,down_sampled_merged_path)

    T = estimate_transformation(list_matched_points)
    if T is not None:
        save_transformation(T,transformation_path)
    else:
        print(":: Unable to estimate transformation. Try again with more scatter points. ")
    # upload happens here

if __name__ == "__main__":
    main()

