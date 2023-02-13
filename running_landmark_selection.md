# Option 1 | Singularity

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

# Option 2 | Docker Desktop on Windows or MacOS

## Install 

Install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/files/latest/download) and set the following configuration:

## Start XLaunch

![Alt text](figs/config1.png?raw=true "Title") <br/>
![Alt text](figs/config2.png?raw=true "Title") <br/>
![Alt text](figs/config3.png?raw=true "Title") <br/>
![Alt text](figs/config4.png?raw=true "Title") <br/>

> **_NOTE:_** You will have to start XLaunch every time that you shutdown your computer and try to run landmark selection again. It does not autolaunch at startup. If you do not have XLaunch running, the container will not launch.

## Set IP address

Open Powershell or Command Prompt in <b>Administrator Mode</b> and find your IP address by running:

```powershell
ipconfig
```

> **_NOTE:_** The IP address will be the one labeled IPv4 Address.

![Alt text](figs/ip.png?raw=true "Title") <br/>

Let's assume that our IPv4 IP address is ```150.135.43.208```, we would then use the DISPLAY value of ```150.135.43.208:0.0``` below.

## Run the container
To run the landmark selection container, run the following command in Powershell:

```powershell
docker run -ti --rm --env DISPLAY=150.135.43.208:0.0 phytooracle/3d_landmark_selection -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a
```

> **_NOTE:_** If the container does not launch, check that: (i) confirm that XLaunch is running, (ii) run ```xhost +local:root``` and try again, (iii) confirm that you set the correct IP address within the DISPLAY variable in your Docker command, or (iv) close Powershell and restart using Adminstrator Mode.