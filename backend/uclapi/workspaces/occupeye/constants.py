import os


class OccupEyeConstants():
    """
    A function-less class that defines cache and URL constants
    for the OccupEye API.
    These are used to try and avoid typos and repeated typing
    of long strings.
    Each {} is a format string container that is replaced by
    an appropriate string from a variable inside the function
    using the constant.
    """
    # Environment Variables
    DEPLOYMENT_ID = os.environ["OCCUPEYE_DEPLOYMENT_ID"]
    DEPLOYMENT_NAME = os.environ["OCCUPEYE_DEPLOYMENT_NAME"]
    BASE_URL = os.environ["OCCUPEYE_BASE_URL"]
    USERNAME = os.environ["OCCUPEYE_USERNAME"]
    PASSWORD = os.environ["OCCUPEYE_PASSWORD"]

    # Redis Keys
    ACCESS_TOKEN_KEY = "occupeye:access_token"
    ACCESS_TOKEN_EXPIRY_KEY = "occupeye:access_token_expiry"

    SURVEYS_LIST_KEY = "occupeye:surveys"
    SURVEY_DATA_KEY = "occupeye:surveys:{}"
    SURVEY_MAPS_LIST_KEY = "occupeye:surveys:{}:maps"
    SURVEY_MAP_DATA_KEY = "occupeye:surveys:{}:maps:{}"
    SURVEY_MAX_TIMESTAMP_KEY = "occupeye:surveys:{}:max_timestamp"
    SURVEY_SENSORS_LIST_KEY = "occupeye:surveys:{}:sensors"
    SURVEY_SENSOR_DATA_KEY = "occupeye:surveys:{}:sensors:{}:data"
    SURVEY_SENSOR_STATUS_KEY = "occupeye:surveys:{}:sensors:{}:status"
    SURVEY_MAP_SENSORS_LIST_KEY = "occupeye:surveys:{}:maps:{}:sensors"
    SURVEY_MAP_SENSOR_PROPERTIES_KEY = (
        "occupeye:surveys:{}:maps:{}:sensors:{}:properties"
    )
    SURVEY_MAP_VMAX_X_KEY = "occupeye:surveys:{}:maps:{}:VMaxX"
    SURVEY_MAP_VMAX_Y_KEY = "occupeye:surveys:{}:maps:{}:VMaxY"
    SURVEY_MAP_VIEWBOX_KEY = "occupeye:surveys:{}:maps:{}:viewbox"

    SUMMARY_CACHE_SURVEY = "occupeye:summaries:{}"
    SUMMARY_CACHE_ALL_SURVEYS = "occupeye:summaries:all"
    SUMMARY_CACHE_ALL_STUDENT_SURVEYS = "occupeye:summaries:all:student"
    SUMMARY_CACHE_ALL_STAFF_SURVEYS = "occupeye:summaries:all:staff"

    IMAGE_BASE64_KEY = "occupeye:image:{}:base64"
    IMAGE_CONTENT_TYPE_KEY = "occupeye:image:{}:content_type"

    TIMEAVERAGE_KEY = "occupeye:query:timeaverage:{}:{}"

    URL_BASE_DEPLOYMENT = "{}/{}".format(BASE_URL, DEPLOYMENT_NAME)

    # Cad-Cap Endpoints
    URL_MAPS_BY_SURVEY = URL_BASE_DEPLOYMENT + "/api/Maps/?surveyid={}"
    URL_SURVEYS = URL_BASE_DEPLOYMENT + "/api/Surveys/"
    URL_SURVEY_DEVICES = URL_BASE_DEPLOYMENT + "/api/SurveyDevices?surveyid={}"

    URL_SURVEY_DEVICES_LATEST = URL_BASE_DEPLOYMENT + \
        "/api/SurveySensorsLatest/{}"

    URL_IMAGE = URL_BASE_DEPLOYMENT + \
        "/api/images/{}?max_width=1000&max_height=1000"

    URL_SURVEY_MAX_TIMESTAMP = URL_BASE_DEPLOYMENT + \
        "/api/SurveyMaxMessageTime/{}"

    URL_MAPS = URL_BASE_DEPLOYMENT + "/api/Maps/{}?origin=tl"

    URL_QUERY = (
        URL_BASE_DEPLOYMENT + "/api/Query?"
        "startdate={}&"
        "enddate={}&"
        "SurveyID={}&"
        "QueryType=ByDateTime&"
        "StartTime=00%3A00&"
        "EndTime=24%3A00&"
        "GroupBy[]=TriggerDate&"
        "GroupBy[]=TimeSlot&"
    )

    # Valid historical time periods
    VALID_HISTORICAL_DATA_DAYS = [1, 7, 30]

    # Set a filter for surveys designed for staff only
    STAFF_SURVEY_IDS = [49, 59]
    VALID_SURVEY_FILTERS = ["all", "staff", "student"]
