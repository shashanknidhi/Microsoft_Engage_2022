# Facial Recognition Based Passenger Boarding System

#### Project Description:
Main functionality of this project is to generate boarding pass of a passenger at check-in counter. 
This works in such a way that when a passenger approaches the check-in counter his/her image is captured by camera installed there,
then using face detection and recognition technology E-Ticket No. of the passenger is displayed on the frame and on the basis of which boarding pass will be generated.

Other functionalities this project has, are:
1.	Add & display passenger details.
2.	Add & display flight details.

But the image for training purpose should be directly uploaded to the dataset/ directory inside the project folder.

For the purpose of facial recognition, a python library called face_recognition, dlib, and opencv_python are used.

To stream the image framer imutils is used. 

Backend is built using django framework of python where SQLite being used for database. 

For frontend design part of the webapp, HTML5,CSS3 and JS are used.


## Steps to run this web application on your local system(Windows):
1. Clone github repo to local system : 
   - Open Windows Powershell or Command Prompt or Git Bash CLI.
   - Go to the directory where you want to clone the github repo.
   - Run the command below to clone repo:
    ```
    git clone https://github.com/shashanknidhi/Microsoft_Engage_2022.git
    ```
2. Set up  Python Virtual Environment:
   - Go to root directory of the project.
   ```
   cd Microsoft_Engage_2022
   ```
   - Enter the command to create a virtual environment:
    ```
    python -m venv project
    ```
   - Activate the virtual environment:
    ```
    project\Scripts\activate.bat
    ```
    Now your terminal should look like:
    ```
    (project) C:/.....
    ```
 3.	Complete pre-requisites  for downloading face_recognition library of python:
    - Download Microsoft Visual Studio 2019 with C/C++ compiler installed.
    - Of course, python3 should be there.
    - Download [Cmake](https://cmake.org/download/) and it to your system environment variables.
    - Download Dlib and face_recognition using the command below or else you can do this in the next step:
      ```
      pip install dlib
      pip install face-recognition
      ```
      In case of any issue, consult this page : https://github.com/ageitgey/face_recognition/issues/175#issue-257710508
4. Install requirements :
    ```
    pip install -r requirements.txt
    ```
5. Go to the 'facial_recognition' directory:
    ```
    cd facial_recognition
    ```
6. Run the following command to run django app.
   ```
   python manage.py runserver
   ```


    
  
  
