def make_get_url_func(url):
    def get_url():
        import urllib2

        f = urllib2.urlopen(url)
        return f.read()
    return get_url

def get_weather(xml_data):
    """
    Shows the weather for the given place.
    """

    import elementtree.ElementTree as ET
    
    page = ET.fromstring(unicode(xml_data, errors="ignore"))

    weather = page.find( "weather/current_conditions" )

    return {
        'f' : weather.find( "temp_f" ).get( "data" ),
        'c' : weather.find( "temp_c" ).get( "data" ),
        'humidity' : weather.find( "humidity" ).get( "data" ),
        'wind' : weather.find( "wind_condition" ).get( "data" )
        }

def test_get_weather():
    xml_data = """<?xml version="1.0"?><xml_api_reply version="1"><weather module_id="0" tab_id="0"><forecast_information><city data="Chicago, IL"/><postal_code data="60657"/><latitude_e6 data=""/><longitude_e6 data=""/><forecast_date data="2008-04-07"/><current_date_time data="2008-04-07 06:38:00 +0000"/><unit_system data="US"/></forecast_information><current_conditions><condition data="Cloudy"/><temp_f data="57"/><temp_c data="14"/><humidity data="Humidity: 47%"/><icon data="/images/weather/cloudy.gif"/><wind_condition data="Wind: N at 0 mph"/></current_conditions><forecast_conditions><day_of_week data="Today"/><low data="40"/><high data="56"/><icon data="/images/weather/cloudy.gif"/><condition data="Cloudy"/></forecast_conditions><forecast_conditions><day_of_week data="Tue"/><low data="45"/><high data="54"/><icon data="/images/weather/thunderstorm.gif"/><condition data="Thunderstorm"/></forecast_conditions><forecast_conditions><day_of_week data="Wed"/><low data="40"/><high data="54"/><icon data="/images/weather/mostly_sunny.gif"/><condition data="Partly Sunny"/></forecast_conditions><forecast_conditions><day_of_week data="Thu"/><low data="38"/><high data="49"/><icon data="/images/weather/chance_of_rain.gif"/><condition data="Chance of Showers"/></forecast_conditions></weather></xml_api_reply>"""

    assert get_weather(xml_data) == {'c': '14', 'humidity': 'Humidity: 47%', 'wind': 'Wind: N at 0 mph', 'f': '57'}

def cmd_weather(ensoapi, place="Sao Paulo"):
    import urllib
    zipcode = cmd_weather.places[place]
    url = "http://www.google.com/ig/api?weather=%s" % urllib.quote( zipcode.encode("utf-8") )
    thread = ThreadedFunc(make_get_url_func(url))
    while thread.isAlive():
        yield
    weather_xml = thread.getRetval()
    if not weather_xml:
        ensoapi.display_message("An error occurred when getting the weather.")
    else:
        wdict = get_weather(weather_xml)
        wdict["place"] = place
        print wdict
        ensoapi.display_message(u"In %(place)s it is "
                                u"%(c)s\u00b0C, "
                                u"%(humidity)s, %(wind)s." % wdict)

cmd_weather.places = { "Sao Paulo" : "sao paulo",
                       "Sao Jose dos Campos" : "sao jose dos campos"
                     }
cmd_weather.valid_args = cmd_weather.places.keys()