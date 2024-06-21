import requests

# URL de l'API Cryptio pour lister les mouvements
url = "https://app-api.cryptio.co/api/movement?transaction_hashes=0xfdf027f88de3290e8493086abdf24b2b1316c3159be2b5ef06109784c81cbbc7"

# En-têtes de la requête
headers = {
    "content-type": "application/json",
    "cryptio-api-key": "2e737658-575d-4b42-8625-616c5f115cb5"
}

# Faire la requête API pour "List all movements"
response = requests.get(url, headers=headers)
data = response.json()["data"]

# Créer des dictionnaires pour suivre les volumes totaux par asset
volumes_in_by_asset = {}
volumes_out_by_asset = {}

# Parcourir les données et calculer les volumes totaux par asset et par direction
for movement in data:
    asset_id = movement["asset"]
    volume = float(movement["volume"])
    
    if movement["direction"] == "in":
        if asset_id not in volumes_in_by_asset:
            volumes_in_by_asset[asset_id] = 0
        volumes_in_by_asset[asset_id] += volume
    elif movement["direction"] == "out":
        if asset_id not in volumes_out_by_asset:
            volumes_out_by_asset[asset_id] = 0
        volumes_out_by_asset[asset_id] += volume

# Comparer les volumes "in" et "out" pour chaque asset
labels_to_apply = {}

for movement in data:
    asset_id = movement["asset"]
    
    total_in = volumes_in_by_asset.get(asset_id, 0)
    total_out = volumes_out_by_asset.get(asset_id, 0)
    
    # Si la balance des volumes "in" et "out" est zéro, appliquer le label "ignore"
    if total_in == total_out:
        label_id = "845eb3d0-2f73-4848-93fe-2f90efbc4d43"  # Label "ignore"
    else:
        label_id = "1e7c5038-52f6-452b-9d40-cac8e572920a"  # Label "revenue"
    
    if label_id not in labels_to_apply:
        labels_to_apply[label_id] = []
    labels_to_apply[label_id].append(movement["id"])

# Appliquer les labels en fonction des volumes calculés
for label_id, movements in labels_to_apply.items():
    # URL pour appliquer le label
    label_url = f"https://app-api.cryptio.co/api/label/{label_id}/apply"
    
    # Payload pour la requête
    payload = {
        "movements": movements
    }
    
    # Faire la requête API pour appliquer le label
    label_response = requests.post(label_url, json=payload, headers=headers)
    
    # Afficher la réponse
    print(f"Label ID: {label_id}, Movements: {movements}, Response: {label_response.text}")

print("Label application completed.")
