import Icon from './views/Icon.jsx'



/** COPY **/
export const copyIcon = (onClick, style) => (
  <Icon
    image={'/dashboard/copy.svg'}
    description="copy token to clipboard"
    onClick={onClick}
    style={style}
  />
)

/** REFRESH **/
export const refreshIcon = (onClick, style) => (
  <Icon
    image={'/dashboard/refresh.svg'}
    description="refresh token"
    onClick={onClick}
    style={style}
  />
)

/** EDIT**/
export const editIcon = (onClick, style) => (
  <Icon image={'/dashboard/edit.svg'}
    description="edit title of app"
    onClick={onClick}
    style={style}
  />
)

/** SAVE **/
export const saveIcon = (onClick, style) => (
  <Icon
    image={'/dashboard/save.svg'}
    description="save details for future"
    onClick={onClick}
    style={style}
  />
)

/** CANCEL **/
export const cancelIcon = (onClick, style) => (
  <Icon image={'/dashboard/trash.svg'}
    description="cancel action"
    onClick={onClick}
    style={style}
  />
)

/** CHECKED */
export const checkedIcon = (style) => (
  <Icon image={'/dashboard/checked.svg'}
    description="Checked"
    onClick={null}
    style={style}
  />
)

/** UNCHECKED */
export const uncheckedIcon = (style) => (
  <Icon image={null}
    onClick={null}
    style={style}
  />
)
