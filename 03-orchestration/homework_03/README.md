# Homework 03

## Setup Instructions

Before beginning, run the `setup.sh` script to create the necessary folder and rename the environment file:

1. Make sure the `setup.sh` script is executable. If it is not, you can make it executable by running:
    ```bash
    chmod +x setup.sh
    ```

2. Run the `setup.sh` script from the terminal:
    ```bash
    ./setup.sh
    ```

This script will:
- Create a new folder called `artifacts` inside the `homework_03` directory.
- Rename the `homework.env` file in the current directory to `.env`.

This setup ensures that:
- The `artifacts` folder is created locally since it's ignored by `.gitignore` and not pushed to GitHub. We need this folder to log artifacts while working.
- The environment file is renamed to `.env` locally to be ignored by Git and correctly referenced by Docker Compose. The `homework.env` file is used in the repository to allow pushing to GitHub.

## Run the Project

To run the project after the setup, simply run `docker compose up`
