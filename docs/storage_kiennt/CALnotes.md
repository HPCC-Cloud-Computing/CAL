# CAL Use cases

## 2 actors: DevUser & OpsUser

1. DevUser
	- Create and Manage Environment: Create ,Delete, Update, Clone Environment Var.
	- Manage Apps. ## Later.
	- Manage Nodes.	
		- Manage Compute Nodes(Instance): Start, Stop, Rebuild, Clone ,Restart, Upload, Build, Deploy App, Bind Domain, Check Status, Restore--- interact with 'env management'
		- Manage Storage Nodes(Volume): Create, Resize, Manage Data.
		- Manage Network Nodes(Network): Create, Add...
	- Monitor: Auto Scale ,Logs.
	- Manage Account: Iaas/Cloud Providers Authenticate Information?
	- Manage Domain.
	- Migration(Move env to another set of hardware - change cloud vendor?)
2. OpsUser - Monitoring --> Using Cloud Vendor Driver + Nagios + Rsyslog.
	- Manage Resources & Usage.
	- Manage users - cloud vendors account.
	- Statistics & Analytics.
	- Manage cloud vendors(Openstack, Aws, Cloudstack....)

	|=======|    |================|		    |===============================|         |=======|      |============|
User--->| Auth1 |--->| Software layer |------------>| CAL(Compute, Network, Storage |-------->| Auth2 |----->| Driver/API |------> IAAS-Cloud Vendors.
	|=======|    |================|		    |===============================|         |=======|      |============|
		     Define Env & Resouce vars     Get cloud vendor which was choosen                        Create Instance 
		     Then this will call CAL obj   in previous step. Call Cloud APIs.                        with apps.
		     Authenticate info for Iaas.   

-- Class CAL: set cloud vendor driver. Att: driver, Method: set_cloud, auth?

-- Class ComputeNode(CAL): 
	- Att: id, image, flavor, state, keypair, network(Doi tuong Class NetworkNode), volume(Doi tuong Class StorageNode), application_to_deploy
	- Method: start, stop, build, rebuild, install_app, exe_app, config_app, check_status, set_network, set_volume.


----> StorageNode: Research about Storage, method relate with storage in Openstack, Opennebula, AWS, .... ---> 
