import React from 'react';
import Cookies from 'js-cookie';

import { CopyActionField } from './copyField.jsx';


class Webhook extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      savedDbState : {
        url: this.props.url,
        siteid: this.props.siteid,
        roomid: this.props.roomid,
        contact: this.props.contact,
      },
      url: this.props.url,
      siteid: this.props.siteid,
      roomid: this.props.roomid,
      contact: this.props.contact,
      verificationSecret: this.props.verification_secret,
      webhookEnabled: this.props.url === '' ? false : true,
      loading: false,
      error: '',
      webhookUpdateSuccess: '',
      changesMade: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.updateVerificationSecret = this.updateVerificationSecret.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();
    this.setState({ loading: true, error: '' });

    fetch('dashboard/api/webhook/edit/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: `url=${this.state.url}` +
      `&siteid=${this.state.siteid}` +
      `&roomid=${this.state.roomid}` +
      `&contact=${this.state.contact}` +
      `&app_id=${this.props.appId}`
    })
    .then((res) => {
      return res.json();
    })
    .then((json) => {
      this.setState({ loading: false });
      if (json.ok) {
        this.setState({
          webhookEnabled: true,
          webhookUpdateSuccess: '  ✅' ,
          savedDbState: {
            url: json.url,
            roomid: json.roomid,
            siteid: json.siteid,
            contact: json.contact,
          },
          changesMade: false,
        });
        setTimeout(() => {
          this.setState({ webhookUpdateSuccess: '' });
        }, 3000);
      } else {
        this.setState({ error: `Error: ${json.message}` });
      }
    })
    .catch(() => {
      this.setState({ loading: false, error: 'Error: An unexpected error ocurred.'});
    });
  }

  handleChange(e) {

    this.setState({
      [e.target.id]: e.target.value,
    }, () => {
      const changesMade = (
        this.state.url !== this.state.savedDbState.url ||
        this.state.siteid !== this.state.savedDbState.siteid ||
        this.state.roomid !== this.state.savedDbState.roomid ||
        this.state.contact !== this.state.savedDbState.contact
      );
      this.setState({ changesMade });
    });
  }

  updateVerificationSecret(e) {
    e.preventDefault();

    fetch('dashboard/api/webhook/refreshsecret/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: `app_id=${this.props.appId}`
    })
    .then((res) => {
      return res.json();
    })
    .then((json) => {
      if(json.ok) {
        this.setState({ verificationSecret: json.new_secret });
      } else {
        throw new Error(`Verification Secret could not be updated.\nMessage: ${json.message}`);
      }
    });
  }

  render() {
    return (
      <div className="webhook">
        Verification Secret
        <CopyActionField
          val={this.state.verificationSecret}
          action={this.updateVerificationSecret}
          icon="fa fa-refresh"
        />
        <form className="pure-form" onSubmit={this.handleSubmit}>
          <fieldset>
            <div className="pure-g">
              <div className="pure-u-1">
                <label htmlFor="url">Webhook URL</label>
                <input
                  id="url"
                  className="pure-input-1"
                  type="url"
                  placeholder="https://example.com/webhook"
                  required
                  value={this.state.url}
                  onChange={this.handleChange}
                />
              </div>
              <div className="pure-u-1">
                <label htmlFor="siteid">siteid (optional)</label>
                <input
                  id="siteid"
                  className="pure-input-1"
                  type="text"
                  placeholder="086"
                  value={this.state.siteid}
                  onChange={this.handleChange}
                />
              </div>
              <div className="pure-u-1">
                <label htmlFor="roomid">roomid (optional)</label>
                <input
                  id="roomid"
                  className="pure-input-1"
                  type="text"
                  placeholder="433"
                  value={this.state.roomid}
                  onChange={this.handleChange}
                />
              </div>
              <div className="pure-u-1">
                <label htmlFor="contact">contact (optional)</label>
                <input
                  id="contact"
                  className="pure-input-1"
                  type="text"
                  placeholder="Michael Arthur"
                  value={this.state.contact}
                  onChange={this.handleChange}
                />
              </div>
            </div>
            <button
              type="submit"
              className="pure-button pure-button-primary"
              disabled={this.state.loading || !this.state.changesMade}
            >
              {this.state.webhookEnabled ? 'Update Webhook' : 'Create Webhook'}
            </button>
            <label>{this.state.webhookUpdateSuccess}</label>
            <br />
            <label>{this.state.error}</label>
          </fieldset>
        </form>
      </div>
    );
  }
}

Webhook.propTypes = {
  url: React.PropTypes.string.isRequired,
  siteid: React.PropTypes.string.isRequired,
  roomid: React.PropTypes.string.isRequired,
  contact: React.PropTypes.string.isRequired,
  verification_secret: React.PropTypes.string.isRequired,
  appId: React.PropTypes.string.isRequired,
};

export default Webhook;
