from streamlit.testing.v1 import AppTest
import pytest

def test_add_task():
    at = AppTest.from_file("app.py", default_timeout=10).run()
    at.text_input(key="add_a_new_task").input("Test Task").run()
    at.button(key="add_task").click().run()
    assert len(at.expander) == 1
    assert "Test Task" in at.expander[0].label

def test_delete_task():
    at = AppTest.from_file("app.py", default_timeout=10).run()
    at.text_input(key="add_a_new_task").input("Test Task").run()
    at.button(key="add_task").click().run()
    assert len(at.expander) == 1
    at.expander[0].button(key="delete_0").click().run()
    assert len(at.expander) == 0

def test_complete_task():
    at = AppTest.from_file("app.py", default_timeout=10).run()
    at.text_input(key="add_a_new_task").input("Test Task").run()
    at.button(key="add_task").click().run()
    at.checkbox(key="task_0").check().run()
    assert at.session_state["score"] == 10
