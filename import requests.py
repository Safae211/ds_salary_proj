import requests

# Make a request to IPinfo Lite
response = requests.get("https://ipinfo.io/json")
data = response.json()

# Print relevant info
print("Your IP address:", data.get("ip"))
print("City:", data.get("city"))
print("Region:", data.get("region"))
print("Country:", data.get("country"))
print("Location coordinates:", data.get("loc"))
