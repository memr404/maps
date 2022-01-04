from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from folium.plugins import Draw
import folium, io, sys, json

if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
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

	folium.GeoJson(point, show=False, name="Point").add_to(m)

	folium.LayerControl().add_to(m)


	draw = Draw(
	   draw_options={
		  'polyline':False,
		  'rectangle':True,
		  'polygon':True,
		  'circle':False,
		  'marker':True,
		  'circlemarker':False},
	   edit_options={'edit':False})
	m.add_child(draw)

	data = io.BytesIO()
	m.save(data, close_file=False)

	class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
		def javaScriptConsoleMessage(self, level, msg, line, sourceID):
			coords_dict = json.loads(msg)
			print(*coords_dict['geometry']['coordinates'])

	view = QtWebEngineWidgets.QWebEngineView()
	page = WebEnginePage(view)
	view.setPage(page)
	view.setHtml(data.getvalue().decode())
	view.show()
	sys.exit(app.exec_())
