# Update Database Firebase Function

This is the code of a [firebase cloud function](https://firebase.google.com/products/functions) that is hosted on the project's firebase instance and allows the update of the Realtime Database. It can be called with any REST-full App (i.e. [Postman](https://www.postman.com/)) or directly from a computer terminal.

Example call:

```
curl --location --request POST 'https://us-central1-topic-thunder-a7103.cloudfunctions.net/updateDatabase' \
--header 'x-api-key: ****-****-****-****-****' \
--header 'Content-Type: application/json' \
--data-raw '{
  "0": {
    "url": "https://github.com/team1/CourseProject",
    "tags": [
      "review",
      "model",
      "topic",
      "sentiment",
      "song",
      "analysis",
    ]
  },
  "1": {
    "url": "https://github.com/team2/CourseProject",
    "tags": [
      "topic",
      "time",
      "model",
      "text",
      "series",
    ]
  }
}'
```

This cloud function does not  need updating as the data changes but in case you need to fix an error or update this cloud function, please contact [Creon Creonopoulos](mailto:creonc2@illinois.edu) for access to the firebase console tied to this project.