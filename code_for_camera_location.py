from pathlib import Path
import json
import folium

# Read and load the geojson file
path = Path('Traffic Camera List.geojson')
lines = path.read_text()
save_data = json.loads(lines)

# Save the processed data back to another geojson file
path = Path('after_process.geojson')
load_data = json.dumps(save_data, indent=4)
path.write_text(load_data)

# Initialize lists to store coordinates, mainroads, and crossroads
all_data = save_data['features']
coords, mainroads, crossroads = [], [], []

for data in all_data:
    # Extract coordinates, mainroad, and crossroad
    coord = data['geometry']['coordinates']  # Assuming coordinates are in [longitude, latitude] format
    main = data['properties']['MAINROAD']
    cross = data['properties']['CROSSROAD']
    
    # Append the extracted data to the respective lists
    coords.append((coord[0][0], coord[0][1], main, cross))  # Append coordinates as (latitude, longitude)
    mainroads.append(main)
    crossroads.append(cross)

# Initialize the map at the first coordinate
if coords:
    mapit = folium.Map(location=[coords[0][1], coords[0][0]], zoom_start=12)

    # Add markers to the map
    for cors in coords:
        popup_content = f"Main Road {cors[2]} <br><br> Cross Road {cors[3]} <br><br> Intersection {cors[2] + cors[3]}"
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(location=[cors[1], cors[0]], popup=popup).add_to(mapit)
    # Save the map to an HTML file
    mapit.save('traffic_cameras_loc_toronto.html')
else:
    print("No coordinates found to plot on the map.")

# Print the extracted coordinates
print(coords)
