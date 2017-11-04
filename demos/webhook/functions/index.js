const functions = require("firebase-functions")
const admin = require("firebase-admin")

admin.initializeApp(functions.config().firebase)

const db = admin.database().ref("/log")

const mockEvent = {
  type: "change",
  payload: "webhook triggered"
}

exports.webhook = functions.https.onRequest((req, res) =>
  db.push(mockEvent).then(snap => res.redirect(303, snap.ref))
)
