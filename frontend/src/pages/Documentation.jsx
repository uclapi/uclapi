import React from 'react'
import ReactDOM from 'react-dom'
import { NavBar } from "../components/layout/Items.jsx"
import SwaggerUI from "swagger-ui-react"
import "Styles/common/uclapi.scss"
import "Styles/navbar.scss"
import "Styles/documentation.scss"
import "swagger-ui-react/swagger-ui.css"
import spec from "../../../uclapi.openapi.json"

const Documentation = () => (
  <div className='vertical-padding'>
    <NavBar isScroll={false} />
    <SwaggerUI spec={spec} />
  </div>
)

ReactDOM.render(
  <Documentation />,
  document.querySelector(`.app`)
)
