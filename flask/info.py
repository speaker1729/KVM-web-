# 前端样例 (create)
"""
{
    "operation":"create"
    "name":"test"
    "cpu":2
    "memory":2
    "disk":10
}
"""
# 前端样例 (delete)
"""
{
    "operation":"delete"
    "name":["test","VM1","VM2"]
}
"""
# 后端样例 (delete)
"""
{
    "message":"连接成功 磁盘删除成功 虚拟机{name} 删除成功 成功关闭连接 ",
    "status":"success"
}
"""
# 后端样例 (create)
"""
{
    "operation":"create",
    name: 'VM1',
    cpu: 2,
    memory: 8,
    disk: 250
}
"""
# 后端样例 (info)
"""
{
    "message": "连接成功 成功获取全部虚拟机状态 成功关闭连接 ",
    "status":"success",
    "VM":[
    {
      name: 'VM1',
      KVM_status: '运行中',
      cpu: 2,
      memory: 8,
      disk: 250,
      CPU_usage: "98%"
    },
    {
      name: 'VM2',
      KVM_status: '运行中',
      cpu: 2,
      memory: 8,
      disk: 250,
      CPU_usage: "97%"
    }
    ]
}
"""
# 后端样例 (hostInfo)
"""
{
    model:"name"
    cpu:"4"
    memory:"12GB"
    disk:"70GB"
    free_disk:"30GB"
    free_memory：“6G”
}
"""