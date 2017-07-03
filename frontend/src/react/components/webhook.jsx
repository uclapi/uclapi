import React from 'react';
import Cookies from 'js-cookie';

import { CopyActionField } from './CopyField.jsx';


class Webhook extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: this.props.url,
      siteid: this.props.siteid,
      roomid: this.props.roomid,
      contact: this.props.roomid,
      verificationSecret: this.props.verification_secret,
      enabled: this.props.url === '' ? false : true,
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.updateVerificationSecret = this.updateVerificationSecret.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();

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
      console.log(res);
      return res.json();
    })
    .then((json) => {
      if (json.ok) {
        setState({ enabled: true })
      }
    });
  }

  handleChange(e) {
    this.setState({
      [e.target.id]: e.target.value,
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
      console.log(res);
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
            <button type="submit" className="pure-button pure-button-primary">
              {this.state.enabled ? 'Update Webhook' : 'Create Webhook'}
            </button>
          </fieldset>
        </form>
      </div>
    );
  }
}

export default Webhook;
