# -*- coding: utf-8 -*-

# Gunicorn Configuration File (for unvicorn)
# Reference - http://docs.gunicorn.org/en/stable/configure.html
#
# To run gunicorn by using this config, run gunicorn by passing
# config file path, ex:
#
#       $ gunicorn --config=gunicorn.py MODULE_NAME:VARIABLE_NAME
#
import multiprocessing


# ===============================================
#           Server Socket
# ===============================================
# The server socket to bind
bind = "0.0.0.0:8081"

# backlog - The maximum number of pending connections
# Generally in range 64-2048
backlog = 2048


# ===============================================
#           Worker Processes
# ===============================================

# The number of worker threads for handling requests. This will
# run each worker with the specified number of threads.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
threads = 1

# The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
workers = multiprocessing.cpu_count() * 2 + 1

# worker_class - The type of workers to use
# A string referring to one of the following bundled classes:
# 1. sync
# 2. eventlet - Requires eventlet >= 0.9.7
# 3. gevent - Requires gevent >= 0.13
# 4. tornado - Requires tornado >= 0.2
#
# You’ll want to read http://docs.gunicorn.org/en/latest/design.html
# for information on when you might want to choose one of the other
# worker classes
worker_class = 'uvicorn.workers.UvicornWorker'

# worker_connections - The maximum number of simultaneous clients
# This setting only affects the Eventlet and Gevent worker types.
worker_connections = 1000

# max_requests - The maximum number of requests a worker will process
# before restarting
# Any value greater than zero will limit the number of requests a work
# will process before automatically restarting. This is a simple method
# to help limit the damage of memory leaks.
max_requests = 0

# max_requests_jitter - The maximum jitter to add to the max-requests setting
# The jitter causes the restart per worker to be randomized by
# randint(0, max_requests_jitter). This is intended to stagger worker
# restarts to avoid all workers restarting at the same time.
max_requests_jitter = 0

# timeout - Workers silent for more than this many seconds are killed
# and restarted
timeout = 30

# graceful_timeout - Timeout for graceful workers restart
# How max time worker can handle request after got restart signal.
# If the time is up worker will be force killed.
graceful_timeout = 30

# keep_alive - The number of seconds to wait for requests on a
# Keep-Alive connection
# Generally set in the 1-5 seconds range.
keep_alive = 2


# ===============================================
#           Debugging
# ===============================================

# check_config - Check the configuration
check_config = False

# reload - Restart workers when code changes
reload = True

# spew - Install a trace function that spews every line executed by the server
spew = False


# ===============================================
#           Logging
# ===============================================

# The Access log file to write to. “-” means log to stderr.
accesslog = None

# access_log_format - The access log format
#
# Identifier  |  Description
# ------------------------------------------------------------
# h          -> remote address
# l          -> ‘-‘
# u          -> currently ‘-‘, may be user name in future releases
# t          -> date of the request
# r          -> status line (e.g. GET / HTTP/1.1)
# s          -> status
# b          -> response length or ‘-‘
# f          -> referer
# a          -> user agent
# T          -> request time in seconds
# D          -> request time in microseconds
# L          -> request time in decimal seconds
# p          -> process ID
# {Header}i  -> request header
# {Header}o  -> response header
# ---------------------------------------------------------------
access_log_format = '%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s'

# The Error log file to write to. “-” means log to stderr.
errorlog = "-"

# loglevel - The granularity of Error log outputs.
# Valid level names are:
#   1. debug
#   2. info
#   3. warning
#   4. error
#   5. critical
loglevel = "debug"

# logger_class - The logger you want to use to log events in gunicorn.
# The default class (gunicorn.glogging.Logger) handle most of normal usages
# in logging. It provides error and access logging.
logger_class = "gunicorn.glogging.Logger"

# logconfig - The log config file to use. Gunicorn uses the standard Python
# logging module’s Configuration file format.
logconfig = None

# syslog_addr - Address to send syslog messages.
#
# Address is a string of the form:
# ‘unix://PATH#TYPE’ : for unix domain socket. TYPE can be ‘stream’ for the
#                      stream driver or ‘dgram’ for the dgram driver.
#                      ‘stream’ is the default.
# ‘udp://HOST:PORT’ : for UDP sockets
# ‘tcp://HOST:PORT‘ : for TCP sockets
syslog_addr = "udp://localhost:514"

# syslog - Send Gunicorn logs to syslog
syslog = False

# syslog_prefix - Makes gunicorn use the parameter as program-name in the
# syslog entries.
# All entries will be prefixed by gunicorn.<prefix>. By default the program
# name is the name of the process.
syslog_prefix = None

# syslog_facility - Syslog facility name
syslog_facility = "user"

# enable_stdio_inheritance - Enable stdio inheritance
# Enable inheritance for stdio file descriptors in daemon mode.
# Note: To disable the python stdout buffering, you can to set the user
# environment variable PYTHONUNBUFFERED .
enable_stdio_inheritance = False

# statsd_host - host:port of the statsd server to log to
statsd_host = None

# statsd_prefix - Prefix to use when emitting statsd metrics (a trailing . is
# added, if not provided)
# statsd_prefix = "."

# ===============================================
#           Process Naming
# ===============================================

# proc_name - A base to use with setproctitle for process naming.
# This affects things like `ps` and `top`.
# It defaults to ‘gunicorn’.
proc_name = None


# ===============================================
#           Security
# ===============================================

# limit_request_line - The maximum size of HTTP request line in bytes
# Value is a number from 0 (unlimited) to 8190.
# This parameter can be used to prevent any DDOS attack.
limit_request_line = 4094

# limit_request_fields - Limit the number of HTTP headers fields in a request
# This parameter is used to limit the number of headers in a request to
# prevent DDOS attack. Used with the limit_request_field_size it allows
# more safety.
# By default this value is 100 and can’t be larger than 32768.
limit_request_fields = 100

