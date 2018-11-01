FROM labhackercd/alpine-python3-nodejs:latest

MAINTAINER Stephen Golub "stephen@golub.io"

RUN npm install -g @angular/cli

# Putting this here to short-circuit if pip fails to install.
RUN pip3 install --upgrade pip

COPY ./ /app/

WORKDIR /app/hebgiphy/ui/angular-pkg

RUN rm -rf node_modules
RUN npm install
RUN ng build

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN ./manage.py collectstatic; \
    ./manage.py makemigrations

EXPOSE 8000

CMD [ "./start.sh" ]
