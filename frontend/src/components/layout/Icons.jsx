// React
import React from 'react'

// Base Icon
import Icon from './views/Icon.jsx'

// Images
import clipboardImage from 'Images/dashboard/clipboard.svg'
import editImage from 'Images/dashboard/edit.svg'
import refreshImage from 'Images/dashboard/refresh.svg'
import saveImage from 'Images/dashboard/save.svg'
import deleteImage from 'Images/dashboard/trash.svg'

/** COPY **/
export const clipboardIcon = (onClick, style) => <Icon image={clipboardImage} description="copy token to clipboard" onClick={onClick} style={style} />

/** REFRESH **/
export const refreshIcon = (onClick, style) => <Icon image={refreshImage} description="refresh token" onClick={onClick} style={style} />

/** EDIT**/
export const editIcon = (onClick, style) => <Icon image={editImage} description="edit title of app" onClick={onClick} style={style} /> 

/** SAVE **/
export const saveIcon = (onClick, style) => <Icon image={saveImage} description="save details for future" onClick={onClick} style={style} /> 

/** CANCEL **/
export const cancelIcon = (onClick, style) => <Icon image={deleteImage} description="cancel action" onClick={onClick} style={style} /> 