# limit_request_field_size - Limit the allowed size of an HTTP request
# header field.
# Value is a number from 0 (unlimited) to 8190.
limit_request_field_size = 8190


# ===============================================
#           Server Mechanics
# ===============================================

# preload_app - Load application code before the worker processes are forked
# By preloading an application you can save some RAM resources as well as
# speed up server boot times. Although, if you defer application loading to
# each worker process, you can reload your application code easily by
# restarting workers.
preload_app = False

# sendfile - Enables or disables the use of sendfile()
sendfile = True

# chdir - Chdir to specified directory before apps loading
chdir = ""

# daemon - Daemonize the Gunicorn process.
# Detaches the server from the controlling terminal and enters the background.
daemon = False

# raw_env - Set environment variable (key=value)
# Pass variables to the execution environment.
raw_env = []

# pidfile - A filename to use for the PID file
# If not set, no PID file will be written.
pidfile = None

# worker_tmp_dir - A directory to use for the worker heartbeat temporary file
# If not set, the default temporary directory will be used.
worker_tmp_dir = None

# user - Switch worker processes to run as this user
# A valid user id (as an integer) or the name of a user that can be retrieved
# with a call to pwd.getpwnam(value) or None to not change the worker process
# user
user = None

# group - Switch worker process to run as this group.
# A valid group id (as an integer) or the name of a user that can be retrieved
# with a call to pwd.getgrnam(value) or None to not change the worker
# processes group.
group = None

# umask - A bit mask for the file mode on files written by Gunicorn
# Note that this affects unix socket permissions.
# A valid value for the os.umask(mode) call or a string compatible with
# int(value, 0) (0 means Python guesses the base, so values like “0”, “0xFF”,
# “0022” are valid for decimal, hex, and octal representations)
umask = 0

# tmp_upload_dir - Directory to store temporary request data as they are read
# This path should be writable by the process permissions set for Gunicorn
# workers. If not specified, Gunicorn will choose a system generated temporary
# directory.
tmp_upload_dir = None

# secure_scheme_headers - A dictionary containing headers and values that the
# front-end proxy uses to indicate HTTPS requests. These tell gunicorn to set
# wsgi.url_scheme to “https”, so your application can tell that the request is
# secure.
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# forwarded_allow_ips - Front-end’s IPs from which allowed to handle set
# secure headers (comma separate)
# Set to “*” to disable checking of Front-end IPs (useful for setups where
# you don’t know in advance the IP address of Front-end, but you still trust
# the environment)
forwarded_allow_ips = "127.0.0.1"

# proxy_protocol - Enable detect PROXY protocol (PROXY mode).
# Allow using Http and Proxy together. It may be useful for work with stunnel
# as https frontend and gunicorn as http server.
# PROXY protocol: http://haproxy.1wt.eu/download/1.5/doc/proxy-protocol.txt
proxy_protocol = False

# proxy_allow_ips - Front-end’s IPs from which allowed accept proxy requests
# (comma separate)
# Set to “*” to disable checking of Front-end IPs (useful for setups where you
# don’t know in advance the IP address of Front-end, but you still trust the
# environment)
proxy_allow_ips = "127.0.0.1"


# ===============================================
#           SSL
# ===============================================

# keyfile - SSL Key file
keyfile = None

# certfile - SSL Certificate file
certfile = None

# ssl_version - SSL Version  to use (see stdlib ssl module’s)
ssl_version = 3

# cert_reqs - Whether client certificate is required (see stdlib ssl module’s)
cert_reqs = 0

# ca_certs - CA certificates file
ca_certs = None

# suppress_ragged_eofs - Suppress ragged EOFs (see stdlib ssl module’s)
suppress_ragged_eofs = True

# do_handshake_on_connect - Whether to perform SSL handshake on socket connect
# (see stdlib ssl module’s)
do_handshake_on_connect = False

# ciphers - Ciphers to use (see stdlib ssl module’s)
ciphers = "TLSv1"


# ===============================================
#           Server Hooks
# ===============================================

def on_starting(server):
    """
    Called just before the master process is initialized.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def on_reload(server):
    """
    Called to recycle workers during a reload via SIGHUP.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def when_ready(server):
    """
    Called just after the server is started.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def pre_fork(server, worker):
    """
    Called just before a worker is forked.

    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """
    pass


def post_fork(server, worker):
    """
    Called just after a worker has been forked.

    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """
    pass


def post_worker_init(worker):
    """
    Called just after a worker has initialized the application.

    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass


def worker_init(worker):
    """
    Called just after a worker exited on SIGINT or SIGQUIT.

    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass


def worker_abort(worker):
    """
    Called when a worker received the SIGABRT signal.
    This call generally happens on timeout.

    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass


def pre_exec(server):
    """
    Called just before a new master process is forked.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def pre_request(worker, req):
    """
    Called just before a worker processes the request.

    The callable needs to accept two instance variables for the Worker and
    the Request.
    """
    worker.log.debug("%s %s" % (req.method, req.path))


def post_request(worker, req, environ, resp):
    """
    Called after a worker processes the request.

    The callable needs to accept two instance variables for the Worker and
    the Request.
    """
    pass


def worker_exit(server, worker):
    """
    Called just after a worker has been exited.

    The callable needs to accept two instance variables for the Arbiter and
    the just-exited Worker.
    """
    pass


def nworkers_changed(server, new_value, old_value):
    """
    Called just after num_workers has been changed.

    The callable needs to accept an instance variable of the Arbiter and two
    integers of number of workers after and before change.

    If the number of workers is set for the first time, old_value would be
    None.
    """
    pass


def on_exit(server):
    """
    Called just before exiting gunicorn.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass
