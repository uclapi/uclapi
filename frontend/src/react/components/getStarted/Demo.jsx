import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import TextField from 'material-ui/TextField';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/styles';


let languages = [
  {
    "name": "python",
    "code": `from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = "AC5ef872f6da5a21de157d80997a64bd33"
AUTH_TOKEN = "[AuthToken]"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
  to="+16518675309",
  from_="+14158141829",
  body="Tomorrow forecast in Financial District, San Francisco is Clear.",
  media_url="https://climacons.herokuapp.com/clear.png",
)`
  },

  {
    "name": "javascript",
    "code": `// Twilio Credentials
var accountSid = 'AC5ef872f6da5a21de157d80997a64bd33';
var authToken = '[AuthToken]';
//require the Twilio module and create a REST client
var client = require('twilio')(accountSid, authToken);
client.messages.create({
  to: "+16518675309",
  from: "+14158141829",
  body: "Tomorrow's forecast in Financial District, San Francisco is Clear.",
  mediaUrl: "https://climacons.herokuapp.com/clear.png",
}, function(err, message) {
  console.log(message.sid);
});`
  },

  {
    name: "java",
    code: `// You may want to be more specific in your imports
import java.util.*;
import com.twilio.sdk.*;
import com.twilio.sdk.resource.factory.*;
import com.twilio.sdk.resource.instance.*;
import com.twilio.sdk.resource.list.*;
public class TwilioTest {
 // Find your Account Sid and Token at twilio.com/user/account
 public static final String ACCOUNT_SID = "AC5ef872f6da5a21de157d80997a64bd33";
 public static final String AUTH_TOKEN = "[AuthToken]";
 public static void main(String[]args) throws TwilioRestException {
  TwilioRestClient client = new TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN);
   // Build the parameters
   List<NameValuePair> params = new ArrayList<NameValuePair>();
   params.add(new BasicNameValuePair("To", "+16518675309"));
   params.add(new BasicNameValuePair("From", "+14158141829"));
   params.add(new BasicNameValuePair("Body", "Tomorrow's forecast is clear"));
   MessageFactory messageFactory = client.getAccount().getMessageFactory();
   Message message = messageFactory.create(params);
   System.out.println(message.getSid());
 }
}`
  },

  {
    name: "ruby",
    code: `require 'rubygems' # not necessary with ruby 1.9 but included for completeness
require 'twilio-ruby'
# put your own credentials here
account_sid = 'AC5ef872f6da5a21de157d80997a64bd33'
auth_token = '[AuthToken]'
# set up a client to talk to the Twilio REST API
@client = Twilio::REST::Client.new account_sid, auth_token
@client.account.messages.create({
  :from => '+14158141829',
  :to => '+16518675309',
  :body => 'Tomorrow\'s forecast in Financial District, San Francisco is Clear.',
  :media_url => 'https://climacons.herokuapp.com/clear.png'
})`
  }
]

export default class Demo extends React.Component {

  render () {
    return (
      <div className="demo">

        <div className="text">
          <h2>Enter your Token</h2>
          <TextField hintText="Your Access Token" />
        </div>

        <div className="code">
          <Tabs>
            {
              languages.map((language, index) => (
                <Tab key={index} label={ language.name }>
                  <div>
                    <SyntaxHighlighter language={language.name}
                      style={dracula}>{language.code}</SyntaxHighlighter>
                  </div>
                </Tab>
              ))
            }
          </Tabs>
        </div>

      </div>
    )
  }

}
