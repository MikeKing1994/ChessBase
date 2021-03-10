# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# Install chocolatey
#COPY powershell.exe .
#RUN powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
#RUN choco feature enable -n allowGlobalConfirmation
#RUN dpkg -i firefox
#RUN apt-get -y install firefox
COPY firefox.exe .

# copy the dependencies file to the working directory
COPY requirements.txt .

# Install Firefox
#RUN choco install firefox --version 86.0

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .
ADD geckodriver/geckodriver.exe /geckodriver/geckodriver.exe

# command to run on container start
CMD [ "python", "./main.py" ]