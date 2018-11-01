HEB Giphy App
=============

Greetings and welcome to the demo of the [GIPHY API](https://developers.giphy.com/docs/).

Requirements
------------

### Authentication

For user authentication, the application uses GitHub's OAuth implementation. You'll need to visit: https://github.com/settings/applications/new

You can specify whatever information you want for "Application Name" and "Homepage URL", however you must specify `http://localhost:8000/oauth/complete/github/`
for the "Authorization callback URL". Where `localhost` is the server that you're going to be hosting it on. If you're just following this README, that is
where it will be.

This will give you a `GITHUB_KEY` and `GITHUB_SECRET` that you'll put in the `app-config.env` file.

### GIPHY App

You'll need to register an app with GIPHY and get a token from them. To create an app, visit: https://developers.giphy.com/dashboard/?create=true

This will give you a `GIPHY_API_KEY` that you'll put in the `app-config.env` file.

### Environment file

We will need to take these acquired values and put them in `app-config.env`:

```
GIPHY_API_KEY=key_from_giphy
GITHUB_SECRET=secret_from_github
GITHUB_KEY=key_from_github
```

Ensure that this file remains next to the `docker-compose.yml` file.

Setup & Installation
--------------------

### Database

This application is configured to use sqlite3. This simplicity means that your database file lives in `db.sqlite3` next to the `docker-compose.yml` file. This will be mounted into the container later on.

If you do not have this file, be sure to create it:

```
touch db.sqlite3
```

### Building

This application is designed be run with `docker-compose`, so setup will require you to clone or download 
the repo somewhere, then to build run:

```
docker-compose build
```

This command will take a while to run, so be patient.

Running
-------

```
docker-compose up -d
```

The `-d` flag is optional. This signals that you don't want to stay attached to the container while it's running.

Usage
-----

The app is now running and can be viewed at http://localhost:8000
