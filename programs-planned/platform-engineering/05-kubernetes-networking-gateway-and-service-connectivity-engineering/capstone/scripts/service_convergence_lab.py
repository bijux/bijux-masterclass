from atlas_net.models import Endpoint
from atlas_net.services import ProgrammedService
from common import emit
e1=Endpoint('10.244.1.10',8080,'api-a','node-a','zone-a'); e2=Endpoint('10.244.2.10',8080,'api-b','node-b','zone-b')
plane=ProgrammedService(2,{'node-a':2,'node-b':2,'node-c':1},{1:(e1,e2),2:(e1,)})
before={n:[e.pod for e in plane.endpoints_for_node(n)] for n in plane.programmed_by_node}; plane.program('node-c',2)
after={n:[e.pod for e in plane.endpoints_for_node(n)] for n in plane.programmed_by_node}
emit('module-03-service-convergence.json',{'desiredGeneration':2,'before':before,'after':after,'staleNode':'node-c'})
