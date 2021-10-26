import {initializeApp} from "firebase/app"
const firebaseConfig = {
    apiKey: "AIzaSyAostvuSXngPvPNOPQH3GMjvs-oWnDd3yI",
    authDomain: "topic-thunder-a7103.firebaseapp.com",
    databaseURL: "https://topic-thunder-a7103-default-rtdb.firebaseio.com",
    projectId: "topic-thunder-a7103",
    storageBucket: "topic-thunder-a7103.appspot.com",
    messagingSenderId: "109953830551",
    appId: "1:109953830551:web:0cec79697a56d4f52a23d2"
}

const app = initializeApp(firebaseConfig)
export const firebase = app
