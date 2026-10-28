from atlas_net.egress import validate_destination,validate_redirect
from common import emit, record
safe=validate_destination('https://updates.example.invalid/a',['203.0.113.9'],'203.0.113.9',allowed_hosts={'updates.example.invalid'},allowed_private={'203.0.113.9'})
rebind=validate_destination('https://updates.example.invalid/a',['203.0.113.9'],'127.0.0.1',allowed_hosts={'updates.example.invalid'})
redirect=validate_redirect('https://updates.example.invalid/a','http://169.254.169.254/latest',allowed_hosts={'updates.example.invalid'})
emit('module-09-egress.json',{'safe':record(safe),'rebind':record(rebind),'redirect':record(redirect)})
