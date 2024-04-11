FROM python:3.10-slim
ARG user
ARG password
ADD requirements.lock /
RUN pip install --upgrade --extra-index-url https://$user:$password@distribution.livetech.site -r /requirements.lock
ADD . /streaming_services
ENV PYTHONPATH=$PYTHONPATH:/streaming_services
WORKDIR /streaming_services/streaming_services/services
CMD python services.py
