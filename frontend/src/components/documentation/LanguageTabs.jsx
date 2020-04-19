import React from 'react'


/*
  This Component is the top nav bar which also controls the language of
  the code examples.

  It passes the selected language to all of its children
*/

export default class LanguageTabs extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      activeLanguage: `python`,
    }
  }

  changeActiveLanguage = (language) => {
    this.setState({ activeLanguage: language })
  }

  renderChildren = (props) => React.Children.map(props.children, (child, ) =>
    React.cloneElement(child, {
      activeLanguage: this.state.activeLanguage,
    })
  )

  render() {
    return (
      <div>
        <div className="main" style={{ padding: `50px` }}>
          {this.renderChildren(this.props)}
        </div>
      </div>
    )
  }

}
