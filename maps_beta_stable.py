import io
import sys
import json
import branca
import ctypes
import folium
import requests
import pandas as pd
from PyQt5 import QtWidgets
from string import Template
import branca.colormap as cm
from datetime import datetime
from folium import MacroElement
from branca.element import Figure
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

timenow = datetime.now().time()
print("Запуск программы в", timenow)

class MyApp(QWidget):
	def __init__(self):
		super().__init__()

		self.timenow = datetime.now().time()
		self.setWindowTitle('TESTING Запуск в ' + str(self.timenow))

		user32 = ctypes.windll.user32
		self.window_width, self.window_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		self.setMinimumSize(self.window_width, self.window_height)
		#self.setMinimumSize(750,450)
		layout = QVBoxLayout()
		self.setLayout(layout)

		polygon = "https://raw.githubusercontent.com/memr404/maps/main/custom.geo.json" # <<------------!!!!
		point = "https://raw.githubusercontent.com/memr404/maps/main/russia_forest_point.json"
		village = "https://raw.githubusercontent.com/memr404/maps/main/russia_village_green_polygon.geojson"


		coordinate = (51.82863658513971, 107.68517779175471)
		m = folium.Map(
			tiles='Stamen Terrain',
			zoom_strt=3, #13
			location=coordinate
		)

		folium.GeoJson(polygon, style_function=lambda feature: {
			'color': 'green',
			'weight': '0.5',
			'fill': True,
			'fill_opacity' : '1'
		}, name="Polygon").add_to(m)

		folium.GeoJson(village, show=False, style_function=lambda feature: {
			'color': 'yellow',
			'weight': '0.5',
			'fill': True,
			'fill_opacity' : '1'
		}, name="Village")#.add_to(m)

		folium.GeoJson(point, name="Point").add_to(m)

		folium.LayerControl().add_to(m)

		class LatLngPopup(MacroElement):
			_template = Template(u"""
					{% macro script(this, kwargs) %}
						var {{this.get_name()}} = L.popup();
						function latLngPop(e) {
							{{this.get_name()}}
								.setLatLng(e.latlng)
								.setContent("Latitude: " + e.latlng.lat.toFixed(4) +
											"<br>Longitude: " + e.latlng.lng.toFixed(4))
								.openOn({{this._parent.get_name()}});
							parent.document.getElementById("id_lng").value = e.latlng.lng.toFixed(4);
							parent.document.getElementById("id_lat").value = e.latlng.lat.toFixed(4);
							}
						{{this._parent.get_name()}}.on('click', latLngPop);
					{% endmacro %}
					""")  # noqa

			def __init__(self):
				super(LatLngPopup, self).__init__()
				self._name = 'LatLngPopup'
		
		folium.LatLngPopup().add_to(m)
		#m.add_child(folium.LatLngPopup())
		#m.add_child(folium.ClickForMarker(popup="Метка")) # icon=folium.Icon(color="red"),
		m
		
		self.timenow = datetime.now().time()
		print("Внедрение файла (JSON) готово в", self.timenow, ". Идёт операция обработки!")
		

		# Сохранение карты и обработка
		data = io.BytesIO()
		m.save(data, close_file=False)

		self.timenow = datetime.now().time()
		print("Обработка завершенна в", self.timenow)
		webView = QWebEngineView()

		webView.setHtml(data.getvalue().decode())
		layout.addWidget(webView)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			font-size: 35px;
		}
	''')
	
	myApp = MyApp()
	myApp.show()

	try:
		sys.exit(app.exec_())
	except SystemExit:
		timenow = datetime.now().time()
		print('Закрытие окна в', timenow)
