from playwright.sync_api import Page

def test_complete_user_flow(page:Page):
    page.goto("http://127.0.0.1:5500/todo_app/frontend/Register.html")

    page.fill("#fullName", "Musa Nene")
    page.fill("#username", "nene")
    page.fill("#email", "nene@gmail.com")
    page.fill("#password", "Nene@2003")
    page.fill("#confirm", "Nene@2003")
    page.click("#submitBtn")

    page.goto("http://127.0.0.1:5500/todo_app/frontend/Login.html")
    page.fill("#username", "nene")
    page.fill("#password", "Nene@2003")
    page.click("#submitBtn")

    page.wait_for_url("**/TodoApp.html")
    page.fill("#diaryContent", "I want to add to the diary. i am stil looking forward to it working")
    page.goto("http://127.0.0.1:5500/todo_app/frontend/Goals.html")
    
    page.wait_for_url("**/Goals.html")

    page.fill("#goalTitleInput", "Learn different things")
    page.click("#addGoalBtn")

    

    assert page.get_by_text("Learn different things").is_visible