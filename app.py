import requests
import time
import os

TOKEN = os.getenv("TODOIST_API_TOKEN")
BASE_URL = "https://api.todoist.com/rest/v2"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_tasks():
    r = requests.get(f"{BASE_URL}/tasks", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def update_task(task_id, labels):
    r = requests.post(
        f"{BASE_URL}/tasks/{task_id}",
        headers=HEADERS,
        json={"labels": labels}
    )
    r.raise_for_status()

def move_label(tasks, from_label, to_label):
    for t in tasks:
        if from_label in t["labels"]:
            current = t["labels"]
            new = [l for l in current if l != from_label]
            if to_label not in new:
                new.append(to_label)
            update_task(t["id"], new)

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

if __name__ == "__main__":
    mode = os.getenv("MODE")  # daily / weekly / monthly
    tasks = get_tasks()

    if mode == "daily":
        run_daily(tasks)
    elif mode == "weekly":
        run_weekly(tasks)
    elif mode == "monthly":
        run_monthly(tasks)
