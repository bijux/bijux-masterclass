from atlas_net.models import Route
from atlas_net.routing import select_route,RouteError
from atlas_net.mtu import Encapsulation,effective_mtu,packet_fits
from common import emit
routes=[Route('0.0.0.0/0','192.0.2.1','eth0'),Route('10.244.1.0/24',None,'cni0')]
out=[]
for name,dst,size in [('route-defect','10.244.2.19',200),('route-defect-large','10.244.2.19',1450)]:
    try: r,c=select_route(dst,routes); out.append({'case':name,'ok':True,'route':r.prefix})
    except RouteError as e: out.append({'case':name,'ok':False,'firstFailure':'route-selection','error':str(e)})
mtu=effective_mtu(1500,[Encapsulation('vxlan',50),Encapsulation('encryption',32)])
for size in [200,1450]: out.append({'case':f'mtu-{size}','ok':packet_fits(size,mtu),'effectiveMtu':mtu,'firstFailure':None if packet_fits(size,mtu) else 'packet-delivery'})
emit('module-01-packet-path.json',{'cases':out})
