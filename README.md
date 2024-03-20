# Moil Dash Camera

This is the application for demo Moil dash camera system.

## There are two ways to install the Dash Camera application. The first is to install the application for Users and the second is to install the application for Develop/ For more details, follow the methods below carefully.

### First step
- Download afk application

![ap](https://user-images.githubusercontent.com/60929939/207020441-0fdd915d-eeba-4040-bbba-0259d7cbe55d.PNG)
![app](https://user-images.githubusercontent.com/60929939/207020501-e6c3d510-77d9-410f-9522-bc02f3eac7dd.PNG)

- Make sure afk file on directory Download

![s](https://user-images.githubusercontent.com/60929939/207050383-78dc7a28-b484-405c-830c-5016c2014e3d.png)

- Open command terminal to install on directory Download

![appp](https://user-images.githubusercontent.com/60929939/207021938-9cd203e6-8bfd-4c6b-9886-e51b9b9cfc5c.PNG)

- Open Application

![apppp](https://user-images.githubusercontent.com/60929939/207022022-8349bb54-bfbd-4ef6-a734-6e60fe23bf37.PNG)

# Second Steps

### Before installation this application, as develop,  you should follow the command below:

1. Fork McutOIL/moil-dash-camera repository to your account

![1](https://user-images.githubusercontent.com/60929939/206126337-60830407-70f8-4755-ae95-eba422a34da2.PNG)

2. Uncheck branch-main (copy)

![2](https://user-images.githubusercontent.com/60929939/206126407-12bbaddf-6e47-465b-834b-fe85a7a29ffa.PNG)

3. Checked your fork

![3](https://user-images.githubusercontent.com/60929939/206126480-87b11360-8e4f-4744-8a5e-30aaa421b3a5.PNG)

### How to install !!!

#### - Clone this repository
- Complete clone repository including moilutils
```
git clone --recurse-submodules https://github.com/Herusyahputra/moil-dash-camera.git
```

#### - Create virtual environment
- Create VENV using python 3.7 or above
```commandline
python3 -m venv venv
```

- Activated the virtual environment
```commandline
source venv/bin/activate
```
- Install requirement

You can select the version of pyqt, its can use pyqt5 or pyqt6. bellow is installing requirement for pyqt6 
```commandline
pip install -r requirement_pyqt5.txt
```

- Run **main.py** in src directory
```commandline
python src/main.py
```
![1 run](https://user-images.githubusercontent.com/60929939/207047368-0ac57afa-4cc3-46c6-a1eb-ae7deeb70595.PNG)

- Input video sources
- Click setting **(gear icon)**

![2 ruun](https://user-images.githubusercontent.com/60929939/207047435-1a3fdd85-30ad-4149-9190-6097ad03fe9a.PNG)

- Select File
![3 runnn](https://user-images.githubusercontent.com/60929939/207047484-f2aa660b-ad19-448a-9868-bf5d2abeaa3d.PNG)

![8-](https://user-images.githubusercontent.com/60929939/206354481-831a8eab-4187-4f08-a11f-633259c02b42.PNG)

### Update submodule moilutils Package

```commandline
git submodule update --remote
```