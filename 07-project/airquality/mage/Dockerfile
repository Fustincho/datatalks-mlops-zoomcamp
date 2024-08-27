FROM mageai/mageai:0.9.73

ENV PROJECT_NAME=mage
ENV MAGE_CODE_PATH=/home/src
ENV USER_CODE_PATH=/home/src/mage

# Set the MAGE_CODE_PATH variable to the path of the Mage code.
ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}"

WORKDIR ${MAGE_CODE_PATH}

COPY . ${USER_CODE_PATH}/

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

CMD [ "mage", "start", "mage" ]