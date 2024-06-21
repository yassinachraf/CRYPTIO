# process_movements.py
import requests
from functools import reduce

def accumulate_volumes(acc, movement):
    asset_id = movement["asset"]
    volume = float(movement["volume"])
    
    if movement["direction"] == "in":
        acc[0][asset_id] = acc[0].get(asset_id, 0) + volume
    elif movement["direction"] == "out":
        acc[1][asset_id] = acc[1].get(asset_id, 0) + volume
    
    return acc

def determine_label(movement, volumes_in_by_asset, volumes_out_by_asset, revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name):
    asset_id = movement["asset"]
    total_in = volumes_in_by_asset.get(asset_id, 0)
    total_out = volumes_out_by_asset.get(asset_id, 0)
    
    label_id = ignore_label_id if total_in == total_out else revenue_label_id
    label_name = ignore_label_name if total_in == total_out else revenue_label_name
    return (label_id, movement["id"], label_name)

def group_labels(acc, item):
    label_id, movement_id, label_name = item
    if label_id not in acc:
        acc[label_id] = (label_name, [])
    acc[label_id][1].append(movement_id)
    return acc

def process_movements(base_url, headers, transaction_hash, revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name):
    movement_url = f"{base_url}/movement?transaction_hashes={transaction_hash}"
    response = requests.get(movement_url, headers=headers)
    data = response.json()["data"]

    volumes_in_by_asset, volumes_out_by_asset = reduce(accumulate_volumes, data, ({}, {}))

    labels_to_apply = list(map(lambda movement: determine_label(movement, volumes_in_by_asset, volumes_out_by_asset, revenue_label_id, ignore_label_id, revenue_label_name, ignore_label_name), data))

    grouped_labels_to_apply = reduce(group_labels, labels_to_apply, {})

    for label_id, (label_name, movements) in grouped_labels_to_apply.items():
        label_url = f"{base_url}/label/{label_id}/apply"
        payload = {"movements": movements}
        label_response = requests.post(label_url, json=payload, headers=headers)
        print(f"The label '{label_name.upper()}' has been applied to the following movement(s): {movements}")

    print("Label application completed.")
