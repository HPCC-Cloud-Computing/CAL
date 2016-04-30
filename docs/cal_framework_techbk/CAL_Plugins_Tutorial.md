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
           
        
        def detail(self, req):
            data = {
                'action': 'detail',
                'controller': 'basic',
            }
            return data
        
        def mem_action(self, req, id):
            data = {
                'action': 'mem_action',
                'controller': 'basic',
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
        collection = {'detail': 'GET'}
        member = {'mem_action': 'GET'}
```

Cả hai đoạn code trên ta để trong cùng một file là basics.py


##  Explain:

1. Khi resource Basics được sử dụng nó tương đương với các url sau:
    
    Action mặc định:
    - GET /basics       => basics.index()
    - POST /basics      => basics.create()
    - PUT /basic/1      => basics.update(id)
    - DELETE /basic/1   => basics.delete(id)
    - GET /basic/1      => basics.show(id)
    ...
    Addition actions:
    - GET /basic/detail => basics.detail()
    - GET /basic/1/mem_action => basic.mem_action(id)

2. Giải thích class Controller:

    Các hàm được khai báo trong class Controller tương ứng với một action.
    Các action này có thể là action của Collection(Resource) hoặc action của member of collection.
    Ví dụ: 
    
        - Các function của action collection là: `index`, `create`.
        - Các action của member là các hàm còn lại.
    Các hàm này có một tham sô mặc định là req tức là đối tượng Request.
    Các hàm này khi code chỉ cần return 1 biến kiểu dict or list.

3. Giải thích các thuộc tính trong class Basics:

    - collection_name: là tên của resource
    - member_name: là tên của member resource, ví dụ resource basics thì có member_name là basic.
    - controller: là đối tượng controller.
    - parent_resource: chỉ rõ resource cha.
    - collection: là danh sách additional action cho resource.
    - member: là danh sách additional action cho member resource.

4. Giải thích `collecion` và `member`:

    Thực ra mình đã giải thích 2 parameter này ở 3. Tuy nhiên ở đây mình muốn nhấn mạnh làm sao sử
    dụng hai parameter này.
    Như ví dụ ở trên ta đã thấy, ngoài những action mặc định ta có thể khai báo thêm các Additions Action
    cho chính resource (hàm `detail`) hoặc member của resource (hàm `mem_action`).
    `collection` và `member` là một dict chứ danh sách các `action` và `method` của action đấy.
    Ví dụ: 
    
        collection = {'detail': 'GET'}
        member = {'mem_action': 'GET'}

##  FAQ?

1. Vậy file basics.py thì để ở đâu trong project?

    Tùy theo version, nếu đang ta thêm Resource cho version 1 thì để file basics.py
    sẽ để vào thư mục: CAL/cal/v1/resource_extensions.

2. stevedore ManagerResouce hoạt động như thế nào?

    Nó sẽ load class Basics, add thông tin của resource vào routes.Mapper.
    Detail: Update at next time... 

3. Làm sao để tôi có thể viết test cho resource?

    Comming soon...

4. Làm sao để tôi giải đáp những thắc mắc khi đọc tài liệu này?

    Liên hệ với techbk bạn nhé :(
