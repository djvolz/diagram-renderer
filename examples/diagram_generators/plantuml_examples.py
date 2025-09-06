"""
PlantUML diagram example definitions.
"""


def get_plantuml_examples():
    """Get all PlantUML diagram examples"""
    return {
        "plantuml_sequence_diagram.html": {
            "name": "PlantUML Sequence Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title User Authentication Flow

actor User
participant "Web App" as App
participant "Auth Service" as Auth
database "User DB" as DB

User -> App: Login Request
App -> Auth: Validate Credentials
Auth -> DB: Query User Data
DB --> Auth: User Found
Auth --> App: JWT Token
App --> User: Login Success

User -> App: Access Protected Resource
App -> Auth: Validate Token
Auth --> App: Token Valid
App -> DB: Fetch User Data
DB --> App: User Data
App --> User: Display Resource
@enduml""",
        },
        "plantuml_class_diagram.html": {
            "name": "PlantUML Class Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title E-commerce System Classes

class User {
    -id: int
    -email: string
    -password: string
    +login()
    +logout()
    +updateProfile()
}

class Order {
    -orderId: int
    -orderDate: date
    -total: decimal
    +calculateTotal()
    +addItem()
    +removeItem()
}

class Product {
    -productId: int
    -name: string
    -price: decimal
    -stock: int
    +updateStock()
    +getPrice()
}

class OrderItem {
    -quantity: int
    -unitPrice: decimal
    +getSubtotal()
}

User ||--o{ Order : places
Order ||--o{ OrderItem : contains
Product ||--o{ OrderItem : "included in"
@enduml""",
        },
        "plantuml_use_case_diagram.html": {
            "name": "PlantUML Use Case Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title E-commerce System Use Cases

left to right direction

actor Customer
actor Administrator
actor "Payment Gateway" as PG

rectangle "E-commerce System" {
    usecase "Browse Products" as UC1
    usecase "Add to Cart" as UC2
    usecase "Checkout" as UC3
    usecase "Process Payment" as UC4
    usecase "Manage Inventory" as UC5
    usecase "View Orders" as UC6
    usecase "Generate Reports" as UC7
}

Customer --> UC1
Customer --> UC2
Customer --> UC3
UC4 --> PG
Administrator --> UC5
Administrator --> UC6
Administrator --> UC7
UC3 ..> UC4 : includes
@enduml""",
        },
        "plantuml_component_diagram.html": {
            "name": "PlantUML Component Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title System Architecture Components

package "Frontend" {
    [Web Application] as webapp
    [Mobile App] as mobile
}

package "API Gateway" {
    [Load Balancer] as lb
    [API Router] as router
}

package "Microservices" {
    [User Service] as user
    [Order Service] as order
    [Product Service] as product
    [Payment Service] as payment
}

package "Data Layer" {
    database "User DB" as userdb
    database "Order DB" as orderdb
    database "Product DB" as productdb
    cloud "Payment Gateway" as paymentgateway
}

webapp --> lb
mobile --> lb
lb --> router
router --> user
router --> order
router --> product
router --> payment

user --> userdb
order --> orderdb
product --> productdb
payment --> paymentgateway
@enduml""",
        },
        "plantuml_state_diagram.html": {
            "name": "PlantUML State Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title Order State Machine

[*] --> Draft

Draft : Order being created
Draft --> Submitted : submit()

Submitted : Awaiting validation
Submitted --> Processing : validate()
Submitted --> Cancelled : cancel()

Processing : Payment processing
Processing --> Confirmed : payment_success()
Processing --> Failed : payment_failed()

Failed : Payment failed
Failed --> Submitted : retry()
Failed --> Cancelled : cancel()

Confirmed : Order confirmed
Confirmed --> Shipped : ship()
Confirmed --> Cancelled : cancel()

Shipped : Order in transit
Shipped --> Delivered : deliver()

Delivered : Order completed
Cancelled : Order cancelled

Delivered --> [*]
Cancelled --> [*]
@enduml""",
        },
        "plantuml_deployment_diagram.html": {
            "name": "PlantUML Deployment Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
title System Deployment Architecture

node "Load Balancer" {
    [nginx] as nginx
}

node "Web Servers" {
    [Web Server 1] as web1
    [Web Server 2] as web2
}

node "Application Servers" {
    [App Server 1] as app1
    [App Server 2] as app2
    [Background Jobs] as jobs
}

node "Database Cluster" {
    database "Primary DB" as primarydb
    database "Replica DB" as replicadb
    database "Cache" as cache
}

cloud "External Services" {
    [Payment API] as payment
    [Email Service] as email
    [Analytics] as analytics
}

nginx --> web1
nginx --> web2
web1 --> app1
web2 --> app2
app1 --> primarydb
app2 --> primarydb
primarydb --> replicadb
app1 --> cache
app2 --> cache
jobs --> payment
jobs --> email
jobs --> analytics
@enduml""",
        },
        "plantuml_object_diagram.html": {
            "name": "PlantUML Object Diagram",
            "type": "plantuml",
            "code": """@startuml
title Sample E-commerce Order

class User {
  id = 123
  email = "john@example.com"
}

class Order {
  orderId = 789
  total = 89.97
}

User ||--o{ Order : places
@enduml""",
        },
        "plantuml_network_diagram.html": {
            "name": "PlantUML Network Diagram",
            "type": "plantuml",
            "code": """@startuml
!theme plain
!include <aws/common>
!include <aws/Storage/AmazonS3/AmazonS3>
!include <aws/Compute/AmazonEC2/AmazonEC2>

title Cloud Infrastructure

package "VPC" {
    package "Public Subnet" {
        [Load Balancer] as lb
        [NAT Gateway] as nat
    }

    package "Private Subnet" {
        [Web Server 1] as web1
        [Web Server 2] as web2
        [Application Server] as app
    }

    package "Database Subnet" {
        database "Primary DB" as db1
        database "Replica DB" as db2
    }
}

cloud "Internet" as internet
cloud "CDN" as cdn

internet --> lb
lb --> web1
lb --> web2
web1 --> app
web2 --> app
app --> db1
db1 --> db2
nat --> internet
cdn --> internet
@enduml""",
        },
    }
