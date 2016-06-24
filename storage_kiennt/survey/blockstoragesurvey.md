# Survey Report

## Overview.

### Introduction.

Với những ưu điểm của công nghệ điện toán đám mây, phát triển và triển khai dịch vụ, ứng dụng trên nền môi trường đám mây đang là xu thế hiện nay. Vì thế có hàng trăm nhà cung cấp dịch vụ đám mây (Cloud vendor): OpenStack, VMware vCloud, AWS, Azure... Do vấn đề cạnh tranh trong kinh doanh cùng với việc thiếu đi một chuẩn chính thức cho các dịch vụ cloud, đã gây hệ quả không thể tránh khỏi : Mỗi nhà cung cấp lại áp đặt một chuẩn, kỹ thuật riêng dịch vụ cloud của công ty. Mỗi công nghệ như hypervisor, networking, data storage facilities ,... lại có một cách sử dụng khác nhau trong dịch vụ được cung cấp bởi nhà cung cấp khác nhau. Điều này vô hình chung trói người dùng vào những nền tảng đám mây đã có. Đồng thời, vấn đề lưu trữ và chuyển dịch dữ liệu giữa các nền tảng đám mây khác nhau cũng trở nên khó khăn. 

Chính vì thế, đứng trên góc nhìn của những nhà phát triển dịch vụ, người dùng cần đưa ra giải pháp cho phép đơn giản hóa việc phát triển và triển khai ứng dụng trên nhiều nền tảng đám mây, không bị trói buộc vào một nhà cung cấp duy nhất. 

Chúng tôi sẽ đưa ra một hướng tiếp cận mới, cho phép triển khai ứng dụng trên các nền tảng cloud khác nhau, và ngoài ra còn cho phép dịch chuyển ứng dụng giữa các nền tảng ấy. Nền tảng của hướng tiếp cận này là Cloud Abstraction Layer(CAL), hỗ trợ quản lý một vòng đời toàn bộ của dịch vụ: từ phát triển, triển khai cho đến đi vào hoạt động nên đám mây IaaS. Dựa trên CAL, quá trình phát triển và triển khai dịch vụ sẽ trở nên dễ dàng và đơn giản hơn. Quan trọng hơn là nó hỗ trợ khả năng tương tác qua lại giữa các nền tảng đám mây khác nhau. 

Trong tài liệu này, chúng tôi sẽ trình bày về tổng quan các phương thức của dịch vụ lưu trữ khối (Block Storage)[2] tại các nền tảng đám mây khác nhau, từ đó rút ra được nhưng phương thức chung, định hình thiết kế của CAL. 
    
    
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

5. Use cases của dịch vụ lưu trữ khối (Block Storage).

    Những use case chính của block-storage:
    - Block Storage phù hợp cho các cơ sở dữ liệu vì cơ sở dữ liệu đòi hỏi hiệu năng I/O nhất quán và kết nối với độ trễ thấp.
    - Sử dụng Block Storage cho RAID Volume - kết hợp nhiều ổ đĩa được tổ chức thông qua stripping và mirroring.
    - Các ứng dụng yêu cầu xử lý phía dịch vụ (service side processing) như Java, PHP và .NET.
    - Ứng dụng quan trọng như Oracle, SAP, Microsoft Exchange & Microsoft SharePoint.

### High Level Design.

### Detail Design.

## Detail.

Trong phạm vi tài liệu, chúng tôi sẽ chỉ tiến hành tìm hiểu và nghiên cứu về phương thức của 3 dịch vụ lưu trữ theo khối(block-storage):
- OpenStack Cinder.
- Amazon EBS Volume.
- Rackspace Cloud Block Storage.

### Listed & Comprasion.

