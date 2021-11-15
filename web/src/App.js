import React, { useEffect, useState } from "react"
import "./App.css"
import { firebase } from "./shared/firebaseConfig"
import { getDatabase, ref, onValue } from "firebase/database"

const RENDER_TAGS_LIST = true

function App() {
  const [data, setData] = useState(null)
  const [tags, setTags] = useState([])
  const [selectedTags, setSelectedTags] = useState([])

  useEffect(() => {
    const db = ref(getDatabase(firebase))
    const listener = onValue(
      db,
      (snapshot) => {
        if (snapshot.exists()) {
          const data = snapshot.val()

          if (RENDER_TAGS_LIST) {
            // Flattening all docs to get a nice table list view
            let allDocs = []
            for (const topic in data) {
              if (topic === "Free Topics") {
                const freeTopics = data[topic]
                for (const innerTopic in freeTopics) {
                  allDocs = allDocs.concat(freeTopics[innerTopic])
                }
              } else {
                allDocs = allDocs.concat(data[topic])
              }
            }

            setTags(
              Array.from(
                new Set(allDocs.reduce((prev, d) => prev.concat(d.tags), []))
              )
            )
            setData(allDocs)
          } else {
            setData(data)
          }
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

  const renderTopicsList = () => {
    return (
      <div>
        {Object.keys(data).map((key) => {
          const category = data[key]
          return (
            <div key={key}>
              <h2>{key}</h2>
              <ul>
                {key === "Free Topics"
                  ? Object.keys(category).map((subCatKey) => {
                      return (
                        <li key={subCatKey}>
                          <h3>{subCatKey}</h3>
                          <ul>
                            {Object.keys(category[subCatKey]).map((itemKey) => {
                              return (
                                <li key={itemKey}>
                                  {category[subCatKey][itemKey].url}
                                </li>
                              )
                            })}
                          </ul>
                        </li>
                      )
                    })
                  : Object.keys(category).map((subCatKey) => {
                      return <li key={subCatKey}>{category[subCatKey].url}</li>
                    })}
              </ul>
            </div>
          )
        })}
      </div>
    )
  }

  const renderTagsList = () => {
    return (
      <>
        <div className="filter-box">
          <p className="instructions">
            *Select all the tags you'd like to filter the projects by
          </p>
          <div className="filter-container">
            {tags.map((t) => {
              const isSelected = selectedTags.includes(t)
              return (
                <div
                  key={t}
                  onClick={() => setSelectedTag(t)}
                  className={`tag ${isSelected ? "tag-selected" : ""}`}
                >
                  {t}
                </div>
              )
            })}
          </div>
        </div>
        <table>
          <thead>
            <tr className="table-header-row">
              <td>Github URL</td>
              <td>Tags</td>
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => {
              let el = (
                <tr key={idx} className="table-item-row">
                  <td>
                    <a href={item.url} target="_blank" rel="noreferrer">
                      {item.url}
                    </a>
                  </td>
                  <td>{Object.values(item.tags).join(", ")}</td>
                </tr>
              )
              if (selectedTags.length) {
                if (!selectedTags.some((tag) => item.tags.includes(tag))) {
                  el = null
                }
              }
              return el
            })}
          </tbody>
        </table>
      </>
    )
  }

  const setSelectedTag = (tag) => {
    const currentSelectedTags = [...selectedTags]
    const index = currentSelectedTags.indexOf(tag)
    if (index === -1) {
      currentSelectedTags.push(tag)
    } else {
      currentSelectedTags.splice(index, 1)
    }

    setSelectedTags(currentSelectedTags)
  }

  return (
    <div className="App">
      <div className="App-body">
        <h1 style={{ marginBottom: 100 }}>
          <u>UIUC CS410 Final Project Filter</u>
        </h1>
        {!data ? null : RENDER_TAGS_LIST ? renderTagsList() : renderTopicsList()}
      </div>
    </div>
  )
}

export default App
