import libvirt
import time


def check_allow_size(conn, disk):
    pool_total_remain = check_remain_size(conn)
    disk_size = disk * 1024 * 1024 * 1024
    if disk_size > pool_total_remain:
        return True
    else:
        return False


def check_remain_size(conn):
    pool = conn.storagePoolLookupByName("default")
    pool_info = pool.info()
    pool_available = pool_info[3]

    volumes = pool.listVolumes()

    volume_real_size = 0
    for volume in volumes:
        vol = pool.storageVolLookupByName(volume)
        vol_info = vol.info()
        vol_size = vol_info[2]
        volume_real_size += vol_size

    volume_total_size = 0
    for volume in volumes:
        vol = pool.storageVolLookupByName(volume)
        vol_info = vol.info()
        vol_size = vol_info[1]
        volume_total_size += vol_size

    pool_total_remain = pool_available + volume_real_size - volume_total_size
    return pool_total_remain


def get_conn():
    # 打开qemu
    conn = libvirt.open("qemu:///system")

    if conn is None:
        message = "连接失败 "
    else:
        message = "连接成功 "
    return conn, message


def close_conn(conn):  # 关闭连接
    try:
        conn.close()
        message = "成功关闭连接 "
    except:
        message = "关闭连接失败 "
    return message


def show_vm(conn):
    vm = []
    domains = conn.listAllDomains()  # 获取所有虚拟机
    for domain in domains:
        detail = {}

        name = domain.name()
        detail["name"] = name

        state, _ = domain.state()
        KVM_status = "未知"
        if state == libvirt.VIR_DOMAIN_RUNNING:
            KVM_status = "运行中"
            CPU_usage = caclulate_CPU_usage(domain)
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            KVM_status = "已暂停"
            CPU_usage = "0%"
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            KVM_status = "已关机"
            CPU_usage = "0%"
        detail["KVM_status"] = KVM_status
        detail["CPU_usage"] = CPU_usage

        cpu = domain.info()[3]
        detail["cpu"] = cpu

        memory = domain.info()[2]//1024**2
        detail["memory"] = memory

        pool = conn.storagePoolLookupByName("default")
        vol = pool.storageVolLookupByName(f"{name}.qcow2")
        vol_info = vol.info()
        disk = vol_info[1]//1024**3
        detail["disk"] = disk

        vm.append(detail)

    return vm

def caclulate_CPU_usage(domain):
    # 获取虚拟机CPU使用率（需要两次获取状态间的时间差）
    cpu_time1 = domain.getCPUStats(True)[0]['cpu_time']
    time.sleep(1)  # 等待一秒
    cpu_time2 = domain.getCPUStats(True)[0]['cpu_time']
    cpu_usage = ((cpu_time2 - cpu_time1) / 1e9) * 100  # 将ns转换为秒并计算CPU使用率
    return f"{int(cpu_usage)}%"