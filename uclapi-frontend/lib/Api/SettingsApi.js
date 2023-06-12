import axios from "axios";

class SettingsApi {
  static req = axios.create({
    baseURL: "/oauth",
  });
  static get = (url, config) => SettingsApi.req.get(url, config);

  static getSettings = async () => {
    const { data } = await SettingsApi.get("/user/settings");
    return data;
  };

  static deauthoriseApp = async (clientId) => {
    const { data } = await SettingsApi.get("/deauthorise", {
      params: {
        client_id: clientId,
      },
      xsrfHeaderName: "X-CSRFToken",
    });
    return data;
  };
}

export default SettingsApi;
