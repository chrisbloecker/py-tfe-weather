import requests
import xml.etree.ElementTree as ET


def get_temperature():
    """
    Retrieves the current temperature from TFE @ Umeå University.

    Raises:
        ToDo: figure out which exceptions can be thrown

    Returns:
        The current temperature in degrees celsius if the service can be reached
        and the response can be parsed into a float, None otherwise.
    """

    url     = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Temp"
    content = requests.get(url).content.decode("utf-8")

    root    = ET.fromstring(content)

    return float(root.text.replace(",", "."))


def degree_to_compass(degree):
    """
    Converts the wind direction from degrees to a compass bearing.

    Shamelessly copied from @steve-gregory
    https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
    """
    val      = int((degree / 22.5) + .5)
    bearings = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return bearings[val % 16]


def get_weather():
    """
    Retrieves the current weather from TFE @ Umeå University.

    Raises:
        ToDo: figure out which exceptions can be thrown

    Returns:
        A dictionary with the current weather of the following form:
        { "state"        : str
        , "temperature"  : float
        , "humidity"     : float
        , "pressure"     : int
        , "wind_speed"   : float
        , "wind_bearing" : int
        }
    """

    url     = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Aktuellavarden"
    content = requests.get(url).content.decode("utf-8")

    root    = ET.fromstring(content)
    values  = ET.fromstring(root.text)

    res = dict( temperature  = float(values.find("tempmed").text.replace(",", "."))
              , humidity     = float(values.find("fukt").text.replace(",", "."))
              , pressure     = int(values.find("tryck").text)
              , wind_speed   = float(values.find("vindh").text.replace(",", ".")) * 3.6
              , wind_bearing = degree_to_compass(int(values.find("vindr").text))
              )

    # ToDo: we need to calculate the state from the values. For now, it's always sunny in Umeå
    state = "sunny"

    res["state"] = state

    return res
