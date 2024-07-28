<template>
  <div class="home">
    <el-menu
        default-active="1-4-1"
        class="el-menu-vertical-demo"
        background-color="#333"
    >
      <router-link :to="{ name: 'home' }">
        <el-menu-item index="1" class="menu-item-center">
          <i class="el-icon-s-home"></i>
        </el-menu-item>
      </router-link>
    </el-menu>
    <div class="center">
      <router-view></router-view>
    </div>
  </div>
</template>

<style>
.home {
  width: 100vw;
  height: 100vh;
  position: relative;
  display: flex;
  overflow: hidden;
}

.center {
  position: absolute;
  right: 0;
  top: 0;
  width: 95vw;
  height: 100%;
}

.el-menu-vertical-demo {
  box-sizing: border-box;
  width: 5vw;
  height: 100vh;
  z-index: 9;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.menu-item-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-menu-vertical-demo .el-menu-item.is-active {
  background-color: #000000;
}

.el-menu-item i {
  color: #FFF;
  font-size: 56px;
  font-weight: bold;
}
</style>