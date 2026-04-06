<template>
  <div class="h-full flex flex-col space-y-4">
    <div class="flex items-end justify-between border-b pb-4">
      <div class="flex items-baseline space-x-4">
        <h1 class="text-2xl font-bold text-gray-800">エリア可視化</h1>
        <span class="text-sm text-gray-500 font-medium">東京都 渋谷区・新宿区周辺</span>
      </div>
      <div class="flex space-x-6">
        <div class="text-right">
          <p class="text-xs text-gray-400">総UU数</p>
          <p class="text-lg font-bold text-gray-700">48,212</p>
        </div>
        <div class="text-right">
          <p class="text-xs text-gray-400">マッチ率</p>
          <p class="text-lg font-bold text-blue-600">92.1%</p>
        </div>
      </div>
    </div>

    <div class="flex-1 flex space-x-6 overflow-hidden pb-4">
      
      <div class="flex-1 bg-slate-100 rounded-2xl border-2 border-gray-200 relative overflow-hidden shadow-inner">
        <div id="mapbox-container" class="absolute top-0 left-0 w-full h-full"></div>
        <canvas id="deck-canvas" class="absolute top-0 left-0 w-full h-full"></canvas>

        <div class="absolute bottom-4 left-4 bg-white/90 backdrop-blur px-3 py-2 rounded-lg shadow-sm border border-gray-200 z-10">
          <p class="text-[10px] text-gray-600 leading-tight">
            <span class="font-bold text-red-500">※プライバシー保護のため、</span><br>
            同一メッシュ3UU未満のエリアは非表示となっています。
          </p>
        </div>
      </div>

      <div class="w-80 space-y-6 overflow-y-auto pr-2">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 class="text-sm font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-2">⚙️</span>表示設定
          </h2>
          <div class="space-y-3">
            <label class="flex items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer border border-transparent hover:border-gray-100 transition">
              <input type="radio" name="viz-type" value="heatmap" v-model="layerType" class="w-4 h-4 text-blue-600">
              <span class="ml-3 text-sm font-medium text-gray-700">ヒートマップ</span>
            </label>
            <label class="flex items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer border border-transparent hover:border-gray-100 transition">
              <input type="radio" name="viz-type" value="hexagon" v-model="layerType" class="w-4 h-4 text-blue-600">
              <span class="ml-3 text-sm font-medium text-gray-700">メッシュ (Hexagon)</span>
            </label>
            <div class="pt-2 mt-2 border-t border-gray-100">
              <label class="flex items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition">
                <input type="checkbox" v-model="showPoi" class="w-4 h-4 rounded text-blue-600">
                <span class="ml-3 text-sm font-medium text-gray-700">POIピンマーカー</span>
              </label>
              <label class="flex items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition">
                <input type="checkbox" v-model="applyKAnonymity" class="w-4 h-4 rounded text-blue-600">
                <span class="ml-3 text-sm font-medium text-gray-700 font-bold text-blue-600">k-匿名化適用</span>
              </label>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 class="text-sm font-bold text-gray-800 mb-4">凡例</h2>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-4 h-4 rounded-full bg-red-500"></div>
                <span class="text-xs text-gray-600">高密度 (100+ UU)</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-4 h-4 rounded-full bg-orange-400"></div>
                <span class="text-xs text-gray-600">中密度 (50-99 UU)</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-4 h-4 rounded-full bg-yellow-300"></div>
                <span class="text-xs text-gray-600">低密度 (3-49 UU)</span>
              </div>
            </div>
            <div class="flex items-center space-x-3 opacity-50">
              <div class="w-4 h-4 rounded-full bg-gray-200 border border-gray-300 border-dashed"></div>
              <span class="text-xs text-gray-600">秘匿 (3UU未満)</span>
            </div>
            <div class="flex items-center space-x-3 pt-2">
              <div class="w-4 h-4 flex items-center justify-center text-[10px]">📍</div>
              <span class="text-xs text-gray-600">計測地点 (POI)</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { Deck } from '@deck.gl/core';
