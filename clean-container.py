# -*-coding:Utf-8 -*

# import
from docker import Client
import datetime, sys



def showdetailcontainer(container_info):
    print ("Detail of the container %s : " % container_info['Names'][0].encode("ascii", "ignore"))
    print ("Created %s " % datetime.datetime.fromtimestamp(int(container_info['Created'])).strftime('%Y-%m-%d %H:%M:%S'))
    print ("Image Source: %s " % container_info['Image'].encode("ascii", "ignore") )
    print ("Status %s " % container_info['Status'])
    if not container_info['Mounts']:
        print ("None volumes mounted" )
    else: # 1 or more volumes mounted
        for containervolume in container_info['Mounts']:
            print ("Volume %s mounted at %s" % (containervolume['Name'].encode("ascii", "ignore"), containervolume['Destination'].encode("ascii", "ignore")))




def choosercontainers(listcontainerstoclean, thecontainer):
    print("\nClean the container: %s from %s %s" % (thecontainer['Names'][0].encode("ascii", "ignore"),thecontainer['Image'].encode("ascii", "ignore"), thecontainer['Status']))
    answertoclean = raw_input("(Y)es,(N)o,(D)etail the container: ")

    if answertoclean in ['y', 'Y', 'yes', 'Yes', 'YES']:
        print ("we will clean %s" % thecontainer['Names'][0].encode("ascii", "ignore"))
        listcontainerstoclean.append ({'Id' : acontainer['Id'].encode("ascii", "ignore"), 'Name' : acontainer['Names'][0].encode("ascii", "ignore")})
    elif answertoclean in ['n', 'N', 'no', 'No', 'NO']:
        print ("Next")
    elif answertoclean in ['d', 'D', 'detail', 'Detail', 'DETAIL']:
        showdetailcontainer(thecontainer)
        listcontainerstoclean = choosercontainers(listcontainerstoclean, thecontainer)
    else:
        print("\nFat finger detected, try again")
        listcontainerstoclean = choosercontainers(listcontainerstoclean, thecontainer)

    return listcontainerstoclean





def confirmanswer():
    answertoclean = raw_input("\nConfirm deletion of these containers (Y/N): ")

    if answertoclean in ['y', 'Y', 'yes', 'Yes', 'YES']:
        print ("\nYeahh, Kill 'Em All !!!\n")
        return 1
    elif answertoclean in ['n', 'N', 'no', 'No', 'NO']:
        print ("\nMission aborted\n")
        return 0
    else:
        print("\nFat finger detected, try again\n")
        return confirmanswer()

    return 0





#connect to local docker
dockercli = Client(base_url='unix://var/run/docker.sock')

# the list of the container to delete, will look like
containers_to_clean = []

print ("\nChoose which containers to clean:")
#
myfilter = dict(status="exited") # filter existed containers
stoppedcontainers = dockercli.containers(all=1,filters=myfilter) # all existed containers

for acontainer in stoppedcontainers:
    containers_to_clean = choosercontainers(containers_to_clean, acontainer)


#no container selected, exit
if not containers_to_clean:
    print ("\nReally ?????\n")
    sys.exit(1)


# show the containers selected
print ("\nWe will delete: ")
for bcontainer in containers_to_clean:
    print bcontainer["Name"]

# ask confirm before delete
if confirmanswer() == 1:
    for ccontainer in containers_to_clean:
        print ("Kill container %s "% ccontainer["Name"])
        dockercli.remove_container(ccontainer["Id"])
    sys.exit(0)
else:
    print ("\nI waste my time with you ....\n")
    sys.exit(1)

# Memo
#
# [{u'Status': u'Exited (130) 5 weeks ago',
#  u'Created': 1468257527,
#   u'Image': u'sgendrot/blogpro:0.1',
#    u'Labels': {},
#    u'NetworkSettings': {u'Networks':
#    {u'bridge': {u'NetworkID': u'', u'MacAddress': u'',
#    u'GlobalIPv6PrefixLen': 0, u'Links': None, u'GlobalIPv6Address': u'',
#     u'IPv6Gateway': u'', u'IPAMConfig': None, u'EndpointID': u'', u'IPPrefixLen': 0,
#      u'IPAddress': u'', u'Gateway': u'', u'Aliases': None}}},
#       u'HostConfig': {u'NetworkMode': u'default'},
#       u'ImageID': u'sha256:4141d115adfa0d069368ae7c3588a07a0bcdda72de8209f2eef5318ac9d6de70',
#        u'State': u'exited', u'Command': u'bash', u'Names': [u'/WP2'], u'Mounts':
#         [{u'RW': True, u'Name': u'www', u'Propagation': u'rprivate', u'Destination':
#  u'/var/www', u'Driver': u'local', u'Source': u'/var/lib/docker/volumes/www/_data', u'Mode': u'z'}],
#   u'Id': u'478e4df7bb93643cacda19fe2ef57565ea197b7b61bf6d616292f281766d5b6f', u'Ports': []}]
