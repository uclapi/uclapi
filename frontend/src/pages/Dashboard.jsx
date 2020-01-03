import 'Styles/common/uclapi.scss'

import dayjs from 'dayjs'
import React from 'react'
import ReactDOM from 'react-dom'

// Components
import { ButtonView, CardView, Column, Demo, 
  Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

import AppList from '../components/dashboard/appList.jsx'
import Layout from '../components/dashboard/layout.jsx'

class Dashboard extends React.Component {
  constructor(props) {
    super(props)
    window.initialData.apps.sort((a, b) => {
      const dateA = dayjs(a.created)
      const dateB = dayjs(b.created)

      if (dateA.isBefore(dateB)) {
        return -1
      } else if (dateB.isBefore(dateA)) {
        return 1
      } else {
        return 0
      }
    })
    this.state = { data: window.initialData }
  }
  render() {
    const { data: { name, cn, apps } } = this.state 

    return (
      <>
        <NavBar isScroll={false} />

        <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100%`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `50px` }}>
            <TextView text={`Welcome, ` + name} heading={1} align={`left`} />
            <TextView text={`Your username is: ` + cn} heading={2} align={`left`} />

            <AppList apps={apps} />
          </Column>
        </Row>
      </>
    )
  }
}

ReactDOM.render(
  <Dashboard />,
  document.querySelector(`.app`)
)
