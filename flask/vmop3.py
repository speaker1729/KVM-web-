import vmop1

# 定义ISO镜像文件路径
iso = "/home/lan/CentOS-7-x86_64-DVD-2009.iso"


def vm_check(conn, memory, cpu, disk):  # 主机信息
    node_info = conn.getInfo()  # 获取虚拟化主机信息

    memory_max = node_info[1] // 1024
    if memory > memory_max:
        message = "内存过载 "
        return False, message

    cpu_max = node_info[2]
    if cpu > cpu_max:
        message = "CPU过载 "
        return False, message

    if vmop1.check_allow_size(conn, disk):
        message = "磁盘过载 "
        return False, message

    message = "硬件申请成功 "
    return True, message


def vm_create_with_check(conn, name, memory, cpu, disk):
    check, message = vm_check(conn, memory, cpu, disk)
    if check:
        message += vm_create(conn, name, memory, cpu, disk)
    else:
        message += "硬件资源不足 创建虚拟机失败 "
    return message


def vm_create(conn, name, memory, cpu, disk):
    # 创建磁盘
    message, fault = create_img(conn, name, disk)

    try:
        # 检查磁盘
        if fault:
            raise ValueError("disk not found")
        # 创建虚拟机
        xml_desc = \
            f'''
            <domain type='kvm'>
            <name>{name}</name>
            <memory unit='G'>{memory}</memory>
            <vcpu placement='static'>{cpu}</vcpu>
            <os>
                <type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
            </os>
            <features>
                <acpi/>
                <apic/>
            </features>
            <cpu mode='custom' match='exact' check='partial'>
                <model fallback='allow'>Broadwell-noTSX-IBRS</model>
                <feature policy='require' name='md-clear'/>
                <feature policy='require' name='spec-ctrl'/>
                <feature policy='require' name='ssbd'/>
            </cpu>
            <clock offset='utc'>
                <timer name='rtc' tickpolicy='catchup'/>
                <timer name='pit' tickpolicy='delay'/>
                <timer name='hpet' present='no'/>
            </clock>
            <on_poweroff>destroy</on_poweroff>
            <on_reboot>restart</on_reboot>
            <on_crash>destroy</on_crash>
            <pm>
                <suspend-to-mem enabled='no'/>
                <suspend-to-disk enabled='no'/>
            </pm>
            <devices>
                <emulator>/usr/libexec/qemu-kvm</emulator>
                <disk type='file' device='disk'>
                    <driver name='qemu' type='qcow2'/>
                    <source file='/var/lib/libvirt/images/{name}.qcow2'/>
                    <target dev='hda' bus='ide'/>
                    <boot order='1'/>
                    <address type='drive' controller='0' bus='0' target='0' unit='0'/>
                </disk>
                <disk type='file' device='cdrom'>
                    <driver name='qemu' type='raw'/>
                    <source file='{iso}'/>
                    <target dev='hdb' bus='ide'/>
                    <readonly/>
                    <boot order='2'/>
                    <address type='drive' controller='0' bus='0' target='0' unit='1'/>
                </disk>
                <controller type='usb' index='0' model='ich9-ehci1'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
                </controller>
                <controller type='usb' index='0' model='ich9-uhci1'>
                    <master startport='0'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0' multifunction='on'/>
                </controller>
                <controller type='usb' index='0' model='ich9-uhci2'>
                    <master startport='2'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x1'/>
                </controller>
                <controller type='usb' index='0' model='ich9-uhci3'>
                    <master startport='4'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x2'/>
                </controller>
                <controller type='pci' index='0' model='pci-root'/>
                <controller type='ide' index='0'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
                </controller>
                <controller type='virtio-serial' index='0'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
                </controller>
                <interface type='network'>
                    <mac address='52:54:00:ee:f2:ad'/>
                    <source network='default'/>
                    <model type='rtl8139'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                </interface>
                <serial type='pty'>
                    <target type='isa-serial' port='0'>
                        <model name='isa-serial'/>
                    </target>
                </serial>
                <console type='pty'>
                    <target type='serial' port='0'/>
                </console>
                <channel type='spicevmc'>
                    <target type='virtio' name='com.redhat.spice.0'/>
                    <address type='virtio-serial' controller='0' bus='0' port='1'/>
                </channel>
                <input type='mouse' bus='ps2'/>
                <input type='keyboard' bus='ps2'/>
                <graphics type='spice' autoport='yes'>
                    <listen type='address'/>
                    <image compression='off'/>
                </graphics>
                <sound model='ich6'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                </sound>
                <video>
                    <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1' primary='yes'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
                </video>
                <redirdev bus='usb' type='spicevmc'>
                    <address type='usb' bus='0' port='1'/>
                </redirdev>
                <redirdev bus='usb' type='spicevmc'>
                    <address type='usb' bus='0' port='2'/>
                </redirdev>
                <memballoon model='virtio'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
                </memballoon>
            </devices>
        </domain>
        '''

        conn.defineXML(xml_desc)
        message += "创建虚拟机成功 "
    except Exception as e:
        message = '创建虚拟机失败 '
        print(e)

    return message


def create_img(conn, name, size):
    try:
        pool = conn.storagePoolLookupByName('default')
        vol_xml = f"""
                <volume type='file'>
                  <name>{name}.qcow2</name>
                  <capacity unit='G'>{size}</capacity>
                  <allocation unit='G'>{size}</allocation>
                  <target>
                    <format type='qcow2'/>
                  </target>
                </volume>
        """
        vol = pool.createXML(vol_xml, 0)
        message = '磁盘创建成功 '
        fault = False
    except Exception as e:
        message = '磁盘创建失败 '
        fault = True
        print(e)
    return message, fault


def vm_delete(conn, name):
    dom = conn.lookupByName(name)
    message, fault = delete_img(conn, name)
    try:
        if fault:
            raise ValueError("disk not found")
        dom.undefine()
        message += f"虚拟机{name} 删除成功 "
    except Exception as e:
        message = f"虚拟机{name} 删除失败 "
        print(e)
    return message


def delete_img(conn, name):
    try:
        pool = conn.storagePoolLookupByName("default")
        vol = pool.storageVolLookupByName(f"{name}.qcow2")
        vol.delete(0)
        message = "磁盘删除成功 "
        fault = False
    except Exception as e:
        message = '磁盘删除失败 '
        fault = True
        print(e)
    return message, fault
