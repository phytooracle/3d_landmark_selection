# Singularity

## Installing Singularity
To installed Singularity run:

```bash
wget https://github.com/apptainer/singularity/releases/download/v3.8.7/singularity-container_3.8.7_amd64.deb && sudo apt install ./singularity-container_3.8.7_amd64.deb
```

To confirm that singularity was installed run:

```bash
singularity --version
```

## Download container
To download the landmark selection container run:

```bash
singularity build landmark_selection.simg docker://phytooracle/3d_landmark_selection:latest
```

You should now see a new file called ```landmark_selection.simg``` within your working directory.

## Running the container
First enable the xhost by running: 

```bash
xhost +local:root
```

Then, run the container:

```bash
singularity run -B $(pwd):/mnt --pwd /mnt landmark_selection.simg -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a
```

You should now see the container downloading data, and you will be prompted to select an RGB orthomosaic (select the closest date to the 3D scan data that you are landmark selecting).

# Docker Desktop on workstation

## Install 

Install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/files/latest/download) and set the following configuration:
![Alt text](figs/config1.png?raw=true "Title")\
![Alt text](figs/config2.png?raw=true "Title")\
![Alt text](figs/config3.png?raw=true "Title")\
![Alt text](figs/config4.png?raw=true "Title")\

## Run the container
To run the landmark selection container, run:

```bash
docker run -ti --rm -e DISPLAY=$DISPLAY -B $(pwd):/mnt --pwd /mnt landmark_selection.simg -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a
```