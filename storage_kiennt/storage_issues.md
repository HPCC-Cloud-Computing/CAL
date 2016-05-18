# STORAGE ISSUES CROSS CLOUD.

## Overview.

Trong môi trường multi-cloud, việc sử dụng storage gặp phải những vấn đề sau:
- Di chuyển tài nguyên lưu trữ giữa 2 cloud.
- Vấn đề attach volume cho multi instances.
- Vấn đề attach volume với instance và di chuyển instance giữa 2 cloud.
- Chia sẻ volume giữa nhiều instance ở các cloud khác nhau.
- Vấn đề build lại instance từ snapshot volume.

## Detail.

### 1. Di chuyển tài nguyên lưu trữ giữa 2 cloud.

- Vấn đề: Khi di chuyển volume, hay các object được lưu trữ trong Object Storage, cần phải lưu ý đến định dạng của volume có tương thích, kiểu dữ liệu, dung lượng dữ liệu, đường dẫn đến dữ liệu(đối với Object Storage),...
- Giải pháp: 
    + Check khối lượng dữ liệu sẽ di chuyển. 
    + Sau đó cần check tài nguyên lưu trữ khả dụng bên cloud đích đến.
    + Khi thực hiện di chuyển dữ liệu, cần chắc chắn đường truyền ổn định --> check kết nối. 
    + Sau đó, check xem dữ liệu đã được di chuyển hoàn toàn sang bên cloud đích đến hay chưa. Check status của dữ liệu.

### 2. Vấn đề attach volume cho multi instances.

- Vấn đề: Hiện tại, Amazon EBS chỉ cho phép attach instance - volume theo kiểu 1 - N, nghĩa là 1 instance có thể attach được với nhiều volume(40). Tuy nhiên, theo hướng phát triển hiện tại, Openstack Cinder (và cả project Openstack Manila) đã cho phép attach theo kiểu N - N, 1 instance có thể attach nhiều volume, tuy nhiên 1 volume cũng có thể được mount bởi nhiều instance, làm volume 'chung', chia sẻ tài nguyên lưu trữ. Vậy nên, khi chuyển dịch volume giữa các cloud, thì cần phải lưu ý đến vấn đề: volume được attach bởi bao nhiêu instance? Hay mỗi instance được attach bởi bao nhiêu volume?

- Giải pháp: Check số lượng các instance đang sử dụng volume. Nếu thỏa mãn, có thể di chuyển thì mới cho phép thực hiện.

### 3. Vấn đề attach volume với instance và di chuyển instance giữa 2 cloud.

- Vấn đề: Trong trường hợp cơ bản, 1 instance được attach với 1 volume. Khi di chuyển instance sang cloud khác, vẫn muốn sử dụng dịch vụ lưu trữ sử dụng volume, vậy có 2 cách giải quyết:
    + Giữ nguyên volume ở cloud ban đầu, chỉ di chuyển instance. Đồng thời thông qua network, tiến hành mount volume.
    + Di chuyển cả volume và instance sang cloud mới.
- Giải pháp: Đầu tiên, phải check phương án được lựa chọn.
    + Nếu lựa chọn phương án 1: Tiến hành theo mô hình NFS server.
    + Nếu lựa chọn phương án 2: Check tình trạng volume, số lượng instance đang sử dụng volume đó.(Đưa về issue 1).

### 4. Chia sẻ volume giữa nhiều instance ở các cloud khác nhau.

- Vấn đề: Volume có thể được sử dụng bởi nhiều instance ở nhiều cloud khác nhau. Việc phân quyển sử dụng volume ở các cloud đó.
- Giải pháp: Check network, yêu cầu cài đặt và sử dụng NFS.

### 5. Vấn đề build lại instance từ snapshot volume.

- Vấn đề: build lại instance từ snapshot đã được lưu trong volume. Tuy nhiên, có thể build được từ snapshot ở cloud khác?
- Giải pháp:

## Refs.
1. [Docs của Amazon EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstances.html)
2. [Multi attach volume OpenStack](https://specs.openstack.org/openstack/cinder-specs/specs/kilo/multi-attach-volume.html)
3. [Openstack NFS driver](http://docs.openstack.org/kilo/config-reference/content/NFS-driver.html)