import streamlit as st
from streamlit_push_notifications import send_push
import datetime

def main():
    st.title("AI-Powered Event Manager")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
        st.session_state.score = 0
        st.session_state.gratitude_notes = ""
        st.session_state.notifications = []

    task_input = st.text_input("Add a new task:", key="add_a_new_task")
    task_deadline_date = st.date_input("Deadline date")
    task_deadline_time = st.time_input("Deadline time")

    if st.button("Add Task", key="add_task"):
        if task_input:
            deadline = datetime.datetime.combine(task_deadline_date, task_deadline_time)
            st.session_state.tasks.append({
                "task": task_input,
                "completed": False,
                "subtasks": [],
                "attachments": [],
                "links": [],
                "deadline": deadline
            })
            st.rerun()

    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])
    total_tasks = len(st.session_state.tasks)
    progress = completed_tasks / total_tasks if total_tasks > 0 else 0
    st.progress(progress)
    st.metric("Score", st.session_state.score)

    st.sidebar.header("Notifications")
    for notification in st.session_state.notifications:
        st.sidebar.info(notification)

    st.header("To-Do List")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            completed = st.checkbox("Status", value=task["completed"], key=f"task_{i}", label_visibility="collapsed")
            if completed != task["completed"]:
                st.session_state.tasks[i]["completed"] = completed
                if completed:
                    st.session_state.score += 10
                    st.balloons()
                else:
                    st.session_state.score -= 10
                st.rerun()
        with col2:
            with st.expander(f"{task['task']} (Deadline: {task['deadline'].strftime('%Y-%m-%d %H:%M')})"):
                new_task = st.text_input("Edit task", task["task"], key=f"edit_{i}")
                if new_task != task["task"]:
                    st.session_state.tasks[i]["task"] = new_task
                    st.rerun()

                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

                if st.button("Send Reminder", key=f"remind_{i}"):
                    send_push("Task Reminder", f"Don't forget to complete your task: {task['task']}",)
                    st.session_state.notifications.append(f"Reminder sent for task: {task['task']}")

                st.subheader("Sub-tasks")
                sub_task_input = st.text_input("Add a sub-task", key=f"sub_task_input_{i}")
                if st.button("Add Sub-task", key=f"add_sub_task_{i}"):
                    if sub_task_input:
                        st.session_state.tasks[i]["subtasks"].append(sub_task_input)
                        st.rerun()

                for j, sub_task in enumerate(task["subtasks"]):
                    st.checkbox(sub_task, key=f"sub_task_{i}_{j}")

                st.subheader("Attachments")
                uploaded_file = st.file_uploader("Upload a file", key=f"file_uploader_{i}", type=None, accept_multiple_files=True)
                if uploaded_file:
                    for file in uploaded_file:
                        st.session_state.tasks[i]["attachments"].append(file.name)

                for attachment in task["attachments"]:
                    st.write(attachment)

                st.subheader("Links")
                link_input = st.text_input("Add a link", key=f"link_input_{i}")
                if st.button("Add Link", key=f"add_link_{i}"):
                    if link_input:
                        st.session_state.tasks[i]["links"].append(link_input)
                        st.rerun()

                for link in task["links"]:
                    st.write(link)

    st.header("Self-Gratitude Journal")
    gratitude_notes = st.text_area("What are you grateful for today?", st.session_state.gratitude_notes)
    if gratitude_notes != st.session_state.gratitude_notes:
        st.session_state.gratitude_notes = gratitude_notes


if __name__ == "__main__":
    main()
