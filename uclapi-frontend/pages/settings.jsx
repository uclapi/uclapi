import {
  cyan,
  grey,
  pink,
} from '@mui/material/colors'
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles'
import { Footer } from '@/components/layout/Items.jsx'
import React, { useState , useEffect } from 'react'

import LogInLayout from '@/components/appsettings/LogInLayout.jsx'
import SettingsLayout from '@/components/appsettings/SettingsLayout.jsx'
import Api from '../lib/Api'

const {
  500: cyan500,
} = cyan
const {
  100: grey100,
  300: grey300,
  400: grey400,
  500: grey500,
  900: darkBlack,
} = grey
const {
  A200: pinkA200,
} = pink
const white = `#ffffff`
const fullBlack = `#000000`

const muiTheme = createTheme({
  fontFamily: `Roboto, sans-serif`,
  palette: {
    primary1Color: `#434343`,
    primary2Color: `#434343`,
    primary3Color: grey400,
    accent1Color: pinkA200,
    accent2Color: grey100,
    accent3Color: grey500,
    textColor: darkBlack,
    alternateTextColor: white,
    canvasColor: white,
    borderColor: grey300,
    pickerHeaderColor: cyan500,
    shadowColor: fullBlack,
  },
})

const AppSettings = () => {
  const [data, setData] = useState({
    status: ``,
    fullname: ``,
    user_id: 0,
    department: ``,
    scopes: [],
    apps: [],
  })

  useEffect(() => {
    (async () => {
      const data = await Api.settings.getSettings()
      setData(data)
    })()
  }, [])

  const {
    status,
    url,
    fullname,
    department,
    apps,
  } = data

  if (status !== `ONLINE`) {
    return <MuiThemeProvider theme={muiTheme}>
      <LogInLayout url={url} />
      <Footer />
    </MuiThemeProvider>
  } else {
    return <MuiThemeProvider theme={muiTheme}>
      <SettingsLayout
        fullname={fullname}
        department={department}
        authorised_apps={apps}
      />
      <Footer />
    </MuiThemeProvider>
  }
}

export default AppSettings
