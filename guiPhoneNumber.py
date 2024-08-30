import tkinter as tk
from tkinter import messagebox
import phonenumbers
from phonenumbers import geocoder as phone_geocoder, carrier

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

        return location_description, provider_name, None

    except phonenumbers.phonenumberutil.NumberParseException as e:
        return None, None, f"Error parsing phone number: {e}"
    except Exception as e:
        return None, None, f"An error occurred: {e}"

def on_submit():
    number = entry.get()
    location_description, provider_name, error_message = get_location_from_phone(number)
    
    if error_message:
        messagebox.showerror("Error", error_message)
        return
    
    result_label.config(text=f"Location: {location_description}\nService Provider: {provider_name}")

# Create the main window
root = tk.Tk()
root.title("Phone Number Location Finder")

# Create and place widgets
tk.Label(root, text="Enter phone number with country code:").pack(padx=10, pady=5)

entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=5)

submit_button = tk.Button(root, text="Find Location", command=on_submit)
submit_button.pack(padx=10, pady=5)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
