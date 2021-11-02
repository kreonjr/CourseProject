import React, { useEffect, useState } from "react"
import "./App.css"
import { firebase } from "./shared/firebaseConfig"
import { getDatabase, ref, onValue } from "firebase/database"

function App() {
  const [data, setData] = useState({})

  useEffect(() => {
    const db = ref(getDatabase(firebase))
    const listener = onValue(
      db,
      (snapshot) => {
        if (snapshot.exists()) {
          setData(snapshot.val())
        } else {
          console.log("No data available")
        }
      },
      (error) => {
        console.error(error)
      }
    )

    return () => {
      listener()
    }
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          UIUC CS410 Course Project Browser
        </h1>
        <p>
          {Object.keys(data).map((key) => {
            const category = data[key]
            if (key === "Free Topics") {
              return (
                <div>
                  <h2>{key}</h2>
                  <ul>
                    {Object.keys(category).map((subCatKey) => {
                      return (
                        <li>
                          <h3>{subCatKey}</h3>
                          <ul>
                            {Object.keys(category[subCatKey]).map((itemKey) => {
                              return <li>{category[subCatKey][itemKey].url}</li>
                            })}
                          </ul>
                        </li>
                      )
                    })}
                  </ul>
                </div>
              )
            } else {
              return (
                <div>
                  <h2>{key}</h2>
                  <ul>
                    {Object.keys(category).map((subCatKey) => {
                      return <li>{category[subCatKey].url}</li>
                    })}
                  </ul>
                </div>
              )
            }
          })}
        </p>
      </header>
    </div>
  )
}

export default App
