# My Flask Application

This is a simple Flask application deployed in a container.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed Podman or Docker on your machine. 

## Building the Container

To build the container for this Flask application, follow these steps:

1. **Open your terminal** and navigate to the root directory of this project where the `Containerfile` is located.

2. **Run the build command**. Replace `my-flask-app` with your desired Docker image name:

    ```bash
    podman build -t flaskjakt .
    docker build -t flaskjakt .
    ```

    This command builds a image named `flaskjakt` using the `Containerfile` in the current directory.

3. **Wait for the build to complete**. 

## Running the Docker Container

After building the image, run the container with the following command:

```bash
docker run -p 5000:5000 flaskjakt
```

This command maps port 5000 on your host machine to port 5000 in the container, allowing you to access the Flask application via http://localhost:5000.

