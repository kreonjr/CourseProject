# Uploading data to Firebase

## Overview

The script here is the final step to update the WebApp with the output found in `python/text_mining/firebase-output.json`

## Requirements

The scripts were tested and run in Python 3.8.12 but should work with other 3.8.x versions just as well.

Python packages used:
* requests 2.26.0
* python-dotenv 0.19.2

---

<span style="color:red">__Important Note!!__</span>

For security reasons (*mainly so that not everyone can write to our database*), you will also need to create a file called `.env` in the same folder as this __README__, which will contain the firebase api key to update the database. If you want to test our database upload system, please reach out and we will be more than happy to share the key with you.

Example .env:
```
UPLOAD-API-KEY=******
```

---

## Scripts

### `uploadToFirebase.py`

Reads the content of the file `firebase-output.json` and uploads it the [Firebase Real-Time Database](https://firebase.google.com/docs/database) instance tied to our team. Once there, our WebApp is coded to listen to any changes to the database and re-render with the updated information.

#### Output

* `Database updated`: Success Message