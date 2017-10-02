import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


export default class VersionHeader extends React.Component {

    render () {
      return (
        <Topic
          noExamples={true}>
          <p>
            The base url is <code>https://uclapi.com/roombookings/</code>
          </p>
          <Table>
            <Cell
              name="Version Header"
              example="uclapi-roombookings-version" />
            <Cell
              name="Latest Version"
              example="uclapi-roombookings-version" />
          </Table>
        </Topic>
      )
    }

}
