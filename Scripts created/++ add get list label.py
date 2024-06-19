import requests

# URL de base de l'API Cryptio
base_url = "https://app-api.cryptio.co/api"

# En-têtes de la requête
headers = {
    "content-type": "application/json",
    "cryptio-api-key": "2e737658-575d-4b42-8625-616c5f115cb5"
}

# Fonction pour obtenir les IDs des labels "Revenue" et "Ignore"
def get_label_ids():
    label_url = f"{base_url}/label"
    response = requests.get(label_url, headers=headers)
    labels = response.json()["data"]

    revenue_label_id = None
    ignore_label_id = None

    for label in labels:
        if label["name"].lower() == "revenue":
            revenue_label_id = label["id"]
        elif label["name"].lower() == "ignore":
            ignore_label_id = label["id"]

    return revenue_label_id, ignore_label_id

# Obtenir les IDs des labels
revenue_label_id, ignore_label_id = get_label_ids()

# URL de l'API pour lister les mouvements
movement_url = f"{base_url}/movement?transaction_hashes=0xfdf027f88de3290e8493086abdf24b2b1316c3159be2b5ef06109784c81cbbc7"

# Faire la requête API pour "List all movements"
response = requests.get(movement_url, headers=headers)
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
        label_id = ignore_label_id
    else:
        label_id = revenue_label_id
    
    if label_id not in labels_to_apply:
        labels_to_apply[label_id] = []
    labels_to_apply[label_id].append(movement["id"])

# Appliquer les labels en fonction des volumes calculés
for label_id, movements in labels_to_apply.items():
    # URL pour appliquer le label
    label_url = f"{base_url}/label/{label_id}/apply"
    
    # Payload pour la requête
    payload = {
        "movements": movements
    }
    
    # Faire la requête API pour appliquer le label
    label_response = requests.post(label_url, json=payload, headers=headers)
    
    # Afficher la réponse
    print(f"Label ID: {label_id}, Movements: {movements}, Response: {label_response.text}")

print("Label application completed.")
