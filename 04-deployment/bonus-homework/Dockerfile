FROM mageai/mageai:latest

ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

# Set the MAGE_CODE_PATH variable to the path of the Mage code.
ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}"

# Set the USER_CODE_PATH variable to the path of user project.
# The project path needs to contain project name.
# Replace [project_name] with the name of your project (e.g. demo_project)
ENV USER_CODE_PATH=${USER_CODE_PATH}

WORKDIR ${USER_CODE_PATH}

COPY Pipfile Pipfile.lock ${USER_CODE_PATH}/

RUN pip install pipenv

RUN pipenv install --system --deploy

WORKDIR ${MAGE_CODE_PATH}