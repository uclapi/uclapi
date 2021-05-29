import React from 'react'
import ReactDOM from 'react-dom'
import InternalServerErrorPage from "./500"

ReactDOM.render(
  <InternalServerErrorPage />,
  document.querySelector(`.app`)
)

