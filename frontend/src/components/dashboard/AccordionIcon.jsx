import React from 'react'
import { FiChevronDown, FiChevronRight } from 'react-icons/fi'
import './AccordionIcon.scss'

const AccordionIcon = ({ isActive }) => (
  <div className="accordion-icon">
    {isActive ? <FiChevronDown /> : <FiChevronRight />}
  </div>
)

export default AccordionIcon