import { HeatmapLayer, HexagonLayer } from '@deck.gl/aggregation-layers';
import { ScatterplotLayer } from '@deck.gl/layers';
import axios from 'axios';

import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

let deckInstance = null;
let mapboxInstance = null;
const mapData = ref([]);

const layerType = ref('heatmap');
const showPoi = ref(true);
const applyKAnonymity = ref(true);

const renderLayers = () => {
  const layers = [];
  let activeData = mapData.value;
  if (applyKAnonymity.value) {
    activeData = mapData.value.filter(d => d.weight >= 3);
  }

  if (layerType.value === 'heatmap') {
    layers.push(
      new HeatmapLayer({
        id: 'heatmap-layer',
        data: activeData,
        getPosition: d => d.position,
        getWeight: d => d.weight,
        radiusPixels: 30,
        intensity: 1,
        threshold: 0.05
      })
    );
  } else if (layerType.value === 'hexagon') {
    layers.push(
      new HexagonLayer({
        id: 'hexagon-layer',
        data: activeData,
        getPosition: d => d.position,
        getWeight: d => d.weight,
        radius: 100,
        extruded: false,
        colorRange: [
          [1, 152, 189],
          [73, 227, 206],
          [216, 254, 181],
          [254, 237, 177],
          [254, 173, 84],
          [209, 55, 78]
        ]
      })
    );
  }

  if (showPoi.value) {
    layers.push(
      new ScatterplotLayer({
        id: 'poi-layer',
        data: [{ position: [139.7671, 35.6812] }],
        getPosition: d => d.position,
        getFillColor: [239, 68, 68, 255],
        getRadius: 150,
        stroked: true,
        getLineColor: [255, 255, 255, 255],
        lineWidthMinPixels: 2
      })
    );
  }

  return layers;
};

watch([layerType, showPoi, applyKAnonymity], () => {
  if (deckInstance) {
    deckInstance.setProps({ layers: renderLayers() });
  }
});

onMounted(async () => {
  const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;
  const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  try {
    const response = await axios.get(`${baseUrl}/api/map-data`);
    mapData.value = response.data.data;
    console.log('[API成功] 地図データの取得が完了しました');
  } catch (error) {
    console.error('[API失敗] 地図データの取得に失敗しました:', error);
    return;
  }

  mapboxInstance = new mapboxgl.Map({
    container: 'mapbox-container',
    // 変更点：Googleマップに近い Streets スタイルに変更
    style: 'mapbox://styles/mapbox/streets-v12',
    accessToken: MAPBOX_TOKEN,
    center: [139.7671, 35.6812],
    zoom: 12,
    pitch: 0,
    bearing: 0,
    interactive: false
  });

  // 変更点：地図の読み込み完了後、地域名のラベルを日本語に切り替える
  mapboxInstance.on('style.load', () => {
    console.log('[Mapbox] スタイル読み込み完了。日本語化を開始します');
    const layers = mapboxInstance.getStyle().layers;
    for (const layer of layers) {
      if (layer.type === 'symbol' && layer.layout && layer.layout['text-field']) {
        mapboxInstance.setLayoutProperty(layer.id, 'text-field', [
          'coalesce',
          ['get', 'name_ja'], // 日本語名を優先
          ['get', 'name']     // なければデフォルト名
        ]);
      }
    }
    console.log('[Mapbox] 地図の日本語化処理を適用しました');
  });

  deckInstance = new Deck({
    canvas: 'deck-canvas',
    initialViewState: {
      longitude: 139.7671,
      latitude: 35.6812,
      zoom: 12,
      pitch: 0,
      bearing: 0
    },
    controller: true,
    onViewStateChange: ({ viewState }) => {
      mapboxInstance.jumpTo({
        center: [viewState.longitude, viewState.latitude],
        zoom: viewState.zoom,
        bearing: viewState.bearing,
        pitch: viewState.pitch
      });
    },
    layers: renderLayers()
  });

  console.log('[deck.gl] エリア可視化の初期化が完了しました');
});

onUnmounted(() => {
  if (deckInstance) {
    deckInstance.finalize();
  }
  if (mapboxInstance) {
    mapboxInstance.remove();
  }
});
</script>