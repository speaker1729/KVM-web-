import libvirt

import os
import psutil

import vmop1
import vmop2
import vmop3


def operation_bus(operation, arg):
    """
    接受命令和参数表的命令执行总线
    :param operation: 从json解析出的操作 str
    :param arg: 从json解析出的含相关参数字典 dict[str:object]
    :return: 符合后端样例的操作结果
    """
    conn, message = vmop1.get_conn()
    # 后端发回
    data = {}
    # 执行操作
    if conn:
        if operation == "create":
            message += vmop3.vm_create_with_check(conn, arg["name"], arg["memory"], arg["cpu"], arg["disk"])
            data["name"] = arg["name"]
            data["cpu"] = arg["cpu"]
            data["memory"] = arg["memory"]
            data["disk"] = arg["disk"]
        elif operation == "delete":
            message += vmop3.vm_delete(conn, arg["name"])
        elif operation == "start":
            message += vmop2.vm_start(conn, arg["name"])
        elif operation == "suspend":
            message += vmop2.vm_suspend(conn, arg["name"])
        elif operation == "resume":
            message += vmop2.vm_resume(conn, arg["name"])
        elif operation == "shutdown":
            message += vmop2.vm_destroy(conn, arg["name"])
        else:
            message += "未知命令 "

    message += vmop1.close_conn(conn)

    data["message"] = message
    data["status"] = message_check(message)
    return data


def get_all_vm_info():
    conn, message = vmop1.get_conn()
    # 后端发回
    data = {}
    # 执行操作
    try:
        VM = vmop1.show_vm(conn)
        message += "成功获取全部虚拟机 "
    except Exception as e:
        VM = []
        message += "获取全部虚拟机失败 "
        print(e)

    message += vmop1.close_conn(conn)

    data["message"] = message
    data["status"] = message_check(message)
    data["VM"] = VM
    return data


def message_check(message):
    if "失败" in message:
        return "error"
    else:
        return "success"


def get_host_info():  # 主机信息
    conn, message = vmop1.get_conn()
    # 后端发回
    data = {}
    # 执行操作
    nodeInfo = conn.getInfo()  # 获取虚拟化主机信息
    data["model"] = str(nodeInfo[0])
    data["cpu"] = str(nodeInfo[2])
    data["memory"] = f"{nodeInfo[1]//1024} GB"
    # 获取内存信息
    memory_info = psutil.virtual_memory()
    # 获取空闲内存大小
    mem = memory_info.available
    data["free_memory"] = f"{mem/1024**3:.1f} GB"  # 主机空闲内存

    partitions = os.statvfs("/")
    total_size = partitions.f_frsize * partitions.f_blocks
    data["disk"] = f"{total_size / (1024 ** 3):.2f} GB"

    data["free_disk"] = f"{vmop1.check_remain_size(conn)//1024**3} GB"  # 主机理论磁盘空闲

    message += vmop1.close_conn(conn)
    return data


if __name__ == '__main__':
    # 打开qemu
    conn, message = vmop1.get_conn()

    print(get_host_info())

    vmop1.close_conn(conn)

