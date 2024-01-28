import overpy
api = overpy.Overpass()

import requests

def overpass_query(bbox):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        (
            way["building"](40.9711,29.0182,41.0249,29.0653);
        );
        out center;
    """

    params = {
        'data': overpass_query.replace("\n", "").replace("bbox", bbox)
    }

    response = requests.post(overpass_url, data=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Sorgu başarısız. Durum kodu: {response.status_code}")
        print(response.text)  # Yanıt içeriğini yazdırın
        return None

def extract_roof_points(building_data):
    roof_points = []

    for element in building_data.get("elements", []):
        if element["type"] == "way" and "nodes" in element and "tags" in element:
            if element["tags"].get("building") == "yes":
                # Bina çatısını oluşturan noktaları ekleyin
                roof_points.extend(element["nodes"])

    return roof_points

# Örnek olarak, İstanbul Üsküdar bölgesi için bbox koordinatları
bbox_coordinates = "29.0182,40.9711,29.0653,41.0249"

# Overpass API'yi kullanarak bina verilerini al
result = overpass_query(bbox_coordinates)

if result:
    # Bina çatı noktalarını çıkart
    roof_points = extract_roof_points(result)

    # Çatı noktalarını ekrana yazdır
    print("Bina Çatı Noktaları:")
    print(roof_points)
else:
    print("Veri alınamadı.")
