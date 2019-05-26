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
    STAFF_SURVEY_IDS = [59]
    VALID_SURVEY_FILTERS = ["all", "staff", "student"]

    # address mapping

    SURVEY_LOCATIONS = {
        "UCL Torrington 1-19 113": {
         "lat": "51.521886", "long": "-0.134415",
         "address": [
            "1-19 Torrington Pl",
            "Fitzrovia",
            "London",
            "WC1E 7HB"
         ]
        },
        "UCL Student Centre": {
         "lat": "51.524916", "long": "-0.132371",
         "address": [
            "27-28 Gordon Square",
            "Bloomsbury",
            "London",
            "WC1H 0AH"
         ]
        },
        "UCL SSEES Library": {
         "lat": "51.525342", "long": "-0.131602",
         "address": [
            "16 Taviton St",
            "Bloomsbury",
            "London",
            "WC1H 0BW"
         ]
        },
        "UCL SENIT Suite": {
         "lat": "51.524280", "long": "-0.133026",
         "address": [
            "Wilkins Building",
            "Gower St",
            "London",
            "WC1E 6BT"
         ]
        },
        "UCL Senate House Hub": {
         "lat": "51.521094", "long": "-0.128735",
         "address": [
            "Senate House University of London",
            "Malet St",
            "London",
            "WC1E 7HU"
         ]
        },
        "UCL Science Library": {
         "lat": "51.523556", "long": "-0.132588",
         "address": [
            "DMS Watson Building",
            "Malet Place",
            "London",
            "WC1E 6BT"
         ]
        },
        "UCL School of Pharmacy Library": {
         "lat": "51.524967", "long": "-0.122872",
         "address": [
            "29-39 Brunswick Square",
            "Bloomsbury",
            "London",
            "WC1N 1AX"
         ]
        },
        "UCL Main Library": {
         "lat": "51.524748", "long": "-0.133535",
         "address": [
            "Wilkins Building",
            "Gower St",
            "London",
            "WC1E 6BT"
         ]
        },
        "UCL Language & Speech Science Library": {
         "lat": "51.525847", "long": "-0.122785",
         "address": [
            "2 Wakefield St",
            "Kings Cross",
            "London",
            "WC1N 1PJ"
         ]
        },
        "UCL Institute of Orthopaedics Library": {
         "lat": "51.631529", "long": "-0.306551",
         "address": [
            "Sir Herbert Seddon Teaching Centre",
            "Royal National Orthopaedic Hospital",
            "Brockley Hill, Stanmore",
            "HA7 4LP"
         ]
        },
        "UCL Institute of Neurology, Queen Square Library": {
         "lat": "51.522398", "long": "-0.122973",
         "address": [
            "23 Queen Square",
            "London",
            "WC1N 3BG",
            ""
         ]
        },
        "UCL Institute of Education Library": {
         "lat": "51.522897", "long": "-0.127864",
         "address": [
            "20 Bedford Way",
            "London",
            "WC1H  0AL",
            ""
         ]
        },
        "UCL Institute of Archaeology Library": {
         "lat": "51.524906", "long": "-0.131578",
         "address": [
            "31-34 Gordon Square",
            "WC1H 0PY",
            "",
            ""
         ]
        },
        "UCL Great Ormond Street Institute of Child Health Library": {
         "lat": "51.5232287", "long": "-0.1200982",
         "address": [
            "30 Guilford Street",
            "London",
            "WC1N 1EH",
            ""
         ]
        },
        "UCL Eastman Dental Library": {
         "lat": "51.526314", "long": "-0.117660",
         "address": [
            "256 Gray's Inn Road",
            "King's Cross",
            "London",
            "WC1X 8LD"
         ]
        },
        "UCL Ear Institute & Hearing Loss Library": {
         "lat": "51.529268", "long": "-0.119571",
         "address": [
            "330-336 Grays Inn Rd",
            "Kings Cross",
            "London",
            "WC1X 8EE"
         ]
        },
        "UCL Cruciform Hub": {
         "lat": "51.524054", "long": "-0.135032",
         "address": [
            "Cruciform Building, Gower St",
            "Fitzrovia",
            "London",
            "WC1E 6BT"
         ]
        },
        "UCL Christopher Ingold G20": {
         "lat": "51.525370", "long": "-0.132171",
         "address": [
            "20 Gordon St",
            "Kings Cross",
            "London",
            "WC1H 0AJ"
         ]
        },
        "UCL chadwick B04": {
         "lat": "51.524233", "long": "-0.134336",
         "address": [
            "Chadwick building, Gower St",
            "Bloomsbury",
            "London",
            "WC1E 6DE"
         ]
        },
        "UCL Chadwick 223": {
         "lat": "51.524233", "long": "-0.134336",
         "address": [
            "Chadwick building, Gower St",
            "Bloomsbury",
            "London",
            "WC1E 6DE"
         ]
        },
        "UCL Bedfordway G11": {
         "lat": "51.523857", "long": "-0.128845",
         "address": [
            "26 Bedford Way",
            "Bloomsbury",
            "London",
            "WC1H 0AP"
         ]
        },
        "UCL Bedfordway 316": {
         "lat": "51.523857", "long": "-0.128845",
         "address": [
            "26 Bedford Way",
            "Bloomsbury",
            "London",
            "WC1H 0AP"
         ]
        },
        "UCL Bartlett Library": {
         "lat": "51.526812", "long": "-0.129855",
         "address": [
            "14 Upper Woburn Pl",
            "Bloomsbury",
            "London",
            "WC1H 0NN"
         ]
        },
        "UCL Archaeology 501": {
         "lat": "51.524908", "long": "-0.131575",
         "address": [
            "31-34 Gordon Square",
            "Kings Cross",
            "London",
            "WC1H 0PY"
         ]
        },
        "UCL Archaeology 117": {
         "lat": "51.524908", "long": "-0.131575",
         "address": [
            "31-34 Gordon Square",
            "Kings Cross",
            "London",
            "WC1H 0PY"
         ]
        },
        "UCL Anatomy Hub ": {
         "lat": "51.523625", "long": "-0.133624",
         "address": [
            "Anatomy Building",
            "Gower St",
            "London",
            "WC1E 6XA"
         ]
        },
        "UCL 23 Gordon Square  history cluster": {
         "lat": "51.524497", "long": "-0.132115",
         "address": [
            "23 Gordon Square",
            "London",
            "WC1H 0AG",
            ""
         ]
        },
        "The Joint Library of Ophthalmology": {
         "lat": "51.527235", "long": "-0.091205",
         "address": [
            "11-43 Bath Street",
            "London",
            "EC1V 9EL",
            ""
         ]
        },
        "Royal Free Hospital Medical Library": {
         "lat": "51.552507", "long": "-0.165783",
         "address": [
            "Rowland Hill Street",
            "Hampstead",
            "London",
            "NW3 2PF"
         ]
        },
        "Graduate Hub - RP Dev Testing": {
         "lat": "51.524143", "long": "-0.133525",
         "address": [
            "South Wing, Gower St",
            "Kings Cross",
            "London",
            "WC1E 6DE",
         ]
        },
        "Graduate Hub": {
         "lat": "51.524143", "long": "-0.133525",
         "address": [
            "South Wing, Gower St",
            "Kings Cross",
            "London",
            "WC1E 6DE",
         ]
        },
        "Foster Court": {
         "lat": "51.523555", "long": "-0.132497",
         "address": [
            "Foster Court, Gower St",
            "Bloomsbury",
            "London",
            "WC1E 6BT"
         ]
        },
        "1 Saint Martin Le Grand": {
         "lat": "51.516380", "long": "-0.097666",
         "address": [
            "1 St Martin's Le Grand",
            "London",
            "EC1A 4NP",
            ""
         ]
        }
    }
