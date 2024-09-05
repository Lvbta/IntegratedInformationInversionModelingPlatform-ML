<template>
  <div>
    <div class="layerlist" ref="layerlist">
      <div class="layer-head">
        <div class="layer-title" @mousedown="headMousdown">
          <i class="iconfont icon-layers"></i> &nbsp;图层
        </div>
        <span class="iconfont icon-searchclose" title="关闭"></span>
        <h6 v-if="selectLayerName !== ''">
          你选择的图层是{{ selectLayerName }}
        </h6>
      </div>
      <div class="layer-body">
        <a-tree
          :treeData="treeData"
          :show-line="true"
          @select="selecetNodes"
          defaultExpandAll
          :autoExpandParent="true"
        >
          <template slot="custom" slot-scope="item">
            <!-- 如果是新节点 -->
            <span v-if="item.newItemType === '0'">
              <span class="node-title">{{ item.title }}</span>
              <div class="node-button">
                <span
                  class="iconfont icon-tianjiatuceng"
                  @click="openNewLayer(item)"
                  title="新建解译区域"
                ></span>
              </div>
            </span>
            <span v-else-if="item.newItemType === '2'">
              <span class="node-title">{{ item.title }}</span>
              <div class="node-button">
                <span
                  class="iconfont icon-xianshi"
                  :ref="item.id"
                  @click="toggleLayerShow(item)"
                  title="显示/隐藏"
                ></span>
                <!--                <span-->
                <!--                  class="iconfont icon-daolu1"-->
                <!--                  @click="addCenterLine(item)"-->
                <!--                  :ref=item.key-->
                <!--                  title="生成/隐藏中心线"-->
                <!--                  :style=centerLineDisabled-->
                <!--                ></span>-->
                <span
                  class="iconfont icon-dingwei"
                  @click="zoomLayers(item)"
                  title="定位"
                ></span>
              </div>
            </span>
          </template>
        </a-tree>
      </div>
      <!--      <div class="layer-footer">-->
      <!--        <div style="border-top: 2px #aaaaaa solid;padding: 10px">-->
      <!--          <span style="font-size: 14px">矢量-道路</span>-->
      <!--          <div class="node-button" style="right:20px">-->
      <!--                <span-->
      <!--                        class="iconfont icon-xianshi"-->
      <!--                        @click="toggleWMSLayerShow"-->
      <!--                        title="显示/隐藏"-->
      <!--            ></span>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </div>-->
    </div>
    <new-layer
      v-show="isNewLayerShow"
      :selectNodeitem="selectNodeitem"
      @closeNewLayer="closeNewLayer"
      @createLayer="addLayerNodes"
    ></new-layer>
  </div>
</template>

<script>
import newLayer from "./newLayer";
let treeData = [
  {
    id: 1,
    key: 1,
    newItemType: "0", // 该节点是否是新增节点
    title: "图层",
    depth: 1, // 该节点的层级
    scopedSlots: { title: "custom" }, // 自定义组件需要绑定
    children: [],
  },
];
export default {
  name: "layerList",
  data () {
    return {
      autoExpandParent: true,
      checkedKeys: ["0-1"],
      selectedKeys: [],
      treeData,
      isNewLayerShow: false,
      selectNodeitem: null,
      selectLayerName: "",
      groupIndex: 1,
    };
  },
  components: {
    newLayer,
  },
  props: {
    centerLineDisabled: String
  },
  watch: {
    centerLineDisabled (val, oldVal) {

    }
  },
  methods: {
    openNewLayer (item) {
      this.isNewLayerShow = true;
      this.selectNodeitem = item;
    },
    addLayerNodes (layer, item) {
      this.addlayer(layer);
      let newItem = {
        id: Math.ceil(Math.random() * 10000), // 避免和已有的id冲突
        key: Math.ceil(Math.random() * 10000), // 避免和已有的key冲突
        name: layer.layerName,
        newItemType: "2",
        title: layer.layerName,
        depth: item.depth + 1, // 如果需要添加顶级节点，值为0
        scopedSlots: { title: "custom" },
      };
      let index = this.treeData.indexOf(item.dataRef);
      this.treeData[index].children.push(newItem);
    },
    addlayer (layer) {
      this.$emit("addlayer", layer);
    },
    selecetNodes (keys, event) {
      let nodeType = event.node.dataRef.newItemType;
      if (nodeType === "2") {
        this.selectLayerName = event.node.dataRef.name;
        this.$emit("selectVectorLayerByNodes", event.node);
      }
    },
    headMousdown (e) {
      let x = e.pageX - this.$refs.layerlist.offsetLeft;
      let y = e.pageY - this.$refs.layerlist.offsetTop;
      let move = (e) => {
        this.$refs.layerlist.style.left = e.pageX - x + "px";
        this.$refs.layerlist.style.top = e.pageY - y + "px";
      };
      //鼠标移动，鼠标在页面的坐标减去鼠标在盒子内的坐标就是模态框的left top值
      document.addEventListener("mousemove", move);
      //鼠标弹起 鼠标移动事件移除
      document.addEventListener("mouseup", function () {
        document.removeEventListener("mousemove", move);
      });
    },
    toggleLayerShow (item) {
      this.$emit("toggleLayerShow", item.dataRef);
      let showSpan = this.$refs[item.id]
      //alert(showSpan.className)
      showSpan.className = (showSpan.className === "iconfont icon-yincang") ? "iconfont icon-xianshi" : "iconfont icon-yincang"
    },
    toggleWMSLayerShow () {
      this.$emit("toggleWMSLayerShow");
    },
    zoomLayers (item) {
      this.$emit("zoomLayers", item.dataRef);
    },
    closeNewLayer () {
      this.isNewLayerShow = false;
    },
    addCenterLine (item) {
      this.$emit("addCenterLine", item.name);
      let showCenter = this.$refs[item.key];
      showCenter.className = (showCenter.className === "iconfont icon-daolu1") ? "iconfont icon-daolu-xian" : "iconfont icon-daolu1";
    }
  },
};
</script>

