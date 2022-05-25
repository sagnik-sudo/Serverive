- `python -m virtualenv "venv"`
- `./venv/Scripts/activate`

# Serverive

## Description

Storage Module for the pro user.

## Steps to start

1. Enable Virtual Environment

    ``` virtualenv venv ```

    ``` source venv/bin/activate ```

2. Install dependencies

    ``` pip install -r requirements.txt ```

3. Run the tool

    ```python start.py```

4. Open the browser and go to <http://localhost:7777/serverive>

_You are good to go!_

## Prerequisites

1. Install below packages
    - Install Python `3.10.4` or above from <https://www.python.org/downloads/>
    - Install `pip` from <https://pip.pypa.io/en/stable/>
    - Install `virtualenv` from <https://virtualenv.pypa.io/en/stable/>
    - Install `MinIO` from <https://docs.min.io/docs/minio-quickstart-guide.html>

2. Host Minio on Port `9000` in own server or server of your choice.
    - Host Guide: <https://docs.min.io/docs/minio-quickstart-guide.html>

        - Linux:

            ```
            wget https://dl.min.io/server/minio/release/linux-amd64/minio
            chmod +x minio
            ./minio server /data
            ```

        - Windows:

            ```
            wget https://dl.min.io/server/minio/release/windows-amd64/minio.exe
            chmod +x minio.exe
            ./minio.exe server /data
            ```

3. Modify MinIO Host Details in `src/config.py`

## Maintainer

Name: [Sagnik Das](https://github.com/sagnik-sudo)

Email: [sagnikdas2305@gmail.com](sagnikdas2305@gmail.com)

## Suggestions are welcome

For suggestions and contributions, please visit [here](https://github.com/sagnik-sudo/Serverive/issues)

If you like my work, please star it on [here](https://github.com/sagnik-sudo/Serverive)
