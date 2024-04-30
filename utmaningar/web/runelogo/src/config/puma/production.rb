environment 'production'
pidfile '/tmp/puma.pid'
ctl_socket = '/tmp/pumactl.sock'
state_path '/tmp/puma.state'
quiet

threads 5, 5
workers 4

