import phonenumbers
from phonenumbers import geocoder as phone_geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode

# OpenCage API key
Key = "6d6f969fd9024ac8afde957f0c86a5ba"

def get_location_from_phone(number):
    try:
        # Parse the phone number
        check_number = phonenumbers.parse(number)
        
        # Get the location description
        location_description = phone_geocoder.description_for_number(check_number, "en")
        if not location_description:
            raise ValueError("Location description not found.")

        # Get the service provider
        service_provider = phonenumbers.parse(number)
        provider_name = carrier.name_for_number(service_provider, "en")

        print(f"Location: {location_description}")
        print(f"Service Provider: {provider_name}")

        # Use OpenCage Geocoding to get coordinates
        geocoder_service = OpenCageGeocode(Key)
        query = str(location_description)
        results = geocoder_service.geocode(query)
        
        if not results:
            raise ValueError("Geocoding did not return any results.")
        
        # Extract latitude and longitude
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        print(f"Latitude: {lat}, Longitude: {lng}")

        # Create a map with a marker
        map_location = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=location_description).add_to(map_location)
        map_location.save("mylocation.html")

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"Error parsing phone number: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get phone number input
number = input("Enter phone number with country code: ")
get_location_from_phone(number)
