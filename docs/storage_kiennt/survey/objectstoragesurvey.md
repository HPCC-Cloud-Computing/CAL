# Survey Report

## Overview.

### Introduction.

Với những ưu điểm của công nghệ điện toán đám mây, phát triển và triển khai dịch vụ, ứng dụng trên nền môi trường đám mây đang là xu thế hiện nay. Vì thế có hàng trăm nhà cung cấp dịch vụ đám mây (Cloud vendor): OpenStack, VMware vCloud, AWS, Azure... Do vấn đề cạnh tranh trong kinh doanh cùng với việc thiếu đi một chuẩn chính thức cho các dịch vụ cloud, đã gây hệ quả không thể tránh khỏi : Mỗi nhà cung cấp lại áp đặt một chuẩn, kỹ thuật riêng dịch vụ cloud của công ty. Mỗi công nghệ như hypervisor, networking, data storage facilities ,... lại có một cách sử dụng khác nhau trong dịch vụ được cung cấp bởi nhà cung cấp khác nhau. Điều này vô hình chung trói người dùng vào những nền tảng đám mây đã có. Đồng thời, vấn đề lưu trữ và chuyển dịch dữ liệu giữa các nền tảng đám mây khác nhau cũng trở nên khó khăn. 

Chính vì thế, đứng trên góc nhìn của những nhà phát triển dịch vụ, người dùng cần đưa ra giải pháp cho phép đơn giản hóa việc phát triển và triển khai ứng dụng trên nhiều nền tảng đám mây, không bị trói buộc vào một nhà cung cấp duy nhất. 

Chúng tôi sẽ đưa ra một hướng tiếp cận mới, cho phép triển khai ứng dụng trên các nền tảng cloud khác nhau, và ngoài ra còn cho phép dịch chuyển ứng dụng giữa các nền tảng ấy. Nền tảng của hướng tiếp cận này là Cloud Abstraction Layer(CAL), hỗ trợ quản lý một vòng đời toàn bộ của dịch vụ: từ phát triển, triển khai cho đến đi vào hoạt động nên đám mây IaaS. Dựa trên CAL, quá trình phát triển và triển khai dịch vụ sẽ trở nên dễ dàng và đơn giản hơn. Quan trọng hơn là nó hỗ trợ khả năng tương tác qua lại giữa các nền tảng đám mây khác nhau. 

Trong tài liệu này, chúng tôi sẽ trình bày về tổng quan các phương thức của dịch vụ lưu trữ đối tượng (Object Storage)[2] tại các nền tảng đám mây khác nhau, từ đó rút ra được nhưng phương thức chung, định hình thiết kế của CAL.
    
    
### Related work.

Mặc dù đã có những nỗ lực nhằm đưa ra chuẩn chung cho nền tảng cloud như Open Virtualization Format(OVF), Open Cloud Computing Interface(OCCI), ApacheLibCloud, jCloud,... , nhưng rõ ràng tất cả đều chưa được một giải pháp triệt để cho vấn đề phát triển và triển khai ứng dụng trên môi trường cloud.

Thay vì tạo nên một chuẩn chung, SimpleCloud API, ApacheLibcloud[3], jCloud[4],... lại được thiết kế và thực thi nhằm quản lý tài nguyên trên môi trường đám mây. Ưu điểm của các API abstractions là không bị phụ thuộc vào các nhà cung cấp nền tảng. Tuy nhiên, những công nghệ này không giúp người dùng phát triển và triển khai ứng dụng trên nền tảng đám mây một cách dễ dàng hơn. Người dùng vẫn phải kết nối trực tiếp đến máy ảo, cài đặt và cấu hình mọi thứ - điều này rõ ràng đòi hỏi những kiến thức và kỹ năng không phải ai cũng có. Thời điểm hiện tại, chưa công nghệ nào ở trên cung cấp việc chức năng hóa các task cài đặt, cấu hình.

Bảng so sánh CAL và những giải pháp đã được triển khai

