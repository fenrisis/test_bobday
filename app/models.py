from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    age: int


class Department(BaseModel):
    department_name: str
    employees: list[Employee]