<style >
/* li.ant-tree-treenode-switcher-open{
  left: 10px;
  top: 0px;
  width: 230px;
  padding: 5px 11px 5px 11px;
} */
.ant-tree-treenode-switcher-open {
  left: 10px;
}
.ant-tree-treenode-switcher-close {
  padding-left: 10px;
  left: 3px;
}
.ant-tree
  li
  .ant-tree-node-content-wrapper.ant-tree-node-content-wrapper-normal.ant-tree-title.node-button {
  right: 17px;
}
/* .ant-tree-treenode-switcher-close.node-button{
  right: 17px;
} */
.ant-tree-node-content-wrapper-open:hover {
  background: transparent;
}
.ant-tree.ant-tree-show-line li span.ant-tree-switcher.ant-tree-switcher-noop {
  color: rgb(251, 251, 251);
  background: transparent;
  top: 2px;
}
.ant-tree.ant-tree-show-line li span.ant-tree-switcher.ant-tree-switcher_open {
  color: rgb(251, 251, 251);
  background: transparent;
}
.ant-tree.ant-tree-show-line li span.ant-tree-switcher.ant-tree-switcher_close {
  color: rgb(251, 251, 251);
  background: transparent;
}
.ant-tree
  li
  .ant-tree-node-content-wrapper.ant-tree-node-content-wrapper-normal.ant-tree-node-selected {
  background-color: transparent;
}

.ant-tree
  li
  .ant-tree-node-content-wrapper.ant-tree-node-content-wrapper-nomal:hover {
  background: transparent;
}
.ant-tree li .ant-tree-node-content-wrapper:hover {
  background-color: rgb(198 231 255 / 80%);
}
.ant-tree-node-content-wrapper.ant-tree-node-content-wrapper-open.ant-tree-node-selected {
  background-color: transparent;
}
.ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected {
  background: transparent;
}
.ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected:hover {
  background: transparent;
}

.layerlist {
  position: fixed;
  right: 10px;
  top: 150px;
  width: 250px;
  background-color: rgba(13, 19, 26, 0.6);
  z-index: 9999;
  border: 1px solid rgba(32, 160, 255, 0.3);
  border-radius: 5px;
  color: #cecece;
}
.layer-head {
  position: relative;
  height: 45px;
  border-bottom: 1px solid rgba(32, 160, 255, 0.3);
  line-height: 40px;
  padding: 0 10px;
}
.layer-title {
  cursor: move;
}
.layer-head .layer-title {
  float: left;
}
.layer-head span {
  float: right;
}
.layer-head h6 {
  position: absolute;
  bottom: -38px;
  color: #aaaaaa;
}

.ant-tree-treenode-switcher-close {
  position: relative;
}

.node-title {
  color: #ffff;
}

.node-button {
  position: absolute;
  display: inline-block;
  right: 20px;
  color: #fefefe;
}

.node-button span {
  margin-left: 12px;
}
/* .node-button span:hover{
  color: #aaaaaa;
} */
</style>