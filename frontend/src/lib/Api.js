import axios from 'axios'
import Cookies from 'js-cookie'
import qs from 'qs'

class Api {
  static req = axios.create({
    baseURL: `/dashboard/api`,
    withCredentials: true,
    headers: {
      'Content-Type': `application/x-www-form-urlencoded`,
      'X-CSRFToken': Cookies.get(`csrftoken`),
    },
  })

  static post = (url, body) => Api.req.post(url, qs.stringify(body))

  static regenToken = async (appId) => {
    const { data: { app: { token } } } = await Api.post(`/regen/`, { app_id: appId })
    return token
  }

  static regenVerificationSecret = async (appId) => {
    const { data: { new_secret } } = await Api.post(`/webhook/refreshsecret/`, { app_id: appId })
    return new_secret
  }

  static updateWebhookSettings = async (appId, settings) => {
    const { data: { ok, message, ...values } } = await Api.post(`/webhook/edit/`, {
      app_id: appId,
      ...settings,
    })
    if(!ok){
      throw new Error(message)
    }
    return values
  }

  static addNewProject = async (name) => {
    const { data: { app } } = await Api.post(`/create/`, { name })
    return app
  }

  static deleteProject = async (appId) => {
    const { data } = await Api.post(`/delete/`, { app_id: appId })
    return data
  }

  static renameProject = async (appId, name) => {
    const { data } = await Api.post(`/rename/`, {
      app_id: appId,
      new_name: name,
    })
    return data
  }

  static saveOAuthCallback = async (appId, url) => {
    const { data: { success, message } } = await Api.post(`/setcallbackurl/`, {
      app_id: appId,
      callback_url: url,
    })
    if(!success){
      throw new Error(message)
    }
    return success
  }

  static setScope = async (appId, scopes) => {
    const { data } = await Api.post(`/updatescopes/`, {
      app_id: appId,
      scopes,
    })
    return data
  }
}

export default Api