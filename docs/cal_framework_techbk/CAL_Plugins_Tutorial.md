# CAL Plugins
## Background


## Basic Plugin structure

Dưới đây là một ví dụ đơn giản về cách tạo một resource.

Đầu tiên ta khai báo một Controller Object.
```python

    class BasicController(object):
    
        # Define support for GET on a collection
        def index(self, req):
            data = {
                'action': "index",
                'controller': "basic"
            }
            return data
    
        def delete(self, req, id):
            data = {
                'action': "delete",
                'controller': "basic",
                'id': id
            }
            return data
    
        def update(self, req, id):
            data = {
                'action': "update",
                'controller': "basic",
                'id': id
            }
            return data
    
        def create(self, req):
            data = {
                'action': "create",
                'controller': "basic"
            }
            return data
    
        def show(self, req, id):
            data = {
                'action': "show",
                'controller': "basic",
                'id': id
            }
            return data
```

Sau đó ta khai báo một đối tượng Resource Extension như sau:

```python

    class Basics:
        collection_name = 'basics'
        member_name = 'basic'
        controller = BasicController()
        parent_resource = {}
        collection = {}
        member = {}
```

Cả hai đoạn code trên ta để trong cùng một file là basics.py


##  Explain:

1. Khi resource Basics được sử dụng nó tương đương với các url sau:
o GET /basics       => basics.index()
o POST /basics      => basics.create()
o PUT /basic/1      => basics.update(id)
o DELETE /basic/1   => basics.delete(id)
o GET /basic/1      => basics.show(id)

2. Giải thích class Controller:
Các hàm được khai báo trong class Controller tương ứng với một action.
Các hàm này khi code chỉ cần return 1 biến kiểu dict.

3. Giải thích các thuộc tính trong class Basics:
collection_name: là tên của resource
member_name: là tên của member resource, ví dụ resource basics thì có member_name là basic.
controller: là đối tượng controller.
parent_resource: chỉ rõ resource cha.
collection: là danh sách additional action cho resource.
member: là danh sách additional action cho member resource.

##  FAQ?

1. Vậy file basics.py thì để ở đâu trong project?
Tùy theo version, nếu đang ta thêm Resource cho version 1 thì để file basics.py
sẽ để vào thư mục: CAL/cal/v1/resource_extensions.

2. stevedore ManagerResouce hoạt động như thế nào?
Nó sẽ load class Basics, add thông tin của resource vào routes.Mapper.
Detail: Update at next time... :v :v :v

3. Làm sao để tôi có thể viết test cho resource?
Comming soon... :v :v

4. Làm sao để tôi giải đáp những thắc mắc khi đọc tài liệu này?
Liên hệ với techbk bạn nhé :(