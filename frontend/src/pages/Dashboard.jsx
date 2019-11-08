import 'Styles/dashboard.scss'

import dayjs from 'dayjs'
import React from 'react'
import ReactDOM from 'react-dom'

import AppList from '../components/dashboard/appList.jsx'
import Layout from '../components/dashboard/layout.jsx'
import Profile from '../components/dashboard/profile.jsx'

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
    return <div>
      <Layout>
        <Profile name={this.state.data.name} cn={this.state.data.cn} />
        <AppList apps={this.state.data.apps} />
      </Layout>
    </div>
  }
}

ReactDOM.render(
  <Dashboard />,
  document.querySelector(`.app`)
)
