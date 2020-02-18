// Styling
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Dependencies
import dayjs from 'dayjs'
import Cookies from 'js-cookie'
import React from 'react'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'

// Styles
import { styles } from 'Layout/data/dashboard_styles.jsx'
import { CardView, Column, Footer, NavBar, Row, TextView, 
  ButtonView, Field, ConfirmBox, CheckBox } from 'Layout/Items.jsx'

// UI App Component
import App from '../components/dashboard/App.jsx'

const defaultHeaders = {
  'Content-Type': `application/x-www-form-urlencoded`,
  'X-CSRFToken': Cookies.get(`csrftoken`),
}
  
class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

    // Sort the apps by last updated property
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

    this.state = { 
      data: window.initialData,
      view: `default`,
      toDelete: -1,
    }
  }

  render() {
    const { data: { name, cn, apps }, view, toDelete} = this.state 

    const actions = {
      toggleEditTitle: this.toggleEditTitle,
      regenToken: this.regenToken,
      regenVerificationSecret: this.regenVerificationSecret,
      webhook: {
        saveURL: this.saveWebhookURL,
        saveContact: this.saveWebhookContact,
        saveSiteID: this.saveWebhookSiteID,
        saveRoomID: this.saveWebhookRoomID,
      },
      saveEditTitle: this.saveEditTitle,
      cancelEditTitle: this.cancelEditTitle,
      setScope: this.setScope,
      saveOAuthCallback: this.saveOAuthCallback,
      addNewProject: this.addNewProject,
      deleteProject: this.deleteProject,
      deleteConfirm: this.deleteConfirm
    }

    if(this.DEBUGGING) { console.log("re-rendered dashboard") }
    console.log(apps)

    return (
      <>
        <NavBar isScroll={false} />

        <Modal 
          isOpen={view == `add-project`}
          contentLabel="Create app form"
          onRequestClose={ () => this.setState({view: `default`}) }
          className="Modal"
          overlayClassName="Overlay"
          style={styles.modal}
        >
          <ConfirmBox
            text="Enter the name of your new project"
            success={(value) => { actions.addNewProject(value) } }
            fail={() => { this.setState({view: `default`}) } }
          />
        </Modal>

        <Modal 
          isOpen={view == `delete-project`}
          contentLabel="Delete app form"
          onRequestClose={ () => this.setState({view: `default`}) }
          className="Modal"
          overlayClassName="Overlay"
          style={styles.modal}
        >
          {toDelete !== -1 ? (
            <ConfirmBox
              text={"Enter the name of your project to confirm deletion (" + apps[toDelete].name  + ")"}
              success={(value) => { actions.deleteProject(toDelete) } }
              fail={() => { this.setState({view: `default`}) } }
              value={ apps[toDelete].name }
              shouldCheckValue
            />
          ) : null }
        </Modal>

        <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100%`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `80px` }}>
            <TextView text={`Welcome, ` + name}
              heading={1}
              align={`left`} 
              style={styles.baseText}
            />
            <TextView text={`Your username is: ` + cn}
              heading={2}
              align={`left`} 
              style={styles.lightText}
            />

            <div className="app-holder" style={styles.appHolder}>
              {apps.map( (app, index) => (
                <App
                  app={app}
                  index={index}
                  actions={actions}
                />
              ))}
              {apps.length === 0 ? (
                 <CardView width='1-1' type='default' noPadding>
                  <Row noPadding>
                    <Column width='1-1'
                      horizontalAlignment='center'
                      style={{
                        paddingTop: 30,
                        paddingBottom: 20,
                      }}
                    >
                      <TextView
                        text={"You haven't created any apps yet, click below to get started!"}
                        heading={2}
                        align={`center`}
                        style={styles.noPadding}
                      />
                    </Column>
                  </Row>
                </CardView>
              ) : null}
            </div>
            <ButtonView text={`Add new project`} type={`default`} 
              style={{ cursor: `pointer` }} 
              onClick={ () => { this.setState({ view: `add-project` }) } } fakeLink/>
          </Column>
        </Row>

        <Footer />
      </>
    )
  }

  addNewProject = (name) => {
    this.queryDashboardAPI(`/dashboard/api/create/`, `name=` + name, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Add the new app to the state so it gets rendered
      let newApp = json.app
      newApp['name'] = name

      var newData = {...this.state.data}
      newData.apps.push(newApp)

      // Go to new state visually
      this.setState({
        view: `default`, 
        data: newData
      })
    })
  }

  deleteConfirm = (index) => {
    this.setState({ 
      view: `delete-project`, 
      toDelete: index,
    })
  }

  deleteProject = (index) => {
    const { data } = this.state

    this.queryDashboardAPI(`/dashboard/api/delete/`, `app_id=` + data.apps[index].id, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Remove the deleted app
      console.log("deleting index: " + index)
      var newData = {...this.state.data}
      newData.apps.splice(index, 1)
      console.log(newData.apps)

      // Go to default state visually
      this.setState({  
        toDelete: -1,
        view: `default`, 
        data: newData
      })
    })
  }

  saveEditTitle = (index, value) => {
    const { data } = this.state
    
    this.queryDashboardAPI(`/dashboard/api/rename/`, `new_name=` + value + `&app_id=` + data.apps[index].id, (json) => {
      if(this.DEBUGGING) { console.log(json) }
    })
    
    data.apps[index].name = value
    this.setState({ data: data })
  }

  saveOAuthCallback = (index, value) => {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      const { data } = this.state
      data.apps[index].oauth.callback_url = value

      this.queryDashboardAPI(`/dashboard/api/setcallbackurl/`, `app_id=` + updatedData.apps[index].id + `&callback_url=` + value, (json) => {
        console.log(json)
      })

      this.setState({ data: data })
    }
  }

  setScope = (index, scope, value) => {
    const { data } = this.state

    // Update data
    data.apps[index].oauth.scopes[scope].enabled = value

    // Convert scopes into form for backend
    const scopes = data.apps[index].oauth.scopes
    const scopesData = scopes.map( scope => 
      ({
        name: scope.name, 
        checked: scope.enabled
      }))

    const json = JSON.stringify(scopesData)

    this.queryDashboardAPI(`/dashboard/api/updatescopes/`, `app_id=` + data.apps[index].id + 
      `&scopes=` + encodeURIComponent(json), (json) => {
        console.log(json)
    })

    this.setState({ data: data })
  }

  regenToken = (index) => {
    const { data } = this.state 

    this.queryDashboardAPI(`/dashboard/api/regen/`, `app_id=` + data.apps[index].id, (json) => {
      data.apps[index].token = json.app.token 
      this.setState({ data: data })
    })
  }

  regenVerificationSecret = (index) => {
    const { data } = this.state 

    this.queryDashboardAPI(`dashboard/api/webhook/refreshsecret/`, `app_id=` + data.apps[index].id, (json) => {
      data.apps[index].webhook.verification_secret = json.new_secret
      this.setState({ data: data })
    })
  }

  saveWebhookURL = (index, value) => {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      this.updateWebhookSettings({url: value}, index) 
    }
  }

  saveWebhookContact = (index, value) => { this.updateWebhookSettings({contact: value}, index) }
  saveWebhookSiteID = (index, value) => { this.updateWebhookSettings({siteid: value}, index) }
  saveWebhookRoomID = (index, value) => { this.updateWebhookSettings({roomid: value}, index) }

  updateWebhookSettings = (newValues, index) => {
    const { data } = this.state

    const app = data.apps[index]
    var values = {...app.webhook, ...newValues}

    const parameters = `url=` + values.url + `&siteid=` + values.siteid + `&roomid=` + values.roomid 
      + `&contact=` + values.contact + `&app_id=` + data.apps[index].id

    this.queryDashboardAPI(`dashboard/api/webhook/edit/`, parameters, (json) => {
        console.log(`For parameters: ` + parameters)
        console.log(json)
    })

    data.apps[index].webhook = values
    this.setState({ data: data })
  }

  queryDashboardAPI = (url, querystring, callback) => {
    fetch(url, {
      method: `POST`,
      credentials: `include`,
      headers: defaultHeaders,
      body: querystring,
    }).then((res)=>{
      return res.json()
    }).then(callback)
    .catch((err)=>{
      console.log(`Failed to save details to: ` + url)
      console.log(err)
    })
  }
}

ReactDOM.render(
  <Dashboard />,
  document.querySelector(`.app`)
)