1. OpenStack Cinder. [6]

    Cinder là code-name của một dự án trong OpenStack, có nhiệm vụ lưu trữ dữ liệu trên các volume, cũng như đóng vai trò backup, tạo snapshot cho hệ thống máy ảo VMs.
    
    Biểu đồ lớp bóc tách từ package python-cinderclient(Ấn vào để phóng to):
    
    ![alt text](https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/survey/pic/cinderclient.png)    
    
    **Method**
    
    - get(volume_id)
    - list(detailed, search_opts, marker, limit, sort_key, sort_dir, sort)
    - delete(volume. cascade)
    - update(volume)
    - attach(volume, instance_uuid, mountpoint, mode, hostname)
    - detach(volume, attachment_uuid)
    - reserve(volume)
    - unreserve(volume)
    - begin_detaching(volume)
    - roll_detaching(volume)
    - initialize_connection(volume, connector)
    - terminate_connection(volume, connector)
    - set_metadata(volume, metadata)
    - delete_metadata(volume, keys)
    - delete_image_metadata(volume, keys)
    - set_image_metadata(volume, metadata)
    - show_image_metadata(volume)
    - upload_to_image(volume, force, image_name, container_format, disk_format)
    - force_delete(volume)
    - reset_state(volume, state, attach_status, migration_status)
    - extend(volume, new_size)
    - get_encrytion_metadata(volume_id)
    - migrate_volume(volume, host, force_host_copy, lock_volume)
    - migrate_volume_completion(old_volume, new_volume, error)
    - update_all_metadata(volume, metadata)
    - update_readonly_flag(volume, flag)
    - retype(volume, volume_type, policy)
    - set_bootable(volume, flag)
    - manage(host, ref, name, description, volume_type, availability-zone, metadata, bootable)
    - unmange(volume)
    - promote(volume)
    - reenable(volume)
    - get_pools(detail)

