from os import scandir
import pdb, sys
from json import load
from cv2 import boundingRect
from utils import *
from config import Config

def main():

    conf = Config() # This contains command line arguments, and phytooracle_data classes.

    #orth_path = '/home/ariyan/Desktop/LandmarkSelection/2020-03-01_ortho_10pct_cubic.tif'
    #down_sampled_merged_path = "/home/ariyan/Desktop/LandmarkSelection/2020-02-29_merged_downsampled_preprocessed/merged_downsampled"
    #meta_path = "/home/ariyan/Desktop/LandmarkSelection/2020-02-29_metadata/metadata"
    #transformation_path = "/home/ariyan/Desktop/LandmarkSelection/season_10_lettuce_yr_2020/level_1/scanner3DTop/2020-03-01/preprocessing/transfromation.json"
    #transformation_path = "/media/ariyan/Data/University/IVILAB/Phytooracle/Phytooracle_data/season_10_lettuce_yr_2020/level_1/scanner3DTop/2020-02-29/preprocessing/transformation.json"

    if conf.args.season == 10:
        scan_date = conf.args.scan
    if conf.args.season == 11:
        scan_date = conf.args.scan
    elif conf.args.season == 12:
        scan_date = conf.args.scan
    
    valid_ortho_dates = conf.ortho.get_dates()

    if scan_date not in conf.three_dee.get_dates():
        print()
        print("ERROR: Invalid date selected.  No 3d scan found for that date")
        print("Here is a list of valid dates...")
        print(conf.three_dee.get_dates())
        sys.exit(0);

    if conf.args.season == 10 or conf.args.season == 11:
        if scan_date not in valid_ortho_dates:
            print(f"Didn't find {scan_date} in the current season ortho scan dates.")
            from phytooracle_data import find_nearest_date
            nearest_date = find_nearest_date(valid_ortho_dates, scan_date)
            rgb_date = nearest_date.strftime("%Y-%m-%d")
            print(f"    We will use this date instead: {rgb_date}")
        else:
            rgb_date = scan_date
    elif conf.args.season == 12:
        rev_ortho_dates = [d.split("__")[0] for d in valid_ortho_dates]
        rev_scan_date = scan_date.split("__")[0]
        
        if rev_scan_date not in rev_ortho_dates:
            print(f"Didn't find {rev_scan_date} in the current season ortho scan dates.")
            from phytooracle_data import find_nearest_date
            nearest_date = find_nearest_date(valid_ortho_dates, rev_scan_date)
            rgb_date = nearest_date.strftime("%Y-%m-%d")
            print(f"    We will use this date instead: {rgb_date}")
        else:
            rgb_date = [d for d in valid_ortho_dates if d.split("__")[0] == rev_scan_date]
            rgb_date = rgb_date[0]
 
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
        local_transformation_json_file = conf.three_dee.local_preprocessing_transformation_json_file_path(conf.args.scan)
        save_transformation(T,local_transformation_json_file, conf)
        conf.three_dee.upload_transformation_json_file(conf.args.scan, local_transformation_json_file)
    else:
        print(":: Unable to estimate transformation. Try again with more scatter points. ")
    # upload happens here

if __name__ == "__main__":
    main()

