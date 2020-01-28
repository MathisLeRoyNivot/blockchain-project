FROM python:3

RUN mkdir /app
WORKDIR /app
COPY requirements.txt blockchain.py assets/Maupassant_Bel_Ami.pdf /app/
ENV FLASK_APP=blockchain.py

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 5000

CMD [  "python", "blockchain.py" ]