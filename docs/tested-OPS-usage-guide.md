# Usage Guide for Tested OPS de-facto API and OPS AWS EC2 API

## OPS de-facto API tested
- Environment: Physical Server
- Local Address:  192.168.50.16
- Architecture:
	- Install Mitaka All in One
	- Installed Projects: Keystone, Nova, Glance, Neutron, Horizon
	- Using OVS for Neutron
	- External Network IP: 192.168.50.16
	- Internal Network IP: 10.1.2.16 
- Access:
	- From Local Network (HPCC* 192.168.50.x): 
		- Access to bkcloud16 node server: ssh bkcloud16@192.168.50.16
	- From Public Network:
		- Access to bkcloud12 node server
		- Access to bkcloud16 node server: ssh bkcloud16@192.168.50.16 
- Usage Info: 
	- Auth Script: /home/bkcloud16/admin.sh
	- OPS Admin username/password: admin/bkcloud 
	- Endpoint URL: http://192.168.50.16:35357/v3/
 
## OPS AWS EC2 API
- Environment: KVM VM on Server 192.168.50.16
- Local Address: 192.168.122.75
- Architecture:
	- Install Devstack Mitaka All in One
	- Installed Projects: Keystone, Nova, Glance, Neutron, Cinder, Horizon, EC2-API
	- Using OVS for Neutron
- Access:
	- From Local Network (HPCC* 192.168.50.x):
		- Access to bkcloud 16 node server
		- Access to KVM VM on bkcloud16 node server: ssh stack@192.168.122.75 (password: bkcloud)
	- From Public Network:
		- (Same way above to bkcloud16 node server)
		- Access to KVM VM on bkcloud16 node server: ssh stack@192.168.122.75 (password: bkcloud)
- Usage Info: 
	- Auth Script: /home/stack/devstack/admin.sh
	- OPS Admin username/password: admin/nhatbkk57 
	- Endpoint URL: http://192.168.122.75:35357/v3/
	- EC2-API Endpoint URL: http://192.168.122.75:8788
