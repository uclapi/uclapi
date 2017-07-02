import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import AutoComplete from 'material-ui/AutoComplete';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {dracula} from 'react-syntax-highlighter/dist/styles';
import RaisedButton from 'material-ui/RaisedButton';
import 'whatwg-fetch';


let rooms = [
  'Wilkins Building (Main Building) Portico',
  'Torrington (1-19) 433',
  'Darwin Building B05',
  'Darwin Building B15',
  'Darwin Building B40 LT',
  'Cruciform Building B.3.01',
  'Cruciform Building B.3.05',
  'Cruciform Building B.3.06',
  'Cruciform Building B.3.07',
  'Cruciform Building B.4.01',
  'Cruciform Building B1.03',
  'Cruciform Building Foyer 102 Seminar Room 2',
  'Cruciform Building Foyer 201 Seminar Room 3',
  'Gordon Square (25) B30',
  'Foster Court 112',
  'Foster Court 113',
  'Gordon Square (23) 101',
  'Foster Court 235',
  'Foster Court 243',
  'Rockefeller Building 337 David Sacks',
  'Rockefeller Building 338',
  'Rockefeller Building 339',
  'Malet Place Engineering Building 1.02',
  'Malet Place Engineering Building 1.03',
  'South Wing G12 Council Room',
  'Engineering Front Suite 104',
  'Malet Place Engineering Building 1.04',
  'Gordon Square (26) B32',
  'Taviton (16) 431',
  'Engineering Front Executive Suite 103',
  'Gordon Square (16-18) 101',
  'Pearson Building (North East Entrance) G17',
  'Gordon Square (24) 105',
  'Gordon Square (25) 107',
  'Pearson Building (North East Entrance) G22 LT',
  'Pearson Building (North East Entrance) G23',
  'Foster Court 114',
  'Pearson Building (North East Entrance) G26',
  'Taviton (16) 432',
  'Rockefeller Building 335',
  'Birkbeck Gordon Square (43) Cinema',
  'Birkbeck Gordon Square (43) 104',
  'Birkbeck Gordon Square (43) 120',
  'Birkbeck Gordon Square (43) 122',
  'Birkbeck Gordon Square (43) 321',
  'Birkbeck Gordon Square (43) 324',
  'Birkbeck Gordon Square (43) 327',
  'Birkbeck Gordon Square (43) B01',
  'Birkbeck Gordon Square (43) B06',
  'Birkbeck Gordon Square (43) B07',
  'Birkbeck Gordon Square (43) G01',
  'Birkbeck Gordon Square (43) G02',
  'South Quad Pop Up Learning Hub 101',
  'Christopher Ingold Building G20 - Public Cluster',
  'DMS Watson Building G15 - Public Cluster',
  'Medawar Building G02 Watson LT',
  'Taviton (14) 129',
  'Taviton (14) 130',
  'Taviton (14) 131',
  'IOE - Bedford Way (20) - 790',
  'Taviton (14) 132',
  'Anatomy B15',
  'Taviton (16) 345',
  'Taviton (16) 346',
  'Taviton (16) 535',
  'Taviton (16) 534',
  'South Wing 9 Garwood LT',
  'Foster Court 130',
  'Foster Court 132',
  'Foster Court 233',
  'Wilkins Garden Room',
  'IOE - Bedford Way (20) - 435 - The Space Observation Suite',
  'Taviton (16) 433',
  'IOE - Bedford Way (20) - 828',
  'IOE - Bedford Way (20) - 305 - Clarke Hall',
  'IOE - Bedford Way (20) - 435 - The Space Observation Suite',
  'Gordon House 106',
  'IOE - Bedford Way (20) - 435 - The Space Observation Suite',
  'Cruciform Building B1.04',
  'Cruciform Building B1.05',
  'Cruciform Building B1.06',
  'Cruciform Building B1.07',
  'Cruciform Building B115A - Public Cluster',
  'Cruciform Building B.3.08',
  'Cruciform Building B304 - LT1',
  'Cruciform Building B404 - LT2',
  'Cruciform Building Foyer 101 Seminar Room 1',
  'Gordon Square (25) B26',
  'Birkbeck Malet Street 404/405',
  'Birkbeck Malet Street 423',
  'Birkbeck Malet Street B29',
  'Birkbeck Malet Street B30',
  'Birkbeck Malet Street B35',
  'Birkbeck Malet Street B36',
  'Gordon Square (16-18) B03',
  'Gordon Square (16-18) B02',
  'Taviton (16) 532',
  'Gordon Square (16-18) G01',
  'Gordon Square (16-18) G06',
  'Gordon Square (16-18) G09',
  'Gordon Square (22) B15',
  'Gordon Square (26) G10',
  'Christopher Ingold Building XLG2 Auditorium',
  'IOE - Bedford Way (20) - 675',
  'Chadwick Building 2.18',
  'Chadwick Building 2.23 - Public Cluster',
  'Chadwick Building B05 LT',
  'Physics Building A1/3',
  'IOE - Bedford Way (20) - 901',
  'Chadwick Building G07',
  'IOE - Bedford Way (20) - 104 - Elvin Hall',
  'IOE - Bedford Way (20) - 104 - Elvin Hall',
  'IOE - Bedford Way (20) - 104 - Elvin Hall',
  'North Lodge 001',
  'South Quad Pop Up Learning Hub G01 LT',
  'South Quad Pop Up Learning Hub 103',
  'South Quad Pop Up Learning Hub 102',
  'Roberts Building 421',
  'Roberts Building 422',
  'IOE - Bedford Way (20) - 790',
  'IOE - Bedford Way (20) - 790',
  'IOE - Bedford Way (20) - 802',
  'IOE - Bedford Way (20) - 802',
  'IOE - Bedford Way (20) - 802',
  'IOE - Bedford Way (20) - 828',
  'IOE - Bedford Way (20) - 828',
  'IOE - Bedford Way (20) - 834',
  'IOE - Bedford Way (20) - 834',
  'IOE - Bedford Way (20) - 834',
  'IOE - Bedford Way (20) - 836',
  'Roberts Building 508',
  'IOE - Bedford Way (20) - 836',
  'Roberts Building Foyer G02',
  'Roberts Building G06 Sir Ambrose Fleming LT',
  'IOE - Bedford Way (20) - 836',
  'IOE - Bedford Way (20) - 901',
  'IOE - Bedford Way (20) - 901',
  'Wilkins Building (Main Building) South Cloisters',
  'Wilkins Building (Main Building) Whistler Room',
  'Rockefeller Building 333',
  'Rockefeller Building 336',
  'Gordon Square (16-18) B10',
  'Gordon Square (16-18) B09',
  'Gordon Square (26) G09',
  'Roberts Building G08 Sir David Davies LT',
  'South Wing G14 Committee Room',
  'Taviton (14) 128',
  'Gordon Street (25) Maths 500',
  'Gordon Street (25) D103',
  'Medical Sciences G46 H O Schild Pharmacology LT',
  'Torrington (1-19) 115 Galton LT',
  'Taviton (16) 347',
  'Anatomy G04 Gavin de Beer LT',
  'Gordon Street (25) Maths 505',
  'Torrington (1-19) B17 Basement LT',
  'Gordon Street (25) E28 Harrie Massey LT',
  'Medical Sciences 131 A V Hill LT',
  'Anatomy G29 J Z Young LT',
  'Tottenham Court Road (188) Room 01',
  'Tottenham Court Road (188) Room 03',
  'Tottenham Court Road (188) Room 04',
  'Tottenham Court Road (188) Room 02',
  'Tottenham Court Road (188) Room 05',
  'IOE - Bedford Way (20) - 420 - Committee Room 3',
  'IOE - Bedford Way (20) - 418 - Committee Room 2',
  'IOE - Bedford Way (20) - 418 - Committee Room 2',
  'IOE - Bedford Way (20) - 420 - Committee Room 3',
  'IOE - Bedford Way (20) - 421 - Nunn Hall',
  'IOE - Bedford Way (20) - 419',
  'IOE - Bedford Way (20) - 420 - Committee Room 3',
  'IOE - Bedford Way (20) - 421 - Nunn Hall',
  'IOE - Bedford Way (20) - 421 - Nunn Hall',
  'IOE - Bedford Way (20) - 425 - PC Lab 2',
  'IOE - Bedford Way (20) - 803',
  'IOE - Bedford Way (20) - 803',
  'Archaeology 501 - Public Cluster',
  'IOE - Bedford Way (20) - 804',
  'IOE - Bedford Way (20) - 803',
  'IOE - Bedford Way (20) - 804',
  'IOE - Bedford Way (20) - 804',
  'IOE - Bedford Way (20) - 805',
  'IOE - Bedford Way (20) - 805',
  'IOE - Bedford Way (20) - 822',
  'IOE - Bedford Way (20) - 822',
  'Foster Court B29 - Public Cluster',
  'Gordon Square (23) 203 - Public Cluster',
  'Gordon Street (25) 105 - Public Cluster',
  'Torrington (1-19) 113 - Public Cluster',
  'Gordon Square (20) B03 Sem 1',
  'IOE - Bedford Way (20) - 822',
  'IOE - Bedford Way (20) - 826',
  'IOE - Bedford Way (20) - 826',
  'IOE - Bedford Way (20) - 826',
  'Gordon Square (23) 102',
  'Foster Court 123',
  'IOE - Bedford Way (20) - 427 - PC Lab 3',
  'Foster Court 217',
  'Foster Court 219',
  'IOE - Bedford Way (20) - 746',
  'IOE - Bedford Way (20) - 746',
  'IOE - Bedford Way (20) - 746',
  'IOE - Bedford Way (20) - 770',
  'IOE - Bedford Way (20) - 770',
  'IOE - Bedford Way (20) - 777',
  'IOE - Bedford Way (20) - 777',
  'IOE - Bedford Way (20) - 777',
  'IOE - Bedford Way (20) - 780',
  'IOE - Bedford Way (20) - 780',
  'IOE - Bedford Way (20) - 780',
  'IOE - Bedford Way (20) - 784',
  'IOE - Bedford Way (20) - 784',
  'IOE - Bedford Way (20) - 784',
  'Drayton House B03 Ricardo LT',
  'Drayton House B04',
  'Drayton House B05',
  'Drayton House B06',
  'Roberts Building 102',
  'Roberts Building 103',
  'Roberts Building 105a',
  'Roberts Building 105b',
  'Roberts Building 106',
  'Roberts Building 110',
  'Roberts Building 309',
  'IOE - Bedford Way (20) - 944',
  'IOE - Bedford Way (20) - 935',
  'IOE - Bedford Way (20) - 915',
  'IOE - Bedford Way (20) - 944',
  'Rockefeller Building B14',
  'Rockefeller Building B14A',
  'Rockefeller Building B15',
  'Rockefeller Building B16',
  'Rockefeller Building G02',
  'IOE - Bedford Way (20) - 944',
  'Rockefeller Building G15',
  'IOE - Bedford Way (20) - 102 - Drama Studio',
  'Rockefeller Building G16',
  'IOE - Bedford Way (20) - 102 - Drama Studio',
  'IOE - Bedford Way (20) - 102 - Drama Studio',
  'IOE - Bedford Way (20) - 103 - Jeffery Hall',
  'IOE - Bedford Way (20) - 103 - Jeffery Hall',
  'IOE - Bedford Way (20) - 103 - Jeffery Hall',
  'IOE - Bedford Way (20) - 305 - Clarke Hall',
  'IOE - Bedford Way (20) - 305 - Clarke Hall',
  'Medawar Building G01 Lankester LT',
  'Wilkins Building (Main Building) Gustave Tuck LT',
  'Wilkins Building (Main Building) Haldane Room',
  'Wilkins Building (Main Building) JBR',
  'IOE - Bedford Way (20) - 709a',
  'IOE - Bedford Way (20) - 709a',
  'IOE - Bedford Way (20) - 709a',
  'Wilkins Building (Main Building) Lower South Hall',
  'Wilkins Building (Main Building) Main Quad - South Side',
  'Wilkins Building (Main Building) Main Quad Events Venue - North Side',
  'Wilkins Building (Main Building) North Cloisters',
  'Wilkins Building (Main Building) North Observatory',
  'IOE - Bedford Way (20) - 537',
  'IOE - Bedford Way (20) - 537',
  'IOE - Bedford Way (20) - 537',
  'Malet Place Engineering Building 1.20',
  'IOE - Bedford Way (20) - 539',
  'IOE - Bedford Way (20) - 539',
  'IOE - Bedford Way (20) - 539',
  'IOE - Bedford Way (20) - 603',
  'Bedford Way (26) 316 - Public Cluster',
  'IOE - Bedford Way (20) - 603',
  'IOE - Bedford Way (20) - 603',
  'IOE - Bedford Way (20) - 541',
  'Bedford Way (26) G11 - Public Cluster',
  'Bedford Way (26) LG04',
  'IOE - Bedford Way (20) - 541',
  'IOE - Bedford Way (20) - 541',
  'IOE - Bedford Way (20) - 604',
  'IOE - Bedford Way (20) - 604',
  'IOE - Bedford Way (20) - 604',
  'IOE - Bedford Way (20) - 639',
  'IOE - Bedford Way (20) - 639',
  'IOE - Bedford Way (20) - 639',
  'IOE - Bedford Way (20) - 642',
  'IOE - Bedford Way (20) - 642',
  'Chandler House G10',
  'IOE - Bedford Way (20) - 642',
  'IOE - Bedford Way (20) - 728',
  'IOE - Bedford Way (20) - 728',
  'IOE - Bedford Way (20) - 728',
  'IOE - Bedford Way (20) - 731',
  'IOE - Bedford Way (20) - 731',
  'IOE - Bedford Way (20) - 731',
  'IOE - Bedford Way (20) - 736',
  'IOE - Bedford Way (20) - 736',
  'IOE - Bedford Way (20) - 736',
  'IOE - Bedford Way (20) - 739',
  'IOE - Bedford Way (20) - 739',
  'IOE - Bedford Way (20) - 739',
  'IOE - Bedford Way (20) - 744',
  'IOE - Bedford Way (20) - 744',
  'IOE - Bedford Way (20) - 744',
  'Archaeology 117 - Public Cluster',
  'Archaeology G6 LT',
  'Chadwick Building G08',
  'Drayton House B19',
  'Chandler House 118',
  'Chandler House B01',
  'Chandler House B02',
  'Christopher Ingold Building  G21 Ramsay LT',
  'Christopher Ingold Building XLG1 Chemistry LT',
  'Drayton House B16 Edgeworth Room',
  'Drayton House B20 Jevons LT',
  'IOE - Bedford Way (20) - 101 - Logan Hall',
  'Bedford Way (26) G03',
  'IOE - Bedford Way (20) - 416 - Committee Room 4',
  'IOE - Bedford Way (20) - 429 - PC Lab 1',
  'IOE - Bedford Way (20) - 416 - Committee Room 4',
  'IOE - Bedford Way (20) - 416 - Committee Room 4',
  'IOE - Bedford Way (20) - 417 - Committee Room 1',
  'IOE - Bedford Way (20) - 417 - Committee Room 1',
  'IOE - Bedford Way (20) - 417 - Committee Room 1',
  'IOE - Bedford Way (20) - 418 - Committee Room 2',
  'IOE - Bedford Way (20) - 936',
  'Foster Court 215',
  'IOE - Bedford Way (20) - 654',
  'Birkbeck Gordon Square (43) G03',
  'Birkbeck Malet Street 109',
  'Birkbeck Malet Street 251',
  'Birkbeck Malet Street 252',
  'Birkbeck Malet Street 253',
  'Birkbeck Malet Street 254',
  'Birkbeck Malet Street 255',
  'Birkbeck Malet Street 351',
  'Birkbeck Malet Street 352',
  'Birkbeck Malet Street 353',
  'Birkbeck Malet Street 354',
  'Birkbeck Malet Street 355',
  'School of Pharmacy B37',
  'School of Pharmacy 225',
  'School of Pharmacy 104 John Hanbury LT',
  'School of Pharmacy 228',
  'School of Pharmacy B42',
  'School of Pharmacy G02 Maplethorpe LT',
  'School of Pharmacy M2',
  'School of Pharmacy M3',
  'IOE - Bedford Way (20) - 675',
  'IOE - Bedford Way (20) - 675',
  'IOE - Woburn Square (18) - SSRU Seminar Room',
  'IOE - Woburn Square (18) - SSRU Seminar Room',
  'IOE - Emerald Street (23-29) - UCL Knowledge Lab Large',
  'IOE - Emerald Street (23-29) - UCL Knowledge Lab Small'
]

