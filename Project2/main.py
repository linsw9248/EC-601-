import googlemaps
from datetime import datetime


def find_places(address, query_type):

    gmaps = googlemaps.Client(key='AIzaSyBPRE58CTevRuuT5vd1vT2L5ujdTiVNuYk')

 
    geocode_result = gmaps.geocode(address)
    latlng = geocode_result[0]['geometry']['location']
    location = f"{latlng['lat']},{latlng['lng']}"


    places_result = gmaps.places_nearby(location=location, radius=1000, open_now=False, type=query_type)

 
    sorted_places = sorted(places_result['results'], key=lambda x: x.get('rating', 0), reverse=True)

    for place in sorted_places:
        print("Name:", place['name'])
        print("Location:", place['geometry']['location'])
        print("Address:", place.get('vicinity', 'N/A'))
        print("Rating:", place.get('rating', 'N/A'))


        destination = f"{place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
        distance_result = gmaps.distance_matrix(origins=location, destinations=destination, mode='walking')
        distance = distance_result['rows'][0]['elements'][0].get('distance', {}).get('text', 'N/A')
        print("Distance:", distance)


        place_details = gmaps.place(place_id=place['place_id'], fields=['opening_hours'])
        if 'opening_hours' in place_details['result']:
            unformatted_hours = place_details['result']['opening_hours'].get('weekday_text', 'N/A')
        
            formatted_open_hours = [hour.replace('\u202f', ' ').replace('\u2009', ' ') for hour in unformatted_hours]
            print("Open Hours:", formatted_open_hours)
        else:
            print("Open Hours: N/A")

        print("-----------------------------")


if __name__ == "__main__":
    user_address = input("Please enter an address: ")

    print("Select the type of place you are looking for:")
    print("1. Restaurant")
    print("2. Cafe")
    print("3. Gas Station")
    print("4. Grocery Store")

    choice = input("Enter the number corresponding to your choice: ")

    query_type_map = {
        '1': 'restaurant',
        '2': 'cafe',
        '3': 'gas_station',
        '4': 'grocery_or_supermarket'
    }

    query_type = query_type_map.get(choice, 'restaurant')  # Default to 'restaurant' if invalid choice
    find_places(user_address, query_type)
