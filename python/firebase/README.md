# Uploading data to Firebase

## Overview

The script here is the final step to update the WebApp with the output found in `python/text_mining/firebase-output.json`

## Requirements

The scripts were tested and run in Python 3.8.12 but should work with other 3.8.x versions just as well.

Python packages used:
* requests 2.26.0

## Scripts

### `uploadToFirebase.py`

Reads the content of the file `firebase-output.json` and uploads it the [Firebase Real-Time Database](https://firebase.google.com/docs/database) instance tied to our team. Once there, our WebApp is coded to listen to any changes to the database and re-render with the updated information.

#### Output

* `Database updated`: Success Message