export default class Demo extends React.Component {

  constructor(props) {
    super(props);

    // let rootURL = 'http://localhost:8000';

    // if (process.env.NODE_ENV === 'production') {
    //   rootURL = 'https://uclapi.com';
    // }

    let rootURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

    this.state = {
      schedule: "",
      roomNameMap: {
        'python': ``,
        'javascript': ``,
        'bash': ``
      },
      rootURL: rootURL
    };

    this.getLanguages = this.getLanguages.bind(this);
    this.getSchedule = this.getSchedule.bind(this);
  }

  getLanguages() {
    let now = new Date();

    return [
      {
        "name": "python",
        "code": `import requests

params = {
  "token": "${window.initialData.temp_token}",
  "results_per_page": 1,
  "date": ${now.toISOString().substring(0, 10).replace(/-/g, "")}, ${this.state.roomNameMap.python}
}

r = requests.get("https://uclapi.com/roombookings/bookings", params=params)
print(r.json())`
      }, {
        "name": "javascript",
        "code": `const token = "${window.initialData.temp_token}";

fetch(
  "https://uclapi.com/roombookings/bookings?token=",
  token,
  "&results_per_page=1", ${this.state.roomNameMap.javascript}
  "&date=" + ${now.toISOString().substring(0, 10).replace(/-/g, "")}
).then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
      }, {
        name: "bash",
        code: `curl https://uclapi.com/roombookings/bookings \\
-d token=${window.initialData.temp_token} \\
-d results_per_page=1 ${this.state.roomNameMap.bash} \\
-d date='${now.toISOString().substring(0, 10).replace(/-/g, "")}'`
      }
    ]
  }

  getSchedule(roomName) {
    this.state.roomNameMap = {
      'python': `\n  "roomname": "${roomName}",`,
      'javascript': `\n  "&roomname=${roomName}",`,
      'bash': `\\ \n-d roomname='${roomName}'`
    }

    let now = new Date();

    // TODO:
    // Need to create development environment in package.json
    let url = `${this.state.rootURL}/roombookings/bookings?token=` + window.initialData.temp_token + "&roomname=" + roomName + "&date=" + now.toISOString().substring(0, 10).replace(/-/g, "");

    fetch(url).then(response => {
      return response.json();
    }).then((data) => {
      this.setState({
        schedule: JSON.stringify(data, null, 4)
      });
    })
  }

  render() {
    let response = <div></div>;

    if (this.state.schedule) {
      response = <div>
        <hr/>
        <SyntaxHighlighter language={"javascript"} style={dracula}>
          {this.state.schedule}
        </SyntaxHighlighter>
      </div>;
    }

    return (
      <div className="demo">

        <div className="text">
          <h2>Get Today's Bookings for a Room</h2>
          <AutoComplete fullWidth={true} floatingLabelText="Room Name" filter={AutoComplete.caseInsensitiveFilter} openOnFocus={true} dataSource={rooms} onNewRequest={this.getSchedule}/>
        </div>

        <div className="code">
          <Tabs>
            {this.getLanguages().map((language, index) => (
              <Tab key={index} label={language.name}>
                <div>
                  <SyntaxHighlighter language={language.name} style={dracula}>{language.code}</SyntaxHighlighter>
                </div>
              </Tab>
            ))}
          </Tabs>

          {response}
        </div>

      </div>
    )
  }

}
