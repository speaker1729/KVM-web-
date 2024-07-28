<template>
  <el-container style="height: 100vh; border: 1px solid #eee;">
    <el-header>云服务系统 - KVM虚拟机管理</el-header>
    <el-button class="host-info-btn" icon="el-icon-info"
               @click="showHostInfoDialog = true; fetchHostInfo();"></el-button>
    <el-dialog title="主机信息" :visible.sync="showHostInfoDialog" width="500px">
      <div v-if="hostInfo" class="host-info-content">
        <p>模型: {{ hostInfo.model }}</p>
        <p>CPU数量: {{ hostInfo.cpu }}</p>
        <p>内存大小: {{ hostInfo.memory }}</p>
        <p>空闲内存: {{ hostInfo.free_memory }}</p>
        <p>磁盘大小: {{ hostInfo.disk }}</p>
        <p>空闲磁盘: {{ hostInfo.free_disk }}</p>
      </div>
      <div v-else>
        暂无主机信息
      </div>
    </el-dialog>

    <el-main>
      <el-row :gutter="20">
        <!-- VM生命周期管理按钮 -->
        <el-col :span="4">
          <el-button type="primary" icon="el-icon-plus" @click="openCreateVMDialog">创建</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="danger" icon="el-icon-delete" @click="deleteVM">删除</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="success" icon="el-icon-caret-right" @click="startVM">启动</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="info" icon="el-icon-video-play" @click="shutdownVM">关闭</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="warning" icon="el-icon-video-pause" @click="suspendVM">暂停</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="success" icon="el-icon-refresh" @click="resumeVM">恢复</el-button>
        </el-col>
      </el-row>

      <!-- 配置选项表单 -->
      <el-dialog title="创建新的虚拟机" :visible.sync="showCreateVMDialog" width="350px">
        <el-form :model="newVM" label-width="120px">
          <el-form-item label="虚拟机名称">
            <el-input v-model="newVM.name"></el-input>
          </el-form-item>
          <el-form-item label="CPU数量">
            <el-input-number v-model="newVM.cpu" :min="1" :max="4"></el-input-number>
          </el-form-item>
          <el-form-item label="内存大小(GB)">
            <el-input-number v-model="newVM.memory" :min="1" :max="16"></el-input-number>
          </el-form-item>
          <el-form-item label="磁盘大小(GB)">
            <el-input-number v-model="newVM.disk" :min="1" :max="99"></el-input-number>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer" style="display: flex; justify-content: space-between;">
  <el-button @click="showCreateVMDialog = false">取消</el-button>
  <el-button type="primary" @click="createVM">确定</el-button>
