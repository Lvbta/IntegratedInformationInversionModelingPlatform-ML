<template>
  <div id="map" ref="map">
    <LayerManage />

    <sidebar /> <!-- Add the sidebar component here -->
    <user />
    <tools @mapTools="mapTools" />
    <div class="spinContainer" ref="spinContainer">
      <div class="loadingicon"></div>
    </div>
  </div>
</template>

<script>
import LayerManage  from '../layer/LayerManage.vue'; 
import Sidebar from './Sidebar.vue'; 
import user from "./user";
import tools from "./tools";
import "ol/ol.css";
import { Map, View } from "ol";
import { Vector as VectorLayer } from 'ol/layer';
import { Vector as VectorSource } from 'ol/source';
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
import mapconfig from "../../js/mapConfig";
import measure from "../../js/measure";

export default {
  name: "olmap",
  components: {
    user,
    tools,
    Sidebar,
    LayerManage,
    
  },
  data() {
    return {
      map: null,
      measureInteraction: null,
      vectorLayer: null,
    };
  },
  mounted() {
    this.initializeMap();
  },
  methods: {
    initializeMap() {
      try {
        const mapContainer = this.$refs.map;
        const vectorSource = new VectorSource();
        this.vectorLayer = new VectorLayer({
          source: vectorSource,
          style: new Style({
            fill: new Fill({
              color: 'rgba(255, 255, 255, 0.2)',
            }),
            stroke: new Stroke({
              color: '#ffcc33',
              width: 2,
            }),
            image: new CircleStyle({
              radius: 7,
              fill: new Fill({
                color: '#ffcc33',
              }),
            }),
          }),
        });

        this.map = new Map({
          target: mapContainer,
          layers: [mapconfig.imageMap, this.vectorLayer],
          view: new View({
            projection: "EPSG:4326",
            center: [mapconfig.x, mapconfig.y],
            zoom: mapconfig.zoom,
          }),
        });
      } catch (error) {
        console.error("Error initializing map:", error);
      }
    },

    mapTools(targetment) {
      switch (targetment) {
        case "gohome":
          this.map.getView().setCenter([mapconfig.x, mapconfig.y]);
          this.map.getView().setZoom(mapconfig.zoom);
          break;
        case "zoomin":
          this.map.getView().animate({ zoom: this.map.getView().getZoom() + 1 });
          break;
        case "zoomout":
          this.map.getView().animate({ zoom: this.map.getView().getZoom() - 1 });
          break;
        case "celiang":
          if (this.measureInteraction) {
            this.map.removeInteraction(this.measureInteraction.draw);
          }
          this.measureInteraction = measure(this.map, "LineString");
          break;
        case "clearDrawings":
          const source = this.vectorLayer.getSource();
          source.clear();
          if (this.measureInteraction) {
            this.map.removeInteraction(this.measureInteraction.draw);
            this.measureInteraction.source.clear();
            this.map.removeLayer(this.measureInteraction.vector);
            this.measureInteraction.tooltips.forEach(tooltip => {
              this.map.removeOverlay(tooltip);
            });
            this.measureInteraction = null;
          }
          break;
      }
    },
  },
};
</script>

<style>
.loadingicon {
  margin: 32px auto 0px;
  width: 28px;
  height: 28px;
  background: url(../../assets/img/loading.png) no-repeat center center;
  background-size: 100% 100%;
  cursor: pointer;
  color: #cecece;
  transform: rotate(360deg);
  animation: rotation 3s linear infinite;
}

#map {
  position: relative;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.spinContainer {
  display: none;
  justify-content: center;
  align-items: center;
  position: absolute;
  width: 100%;
  height: 100%;
  text-align: center;
  color: #cecece;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99999999;
}
.hidden {
  display: none;
}
.ol-tooltip {
  position: relative;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  color: white;
  padding: 4px 8px;
  opacity: 0.7;
  white-space: nowrap;
  font-size: 12px;
}
.ol-tooltip-measure {
  opacity: 1;
  font-weight: bold;
}
.ol-tooltip-static {
  background-color: #ffcc33;
  color: black;
  border: 1px solid white;
}
.ol-tooltip-measure:before,
.ol-tooltip-static:before {
  border-top: 6px solid rgba(0, 0, 0, 0.5);
  border-right: 6px solid transparent;
  border-left: 6px solid transparent;
  content: "";
  position: absolute;
  bottom: -6px;
  margin-left: -7px;
  left: 50%;
}
.ol-tooltip-static:before {
  border-top-color: #ffcc33;
}
/*隐藏ol的一些自带元素*/
.ol-attribution,
.ol-zoom {
  display: none;
}
</style>
