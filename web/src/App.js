import React, { useEffect, useState } from "react"
import "./App.css"
import { firebase } from "./shared/firebaseConfig"
import { getDatabase, ref, onValue } from "firebase/database"

function App() {
  const [data, setData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [tags, setTags] = useState([])
  const [selectedTags, setSelectedTags] = useState([])
  const [shouldMatchAll, setShouldMatchAll] = useState(false)

  useEffect(() => {
    // Fetch all the data and add a listener so that the apge refreshes if the database data changes
    const db = ref(getDatabase(firebase))
    const listener = onValue(
      db,
      (snapshot) => {
        if (snapshot.exists()) {
          const data = snapshot.val()
          // Flattening all docs to get a nice table list view
          let allDocs = []
          for (const topic in data) {
            allDocs = allDocs.concat(data[topic])
          }

          // Create a unique array of tags to display for filtering
          setTags(
            Array.from(
              new Set(allDocs.reduce((prev, d) => prev.concat(d.tags), []))
            ).sort()
          )

          setData(allDocs)
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

  useEffect(() => {
    // When the selected tags or the matching swithc is changed
    // re-run the filtering to get the newly filtered data
    const filterdData = data.filter((item, idx) => {
      if (selectedTags.length) {
        if (!shouldMatchAll) {
          if (!selectedTags.some((tag) => item.tags.includes(tag))) {
            return false
          }
        } else {
          if (!selectedTags.every((tag) => item.tags.includes(tag))) {
            return false
          }
        }
      }
      return true
    })

    if (!selectedTags.length) {
      setFilteredData([])
    } else {
      setFilteredData(filterdData)
    }
  }, [selectedTags, shouldMatchAll, data])

  const renderTagsList = () => {
    const displayArr = selectedTags.length ? filteredData : data
    return (
      <>
        <div className="filter-box">
          <div className="filter-header">
            <p className="instructions">
              *Select all the tags you'd like to filter the projects by
            </p>
            <div className="filter-options">
              Match Any
              <label className="switch">
                <input
                  type="checkbox"
                  checked={shouldMatchAll}
                  onChange={() => {
                    setShouldMatchAll(!shouldMatchAll)
                  }}
                />
                <span className="slider round" />
              </label>
              Match All
              <div className="separator" />
              <div
                onClick={() => setSelectedTags([])}
                className="tag tag-selected"
              >
                Clear Selections
              </div>
            </div>
          </div>
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
        <div className="tableContainer">
          {!!selectedTags.length && (
            <div className="resultsLabel">{`Results: ${filteredData.length}`}</div>
          )}
          <table>
            <thead>
              <tr className="table-header-row">
                <td>Github URL</td>
                <td>Tags</td>
              </tr>
            </thead>
            <tbody>
              {displayArr.map((item, idx) => {
                return (
                  <tr key={idx} className="table-item-row">
                    <td>
                      <a href={item.url} target="_blank" rel="noreferrer">
                        {item.url}
                      </a>
                    </td>
                    <td>{Object.values(item.tags).join(", ")}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
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
        {!data ? null : renderTagsList()}
      </div>
    </div>
  )
}

export default App
