import firebase from "firebase"

firebase.initializeApp({
  apiKey: "AIzaSyDe6uUHGsa4QnUiLQWwcFddHpztxYKOV_g",
  databaseURL: "https://scrapehost-9f1bf.firebaseio.com"
})
firebase.auth().signInAnonymously()

export default firebase.database().ref("/log")
