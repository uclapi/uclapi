import axios from 'axios'

class SettingsApi {
  static req = axios.create({
    baseURL:`/oauth`,
  })
  static get = (url) => SettingsApi.req.get(url)

  static getSettings = async () => {
    const { data } = await SettingsApi.get(`/user/settings`)
    return data
  }
}

export default SettingsApi