import requests
import time
import os

TOKEN = os.getenv("TODOIST_API_TOKEN")
MODE = os.getenv("MODE")

BASE_URL = "https://api.todoist.com/api/v1"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_tasks():
    r = requests.get(f"{BASE_URL}/tasks/get", headers=HEADERS)
    r.raise_for_status()
    return r.json()["items"]

def update_task(task_id, labels):
    r = requests.post(
        f"{BASE_URL}/tasks/update",
        headers=HEADERS,
        json={
            "id": task_id,
            "labels": labels
        }
    )
    r.raise_for_status()

def move_label(tasks, from_label, to_label):
    count = 0
    for t in tasks:
        labels = t.get("labels", [])

        if from_label in labels:
            new_labels = [l for l in labels if l != from_label]

            if to_label not in new_labels:
                new_labels.append(to_label)

            update_task(t["id"], new_labels)
            print(f"{from_label} → {to_label} | {t['id']}")
            count += 1

    print(f"Total movidas {from_label} → {to_label}: {count}")

def run_daily(tasks):
    move_label(tasks, "@Ayer", "@Atrasado")
    time.sleep(15)
    move_label(tasks, "@Hoy", "@Ayer")
    time.sleep(15)
    move_label(tasks, "@Mañana", "@Hoy")

def run_weekly(tasks):
    move_label(tasks, "@Semana pasada", "@Atrasado")
    time.sleep(15)
    move_label(tasks, "@Esta semana", "@Semana pasada")
    time.sleep(15)
    move_label(tasks, "@Próxima semana", "@Esta semana")

def run_monthly(tasks):
    move_label(tasks, "@Mes pasado", "@Atrasado")
    time.sleep(15)
    move_label(tasks, "@Este mes", "@Mes pasado")
    time.sleep(15)
    move_label(tasks, "@Próximo mes", "@Este mes")

def run_test(tasks):
    move_label(tasks, "@Ayer", "@Hoy")

if __name__ == "__main__":
    print("=== START ===")
    print("MODE:", MODE)

    if not TOKEN:
        raise Exception("Falta TODOIST_API_TOKEN")

    try:
        tasks = get_tasks()
        print(f"Tasks encontradas: {len(tasks)}")
    except Exception as e:
        print("Error obteniendo tareas:", str(e))
        raise

    try:
        if MODE == "daily":
            run_daily(tasks)
        elif MODE == "weekly":
            run_weekly(tasks)
        elif MODE == "monthly":
            run_monthly(tasks)
        elif MODE == "test":
            run_test(tasks)
        else:
            raise Exception(f"MODE desconocido: {MODE}")
    except Exception as e:
        print("Error ejecutando lógica:", str(e))
        raise

    print("=== END ===")
