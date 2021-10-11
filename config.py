import sys

class Config(object):
    def __init__(self, season=10):

        try:
            import dotenv
            env_file = dotenv.find_dotenv()
            dotenv.load_dotenv(env_file)
            parsed_dotenv = dotenv.dotenv_values()
            phytooracle_data_library_path  = parsed_dotenv["phytooracle_data_library_path"]
            # settings['result'] = parsed_dotenv["results_dir"]
        except ModuleNotFoundError:
            print("[FATAL]")
            print("You need to install dotenv")
            print("pip install python-dotenv")
            sys.exit(0)
        except KeyError:
            print("[FATAL]")
            print("We didn't find (or we didn't find what we expected in) your .env file")
            print("Please see README.md regarding .env")
            sys.exit(0)

       
        # Load phytooracle_data package
        try:
            sys.path.append(phytooracle_data_library_path)
            import phytooracle_data.scanner3dTop as scanner3dTop
            import phytooracle_data.stereoTop as stereoTop
            import phytooracle_data.rgb as rgb
        except ModuleNotFoundError:
            print("[FATAL]")
            print(phytooracle_data_library_path)
            print("You need to install phytooracle_data (and tell me where it is with .env)")
            print("https://github.com/phytooracle/phytooracle_data")
            sys.exit(0)
    
        self.ortho     = stereoTop.Ortho(season=season)
        self.three_dee = scanner3dTop.Scanner3dTop(season=season)
        self.rgb       = rgb.RGB_Data(season=season)

        self.dotenv = parsed_dotenv


