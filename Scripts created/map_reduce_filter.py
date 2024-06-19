import requests
from functools import reduce

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

    # Utilisation de filter() et map() pour trouver les IDs des labels
    revenue_label = list(filter(lambda x: x["name"].lower() == "revenue", labels))
    ignore_label = list(filter(lambda x: x["name"].lower() == "ignore", labels))

    revenue_label_id = revenue_label[0]["id"] if revenue_label else None
    ignore_label_id = ignore_label[0]["id"] if ignore_label else None

    return revenue_label_id, ignore_label_id, "revenue" if revenue_label else None, "ignore" if ignore_label else None

# Obtenir les IDs des labels et leurs noms
revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name = get_label_ids()

# URL de l'API pour lister les mouvements
movement_url = f"{base_url}/movement?transaction_hashes=0xfdf027f88de3290e8493086abdf24b2b1316c3159be2b5ef06109784c81cbbc7"

# Faire la requête API pour "List all movements"
response = requests.get(movement_url, headers=headers)
data = response.json()["data"]

# Utilisation de reduce() pour créer des dictionnaires pour les volumes totaux par asset
def accumulate_volumes(acc, movement):
    asset_id = movement["asset"]
    volume = float(movement["volume"])
    
    if movement["direction"] == "in":
        acc[0][asset_id] = acc[0].get(asset_id, 0) + volume
    elif movement["direction"] == "out":
        acc[1][asset_id] = acc[1].get(asset_id, 0) + volume
    
    return acc

volumes_in_by_asset, volumes_out_by_asset = reduce(accumulate_volumes, data, ({}, {}))

# Utilisation de map() pour comparer les volumes "in" et "out" pour chaque asset et créer les labels à appliquer
def determine_label(movement):
    asset_id = movement["asset"]
    total_in = volumes_in_by_asset.get(asset_id, 0)
    total_out = volumes_out_by_asset.get(asset_id, 0)
    
    # Si la balance des volumes "in" et "out" est zéro, appliquer le label "ignore"
    label_id = ignore_label_id if total_in == total_out else revenue_label_id
    label_name = ignore_label_name if total_in == total_out else revenue_label_name
    return (label_id, movement["id"], label_name)

labels_to_apply = list(map(determine_label, data))

# Regrouper les labels par ID
def group_labels(acc, item):
    label_id, movement_id, label_name = item
    if label_id not in acc:
        acc[label_id] = (label_name, [])
    acc[label_id][1].append(movement_id)
    return acc

grouped_labels_to_apply = reduce(group_labels, labels_to_apply, {})

# Appliquer les labels en fonction des volumes calculés
for label_id, (label_name, movements) in grouped_labels_to_apply.items():
    # URL pour appliquer le label
    label_url = f"{base_url}/label/{label_id}/apply"
    
    # Payload pour la requête
    payload = {
        "movements": movements
    }
    
    # Faire la requête API pour appliquer le label
    label_response = requests.post(label_url, json=payload, headers=headers)
    
    # Afficher la réponse avec le nom du label appliqué
    print(f"The label >>> {label_name.upper()} <<< has been applied to the movement(s): {movements}")

print("Label application completed.")