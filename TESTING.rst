..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


      Convention for heading levels:
      =======  Heading 0 (reserved for the title in a document)
      -------  Heading 1
      ~~~~~~~  Heading 2
      +++++++  Heading 3
      '''''''  Heading 4
      (Avoid deeper levels because they do not render well.)


Testing CAL
===========

Testing framework
-----------------

Hiện nay, mới chỉ triển khai Unit tests.

Unit Tests
~~~~~~~~~~

Quá trình phát triển
--------------------

Cấu trúc cây thư mục Unit Test 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cấu trúc cây thư mục Unit Test nên tương ứng với cấu trúc cây thư mục code cần test, và có thêm tiền tố 'test_' ví dụ ::
    - target module: cal.wsgi
    - test.module: cal.tests.unit.test_wsgi

Chạy Unit Test
--------------

Dùng `tox`
~~~~~~~~~

CAL sử dụng `tox`_ để quản lý môi trường ảo nhằm phục vụ cho việc chạy test cases. Nó sử dụng `Testr`_để quản lý việc chạy các test cases.

Tox xử lý việc tạo ra 1 loạt `virtualenvs`.

Testr xử lý việc thực hiện song song một loạt các test cases cũng như tracking các long-running tests.

Thông tin chi tiết có thể tham khảo tại trang wiki:
    
    https://wiki.openstack.org/wiki/Testr

.._Testr: https://wiki.openstack.org/wiki/Testr
.._tox: http://tox.readthedocs.org/en/latest/
.._virtualenvs: https://pypi.python.org/pypi/virtualenv

Để chạy unit tests::
    tox -e py27