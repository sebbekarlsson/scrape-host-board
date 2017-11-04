import "./index.css"
import React, { createElement } from "react"
import { render } from "react-dom"

import db from "./db"

db.on("value", renderLog)

const Line = (line, i) => <div key={i}>{line}</div>
function renderLog(snap) {
  const lines = Object.values(snap.val() || {}).map(JSON.stringify)

  render(lines.map(Line), root)
}
