from fastapi import APIRouter
from ..config import get_config
from ..dependencies import fetch_data, post_data
from ..models import Department, Employee
from ..schemas import PostResponse
import json

router = APIRouter()


@router.get("/process-data/", response_model=PostResponse)
async def process_data():
    config = get_config()
    url_get = config['API']['URL_GET']
    url_post = config['API']['URL_POST']
    username = config['API']['USERNAME']
    password = config['API']['PASSWORD']

    raw_data = await fetch_data(url_get, username, password)
    transformed_data = transform_data(raw_data)
    data_dict = {k: v.dict() for k, v in transformed_data.items()}
    status_code = await post_data(url_post, data_dict, username, password)
    with open("output.json", "w") as f:
        json.dump(data_dict, f)
    return {"status_code": status_code, "data_saved": "output.json"}


def transform_data(raw_data):
    departments = {}
    for employee_data in raw_data["employees"]:
        dept_id = employee_data["department"]["id"]
        employee = Employee(**employee_data)
        if dept_id not in departments:
            departments[dept_id] = Department(department_name=employee_data["department"]["department_name"], employees=[])
        departments[dept_id].employees.append(employee)
    return {dept_id: dept for dept_id, dept in departments.items()}
