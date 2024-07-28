## XML Conversion App

## FastAPI application for XML conversion according to a stylesheet.

## Quick Overview

This simple app aims to export annotations by communicating with the Rossum API, converting its XML response, sending it to a dummy endpoint, and finally returning a JSON response indicating whether the entire pipeline was successful.

## Method

I approached this task as a prototype, aiming for a quick, near-production state to prove the business need. The approach was kept plain yet solid, providing a base open to adjustments:

- Unified to async if needed
- Redis as cache, which can also be used if the app is horizontally scaled
- Docker-compose for local development

## API

- POST /export/<queue-id>/<annotation-id> (with Authorization: Basic <username
  base64 hash>)
- Returns JSON response: {"success": bool}

## Environment Variables

- Environment variables should be defined in a .env file. Feel free to use the provided example.

## How To

- You can run the app locally with both uvicorn and gunicorn servers using make commands if on a Unix-based system.
- Docker-compose is also available, including both the app and Redis.

## TODO

- Basic Auth should be reconsidered for a more production-suitable solution (JWT is both easy and quick to set up).
- Gunicorn is used in the dockerized version with gunicorn.conf.py as an example config.
- Redis is used as the go-to cache solution, but this may be reconsidered depending on needs.
- The app mixes async and sync methods, which should be unified before any storage is introduced.
- More tests are needed.
