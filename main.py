import helper

# 1) Get the Tree ID
# ./provision_tree.sh example-config.sh
tree_id = 1087559795015764672

# 2) Get the IP address
# kubectl port-forward service/trillian-log-service 35791:8090
ip_address = '127.0.0.1:35791'

helper.addLogEntry(ip_address, tree_id, '12345678901')
