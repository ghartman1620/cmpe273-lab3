from ariadne import QueryType, MutationType, graphql_sync, make_executable_schema, gql
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
import sys

students = {}
next_student_id = 1
classes = {}
next_class_id = 1

type_defs = gql("""
    type Query {
        students (id: Int): [Student]
        classes (id: Int): [Class]
    }
    type Mutation {
        create_student (name: String!): Student
        create_class (name: String!): Class
        add_student_to_class(student_id: Int!, class_id: Int!): Class
    }
    type Student {
        id: Int!
        name: String!
        classes: [Class]
    }
    type Class {
        name: String!
        id: Int!
        students: [Student]
    }
""")

query = QueryType()


@query.field("students")
def resolve_students(_, info, id=None):
    if id:
        print(students[id])
        return [students[id]]
    return students.values()


@query.field("classes")
def resolve_classes(_, info, id=None):
    if id:
        print(classes[id])
        return [classes[id]]
    return classes.values()


mutation = MutationType()


@mutation.field("create_student")
def resolve_create_student(_, info, name):
    global students
    global next_student_id
    student = {
        "name": name,
        "id": next_student_id,
        "classes": []
    }
    students[next_student_id] = student
    next_student_id += 1
    return student


@mutation.field("create_class")
def resolve_create_class(_, info, name):
    global classes
    global next_class_id
    new_class = {
        "name": name,
        "id": next_class_id,
        "students": []
    }
    classes[next_class_id] = new_class
    next_class_id += 1
    return new_class


@mutation.field("add_student_to_class")
def resolve_add_student_to_class(_, info, student_id, class_id):
    global classes
    global students
    class_to_add = classes[class_id]
    student_to_add = students[student_id]
    class_to_add["students"].append(student_to_add)
    student_to_add["classes"].append(class_to_add)
    return class_to_add


schema = make_executable_schema(type_defs, query, mutation)

app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
