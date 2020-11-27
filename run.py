from geopy.geocoders import Nominatim
import folium
LOCATOR = Nominatim(user_agent="myGeocoder")
POZNAN_LOCATION = LOCATOR.geocode("Poznań, Poland")


class ListaLadunkow:
    """
    Klasa zawierającego wszystkie ładunki i generująca mapę.
    """
    def __init__(self):
        self.ladunki = []
        self.map = None

    def generuj_mape(self):
        self.map = folium.Map(
            location=[POZNAN_LOCATION.latitude, POZNAN_LOCATION.longitude],
            zoom_start=12,
            tiles='cartodbpositron'
        )
        for location in self.ladunki:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=location.text,
                tooltip=location.tooltip,
                icon=folium.Icon(color=location.priorytet, icon=location.icon)
            ).add_to(self.map)
        self.map.save('index.html')


class LokalizacjaLadunku:
    """
    Szczegóły dotyczące pojedynczego ładunku
    """
    def __init__(self, adres, text="", priorytet=5):
        self.adres = adres
        self.text = "<B>" + text + "</B>" + "<BR>===<BR>" + self.adres
        self.tooltip = text
        if priorytet <= 1:
            self.priorytet = "red"
            self.icon = "info-sign"
        elif priorytet == 2:
            self.priorytet = "orange"
            self.icon = "warning-sign"
        else:
            self.priorytet = "blue"
            self.icon = "cloud"
        self.latitude = None
        self.longitude = None
        self.get_gps_location()

    def get_gps_location(self):
        lokalizacja = LOCATOR.geocode(self.adres)
        self.latitude = lokalizacja.latitude
        self.longitude = lokalizacja.longitude


if __name__ == '__main__':
    lok_class = ListaLadunkow()
    lok_class.ladunki.append(LokalizacjaLadunku("Szyperska 1, Poznań, Poland", "AK47", 1))
    lok_class.ladunki.append(LokalizacjaLadunku("Woźna 2, Poznań, Poland", "H&K", 2))
    lok_class.ladunki.append(LokalizacjaLadunku("Garbary 55, Poznań, Poland", "M4", 3))
    lok_class.generuj_mape()

