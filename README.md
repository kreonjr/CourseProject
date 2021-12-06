# CS410 Course Project Readme

## Team: ***Topic Thunder***
## Project: UIUC CS410 Final Projects Filtering Web App

## Web App Url: https://topic-thunder-a7103.web.app/

<br>

This is a README that helps users get a sense of the project structure, provides instructions on to how to run the code, and describes its end result. For more details on the Techniques, Tools and Data used, please refer to the **Final Project Report** pdf in this Repo.

---

## Project Goal
We built this tool to help anyone that wants to skim through previous project submissions but doesn't want to have to click into every project to get a sense of the topic it might be focused on. This was accomplished by aggregating all github submissions, running some text preprocessing and cleaning, using Gensim to mine topics. Finally, we display the top topic terms as **Tags** to categorize projects and display them on a website.

---

## Project Structure
The project is split into 4 main folders.
- [python](#python)
- [topic-files](#topic-files)
- [web](#web)
- [firebase-functions](#firebase-functions)

### python
This folder contains all the python code related to data collection, data cleaning, topic modeling and database updating.
Each folder contains a README with instructions on how to run the code inside it, but here is what to run to collect fresh data and update the Web App:

```
> cd python/collect_data

> python clone_forks.py

> python get_project_text.py

> cd ../text_mining

> python text_cleaning.py

> python LDA.py

> cd ../firebase

> python uploadToFirebase.py (Requires api-key. See more details in 'python/firebase/' folder README)
```

### topic-files

This folder contains our evaluation files. Since the results of our project are user facing at the end, we had to find a way to do some manual evaluation. This is done by setting a ground truth sample, picking some projects and manually categorizing them under specific topics. Then when our output is generated, we manually went through the sample topics and rated the relevance of the algorithm compared to the ground truth file.

### web

The Web App for this project is already live and updates in real time as the Database is updated. The Web App is written in REACT and is built and deployed on Google's [Firebase Hosting](https://firebase.google.com/products/hosting) Platform. If you would like to run the Web App locally on your computer you just need to run the following commands:

```
> cd web
> yarn install
> yarn start
```

### firebase-functions

This folder contains the code of a cloud function created to update the realtime database on firebase. It is already hosted on firebase as a [firebase function](firebase-function) and it can be called as a RESTful API call to pass the topic mining output data to the database, to feed the Web App. This cloud function is called by the python script `uploadToFirebase.py`, to update the database with the latest output from the topic mining algorithm.