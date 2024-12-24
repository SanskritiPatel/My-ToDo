from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.csv"

# Initialize tasks file
def init_tasks_file():
    try:
        pd.read_csv(TASKS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Task", "Status"])
        df.to_csv(TASKS_FILE, index=False)

# Read tasks
def read_tasks():
    return pd.read_csv(TASKS_FILE)

# Write tasks
def write_tasks(df):
    df.to_csv(TASKS_FILE, index=False)

@app.route("/")
def index():
    tasks = read_tasks()
    return render_template("index.html", tasks=tasks.to_dict(orient="records"))

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    if task:
        tasks = read_tasks()
        new_id = len(tasks) + 1
        new_task = pd.DataFrame([[new_id, task, "Pending"]], columns=["ID", "Task", "Status"])
        tasks = pd.concat([tasks, new_task], ignore_index=True)
        write_tasks(tasks)
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks = read_tasks()
    tasks.loc[tasks["ID"] == task_id, "Status"] = "Completed"
    write_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = read_tasks()
    tasks = tasks[tasks["ID"] != task_id]
    write_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    init_tasks_file()
    app.run(debug=True)




