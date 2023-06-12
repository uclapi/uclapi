
import { FiChevronDown, FiChevronRight } from 'react-icons/fi'
import './AccordionIcon.module.scss'

const AccordionIcon = ({ isActive }) => (
  <div className="accordion-icon">
    {isActive ? <FiChevronDown /> : <FiChevronRight />}
  </div>
)

export default AccordionIcon