2. Amazon EBS Volume. [7]

    Amazon EBS Volume có 3 kiểu Volume chính: 
    - gp2 - General Purpose (SSD) volumes.
    - io1 - Provisioned IOPS (SSD) volumes.
    - standard = Magnetic volumes. 
    Dựa trên CLI API của EBS và documentation của Boto3 [9], chúng tôi đã liệt kê được những phương thức của Amazon EBS Volume như sau:
    
    **Method**

    - create/restore volume from snapshot(dry_run, volume_type, size, availability_zone, encrypted, disk_offering_id, snapshot_id, iops, kms_key_id)
    - attach_to_instance(dry_run, volume_id, instance_id, device)
    - create_snapshot(dry_run, description)
    - create_tags(dry_run, tags): add or overwrites one or more tags for the specified EC2 resources.
    - delete(dry_run, volume_id)
    - describe_attribute(dry_run, attribute)
    - describe_status(dry_run, volume_id, filter, starting_token, page_size, max_items)
    - detach_from_instance(dry_run, instance_id, device, force, volume_id)
    - enable_io(dry_run): enable i/o operations for a volume that had i/o operations disabled.
    - load(): call ec2.client.describe_volumes() to update the attributes of the Volume resouce.
    - modify_attribute(dry_run, auto_enable_io): modify a volume attribute
    - reload()

    **Args**

    - dry-run(boolean): Checks whether you have the required permissions for the action, without actually making the request, and provides an error response. If you have the required permissions, the error response is DryRunOperation . Otherwise, it is UnauthorizedOperation.
    - volume_type(string): The volume type. This can be gp2 for General Purpose (SSD) volumes, io1 for Provisioned IOPS (SSD) volumes, or standard for Magnetic volumes. Default = standard.
    - size(int): The size of the volume, in GiBs. Default: If you're creating the volume from a snapshot and don't specify a volume size, the default is the snapshot size.
    - snapshot_id(string): The snapshot from which to create the volume. (Optional).
    - availability_zone(string): The Availability Zone in which to create the volume. Use describe-availability-zones to list the Availability Zones that are currently available to you.
    - iops(int): Only valid for Provisioned IOPS (SSD) volumes. The number of I/O operations per second (IOPS) to provision for the volume, with a maximum ratio of 30 IOPS/GiB.
    - encrypted(boolean): Specifies whether the volume should be encrypted. Encrypted Amazon EBS volumes may only be attached to instances that support Amazon EBS encryption. Volumes that are created from encrypted snapshots are automatically encrypted. There is no way to create an encrypted volume from an unencrypted snapshot or vice versa. If your AMI uses encrypted volumes, you can only launch it on supported instance types.
    - kms_key_id(string): The full ARN of the AWS Key Management Service (AWS KMS) customer master key (CMK) to use when creating the encrypted volume. This parameter is only required if you want to use a non-default CMK; if this parameter is not specified, the default CMK for EBS is used. The ARN contains the arn:aws:kms namespace, followed by the region of the CMK, the AWS account ID of the CMK owner, the key namespace, and then the CMK ID.
    - volume_id(sring): The ID of the EBS volume. The volume and instance must be within the same Availability Zone.
    - instance_id(string): The ID of the instance.
    - device(string): The device name to expose to the instance (for example, /dev/sdh or xvdh ).
    - volume_ids(list): One or more volume IDs.
    - filters(list): One or more filters.
        + attachment.attach-time - The time stamp when the attachment initiated.
        + attachment.delete-on-termination - Whether the volume is deleted on instance termination.
        + attachment.device - The device name that is exposed to the instance (for example, /dev/sda1 ).
        + attachment.instance-id - The ID of the instance the volume is attached to.
        + attachment.status - The attachment state (attaching | attached | detaching | detached ).
        + availability-zone - The Availability Zone in which the volume was created.
        + create-time - The time stamp when the volume was created.
        + encrypted - The encryption status of the volume.
        + size - The size of the volume, in GiB.
        + snapshot-id - The snapshot from which the volume was created.
        + status - The status of the volume (creating | available | in-use | deleting | deleted | error ).
        + tag :key =*value* - The key/value combination of a tag assigned to the resource.
        + tag-key - The key of a tag assigned to the resource. This filter is independent of the tag-value filter. For example, if you use both the filter "tag-key=Purpose" and the filter "tag-value=X", you get any resources assigned both the tag key Purpose (regardless of what the tag's value is), and the tag value X (regardless of what the tag's key is). If you want to list only resources where Purpose is X, see the + tag :key =*value* filter.
        + tag-value - The value of a tag assigned to the resource. This filter is independent of the tag-key filter.
        + volume-id - The volume ID.
        + volume-type - The Amazon EBS volume type. This can be gp2 for General Purpose (SSD) volumes, io1 for Provisioned IOPS (SSD) volumes, or standard for Magnetic volumes.
    - starting_token(string): A token to specify where to start paginating. This is the NextToken from a previously truncated response.
    - max_items(int): The total number of items to return.
    - force(boolean): Forces detachment if the previous detachment attempt did not occur cleanly (for example, logging into an instance, unmounting the volume, and detaching normally). This option can lead to data loss or a corrupted file system. Use this option only as a last resort to detach a volume from a failed instance. The instance won't have an opportunity to flush file system caches or file system metadata. If you use this option, you must perform file system check and repair procedures.

3. Rackspace Cloud Block Storage. [8]
    Rackspace Cloud Block Storage có 2 kiểu volume: 
    - SSD: SSD volumes deliver even higher performance for databases and other I/O-intensive applications.
    - SATA: SATA volumes work well for your everyday file system needs. This is the default volume type.

    **Method**

    - create/restore volume from snapshot(dry_run, volume_type, size, availability_zone, encrypted, disk_offering_id, snapshot_id, iops, kms_key_id)
    - attach_to_instance(dry_run, volume_id, instance_id, device)
    - create_snapshot(dry_run, description)
    - create_tags(dry_run, tags): add or overwrites one or more tags for the specified EC2 resources.
    - delete(dry_run, volume_id)
    - describe_attribute(dry_run, attribute)
    - describe_status(dry_run, volume_id, filter, starting_token, page_size, max_items)
    - detach_from_instance(dry_run, instance_id, device, force, volume_id)
    - enable_io(dry_run): enable i/o operations for a volume that had i/o operations disabled.
    - load(): call ec2.client.describe_volumes() to update the attributes of the Volume resouce.
    - modify_attribute(dry_run, auto_enable_io): modify a volume attribute
    - reload()

### Summary.

