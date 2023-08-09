# Retail API

Test project for a generic API in a retail application setting.

---

## API paths

| Path                             | Method | Requires Token | Description |
| -------------------------------- | ------ | -------------- | ----------- |
| /api/users/                      | POST   | False | create new user(register) |
| /api/token/login/                | POST   | False | get token for registered user |
| /api/groups/*\<groupName\>*/users/ | GET, POST | True | view group, add user to group |
| /api/groups/*\<groupName\>*/users/*\<int:pk\>*/ | DELETE | True | remove user from group |
| /api/categories/                 | GET    | False | list item categories |
| /api/items/                      | GET    | False | list items |
| /api/items/                      | POST   | True  | create new items |
| /api/items/*\<title\>*/            | GET    | False | retrieve single item |
| /api/items/*\<title\>*/            | PUT, DELETE | True | alter/delete item |
| /api/orders/      | GET, POST    | True  | list/create orders |
| /api/orders/*\<int:pk\>*/        | GET, PUT, DELETE   | True  | alter/delete order |
| /api/cart/items/               | GET, POST, DELETE | True | view, add-to, delete cart |


### Ordering and Pagination:

To implement ordering pass '?ordering=..' with the uri
e.g. http://127.0.0.1:8000/api/items?ordering=price

To implement pagination pass '?page=1' with the uri
e.g. http://127.0.0.1:8000/api/items?page=1&page_size=3


*django admin superuser* : admindjango -p adminuser1
