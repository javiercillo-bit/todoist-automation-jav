import requests
import os
import json

API_TOKEN = os.getenv("TODOIST_API_TOKEN")

URL = "https://api.todoist.com/api/v1/sync"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def get_tasks():
    data = {
        "sync_token": "*",
        "resource_types": json.dumps(["items"])  # "items" = tareas
    }

    response = requests.post(URL, headers=HEADERS, data=data)

    print("Status code:", response.status_code)
    print("Raw response:", response.text[:500])  # evita dump gigante

    response.raise_for_status()

    result = response.json()
    return result.get("items", [])


if __name__ == "__main__":
    print("=== START ===")

    mode = os.getenv("MODE", "prod")
    print("MODE:", mode)

    tasks = get_tasks()

    print(f"Tareas obtenidas: {len(tasks)}")

    # debug: imprime primeras 3
    for t in tasks[:3]:
        print("-", t.get("content"))

    print("=== END ===")
