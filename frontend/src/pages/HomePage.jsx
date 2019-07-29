// Standard React importss
import React from 'react';
import ReactDOM from 'react-dom';

// Styles
import './../sass/common/uclapi.scss';

// Common Components
import { SingleColumn, CenterContent } from 'Layout/Items.jsx';

class HomePage extends React.Component {

  render () {
    return (
      <div className = "home-page">
        <SingleColumn
          height = "600px"
          src = "splash_screen" 
          content = <CenterContent
                      isJustified={true}
                      content={<div className='landing-page-intro'>
                                  <h1>UCL API</h1>
                                  <h2>UCL API is a student-built platform for student 
                                  developers to improve the student experience of everyone at UCL.</h2>
                               </div>}
                    />
        />
        <SingleColumn
          isPadded={true}
          color="dark-grey"
          content = <CenterContent
                      isJustified={true}
                      content={<div className='landing-page-goal'>
                                  <h1>Our Goal</h1>
                                  <h2>Create a ridiculously simple, documentation first, and comprehensive API around UCL
                                  &quot;s digital services and establish an ecosystem of third party UCL apps and 
                                  services that use the API.</h2>
                               </div>}
                    />
        />
        <SingleColumn 
          isPadded={true}
          color="maroon"
          content = <CenterContent
                      isJustified={true}
                      content={<div className='landing-page-links'>
                                  <h1>Get Started using our APIs</h1>
                               </div>}
                    />
        />
        <SingleColumn
          isPadded={true}
          color="dark-grey"
          content = <CenterContent
                      content={<div className='landing-page-blog'>
                                  <h1>Check out our blog for tutorials.</h1>
                                  <h2>UCL API is a student-built platform for student 
                                  developers to improve the student experience of everyone at UCL.</h2>
                               </div>}
                    />
        />
        <SingleColumn
          src="market"
          height="600px"
          content = <CenterContent
                      isJustified={true}
                      content={<div className='landing-page-marketplace'>
                                  <h1>Marketplace</h1>
                                  <h2>Check out UCL Marketplace to find apps built using UCL API</h2>
                               </div>}
                    />
        />
        <SingleColumn
          color="dark-grey"
          isPadded={true}
          content = <CenterContent
                      isJustified={true}
                      content={<div className='landing-page-footer'>
                                  <h1>We&quot;re open source and proud!</h1>
                                  <h2>Check out our fleshy internals on GitHub!</h2>
                               </div>}
                    />
        />
      </div>
    );
  }

}

ReactDOM.render(
  <HomePage />,
  document.querySelector('.app')
);
