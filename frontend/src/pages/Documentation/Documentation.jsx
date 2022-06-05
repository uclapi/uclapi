import React from 'react'
import { NavBar } from "../../components/layout/Items.jsx"
import "Styles/common/uclapi.scss"
import "Styles/navbar.scss"
import "Styles/documentation.scss"
import SwaggerUI from "swagger-ui-react"
import "swagger-ui-react/swagger-ui.css"
import spec from "../../../../uclapi.openapi.json"

function Documentation() {
  return (
    <div className='vertical-padding'>
      <NavBar isScroll={false} />
      <SwaggerUI spec={spec} />
    </div>
  )
}

export default Documentation
