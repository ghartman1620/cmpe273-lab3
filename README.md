Gabriel Hartman CMPE273 Lab 3

# GraphQL Queries that were implemented:

## Create a new student

    mutation {
        create_student(name: "Gabe") {
            name
            id
            classes {
                id
                name
            }
        }
    }

## Get all students

    {
        student {
            id
            name
            classes {
                id
                name
            }
        }
    }

## Get a specific student and their classes

    {
        students (id:1) {
            id
            name
            classes {
                id
                name
            }
        }
    }

## Get all classes and their students

    {
        classes {
            id
            name
            students {
                id
                name
            }
        }
    }

## Get a specific class and its students

    {
        classes(id:1) {
            id
            name
            students {
                id
                name
            }
        }
    }

# Mutations

## Create a new student

    mutation {
        create_student(name:"Gabe") {
            id
            name
        }
    }

## Create a new class

    mutation {
        create_class(name:"CMPE273") {
            name
            id
        }
    }

## Add a student to a class

    mutation {
        add_student_to_class(student_id:2, class_id:1) {
            id
            name
            students {
                name
                id
            }
        }
    }
