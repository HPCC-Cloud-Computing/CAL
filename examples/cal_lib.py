"""
Cloud Abstract Layer (CAL) Library Examples
This script shows the basic use of the CAL as a library.
"""
import logging

# from cal.lib import client

LOG = logging.getLogger('')

_VERSION = '1.0.0'
_RESOURCES = ['network', 'compute']
_PROVIDER = 'OpenStack'


def run():
    """Run the examples"""

    # NOTE(kiennt): Until now, this example isn't finished yet,
    #               because we don't have any completed driver

    # Get a network client with openstack driver.

    # network_client = client.Client(version=_VERSION,
    #                                resource=_RESOURCES[0],
    #                                provider=_PROVIDER)

    # LOG.debug('Init network client(Id of instance: {}) \
    #           with default config' . format(id(network_client)))

    # Create simple network in OpenStack Cloud Host.
    # network_client.create(name, cidr, **kwargs)
    # List all network in OpenStack Cloud Host.
    # net = network_client.list()
    # print('List all network:')
    # TODO(kiennt): Wait to know the format of
    #               that list to show and get
    #               the nearest created network.

    # Show network info with specific id which got from prev.
    # net = network_client.show()

    # Get a compute client with openstack driver.

    # compute_client = client.Client(version=_VERSION,
    #                                resource=_RESOURCES[1],
    #                                provider=_PROVIDER)

    # Create VM.
    # new_vm = compute_client.create_vm(*args, **kwargs)
    # List all VM.
    # vms = compute_client.list_vm(*args, **kwargs)
    # TODO(kiennt): Print ids.
    # Show usage resource.


if __name__ == "__main__":
    run()