| Method   | Openstack Cinder                                                                                                                                                                                       | AWS EBS Volume                                                                                                                                   | Rackspace Cloud Block Storage                                                                                                                                        |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| create() | create(size, consistentcygroup_id, snapshot_id, source_volid, name, description, volume_type, user_id, project_id, availability_zone, metadata, imageRef, scheduler_hints, multiattach, souce_replica) | - create/restore volume from snapshot(dry_run, volume_type, size, availability_zone, encrypted, disk_offering_id, snapshot_id, iops, kms_key_id) | create(status, display_name, attachments, availability_zone, bootable, creaeted_at, display_description, volume_type, snapshot_id, source_volid, metadata, id, size) |
| list()   | list(detailed, search_opts, marker, limit, sort_key, sort_dir, sort)                                                                                                                                   | describe_status(dry_run, volume_id, filter, starting_token, page_size, max_items)                                                                | list_volume()                                                                                                                                                        |
| show()   | get(volume_id)                                                                                                                                                                                         |                                                                                                                                                  | show(volume_id)                                                                                                                                                      |
| delete() | delete(volume_id, cascade)                                                                                                                                                                             | delete(volume_id)                                                                                                                                | delete(volume_id)                                                                                                                                                    |
| update() | update(volume_id, name, description)                                                                                                                                                                   |                                                                                                                                                  | update(volume_id, display_name, display_description)                                                                                                                 |
| attach() | attach(volume_id, instance_uuid, mountpoint, mode, hostname)                                                                                                                                           | attach_to_instance(dry_run, volume_id, instance_id, device)                                                                                      |                                                                                                                                                                      |
| detach() | detach(volume_id, attachment_uuid)                                                                                                                                                                     | detach_from_instance(dry_run, instance_id, device, force, volume_id)                                                                             |                                                                                                                                                                      |
|          |                                                                                                                                                                                                        |                                                                                                                                                  

## Challenges & Future work

## Conclusion.

Chúng tôi đã giới thiệu về hướng tiếp cận mới cho việc phát triển và triển khai dịch vụ trên nền tảng đa đám mây. Cốt lõi của phương pháp này là một lớp trừu tượng cấp cao - CAL, cung cấp các phương thức trừu tượng hóa chung nhất các chức năng cơ bản của đa đám mây. Dựa trên lớp này, quá trình phát triển và triển khai dịch vụ sẽ trở nên dễ dàng hơn: nhà phát triển sẽ xây dựng dịch vụ của họ, bằng cách kế thừa các phương thức hiện có của CAL, không phải sử dụng thêm bất kỳ các API trung gian cũng như không phải kết nối trực tiếp đến từng máy ảo VM. Người dùng có thể triển khai ứng dụng, dịch vụ trên nhiều đám mây khác nhau, mà không phải phụ thuộc vào nền tảng đám mây bên dưới.

Ngoài ra, trong tài liệu này, chúng tôi cũng trình bày về quá trình tìm hiểu và nghiên cứu về các phương thức của dịch vụ lưu trữ khối ở nhiều đám mây khác nhau(cụ thể là Amazon EBS Volume, OpenStack Cinder, Rackspace Cloud Block Storage). Từ đó, định nghĩa được các phương thức sẽ có trong lớp trừu tương CAL liên quan đến dịch vụ lưu trữ khối(block storage).

## Refs.

1. A Novel Approach for Developing Interoperable Services in Cloud Environment - Binh Minh Nguyen, Viet Tran, Ladislav Hluchy, Department of Parallel and Distributed Computing, Institute of Informatics, Slovak Academy of Sciences ,Bratislava, Slovakia.
2. [Block Storage](https://en.wikipedia.org/wiki/Block_(data_storage))
3. [ApacheLibCloud](https://libcloud.apache.org/)
4. [jCloud](https://jclouds.apache.org/)
5. [OVF](https://en.wikipedia.org/wiki/Open_Virtualization_Format)
6. [OpenStack Cinder](https://wiki.openstack.org/wiki/Cinder)
7. [Amazon EBS Volume](https://aws.amazon.com/ebs/)
8. [Rackspace Cloud Block Storage](https://www.rackspace.com/cloud/block-storage)
9. [Boto 3](https://boto3.readthedocs.org/en/latest/)