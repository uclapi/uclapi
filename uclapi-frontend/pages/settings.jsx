import React, { useState , useEffect } from 'react'

import SettingsLayout from '@/components/appsettings/SettingsLayout.jsx'
import Api from '../lib/Api'

const AppSettings = () => {
  const [data, setData] = useState({
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
    fullname,
    department,
    apps,
  } = data

  return <SettingsLayout
    fullname={fullname}
    department={department}
    authorised_apps={apps}
  />
}

export default AppSettings
