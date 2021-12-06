const functions = require("firebase-functions")
const admin = require("firebase-admin");

const firebaseConfig = {
  apiKey: "AIzaSyAostvuSXngPvPNOPQH3GMjvs-oWnDd3yI",
  authDomain: "topic-thunder-a7103.firebaseapp.com",
  databaseURL: "https://topic-thunder-a7103-default-rtdb.firebaseio.com",
  projectId: "topic-thunder-a7103",
  appId: "1:109953830551:web:0cec79697a56d4f52a23d2"
}

admin.initializeApp(firebaseConfig)
const db = admin.database();

exports.updateDatabase = functions.https.onRequest((request, response) => {
  if (request.headers["x-api-key"] !== functions.config().upload.key) {
    response.status(401).send("Unauthorized");
  } else {
    if (!request.body || Object.keys(request.body).length == 0) {
      response.status(400).send("Database data missing or empty")
    } else {
      const {topics, dropTags} = request.body
      db.ref("topics").set(topics).then(() => {
        return db.ref("drop_tags").set(dropTags)
      }).then(() => {
        response.status(200).send("Database updated");
      }).catch((error) => {
        response.send(error)
      })
    }
  }
})
