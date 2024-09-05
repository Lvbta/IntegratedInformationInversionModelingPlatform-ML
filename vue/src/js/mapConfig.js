import TileArcGISRest from 'ol/source/TileArcGISRest'
import XYZ from 'ol/source/XYZ'
import { Tile as TileLayer } from 'ol/layer'
import WMTS from 'ol/source/WMTS'
import {get as getProjection } from 'ol/proj'
import { getWidth, getTopLeft } from 'ol/extent'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import Projection from 'ol/proj/Projection'

function createTDTWMTSLayer(url, layerName) {
    const epsg = 'EPSG:4326'
    const projection = getProjection(epsg)
    const projectionExtent = projection.getExtent()
    const size = getWidth(projectionExtent) / 256
    const length = 19
    const resolutions = new Array(length)
    const matrixIds = new Array(length)
    for (let i = 0; i < length; i += 1) {
        const pow = Math.pow(2, i)
        resolutions[i] = size / pow
        matrixIds[i] = i
    }
    const source = new WMTS({
        url: url,
        layer: layerName,
        style: 'default',
        matrixSet: 'c',
        format: 'tiles',
        wrapX: true,
        tileGrid: new WMTSTileGrid({
            origin: getTopLeft(projectionExtent),
            resolutions,
            matrixIds,
        }),
    })
    const layer = new TileLayer({
        source,
    })
    return layer
}

function constructSource(baseUrl, layerName) {
    var gridsetName = 'EPSG:4326'
    var gridNames = [
        'EPSG:4326:0',
        'EPSG:4326:1',
        'EPSG:4326:2',
        'EPSG:4326:3',
        'EPSG:4326:4',
        'EPSG:4326:5',
        'EPSG:4326:6',
        'EPSG:4326:7',
        'EPSG:4326:8',
        'EPSG:4326:9',
        'EPSG:4326:10',
        'EPSG:4326:11',
        'EPSG:4326:12',
        'EPSG:4326:13',
        'EPSG:4326:14',
        'EPSG:4326:15',
        'EPSG:4326:16',
        'EPSG:4326:17',
        'EPSG:4326:18',
        'EPSG:4326:19',
        'EPSG:4326:20',
        'EPSG:4326:21',
    ]
    var style = ''
    var format = 'image/png'
    var projection = new Projection({
        code: 'EPSG:4326',
        units: 'degrees',
        axisOrientation: 'neu',
    })
    var resolutions = [
        0.703125, 0.3515625, 0.17578125, 0.087890625, 0.0439453125, 0.02197265625, 0.010986328125, 0.0054931640625,
        0.00274658203125, 0.001373291015625, 6.866455078125e-4, 3.4332275390625e-4, 1.71661376953125e-4,
        8.58306884765625e-5, 4.291534423828125e-5, 2.1457672119140625e-5, 1.0728836059570312e-5, 5.364418029785156e-6,
        2.682209014892578e-6, 1.341104507446289e-6, 6.705522537231445e-7, 3.3527612686157227e-7,
    ]
    let baseParams = ['VERSION', 'LAYER', 'STYLE', 'TILEMATRIX', 'TILEMATRIXSET', 'SERVICE', 'FORMAT']

    let params = {
        VERSION: '1.0.0',
        LAYER: layerName,
        STYLE: style,
        TILEMATRIX: gridNames,
        TILEMATRIXSET: gridsetName,
        SERVICE: 'WMTS',
        FORMAT: format,
    }
    var url = baseUrl + '?'
    for (var param in params) {
        if (baseParams.indexOf(param.toUpperCase()) < 0) {
            url = url + param + '=' + params[param] + '&'
        }
    }
    url = url.slice(0, -1)
    let source = new WMTS({
        url: url,
        layer: params['LAYER'],
        matrixSet: params['TILEMATRIXSET'],
        format: params['FORMAT'],
        projection: projection,
        tileGrid: new WMTSTileGrid({
            tileSize: [256, 256],
            extent: [-180.0, -90.0, 180.0, 90.0],
            origin: [-180.0, 90.0],
            resolutions: resolutions,
            matrixIds: params['TILEMATRIX'],
        }),
        style: params['STYLE'],
        wrapX: true,
    })
    return source
}
//0表示天地图影像注记，1表示天地图影像,2表示使用Arcgis在线午夜蓝地图服务
var streetmap = function(maptype) {
    var maplayer = null
    let url = ''
    let layerName = ''
    switch (maptype) {
        case 0:
            url = 'http://t0.tianditu.gov.cn/cva_c/wmts?tk=3020b055a26ffadab076acc8c9641b40&service=wmts'
            layerName = 'cva'
            maplayer = createTDTWMTSLayer(url, layerName)
            break
        case 1:
            maplayer = new TileLayer({
                //天地图
                source: new XYZ({
                    url: 'http://t3.tianditu.com/DataServer?T=img_w&tk=7786923a385369346d56b966bb6ad62f&x={x}&y={y}&l={z}',
                }),
            })
            break
        case 2:
            //url="/server/geoserver/gwc/demo";
            url = 'http://localhost:8080/geoserver/gwc/service/wmts'
            layerName = 'cite:tb'
            maplayer = new TileLayer({
                source: constructSource(url, layerName),
            })
            break
        case 3:
            maplayer = new TileLayer({
                //source: new OSM()
                //光伏底图
                source: new XYZ({
                    url: 'http://localhost:8000/services/gf_road_test/tiles/{z}/{x}/{y}.jpg',
                }),
            })
            break
        case 4:
            maplayer = new TileLayer({
                //source: new OSM()
                //xbk底图
                source: new XYZ({
                    url: 'http://localhost:8000/services/test/tiles/{z}/{x}/{y}.jpg',
                }),
            })
            break
    }
    return maplayer
}
var mapconfig = {
    x: 114.3629946, //云中心点经度和纬度
    y: 29.32009325,
    //xbk中心
    //x: 120.0634,
    //y: 23.160563,
    zoom: 8, //地图缩放级别
    imageMap: streetmap(1),
    cavMap: streetmap(0),
    //tbMap: streetmap(2),
    gfTile: streetmap(3),
    xbkTile: streetmap(4),
}

export default mapconfig