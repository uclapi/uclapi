import axios from 'axios'

class Api {
  static req = axios.create({
    baseURL:`/oauth`,
  })
  static get = (url) => Api.req.get(url)

  static getSettings = async () => {
    const { data } = await Api.get(`/user/settings`)
    return data
  }
}

export default Api