|                     | CAL | OVF | OCCI | SimpleCloud API | ApacheLibCloud | jCloud | boto | ApacheCloudStack |
|:-------------------:|:---:|:---:|:----:|:---------------:|:--------------:|:------:|:----:|:----------------:|
|   General Approach  |  A  |  S  |   S  |        A        |        A       |    A   |   A  |         A        |
| Resource Management |  x  |     |   X  |        X        |        X       |    X   |   X  |         X        |
| Service Development |  X  |     |      |                 |                |        |      |                  |
|  Service Deployment |  X  |     |   x  |        x        |        x       |    x   |      |                  |
|   Interoperability  |  X  |  X  |   x  |        x        |        x       |    x   |   x  |         x        |

*Chú thích*
	- A - **A**bstraction approach
	- S - **S**tandardization approach
	- X - major feature
	- x - support feature

## Architecture.

### Use case.

1. Triển khai trên đa đám mây.

	Một ứng dụng có thể được chia phần, và mỗi phần lại được triển khai trên một nền tảng đám mây khác nhau. Tuy nhiên vẫn đảm bảo được khả năng tương tác giữa các phần, cho phép ứng dụng hoạt động bình thường. 
	Lấy ví dụ, một ứng dụng web điển hình thường gồm 3 tầng khác nhau:
	+ Tầng Load Balancer.
	+ Tầng Web Front.
	+ Tầng App Backend.
	Người dùng sẽ sử dụng một private cloud dựa trên OpenStack hoặc VMware, vốn có ít tài nguyên hơn nhưng lại bảo mật hơn các nền tảng public clouds. Vì thế, họ sẽ sử dụng OpenStack API để chạy máy ảo VM có backend của dịch vụ web trên private cloud, đồng thời chạy máy ảo triển khai Load balancer và web front trên public cloud.

2. Dịch chuyển ứng dụng giữa các nền tảng đám mây.

	Lấy ví dụ đơn giản, tôi triển khai một hệ thống bán hành online trên private cloud như OpenStack. Trong trường hợp bình thường, tài nguyên hệ thống và băng thông mạng là đủ, không vấn đề. Tuy nhiên, trong những dịp giảm giá, khi lượt truy cập vào hệ thống tăng đột biến, tôi muốn chuyển hệ thống của tôi sang public cloud tại thời điểm đó. Sau đó, có thể đưa ứng dụng quay trở lại private cloud.
    
    ![alt text](https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/survey/pic/scaleout.jpg)

3. Chuyển dịch dữ liệu giữa các nền tảng đám mây.

	Trong nhiều trường hợp, người dùng có nhu cầu dịch chuyển, chuyển đổi dữ liệu được lưu trữ giữa các nền tảng đám mây khác nhau.

4. Mở rộng khả năng lưu trữ bằng cách sử dụng nhiều dịch vụ lưu trữ của đa nền tảng.

5. Use cases của riêng dịch vụ lưu trữ đối tượng (Object Storage)
    
    Những use case chính của Object Storage:
    - Lưu trữ dữ liệu phi cấu trúc như nhạc, ảnh,...
    - Lưu trữ file backup database dumps và file log.
    - Tập dữ liệu kích thước lớn.
    - Lưu trữ file vào ổ đĩa từ cục bộ.
    

### High Level Design.

### Detail Design.

## Detail.

Trong phạm vi tài liệu, chúng tôi sẽ chỉ tiến hành tìm hiểu và nghiên cứu về phương thức của 3 dịch vụ lưu trữ theo đối tượng tiêu biểu:
- Amazon S3.
- OpenStack Swift.
- Cloud Data Management Interface - CDMI.

### Listed.