</span>
      </el-dialog>

      <!--统计报告与监控-->
      <el-row>
        <el-col :span="24">
          <el-card>
            <div slot="header" class="clearfix">
              <span>虚拟机统计报告与监控</span>
            </div>
            <el-table :data="reportData" style="width: 100%" ref="multipleTable"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection" width="55"></el-table-column>
              <el-table-column prop="name" label="虚拟机名称"></el-table-column>
              <el-table-column prop="KVM_status" label="状态"></el-table-column>
              <el-table-column prop="cpu" label="CPU数量"></el-table-column>
              <el-table-column prop="memory" label="内存大小(GB)"></el-table-column>
              <el-table-column prop="disk" label="磁盘大小(GB)"></el-table-column>
              <el-table-column prop="CPU_usage" label="CPU使用率"></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>

      <el-col :span="3">
        <el-button type="primary" icon="el-icon-refresh-right" @click="get_reportData">刷新</el-button>
      </el-col>

      <!-- 错误处理与报警信息显示 -->
      <div v-for="alert in alerts" :key="alert.id">
        <el-alert
            :title="alert.msg"
            :type="alert.type === 'success' ? 'success' : 'error'"
            :icon="alert.type === 'success' ? 'el-icon-success' : 'el-icon-error'"
            show-icon>
        </el-alert>
      </div>
    </el-main>
    <el-footer>小组成员：李安南、罗成勇、戚正、肖江伟</el-footer>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VmManagement',
  data() {
    return {
      showCreateVMDialog: false,
      newVM: {
        name: '',
        cpu: 1,
        memory: 1,
        disk: 20
      },
      reportData: [],
      showHostInfoDialog: false,
      hostInfo: null,
      alertVisible: false,
      alerts: [], // 存储多个提示信息
      selectedVMs: [], // 存储被选中的虚拟机
    };
  },
  mounted() {
    this.get_reportData();
  },
  methods: {
    openCreateVMDialog() {
      this.showCreateVMDialog = true;
    },
    handleSelectionChange(val) {
      this.selectedVMs = val;
    },
    fetchHostInfo() {
      axios.get('http://localhost:5000/api/hostInfo') // 假设这是获取主机信息的后端URL
          .then(response => {
            if (response.data) {
              this.hostInfo = response.data; // 存储主机信息
            } else {
              this.showAlert('无法获取主机信息', 'error');
            }
          })
          .catch(error => {
            this.showAlert('请求错误: ' + error.message, 'error');
          });
    },
    get_reportData() {
      axios.get('http://localhost:5000/api/getInfo')
          .then(response => {
            console.log(response.data);
            if (response.data && response.data.status === 'success') {
              // 如果成功，清空原有数据并添加新数据
              this.reportData = response.data.VM.map(vm => ({
                name: vm.name,
                KVM_status: vm.KVM_status,
                cpu: vm.cpu,
                memory: vm.memory,
                disk: vm.disk,
                CPU_usage: vm.CPU_usage
              }));
            } else {
              // 如果后端返回失败
              this.showAlert('虚拟机信息获取失败', 'error');
            }
          })
          .catch(error => {
            // 网络或服务器错误
            this.showAlert('请求错误: ' + error.message, 'error');
          });
    },
    createVM() {
      // 检查虚拟机名称
      if (!this.newVM.name) {
        this.showAlert('请输入虚拟机名称', 'error');
        return;
      }
      // 检查虚拟机名称是否包含空格
      if (this.newVM.name.includes(' ')) {
        this.showAlert('虚拟机名称不能包含空格', 'error');
        return;
      }
      const vmExists = this.reportData.some(vm => vm.name === this.newVM.name);
      if (vmExists) {
        this.showAlert('虚拟机名称已存在，请选择一个不同的名称', 'error');
        return;
      }
      const vmData = {
        operation: "create",
        name: this.newVM.name,
        cpu: this.newVM.cpu,
        memory: this.newVM.memory,
        disk: this.newVM.disk
      };
      axios.post(`http://localhost:5000/api/vm`, vmData)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.showAlert(response.data.message, 'success');
              this.get_reportData(); // 调用 get_reportData 来刷新数据
            } else {
              this.showAlert(response.data.message, 'error');
            }
          })
          .catch(error => {
            this.showAlert('请求错误: ' + error.message, 'error');
          })
          .finally(() => {
            this.newVM.name = '';
            this.showCreateVMDialog = false;
          });
    },
    deleteVM() {
      this.performVMOperation('delete');
    },
    startVM() {
      this.performVMOperation('start');
    },
    shutdownVM() {
      this.performVMOperation('shutdown');
    },
    suspendVM() {
      this.performVMOperation('suspend');
    },
    resumeVM() {
      this.performVMOperation('resume');
    },
    performVMOperation(endpoint) {
      if (this.selectedVMs.length > 0) {
        this.selectedVMs.forEach(vm => {
          const vmData = {
            operation: endpoint,
            name: vm.name, // 现在是单个虚拟机的名称
          };

          axios.post(`http://localhost:5000/api/vm`, vmData)
              .then(response => {
                if (response.data && response.data.status === 'success') {
                  this.showAlert(response.data.message, 'success');
                } else {
                  this.showAlert(response.data.message, 'error');
                }
              })
              .catch(error => {
                this.showAlert('请求错误: ' + error.message, 'error');
              })
              .finally(() => {
                this.get_reportData(); // 在所有请求完成后刷新数据
              });
        });
      } else {
        this.showAlert('没有选中的虚拟机', 'error');
      }
    },
    showAlert(msg, type) {
      const alert = {
        id: Date.now(), // 生成唯一ID
        msg: msg,
        type: type,
      };
      this.alerts.push(alert);
      setTimeout(() => {
        this.alerts = this.alerts.filter(a => a.id !== alert.id);
      }, 6000); // 5秒后移除提示
    },
  },
}
</script>

<style>
.el-header {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 0 20px;
  line-height: 60px;
}

.el-footer {
  background-color: #333;
  color: white;
  text-align: center;
  line-height: 60px;
}

.el-main {
  background-color: #e9eef3;
  padding: 20px;
  overflow-y: auto; /* 添加滚动条 */
}

/* 扩展样式，确保内容区域占满剩余空间 */
.el-container {
  display: flex;
  flex-direction: column;
}

.el-main {
  flex: 1;
}

/* 表单和表格样式 */
.el-form-item {
  margin-bottom: 10px;
}

/* 报警信息样式 */
.el-alert {
  margin-bottom: 20px;
}

/* 使表单和按钮宽度一致 */
.el-form-item, .el-button {
  width: 100%;
}

/* 表格样式调整 */
.el-table {
  background-color: white;
}

/* 按钮间距 */
.el-button {
  margin: 0 10px 10px 0;
}

/* 适应所有屏幕尺寸 */
@media (max-width: 768px) {
  .el-form-item, .el-button {
    width: 100%;
  }
}

.host-info-content {
  font-size: 20px;
}

.host-info-btn {
  position: fixed;
  top: 10px;
  right: 5px;
  z-index: 100;
  font-size: 36px;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}
</style>