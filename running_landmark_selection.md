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

## Troubleshooting

### Trob
Running GUI apps on Windows 10 WSL2 can result in errors. If you get an ```xhost:  unable to open display ""``` error after running the xhost command on Windows 10 WSL2 or cannot get the landmark selection GUI running, do the following:

1. Follow the steps [here](https://aalonso.dev/blog/how-to-use-gui-apps-in-wsl2-forwarding-x-server-cdj).
2. Add the line ```export DISPLAY="`grep nameserver /etc/resolv.conf | sed 's/nameserver //'`:0"``` to your ```~/.bashrc``` file.
3. Open Powershell or Command Prompt and run ```wsl --shutdown```.
4. Open your WSL2 terminal and run the singularity command as: ```singularity run --env LIBGL_ALWAYS_INDIRECT=0 -B $(pwd):/mnt --pwd /mnt landmark_selection.simg -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a```.

<!-- * Install one of the WSL2-compatible GPU drivers for your computer:
    * [Intel](https://www.intel.com/content/www/us/en/download/19344/intel-graphics-windows-dch-drivers.html)
    * [AMD](https://www.amd.com/en/support/kb/release-notes/rn-rad-win-wsl-support)
    * [NVIDIA](https://developer.nvidia.com/cuda/wsl)

> **_NOTE:_** For more information on WSLg requirements refer to the [WSLg documentation](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

* Once done, open Powershell or Command prompt and run ```wsl --shutdown```
* Try the steps above again -->

# Option 2 | Docker Desktop on Windows or MacOS

## Windows

### Install X server

Install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/files/latest/download).

### Start XLaunch - Windows
Open XLaunch on Windows or XQuartz on MacOS and set the following configuration:

![Alt text](figs/config1.png?raw=true "Title") <br/>
![Alt text](figs/config2.png?raw=true "Title") <br/>
![Alt text](figs/config3_up.png?raw=true "Title") <br/>
![Alt text](figs/config4.png?raw=true "Title") <br/>

> **_NOTE:_** You will have to start XLaunch every time that you shutdown your computer and try to run landmark selection again. It does not autolaunch at startup. If you do not have XLaunch running, the container will not launch.

### Find IP address

Open Powershell on Windows or Terminal on MacOS and find your IP address by running:

```powershell
ipconfig
```

> **_NOTE:_** The IP address will be the one labeled IPv4 Address.

![Alt text](figs/ip.png?raw=true "Title") <br/>

Let's assume that our IPv4 IP address is ```150.135.43.208```, we would then use the DISPLAY value of ```150.135.43.208:0.0``` below.

### Run the container
To run the landmark selection container, run the following command in Powershell:

```powershell
docker run -ti --rm --env DISPLAY=150.135.43.208:0.0 --env LIBGL_ALWAYS_INDIRECT=0 phytooracle/3d_landmark_selection -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a
```

> **_NOTE:_** If the container does not launch, check that: (i) confirm that XLaunch is running, (ii) run ```xhost +local:root``` and try again, (iii) confirm that you set the correct IP address within the DISPLAY variable in your Docker command, or (iv) close Powershell and restart using Adminstrator Mode.

## MacOS

### Install X server

Install [XQuartz](https://github.com/XQuartz/XQuartz/releases/download/XQuartz-2.8.5/XQuartz-2.8.5.pkg).

### Start XQuartz
Search for and open the XQuartz application. At the top left of your screen, click on XQuartz > Preferences > Security and set the following configuration:

![Alt text](figs/mac1.png?raw=true "Title") <br/>

### Find IP address

Open a terminal and run:

```mac
ifconfig en1
```

Find the row labeld ```inet``` and copy the IP address. Let's assume that our address is ```10.161.215.174```.

### Run the container
To run the landmark selection container, run the following command in Powershell:

```mac
docker run -ti --rm --env DISPLAY=10.161.215.174:0 --env LIBGL_ALWAYS_INDIRECT=0 --privileged phytooracle/3d_landmark_selection -s 2022-02-11__19-59-49-338_lettuce -S 13 -p lettuce -a
```