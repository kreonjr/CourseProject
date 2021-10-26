import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { firebase } from "./shared/firebaseConfig"
import { getDatabase, ref, child, get } from "firebase/database";

function App() {

  const [data, setData] = useState({})

  useEffect(() => {
    const db = ref(getDatabase(firebase))
    get(db).then((snapshot) => {
      if (snapshot.exists()) {
        setData(snapshot.val())
      } else {
        console.log("No data available");
      }
    }).catch((error) => {
      console.error(error);
    });
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h3>All Data</h3>
        <p>
          {JSON.stringify(data)}
        </p>
      </header>
    </div>
  );
}

export default App;
