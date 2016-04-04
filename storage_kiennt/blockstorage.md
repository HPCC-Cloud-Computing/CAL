# Research about Cloud Block Storage - Volume.

## I. Rackspace.

#### 2 volume types:
- SSD: SSD volumes deliver even higher performance for databases and other I/O-intensive applications.
- SATA: SATA volumes work well for your everyday file system needs. This is the default volume type.

##### Ref: 
- [Python API](https://developer.rackspace.com/docs/cloud-block-storage/getting-started/?lang=python)
- [Compare with Openstack Cinder - Rackspace Cloud Block Storage v1 vs Openstack Cinder v2](https://developer.rackspace.com/docs/cloud-block-storage/v1/developer-guide/#document-general-api-info/cbsv1-methods-vs-cinderv2-methods)

#### Methods:

/* - create(status, display_name, attachments, availability_zone, bootable, creaeted_at, display_description, volume_type, snapshot_id, source_volid, metadata, id, size) */ 
- create_volume(display_name, size, volume_type)
- list_volumes()
- get_volume(volume_id)
- update_volume(volume_id, display_name, display_description)
- delete(volume_id)
- list_volume_types()
- create_snapshot(display_name, display_description, volume_id)
- list_snapshots()
- get_snapshot(snapshot_id)
- update_snapshot(snapshot_id, display_name, display_description)
- delete_snapshot(snapshot_id)

## II. Amazon EBS Volume.

##### Methods:

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

#### Args:

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
	attachment.attach-time - The time stamp when the attachment initiated.
	attachment.delete-on-termination - Whether the volume is deleted on instance termination.
	attachment.device - The device name that is exposed to the instance (for example, /dev/sda1 ).
	attachment.instance-id - The ID of the instance the volume is attached to.
	attachment.status - The attachment state (attaching | attached | detaching | detached ).
	availability-zone - The Availability Zone in which the volume was created.
	create-time - The time stamp when the volume was created.
	encrypted - The encryption status of the volume.
	size - The size of the volume, in GiB.
	snapshot-id - The snapshot from which the volume was created.
	status - The status of the volume (creating | available | in-use | deleting | deleted | error ).
	tag :key =*value* - The key/value combination of a tag assigned to the resource.
	tag-key - The key of a tag assigned to the resource. This filter is independent of the tag-value filter. For example, if you use both the filter "tag-key=Purpose" and the filter "tag-value=X", you get any resources assigned both the tag key Purpose (regardless of what the tag's value is), and the tag value X (regardless of what the tag's key is). If you want to list only resources where Purpose is X, see the tag :key =*value* filter.
	tag-value - The value of a tag assigned to the resource. This filter is independent of the tag-key filter.
	volume-id - The volume ID.
	volume-type - The Amazon EBS volume type. This can be gp2 for General Purpose (SSD) volumes, io1 for Provisioned IOPS (SSD) volumes, or standard for Magnetic volumes.
- starting_token(string): A token to specify where to start paginating. This is the NextToken from a previously truncated response.
- max_items(int): The total number of items to return.
- force(boolean): Forces detachment if the previous detachment attempt did not occur cleanly (for example, logging into an instance, unmounting the volume, and detaching normally). This option can lead to data loss or a corrupted file system. Use this option only as a last resort to detach a volume from a failed instance. The instance won't have an opportunity to flush file system caches or file system metadata. If you use this option, you must perform file system check and repair procedures.

#### Ref:
- [Amazon EBS Docs](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-detaching-volume.html)  
- [EC2 Boto3 Docs](http://boto3.readthedocs.org/en/latest/reference/services/ec2.html#volume)

## III. Openstack.

Cinder Client Method(click to zoom in)

![alt text][cinder]
[cinder]: https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/cinderclient.png


### IV. Summary

| Method   | Openstack Cinder                                                                                                                                                                                       | AWS EBS Volume                                                                                                                                   | Rackspace Cloud Block Storage                                                                                                                                        |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| create() | create(size, consistentcygroup_id, snapshot_id, source_volid, name, description, volume_type, user_id, project_id, availability_zone, metadata, imageRef, scheduler_hints, multiattach, souce_replica) | - create/restore volume from snapshot(dry_run, volume_type, size, availability_zone, encrypted, disk_offering_id, snapshot_id, iops, kms_key_id) | create(status, display_name, attachments, availability_zone, bootable, creaeted_at, display_description, volume_type, snapshot_id, source_volid, metadata, id, size) |
| list()   | list(detailed, search_opts, marker, limit, sort_key, sort_dir, sort)                                                                                                                                   | describe_status(dry_run, volume_id, filter, starting_token, page_size, max_items)                                                                | list_volume()                                                                                                                                                        |
| show()   | get(volume_id)                                                                                                                                                                                         |                                                                                                                                                  | show(volume_id)                                                                                                                                                      |
| delete() | delete(volume_id, cascade)                                                                                                                                                                             | delete(volume_id)                                                                                                                                | delete(volume_id)                                                                                                                                                    |
| update() | update(volume_id, name, description)                                                                                                                                                                   |                                                                                                                                                  | update(volume_id, display_name, display_description)                                                                                                                 |
| attach() | attach(volume_id, instance_uuid, mountpoint, mode, hostname)                                                                                                                                           | attach_to_instance(dry_run, volume_id, instance_id, device)                                                                                      |                                                                                                                                                                      |
| detach() | detach(volume_id, attachment_uuid)                                                                                                                                                                     | detach_from_instance(dry_run, instance_id, device, force, volume_id)                                                                             |                                                                                                                                                                      |
|          |                                                                                                                                                                                                        |                                                                                                                                                  |                                                                                                                                                                      |
