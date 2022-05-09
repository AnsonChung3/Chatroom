FROM python:3
WORKDIR D/Coding/FrontBackCombinedProto/back
RUN pip install aiohttp
RUN pip install aiohttp_cors
COPY *.py .

# This allows the port 8080 to talk outside of this container
# By default this only allows it to talk to other docker containers
# If you want to connect to it from outside the container, use the following when running docker:
#   docker run -d -p <port>:8080 <image id>
# That says "when I go to port <port>, forward that request to 8080 on the docker image"
# this is set up with frontend running on 8080 in mind
EXPOSE 8080

CMD [ "python", "./app.py" ]
