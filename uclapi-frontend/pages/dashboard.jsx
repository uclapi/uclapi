/* eslint-disable react/jsx-no-bind */
import {
  CardView, Column, ConfirmBox,
  Container, Row,
} from '@/components/layout/Items.jsx'

import Modal from 'react-modal'
// UI App Component
import App from '@/components/dashboard/App.jsx'
import AcceptableUsePolicy from '@/components/dashboard/AcceptableUsePolicy.jsx'
import Api from '../lib/Api'
import styles from '@/styles/Dashboard.module.scss'
import React from "react";
import { getServerSession } from 'next-auth/next';
import { authOptions } from "./api/auth/[...nextauth]";
import withSession from '@/lib/withSession'
import { MissingAUPAgreementError } from '../lib/Api/DashboardApi';
import { Button } from 'rsuite'
import Head from 'next/head';

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions);
  return { props: { session } };
}

class Dashboard extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: { apps: [] },
      view: `default`,
      toDelete: -1,
    }
  }

  componentDidMount(){
    this.getData()
  }

  render() {
    const name = this.props.session.user.name;
    const cn = this.props.session.user.email.split('@')[0]
    const { data: {  apps }, view, toDelete } = this.state

    const actions = {
      regenToken: this.regenToken,
      regenVerificationSecret: this.regenVerificationSecret,
      renameProject: this.renameProject,
      cancelEditTitle: this.cancelEditTitle,
      setScope: this.setScope,
      saveOAuthCallback: this.saveOAuthCallback,
      addNewProject: this.addNewProject,
      deleteProject: this.deleteProject,
      deleteConfirm: this.deleteConfirm,
      acceptAup: this.acceptAup,
    }

    return (
      <>
        <Head>
          <title>
            Dashboard - UCL API
          </title>
        </Head>

        <Modal
          isOpen={view === `accept-aup`}
          contentLabel="UCL API Acceptable Use Policy"
          onRequestClose={() => this.setState({ view: `default` })}
          className="modal"
          preventScroll={false}
          overlayClassName="overlay"
        >
          <CardView width="1-1" type="default" noPadding>
            {view === `accept-aup` && <AcceptableUsePolicy />}
            <Button
              onClick={() => actions.acceptAup()}
            >
              I agree
            </Button>
            <Button
              color='red'
              appearance='primary'
              onClick={() => this.setState({ view: `default` })}
            >
              Cancel
            </Button>
          </CardView>
        </Modal>

        <Modal
          isOpen={view == `add-project`}
          contentLabel="Create app form"
          onRequestClose={() => this.setState({ view: `default` })}
          className="modal"
          overlayClassName="overlay"
        >
          <ConfirmBox
            text="Enter the name of your new project"
            success={(value) => {
              actions.addNewProject(value);
            }}
            fail={() => {
              this.setState({ view: `default` });
            }}
            shouldCheckValue={false}
          />
        </Modal>

        <Modal
          isOpen={view == `delete-project`}
          contentLabel="Delete app form"
          onRequestClose={() => this.setState({ view: `default` })}
          className="modal"
          overlayClassName="overlay"
        >
          {toDelete !== -1 ? (
            <ConfirmBox
              text={
                `Enter the name of your project to confirm deletion (${
                  apps[toDelete].name
                })`
              }
              success={() => { actions.deleteProject(toDelete) }}
              fail={() => { this.setState({ view: `default` }) }}
              value={apps[toDelete].name}
              shouldCheckValue
            />
          ) : null}
        </Modal>

        <Container
          height='fit-content'
          styling='splash-parallax'
          style={{ minHeight: `100%` }}
        >
          <Row width='1-1'>
            <Column
              width="2-3"
              alignItems="column"
              style={{ margin: `auto` }}
            >
              <h1>Welcome, {name}</h1>
              <h3>username: {cn}</h3>

              <div className={`${styles.appHolder} app-holder`}>
                {apps.length === 0 ? (
                  <CardView width='1-1' type='default' noPadding>
                    <h2>
                      You haven&apos;t created any apps yet, click below to get started!
                    </h2>
                  </CardView>
                ) : apps.map((app, index) => (
                  <App
                    key={app.name}
                    app={app}
                    index={index}
                    actions={actions}
                  />
                ))}
              </div>
            </Column>
          </Row>
          <Row width='1-1'>
            <Button
              className='grey-btn'
              style={{
                borderRadius: `10px`,
                padding: `20px 25px`,
                margin: `auto`
              }}
              onClick={() => { this.setState({ view: `add-project` }) }}
            >
              +
            </Button>
        </Row>
        </Container>
      </>
    )
  }

  getData = async () => {
    const data = await Api.dashboard.getData()
    this.setState({ data })
  }

  addNewProject = async (name) => {
    try {
      const newApp = await Api.dashboard.addNewProject(name)
      const { data } = this.state
      this.setState({
        view: `default`,
        data: {
          ...data,
          apps: [...data.apps, newApp],
        },
      })
    } catch (err) {
      if (err instanceof MissingAUPAgreementError) {
        this.setState({ view: 'accept-aup' })
      }
    }
  }

  deleteConfirm = (index) => this.setState({
    view: `delete-project`,
    toDelete: index,
  })

  acceptAup = async () => {
    try {
      await Api.dashboard.acceptAup()
      this.setState({ view: `add-project` })
    } catch (error) {
      window.alert(error.message)
    }
  }

  deleteProject = async (index) => {
    const { data } = this.state

    try {
      await Api.dashboard.deleteProject(data.apps[index].id)

      this.setState({
        toDelete: -1,
        view: `default`,
        data: {
          ...data,
          apps: [
            ...data.apps.slice(0, index),
            ...data.apps.slice(index + 1),
          ],
        },
      })
    } catch (error) {
      window.alert(error.message)
    }
  }

  renameProject = async (index, value) => {
    const { data } = this.state

    try {
      await Api.dashboard.renameProject(data.apps[index].id, value)
      this.updateAppState(index, { name: value })
    } catch (error) {
      window.alert(error.message)
    }
  }

  saveOAuthCallback = async (index, value) => {
    const { data } = this.state

    try {
      await Api.dashboard.saveOAuthCallback(data.apps[index].id, value)
      this.updateAppState(index, {
        oauth: {
          ...data.apps[index].oauth,
          callback_url: value,
        },
      })
    } catch (error) {
      window.alert(error.message)
    }
  }

  setScope = async (index, scope, value) => {
    const { data } = this.state

    const updatedAppState = ({
      oauth: {
        ...data.apps[index].oauth,
        scopes: [
          ...data.apps[index].oauth.scopes.slice(0, scope),
          {
            ...data.apps[index].oauth.scopes[scope],
            enabled: value,
          },
          ...data.apps[index].oauth.scopes.slice(scope + 1),
        ],
      },
    })

    const { oauth: { scopes } } = updatedAppState
    const scopesData = scopes.map(scope => ({
      name: scope.name,
      checked: scope.enabled,
    }))

    try {
      await Api.dashboard.setScope(
        data.apps[index].id,
        JSON.stringify(scopesData)
      )

      this.updateAppState(index, updatedAppState)
    } catch (error) {
      window.alert(error.message)
    }
  }

  updateAppState = (index, newAppState) => {
    const { data } = this.state
    return this.setState({
      data: {
        ...data,
        apps: [
          ...data.apps.slice(0, index),
          {
            ...data.apps[index],
            ...newAppState,
          },
          ...data.apps.slice(index + 1),
        ],
      },
    })
  }

  regenToken = async (index) => {
    const { data } = this.state
    const token = await Api.dashboard.regenToken(data.apps[index].id)
    this.updateAppState(index, { token })
  }
}

export default withSession(Dashboard)
