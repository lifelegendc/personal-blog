import multiprocessing

# 绑定的IP和端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = 'sync'

# 最大请求数
max_requests = 1000

# 超时时间
timeout = 30

# 日志级别
loglevel = 'info'
