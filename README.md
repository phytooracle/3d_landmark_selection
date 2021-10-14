# 3d_landmark_selection
Repo for developing GUI for season 10 3D pseudo GCP selection.

```
git clone https://github.com/phytooracle/3d_psuedo_GCP_selection.git
git clone https://github.com/phytooracle/phytooracle_data
cd 3d_psuedo_GCP_selection.git
cp sample.env .env
```

Edit .env so that it points to where you put the phytooracle_data repo, *and* where you want to (or already do) store data.

## Conda install

```
conda create -n landmark_gui
conda activate landmark_gui
conda install python=3.7.11
conda install opencv-python
```

Go to http://www.open3d.org/docs/latest/getting_started.html and find the correct link under "Development version (pip)" and use it in the following command...,

```
conda install pip
pip install --pre https://storage.googleapis.com/open3d-releases-master/python-wheels/open3d-0.13.0+299f29e-cp37-cp37m-manylinux_2_27_x86_64.whl
```

```
conda install tifffile
conda install gdal
conda install pyproj
pip install python-dotenv
pip install imagecodecs
```


