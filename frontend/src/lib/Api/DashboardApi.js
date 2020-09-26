import axios from 'axios'
import Cookies from 'js-cookie'
import qs from 'qs'

class DashboardApi {
  static req = axios.create({
    baseURL: `/dashboard/api`,
    withCredentials: true,
    headers: {
      'Content-Type': `application/x-www-form-urlencoded`,
      'X-CSRFToken': Cookies.get(`csrftoken`),
    },
  })

  static post = (url, body) => DashboardApi.req.post(url, qs.stringify(body))
  static get = (url) => DashboardApi.req.get(url)

  static regenToken = async (appId) => {
    const { data: { app: { token } } } = await DashboardApi.post(`/regen/`, { app_id: appId })
    return token
  }

  static regenVerificationSecret = async (appId) => {
    const { data: { new_secret } } = await DashboardApi.post(`/webhook/refreshsecret/`, { app_id: appId })
    return new_secret
  }

  static updateWebhookSettings = async (appId, settings) => {
    const { data: { ok, message, ...values } } = await DashboardApi.post(`/webhook/edit/`, {
      app_id: appId,
      ...settings,
    })
    if(!ok){
      throw new Error(message)
    }
    return values
  }

  static addNewProject = async (name) => {
    const { data: { app } } = await DashboardApi.post(`/create/`, { name })
    return app
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