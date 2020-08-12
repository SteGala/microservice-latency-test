# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

RUN apt-get update -y
RUN apt install python3-pip -y
RUN pip3 install selenium
RUN pip3 install flask

RUN apt-get install wget -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

ADD main.py .
ADD test.py .
ADD chromedriver .

EXPOSE 5000

CMD ["python", "main.py"]