1. Amazon S3. [7]
    
    Amazon S3 cung cấp cho người dùng dịch vụ lưu trữ bền vững, bảo mật và dễ dàng mở rộng. Amazon S3 lưu trữ đối tượng với một giao diện web đơn giản, nhằm lưu trữ và lấy ra dữ liệu tại mọi nơi. 

    Dựa trên CLI API của S3 và documentation của Boto 3 [9], chúng tôi đã liệt kê ra được những phương thức như sau:
    
    **Method**
    - abort_multipart_upload(bucket, key, uploadid, request_player)
    - can_paginate(operation_name)
    - complete_multipart_upload(bucket, key, multipart_upload, uploadid, request_payer)
    - copy_object(acl, bucket, cache_control, content_disposition, content_language, content_type, copy_source, copy_source_if_match, copy_source_if_modified_since, copy_source_if_none_match, copy_source_if_unmodified_since, expires, grant_full_control, grant_read, grant_read_acp, grant_write_acp, key, metadata, metadata_driective, service_side_encryption, storage_class, website_redirect_location, sse_customer_algorithm, sse_customer_key, sse_kms_key_id, copy_source_sse_customer_algorithm, copy_source_sse_customer_key, request_payer)
    - create_bucket(acl, bucket, create_bucket_configuration, grant_full_control, grant_read, grant_read_acp, grant_write, grant_write_acp)
    - create_multipart_upload(acl,bucket, cache_control, content_disposition, content_encoding, content_language, content_type, expires, grant_full_control, grant_read, grant_read_acp, grant_write_acp, key, metadata, server_side_encryption, storage_class, website_redirect_location, sse_customer_algorithm, sse_customer_key, sse_kms_key_id, request_payer)
    - delete_bucket(bucket)
    - delete_bucket_cors(bucket)
    - delete_bucket_lifecycle(bucket)
    - delete_bucket_policy(bucket)
    - delete_bucket_replication(bucket)
    - delete_bucket_tagging(bucket)
    - delete_bucket_website(bucket)
    - delete_object(bucket, key, mfa, version_id, request_payer)
    - delete_objects(bucket, delete, mfa, request_payer)
    - download_file(bucket, key, file_name, extra_args, callback, config)
    - generate_presigned_post(bucket, key, fields, conditions, expries_in)
    - generate_presigned_url(client_method, params, expires_in, http_method)
    - get_bucket_acl(bucket)
    - get_bucket_cors(bucket)
    - get_bucket_lifecycle(bucket)
    - get_bucket_lifecycle_configuration(bucket)
    - get_bucket_location(bucket)
    - get_bucket_logging(bucket)
    - get_bucket_notification(bucket)
    - get_bucket_notification_configuration(bucket)
    - get_bucket_policy(bucket)
    - get_bucket_replication(bucket)
    - get_bucket_payment(bucket)
    - get_bucket_tagging(bucket)
    - get_bucket_versioning(bucket)
    - get_bucket_website(bucket)
    - get_object(bucket, if_match, if_modified_since, if_none_match, if_unmodified_since, key, range, response_content_disposition, response_content_encoding, response_content_type, response_content_language, response_expires, version_id, sse_customer_algorithm, sse_customer_key, request_payer)
    - get_object_acl(bucket, key, version_id, request_payer)
    - get_object_torrent(bucket, key, request_payer)
    - get_paginator(operation_name)
    - get_waiter(waiter_name)
    - head_bucket(bucket)
    - head_object(bucket, if_match, if_modified_since, if_none_match, if_unmodified_since, key, range, version_id, sse_customer_algorithm, sse_customer_key, request_payer)
    - list_buckets()
    - list_multipart_uploads(bucket, delimite, encoding_type, key_marker, max_uploads, prefix, upload_id_marker)
    - list_object_versions(bucket, delimite, encoding_type, key_marker, max_uploads, prefix, upload_id_marker)
    - list_objects(bucket, delimite, encoding_type, marker, max_keys, prefix)
    - list_parts(bucket, key, max_parts, part_number_marker, upload_id, request_payer)
    - put_bucket_acl(acl, access_control_policy, bucket, grant_full_control, grant_read, grant_read_acp, grant_write, grant_write_acp)
    - put_bucket_cors(bucket, cors_configuration)
    - put_bucket_lifecycle(bucket, lifecycle_configuration)
    - put_bucket_lifecycle_configuration(bucket, lifecycle_configuration)
    - put_bucket_logging(bucket, bucket_logging_status)
    - put_bucket_notification(bucket, notification_configuration)
    - put_bucket_notification_configuration(bucket, notification_configuration)
    - put_bucket_policy(bucket, policy)
    - put_bucket_replication(bucket, replication_configuration)
    - put_bucket_request_payment(bucket, request_payment_configuation)
    - put_bucket_tagging(bucket, tagging)
    - put_bucket_versioning(bucket, mfa, versioning_configuration)
    - put_bucket_website(bucket, website_configuration)
    - put_object(acl, body, bucket, cache_control, content_disposition, content_encoding, content_language, content_length, content_md5, content_type, expries, grant_full_control, grant_read, grant_read_acp, grant_write_acp, key, metadata, server_side_encryption, storage_class, website_redirect_location, sse_customer_algorithm, sse_customer_key, sse_kms_key_id, request_payer)
    - put_object_acl(acl, access_control_policy, bucket, grant_full_control, grant_read, grant_read_acp, grant_write, grant_write_acp, key, request_payer)
    - restore_object(bucket, key, version_id, restore_request, request_payer)
    - upload_file(filename, bucket, key, extra_args, callback, config)
    - upload_part(body, bucket, content_length, content_md5, key, part_number, upllad_id, sse_customer_key, sse_customer_algorithm, request_payer)
    - upload_part_copy(bucket, copy_source, copy_source_if_match, copy_source_if_modified_since, copy_source_if_unmodified_since, copy_source_range, key, part_number, upload_id, sse_customer_algorithm, sse_customer_key, copy_source_sse_customer_algorithm, copy_source_sse_customer_key, request_payer)

