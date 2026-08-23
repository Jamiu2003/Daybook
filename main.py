from fastapi import FastAPI
from database import engine, Base, get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from schemas import TodoCreate, GetTodo, TodoUpdate, UserRegisteration, UserLogin, UserResponse, EntryCreate, EntryResponse, GoalCreate, GoalResponse, MilestoneCreate, MilestoneResponse, MilestoneUpdate
from sqlalchemy.orm import Session
from model import Todo, User, Entry, Goal, Milestone
from sqlalchemy import select
from dependencies import get_current_user
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import model
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse




app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
router = APIRouter()
Base.metadata.create_all(bind=engine)
app.include_router(router)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/entries", response_model = EntryResponse)
def create_entry(entry:EntryCreate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    new_entry = Entry(
        content = entry.content,
        mood = entry.mood,
        user_id = current_user.id
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/entries", response_model = list[EntryResponse])
def list_entries(db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Entry).where(Entry.user_id == current_user.id).order_by(Entry.time_created.desc()))

    return result.scalars().all()


@router.get("/", response_model= list[GetTodo])
def todo_list(db:Session = Depends(get_db), current_user:User =Depends(get_current_user)):
    result = db.execute(select(Todo).where(Todo.user_id == current_user.id))
    todo = result.scalars().all()
    return todo


@router.post("/registeration", response_model = UserResponse)
def register(user: UserRegisteration, db:Session = Depends(get_db)):
    result = db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code= 409, detail="User Already Exist")
    result = db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code = 409, detail = "Email Already Exist")

    hashed_password = hash_password(user.password)

    db_user = User(
        username = user.username,
        email = user.email,
        full_name = user.full_name,
        password_hash = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    result = db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code = 401, detail = "Invalid username or email")
    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
        "token_type" : "bearer",
        "full_name" : user.full_name
    }



@router.post("/goals", response_model = GoalResponse)
def goals(goal:GoalCreate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    new_goals = Goal(
        title = goal.title,
        target_date = goal.target_date,
        
        user_id = current_user.id,
    )
    db.add(new_goals)
    db.commit()
    db.refresh(new_goals)

    return new_goals

@router.get("/goals", response_model= list[GoalResponse])
def list_goals(db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Goal).where(Goal.user_id == current_user.id).order_by(Goal.time_created.desc()))
    return result.scalars().all()

@router.delete("/goals/{goal_id}")
def delete_goal(goal_id:int, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id))
    goal = result.scalar_one_or_none()
    if goal is None:
        raise HTTPException(status_code=404, detail = "{goal_id} Not found")
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}

@router.post("/goals/{goal_id}/milestones", response_model = MilestoneResponse)
def create_milestone(goal_id:int, milestone:MilestoneCreate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id))
    goal = result.scalar_one_or_none()
    if goal is None:
        raise HTTPException(status_code=404, detail = "{goal_id} Not found")
    
    new_milestone = Milestone(
        title = milestone.title,
        goal_id = goal_id
    )
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)

    return new_milestone

@router.put("/milestones/{milestone_id}", response_model = MilestoneUpdate)
def update_milestone(milestone_id:int, data: MilestoneUpdate, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(select(Milestone).join(Goal).where(Milestone.id == milestone_id, Goal.user_id == current_user.id))
    milestone = result.scalar_one_or_none()
    if milestone is None:
        raise HTTPException(status_code=404, detail="{milestone_id} Not found")
    milestone.completed = data.completed
    db.commit()
    db.refresh(milestone)

    return milestone

@router.delete("/milestones/{milestone_id}")
def update_milestone(milestone_id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(select(Milestone).join(Goal).where(Milestone.id == milestone_id, Goal.user_id == current_user.id))
    milestone = result.scalar_one_or_none()
    if milestone is None:
        raise HTTPException(status_code=404, detail="{milestone_id} Not found")
   
    db.delete(milestone)
    db.commit()
    return {"message": "Milestone deleted successfully"}



@router.post("/", response_model=GetTodo)
def create_todo(todo:TodoCreate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    new_todo = Todo(
        title = todo.title,
        description = todo.description,
        user_id = current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@router.get("/{todo_id}",response_model = GetTodo)
def get_todo(todo_id = int,db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    
    #todos = db.query(Todo).filter(Todo.id == todo_id)
    result = db.execute(select(Todo).where(Todo.id == todo_id))
    todos = result.scalar_one_or_none()
    if todos is None:
        raise HTTPException(status_code=404, detail= f"{todo_id} not found")
    return todos

@router.put("/{todo_id}", response_model = TodoUpdate)
def update(todo_id: int, todo_data: TodoUpdate, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id))
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail = "{todo_id} not found")
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    db.commit()
    db.refresh(todo)

    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    result = db.execute(select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id))
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail = "{todo_id} not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
