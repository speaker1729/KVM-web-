import libvirt


def vm_start(conn, name):
    try:
        domain = conn.lookupByName(name)
        domain.create()
        message = f"{name} 启动成功 "
    except Exception as e:
        message = f"{name} 启动失败 "
        print(e)
    return message


def vm_suspend(conn, name):
    try:
        domain = conn.lookupByName(name)
        domain.suspend()
        message = f"{name} 暂停成功 "
    except Exception as e:
        message = f"{name} 暂停失败 "
        print(e)
    return message


def vm_resume(conn, name):
    try:
        domain = conn.lookupByName(name)
        domain.resume()
        message = f"{name} 重启成功 "
    except Exception as e:
        message = f"{name} 重启失败 "
        print(e)
    return message


def vm_destroy(conn, name):
    try:
        domain = conn.lookupByName(name)
        domain.destroy()
        message = f"{name} 关闭成功 "
    except Exception as e:
        message = f"{name} 关闭失败 "
        print(e)
    return message
