import propTypes from 'prop-types'
import React from 'react'
import Topic from './Topic.jsx'



const SectionHeader = ({ link, title }) => (
  <Topic
    noExamples
  >
    <h1 id={link} className="section-header">{title}</h1>
  </Topic>
)

SectionHeader.propTypes = {
  link: propTypes.string,
  title: propTypes.string,
}

SectionHeader.defaultProps = {
  link: ``,
  title: ``,
}

export default SectionHeader