import 'ol/ol.css';
import Draw from 'ol/interaction/Draw';
import Overlay from 'ol/Overlay';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';
import {LineString, Polygon} from 'ol/geom';
import {Vector as VectorSource} from 'ol/source';
import {Vector as VectorLayer} from 'ol/layer';
import {getArea, getLength} from 'ol/sphere';
import {unByKey} from 'ol/Observable';

var measure = function measure(map, type) {
    var source = new VectorSource();
    var vector = new VectorLayer({
        source: source,
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
    map.addLayer(vector);

    var sketch;
    var helpTooltipElement;
    var helpTooltip;
    var measureTooltipElement;
    var measureTooltip;
    var tooltips = [];

    var continuePolygonMsg = 'Click to continue drawing the polygon';
    var continueLineMsg = '单击以继续绘线';

    var pointerMoveHandler = function (evt) {
        if (evt.dragging) {
            return;
        }
        var helpMsg = '请单击开始绘制';
        if (sketch) {
            var geom = sketch.getGeometry();
            if (geom instanceof Polygon) {
                helpMsg = continuePolygonMsg;
            } else if (geom instanceof LineString) {
                helpMsg = continueLineMsg;
            }
        }
        helpTooltipElement.innerHTML = helpMsg;
        helpTooltip.setPosition(evt.coordinate);
        helpTooltipElement.classList.remove('hidden');
    };

    map.on('pointermove', pointerMoveHandler);
    map.getViewport().addEventListener('mouseout', function () {
        helpTooltipElement.classList.add('hidden');
    });

    var draw;

    var formatLength = function (line) {
        var sourceProj = map.getView().getProjection();
        var length = getLength(line, { projection: sourceProj });
        var output;
        if (length > 100) {
            output = Math.round((length / 1000) * 100) / 100 + ' ' + 'km';
        } else {
            output = Math.round(length * 100) / 100 + ' ' + 'm';
        }
        return output;
    };

    var formatArea = function (polygon) {
        var sourceProj = map.getView().getProjection();
        var area = getArea(polygon, { projection: sourceProj });
        var output;
        if (area > 10000) {
            output = Math.round((area / 1000000) * 100) / 100 + ' ' + 'km<sup>2</sup>';
        } else {
            output = Math.round(area * 100) / 100 + ' ' + 'm<sup>2</sup>';
        }
        return output;
    };

    function addInteraction() {
        draw = new Draw({
            source: source,
            type: type,
            style: new Style({
                fill: new Fill({
                    color: 'rgba(255, 255, 255, 0.2)',
                }),
                stroke: new Stroke({
                    color: 'rgba(59,185,239,.8)',
                    lineDash: [10, 10],
                    width: 2,
                }),
                image: new CircleStyle({
                    radius: 5,
                    stroke: new Stroke({
                        color: 'rgba(59,185,239,.8)',
                    }),
                    fill: new Fill({
                        color: 'rgba(59,185,239,.8)',
                    }),
                }),
            }),
        });
        map.addInteraction(draw);
        createMeasureTooltip();
        createHelpTooltip();

        var listener;
        draw.on('drawstart', function (evt) {
            sketch = evt.feature;
            var tooltipCoord = evt.coordinate;
            listener = sketch.getGeometry().on('change', function (evt) {
                var geom = evt.target;
                var output;
                if (geom instanceof Polygon) {
                    output = formatArea(geom);
                    tooltipCoord = geom.getInteriorPoint().getCoordinates();
                } else if (geom instanceof LineString) {
                    output = formatLength(geom);
                    tooltipCoord = geom.getLastCoordinate();
                }
                measureTooltipElement.innerHTML = output;
                measureTooltip.setPosition(tooltipCoord);
            });
        });

        draw.on('drawend', function () {
            measureTooltipElement.className = 'ol-tooltip ol-tooltip-static';
            measureTooltip.setOffset([0, -7]);
            tooltips.push(measureTooltip);  // Add tooltip to array
            sketch = null;
            measureTooltipElement = null;
            createMeasureTooltip();
            unByKey(listener);
            map.un('pointermove', pointerMoveHandler);
            map.removeInteraction(draw);
            helpTooltipElement.classList.add('hidden');
        });
    }

    function createHelpTooltip() {
        if (helpTooltipElement) {
            helpTooltipElement.parentNode.removeChild(helpTooltipElement);
        }
        helpTooltipElement = document.createElement('div');
        helpTooltipElement.className = 'ol-tooltip hidden';
        helpTooltip = new Overlay({
            element: helpTooltipElement,
            offset: [15, 0],
            positioning: 'center-left',
        });
        map.addOverlay(helpTooltip);
        tooltips.push(helpTooltip);  // Add tooltip to array
    }

    function createMeasureTooltip() {
        if (measureTooltipElement) {
            measureTooltipElement.parentNode.removeChild(measureTooltipElement);
        }
        measureTooltipElement = document.createElement('div');
        measureTooltipElement.className = 'ol-tooltip ol-tooltip-measure';
        measureTooltip = new Overlay({
            element: measureTooltipElement,
            offset: [0, -15],
            positioning: 'bottom-center',
        });
        map.addOverlay(measureTooltip);
        tooltips.push(measureTooltip);  // Add tooltip to array
    }

    addInteraction();

    return { source, vector, draw, tooltips };
};

export default measure;
