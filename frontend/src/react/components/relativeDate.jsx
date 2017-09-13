import React from 'react';
import moment from 'moment';

class RelativeDate extends React.Component {
  constructor(props){
    super(props);

    /*
      Make moment.js say 'just now' if the time difference is less
      than five seconds either way to get round non-sync'd server and
      client time.
      This may make 'a few seconds ago' somewhat redundant, but it's
      worth it.
    */
    moment.fn.fromNowOrNow = function(a) {
      if (Math.abs(moment().diff(this)) < 5000) {
        return 'just now';
      }
      return this.fromNow(a);
    };
  }

  render(){
    return(
      <div title={moment.utc(this.props.date).local().format('dddd, Do MMMM YYYY, h:mm:ss a')}>
        {this.props.label} {moment.utc(this.props.date).local().fromNowOrNow()}
      </div>
    );
  }
}

RelativeDate.propTypes = {
  date: React.PropTypes.string.isRequired,
  label: React.PropTypes.string
};

export {RelativeDate};