2. OpenStack Swift. [6]

    Swift là một dự án trong OpenStack, là thành phần chịu trách nhiệm quản lý việc lưu trữ theo đối tượng, cho phép người dùng có thể lưu trữ và lấy ra một lượng lớn dữ liệu bằng bộ API đơn giản. Dự án này được xây dựng nhằm mục đích dễ mở rộng và tối ưu hóa cho khả năng bền vững, khả dụng và tính đồng thời của toàn bộ bộ dữ liệu. Swift hỗ trợ tốt cho việc lưu trữ dữ liệu không cấu trúc, liên tục cập nhật và gia tăng về kích thước.
    
    Biểu đồ lớp bóc tách từ package python-swiftclient(Ấn vào để phóng to):
    
    ![alt text](https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/survey/pic/swiftclient.png)
    
    **Method**
    - head_account()
    - get_account(marker, limit, prefix, end_marker, full_listing)
    - post_account(headers, response_dict, query_string, data)
    - head_container(container, headers)
    - get_container(container, marker, limit, prefix, delimiter, end_marker, path, full_listing, headers)
    - put_container(container, headers, response_dict)
    - post_container(container, headers, response_dict)
    - delete_container(container, headers, response_dict)
    - head_object(container, obj, headers)
    - get_object(container, obj, resp_chunk_size, query_string, response_dict, headers)
    - put_object(container, obj, contents, content_length, etag, chunk_sie, content_type, headers, query_string, response_dict)
    - post_object(container, obj, headers, response_dict)
    - delete_object(container, obj, query_string, response_dict)
    - get_capabilities(url)
    
3. CDMI. [8]

    Cloud Data Management Interface định nghĩa nên các interface chức năng mà ứng dụng sẽ sử dụng để khởi tạo, tải về, cập nhật và xóa dữ liệu trên môi trường đám mây.
    
    Phía Client sẽ được phép sử dụng CDMI nằm truy cập các chức năng mà dịch vụ lưu trữ đám mây cung cấp, đồng thời cũng để quản lý các container và dữ liệu được đặt trong đấy. Ngoài ra, metadata cũng được đặt trong container.

### Summary.

1. So sánh Object Model của Swift, S3 & CDMI.

    ![alt text](https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/survey/pic/s3swiftcdmi_model.png)
    
2. Bảng so sánh và tổng kết:

|                                                                                   |                                                      OpenStack Swift                                                      |                                                                                                                                                                                       Amazon S3                                                                                                                                                                                      | Rackspace Cloud Object Storage | CDMI |
|:---------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------:|------|
|                                                                                   | head_account()                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |
|                                                                                   | get_account(marker, limit, prefix, end_marker, full_listing)                                                              |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |
|                                                                                   | post_account(headers, response_dict, query_string, data)                                                                  |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |
|                                                                                   | head_container(container, headers)                                                                                        | head_bucket(bucket)                                                                                                                                                                                                                                                                                                                                                                  |                                |      |
| get_container(container, path)                                                    | get_container(container, marker, limit, prefix, delimiter, end_marker, path, full_listing, headers)                       | get_bucket(bucket)                                                                                                                                                                                                                                                                                                                                                                   |                                |      |
| put_container(container)                                                          | put_container(container, headers, response_dict)                                                                          | create_bucket(acl, bucket, create_bucket_configuration, grant_full_control, grant_read, grant_read_acp, grant_write, grant_write_acp)                                                                                                                                                                                                                                                |                                |      |
|                                                                                   | post_container(container, headers, response_dict)                                                                         |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |
| delete_container(container)                                                       | delete_container(container, headers, response_dict)                                                                       | delete_bucket(bucket)                                                                                                                                                                                                                                                                                                                                                                |                                |      |
| head_object(container, obj)                                                       | head_object(container, obj, headers)                                                                                      | head_object(bucket, if_match, if_modified_since, if_none_match, if_unmodified_since, key, range, version_id, sse_customer_algorithm, sse_customer_key, request_payer)                                                                                                                                                                                                                |                                |      |
| get_object(container, obj, resp_chunk_size, query_string)                         | get_object(container, obj, resp_chunk_size, query_string, response_dict, headers)                                         | get_object(bucket, if_match, if_modified_since, if_none_match, if_unmodified_since, key, range, response_content_disposition, response_content_encoding, response_content_type, response_content_language, response_expires, version_id, sse_customer_algorithm, sse_customer_key, request_payer)                                                                                    |                                |      |
| put_object(container, obj, contents, content_length, content_type, query_string,) | put_object(container, obj, contents, content_length, etag, chunk_sie, content_type, headers, query_string, response_dict) | put_object(acl, body, bucket, cache_control, content_disposition, content_encoding, content_language, content_length, content_md5, content_type, expries, grant_full_control, grant_read, grant_read_acp, grant_write_acp, key, metadata, server_side_encryption, storage_class, website_redirect_location, sse_customer_algorithm, sse_customer_key, sse_kms_key_id, request_payer) |                                |      |
|                                                                                   | post_object(container, obj, headers, response_dict)                                                                       |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |
| delete(container, obj)                                                            | delete_object(container, obj, query_string, response_dict)                                                                | delete_object(bucket, key, mfa, version_id, request_payer)                                                                                                                                                                                                                                                                                                                           |                                |      |
|                                                                                   | get_capabilities(url)                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                      |                                |      |

## Challenges & Future work

## Conclusion.

Chúng tôi đã giới thiệu về hướng tiếp cận mới cho việc phát triển và triển khai dịch vụ trên nền tảng đa đám mây. Cốt lõi của phương pháp này là một lớp trừu tượng cấp cao - CAL, cung cấp các phương thức trừu tượng hóa chung nhất các chức năng cơ bản của đa đám mây. Dựa trên lớp này, quá trình phát triển và triển khai dịch vụ sẽ trở nên dễ dàng hơn: nhà phát triển sẽ xây dựng dịch vụ của họ, bằng cách kế thừa các phương thức hiện có của CAL, không phải sử dụng thêm bất kỳ các API trung gian cũng như không phải kết nối trực tiếp đến từng máy ảo VM. Người dùng có thể triển khai ứng dụng, dịch vụ trên nhiều đám mây khác nhau, mà không phải phụ thuộc vào nền tảng đám mây bên dưới.

Ngoài ra, trong tài liệu này, chúng tôi cũng trình bày về quá trình tìm hiểu và nghiên cứu về các phương thức của dịch vụ lưu trữ đối tượng ở nhiều đám mây khác nhau(cụ thể là Amazon S3, OpenStack Swift, CDMI). Từ đó, định nghĩa được các phương thức sẽ có trong lớp trừu tương CAL liên quan đến dịch vụ lưu trữ đám mây.

## Refs.

1. A Novel Approach for Developing Interoperable Services in Cloud Environment - Binh Minh Nguyen, Viet Tran, Ladislav Hluchy, Department of Parallel and Distributed Computing, Institute of Informatics, Slovak Academy of Sciences ,Bratislava, Slovakia.
2. [Object Storage](https://en.wikipedia.org/wiki/Object_storage)
3. [ApacheLibCloud](https://libcloud.apache.org/)
4. [jCloud](https://jclouds.apache.org/)
5. [OVF](https://en.wikipedia.org/wiki/Open_Virtualization_Format)
6. [OpenStack Swift](http://docs.openstack.org/developer/swift/)
7. [Amazon S3](https://aws.amazon.com/s3/)
8. [CDMI](http://www.snia.org/cdmi)
9. [Boto 3](https://boto3.readthedocs.org/en/latest/)
10. [Implement A Standard API](http://events.linuxfoundation.org/sites/events/files/slides/ImplementingAStandardAPI.pdf)