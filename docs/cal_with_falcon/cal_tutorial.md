# CAL Tutorial.

## Ví dụ tổng quan.

Một cái nhìn tổng quát về cấu trúc 1 app xây dựng trên `falcon` framework.

![big picture](http://falcon.readthedocs.io/en/stable/_images/my-web-app.gif)

Đầu tiên khai báo 1 lớp Controller, để tiện cho việc sử dụng Controller bên Resource, tên phương thức là `x` trong đó x là 1 phương thức HTTP chuẩn (vd: `get`, `post`, `put`,...)

```python

    class BasicController(object):

        def get(self, *args):
            # Thu thập và xử lý dữ liệu
            pass

        def delete(self, *args):
            pass

        def post(self, *args):
            pass

```

Về căn bản, Controller sẽ làm nhiệm vụ xử lý dữ liệu ứng với từng tác vụ. Tuy nhiên, khác với thiết kế CAL trước đó, việc xử lý REST sẽ ở lớp Resource.

Resource thực chất chỉ là 1 class bình thường có những phương thức được đặt tên theo quy ước nhất định: `on_x` trong đó `x` là 1 phương thức HTTP chuẩn, viết thường (vd: `get`, `post`, ...), sẽ tương ứng với phương thức `x` bên phía Controller.

```python

    class BasicResource(object):

        def __init__(self, controller, *args, **kwargs):
            # Khai báo định nghĩa Controller
            # sẽ xử lý dữ liệu cho Resource,
            self.controller

        def on_get(self, req, resp, *args, **kwargs):
            pass

        def on_post(self, req, resp, *args, **kwargs):
            pass

        def on_put(self, req, resp, *args, **kwargs):
            pass

        def on_delete(self, req, resp, *args, **kwargs):
            pass

```

Ví dụ có thể xem tại [file test_wsgi](https://github.com/cloudcomputinghust/CAL/blob/master/cal/tests/unit/test_wsgi.py)

Sau khi xử lý xong phần dữ liệu, để xác định route, cần điền thông tin đường dẫn và Resource xử lý đường dẫn đấy tại v1/<resource>/__init__.py, ví dụ:

```python

    from cal.v1.compute import compute

    def public_endpoint(wsgidriver, conf):
        return [
          ('/path',
           compute.Resource())
        ]

```