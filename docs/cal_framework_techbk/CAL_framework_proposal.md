# CAL Framework Desgin
## Overview
### Introduction
#### History
#### Berief
Để xây dựng một hệ thống multi-cloud, có nhiều thành phần như VM, 
storage, network, ta cần đến một Framework. Framework là một server wsgi.
### Related Work
### Scope
Framework là một web framework, nhận những request từ bên ngoài từ đó các Controller bên dưới 
sẽ thực thi.
## Archietecture
### Use Cases
#### 1. Be a WSGI Server
Wsgi là một web server gateway interface. Ta sẽ build framework dựa theo chuẩn này.
WSGI gồm 3 thành phần như:

- Server:
- Middleware: 
- Application:

Ta sử dụng những thư viện sau để build một wsgi server:

- paste : để run phần server.
- webob : gồm những Class định sẵn như Request, Response khiến việc triển khai dễ dàng hơn.
- pastedeploy : cung cấp cơ chế load app một cách nhanh chóng.
- routes : cung cấp cơ chế router

#### 2. Dynamic Plugins
Wsgi cơ bản rất khó để enable, disable các App nằm bên dưới.
Framework này sẽ cũng cấp một cơ chế là Dynamic Plugins.
Ta sử bộ thư viện stevedore để thực thi cơ chế này.
