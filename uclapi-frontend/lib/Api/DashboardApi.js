import axios from 'axios'
import Cookies from 'js-cookie'
import qs from 'qs'

export class MissingAUPAgreementError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

class DashboardApi {
  static req = axios.create({
    baseURL: `/dashboard/api`,
    withCredentials: true,
    headers: {
      'Content-Type': `application/json`,
    },
  })

  static post = (url, body) => DashboardApi.req.post(url, JSON.stringify(body))
  static get = (url) => DashboardApi.req.get(url)

  static regenToken = async (appId) => {
    const { data: { app: { token } } } = await DashboardApi.post(`/regen/`, { app_id: appId })
    return token
  }

  static acceptAup = async () => {
    const { data } = await DashboardApi.post('/accept-aup/')
    if (!data.success) {
      throw new Error(
        "There was an error accepting the Acceptable Use Policy. Please try again later or contact us if the issue persists"
      )
    }
    return true
  }

  static addNewProject = async (name) => {
    try {
      const { data: { app } } = await DashboardApi.post(`/create/`, { name })
      return app
    } catch (err) {
      if (err.response && err.response.status === 403) {
        throw new MissingAUPAgreementError()
      }
      throw err;
    }
  }

  static deleteProject = async (appId) => {
    const { data } = await DashboardApi.post(`/delete/`, { app_id: appId })
    return data
  }

  static renameProject = async (appId, name) => {
    const { data } = await DashboardApi.post(`/rename/`, {
      app_id: appId,
      new_name: name,
    })
    return data
  }

  static saveOAuthCallback = async (appId, url) => {
    const { data: { success, message } } = await DashboardApi.post(`/setcallbackurl/`, {
      app_id: appId,
      callback_url: url,
    })
    if(!success){
      throw new Error(message)
    }
    return success
  }

  static setScope = async (appId, scopes) => {
    const { data } = await DashboardApi.post(`/updatescopes/`, {
      app_id: appId,
      scopes,
    })
    return data
  }

  static getData = async () => {
    const { data } = await DashboardApi.get(`/apps/`)
    return data
  }
}

export default DashboardApi
