Gabriel Hartman CMPE273 Lab 3

GraphQL operations that were implemented:

Create a new student

    mutation {
        create_student(name: "Gabe") {
            name
            id
            classes
        }
    }

Query an existing student
