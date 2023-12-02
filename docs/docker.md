# Running in Docker

1. Build the Docker image:

```
docker compose build
```

This shouldn't fail. If it does, please open a Github issue detailing your environment and docker compose log.

2. Configure the application: this is exactly the same as it is done when running locally. Copy .sample.env to a file called .env, and fill in the values following the instructions from the main README. Once all values are set, we are ready to run the app.

3. Start the app inside a Docker container:

```
docker compose up
```

This will load the values in the local .env file into the container and use them to run the app. Log messages will be sent to the terminal.
