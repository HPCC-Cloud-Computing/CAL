# Research about Cloud Object Storage.

## I. Amazon S3

#### Methods:

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

#### Ref:

- [Boto 3 Docs](http://boto3.readthedocs.org/en/latest/reference/services/s3.html)

## II. Openstack Swift.

#### Methods:

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

#### Ref:

![alt text][swift]
[swift]: https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/swiftclient.png

## III. CDMI.

#### Ref:

#### Methods:

- create_data_object(mimetype, metadata, domain_uri, deserialize, serialize, copy, move, reference, deserialize_value, value_transfer_encoding, value)
- update__data_object(mimetype, metadata, domain_uri, deserialize, serialize, copy, move, reference, deserialize_value, value_transfer_encoding, value)
- create_container_object(metadata, domain_uri, exports, deserialize, copy, move, deserialize_value)

## IV. Summary.

- [Swift/S3 REST API Compare](https://wiki.openstack.org/wiki/Swift/APIFeatureComparison)
- [Openstack SwiftS3](https://github.com/openstack/swift3)
- [Implement A Standard API](http://events.linuxfoundation.org/sites/events/files/slides/ImplementingAStandardAPI.pdf) - [Source](https://github.com/osaddon/cdmi)
- Compare Swift, S3 & CDMI Object Model.

![alt text][compare]
[compare]: https://raw.githubusercontent.com/cloudcomputinghust/CAL/master/storage_kiennt/s3swiftcdmi_model.png
