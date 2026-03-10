import React, { useState, useMemo, useEffect, useRef } from 'react';
import ReactECharts from 'echarts-for-react';
import './App.css';

function App() {
  const chartRef = useRef(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedData, setSelectedData] = useState(null);

  const [timeRange, setTimeRange] = useState('1m');
  const [startDate, setStartDate] = useState('');

  // 1. 数据生成：严格限制在 -30 到 70 之间
  const fullData = useMemo(() => {
    let base = new Date('2025-01-01');
    let dates = [];
    let values = [];
    let currVal = 20; 
    
    for (let i = 0; i < 365; i++) {
      dates.push(base.toISOString().split('T')[0]);
      
      let step = (Math.random() - 0.5) * 12; 
      currVal += step;
      
      if (currVal > 70) currVal = 70 - Math.random() * 5;
      if (currVal < -30) currVal = -30 + Math.random() * 5;
      
      values.push(Math.round(currVal));
      base.setDate(base.getDate() + 1);
    }
    return { dates, values };
  }, []);

  useEffect(() => {
    const defaultStart = new Date(fullData.dates[fullData.dates.length - 30]);
    setStartDate(defaultStart.toISOString().split('T')[0]);
  }, [fullData]);

  useEffect(() => {
    if (!chartRef.current || !startDate) return;
    const chartInstance = chartRef.current.getEchartsInstance();
    let startIndex = fullData.dates.indexOf(startDate);
    if (startIndex === -1) startIndex = 0;

    let rangeDays = { '7d': 7, '1m': 30, '3m': 90, '1y': 365 }[timeRange];
    let endIndex = Math.min(startIndex + rangeDays - 1, fullData.dates.length - 1);

    chartInstance.dispatchAction({
      type: 'dataZoom',
      startValue: fullData.dates[startIndex],
      endValue: fullData.dates[endIndex]
    });
  }, [startDate, timeRange, fullData]);

  const onDataZoom = (params) => {
    if (!chartRef.current) return;
    const chartInstance = chartRef.current.getEchartsInstance();
    const option = chartInstance.getOption();
    const startValueIndex = option.dataZoom[0].startValue;
    if (startValueIndex !== undefined && fullData.dates[startValueIndex]) {
      setStartDate(fullData.dates[startValueIndex]);
    }
  };

  // 2. 核心图表配置
  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross', label: { backgroundColor: '#1e293b' } } },
    
    // ⚠️ 关键修改：将 bottom 从 10% 提升到 18%，为底部的滑动条腾出足够的空间，防止和日期文字重叠
    grid: { left: '3%', right: '4%', bottom: '18%', top: '8%', containLabel: true },
    
    yAxis: {
      type: 'value', min: -30, max: 70,
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
      axisLabel: { color: '#94a3b8' }
    },
    
    xAxis: {
      type: 'category',
      data: fullData.dates,
      axisLine: { 
        onZero: true, 
        symbol: ['none', 'arrow'], 
        symbolSize: [10, 15],
        lineStyle: { color: '#ffffff', width: 2 } 
      },
      axisLabel: { color: '#94a3b8' }
    },

    // ⚠️ 关键修改：滑动条全面重构升级
    dataZoom: [
      { 
        type: 'slider', 
        bottom: 5, 
        height: 36, // 高度从 15 增加到 36，让全局缩略图清晰可见
        textStyle: { color: '#94a3b8' }, 
        borderColor: 'rgba(255, 255, 255, 0.05)', // 边框改成非常微弱的透明白
        fillerColor: 'rgba(14, 165, 233, 0.15)', // 选中区域的遮罩层改为淡蓝色
        
        // 全局缩略图：未选中部分的样式（暗淡背景）
        dataBackground: {
          lineStyle: { color: '#334155', width: 1 },
          areaStyle: { color: '#0f172a', opacity: 0.8 }
        },
        // 全局缩略图：选中部分的样式（高亮蓝线）
        selectedDataBackground: {
          lineStyle: { color: '#0ea5e9', width: 2 },
          areaStyle: { color: '#0ea5e9', opacity: 0.2 }
        },
        
        // 更换高级的 SVG 矢量手柄图标
        handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
          color: '#0ea5e9',
          shadowBlur: 4,
          shadowColor: 'rgba(0,0,0,0.5)',
          borderWidth: 0
        }
      },
      { 
        type: 'inside', 
        zoomOnMouseWheel: false, 
        moveOnMouseWheel: true   
      }
    ],

    visualMap: {
      show: false,
      pieces: [
        { gt: 0, lte: 70, color: '#0ea5e9' },
        { gte: -30, lte: 0, color: '#ef4444' }
      ]
    },

    series: [{
      name: '舆情指数',
      type: 'line',
      smooth: 0.3,
      symbolSize: 6,
      showSymbol: false,
      emphasis: { focus: 'series', showSymbol: true },
      lineStyle: { width: 3 },
      areaStyle: { opacity: 0.15 },
      
      markPoint: {
        symbol: 'pin',
        symbolSize: 50,
        label: { color: '#fff', fontSize: 10 },
        data: [
          { type: 'max', name: '正面极值', itemStyle: { color: '#0ea5e9' } },
          { type: 'min', name: '负面极值', itemStyle: { color: '#ef4444' } }
        ]
      },
      data: fullData.values
    }]
  };

  const onChartClick = (params) => {
    const date = params.componentType === 'markPoint' ? params.data.coord[0] : params.name;
    const value = params.componentType === 'markPoint' ? params.data.coord[1] : params.value;
    
    const isNegative = value < 0;
    setSelectedData({
      date: date,
      score: value,
      title: `${date} 舆情快报`,
      sentiment: isNegative ? '负面警报' : '正面趋势',
      color: isNegative ? '#ef4444' : '#0ea5e9',
      news: [
        { id: 1, title: isNegative ? '目标系统出现高危通报' : '重点技术方向监测到活跃动态', type: "核心新闻" },
        { id: 2, title: `开源社区讨论热度相比昨日变化 ${Math.abs(Math.round(value))}%`, type: "开源情报" }
      ]
    });
    setDrawerOpen(true);
  };

  return (
    <div className="app-root">
      <nav className="top-nav">
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <span style={{ fontSize: '1.4rem', fontWeight: '900', color: '#fff', letterSpacing: '1px' }}>
            <span style={{ color: '#0ea5e9' }}>OSINT</span> RADAR
          </span>
          <input className="search-bar" placeholder="检索目标、事件、关键字..." />
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#94a3b8', marginRight: '8px' }}>起始日:</span>
            <input 
              type="date" 
              className="control-input" 
              value={startDate} 
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#94a3b8', marginRight: '8px' }}>视距:</span>
            <select className="control-select" value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
              <option value="7d">近 7 天</option>
              <option value="1m">近 1 个月</option>
              <option value="3m">近 3 个月</option>
              <option value="1y">全年 (365天)</option>
            </select>
          </div>
        </div>
      </nav>

      <div className="dashboard-layout">
        <div className="macro-grid">
          <div className="macro-card">
            <div className="card-title">🚨 高危目标指数</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.2rem', fontWeight: 'bold' }}>
              <span style={{ color: '#ef4444' }}>US (-28)</span>
              <span style={{ color: '#ef4444' }}>RU (-12)</span>
              <span style={{ color: '#f59e0b' }}>JP (-5)</span>
            </div>
          </div>
          <div className="macro-card">
            <div className="card-title">📡 情报截获短报</div>
            <div style={{ color: '#0ea5e9', fontSize: '0.9rem', marginBottom: '5px' }}>● 南部基地卫星图像重构完成</div>
            <div style={{ color: '#f8fafc', fontSize: '0.9rem' }}>● 开源社区讨论热度上升 15%</div>
          </div>
          <div className="macro-card">
            <div className="card-title">🏷️ 高频敏感词</div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <span style={{ background: 'rgba(239,68,68,0.2)', color: '#ef4444', padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem' }}>#发射异常</span>
              <span style={{ background: 'rgba(14,165,233,0.2)', color: '#0ea5e9', padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem' }}>#数据解密</span>
            </div>
          </div>
        </div>

        <div className="chart-container">
          <ReactECharts 
            ref={chartRef}
            option={option} 
            style={{ height: '100%', width: '100%' }} 
            onEvents={{ 'click': onChartClick, 'datazoom': onDataZoom }}
          />
        </div>
      </div>

      <div className={`drawer ${drawerOpen ? 'open' : ''}`}>
        <button onClick={() => setDrawerOpen(false)} style={{ float: 'right', background: 'none', border: 'none', color: '#94a3b8', fontSize: '1.5rem', cursor: 'pointer' }}>✕</button>
        {selectedData && (
          <div>
            <h2 style={{ color: selectedData.color }}>情报下钻分析</h2>
            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '20px', borderRadius: '12px', margin: '20px 0', border: `1px solid ${selectedData.color}` }}>
              <div style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '10px' }}>时间节点：{selectedData.date}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                <div style={{ fontSize: '3rem', fontWeight: '900', color: selectedData.color }}>{selectedData.score}</div>
                <div>
                  <div style={{ color: '#f8fafc', fontWeight: 'bold' }}>{selectedData.sentiment}</div>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem' }}>复合算法计算结果</div>
                </div>
              </div>
            </div>
            
            <h4 style={{ color: '#f8fafc', marginBottom: '15px' }}>溯源新闻列表：</h4>
            {selectedData.news.map(n => (
              <div key={n.id} className="news-item" style={{ borderLeftColor: selectedData.color }}>
                <div style={{ fontWeight: 'bold', color: '#f8fafc' }}>{n.title}</div>
                <div style={{ fontSize: '0.8rem', marginTop: '8px', color: '#94a3b8' }}>
                  类型标签: <span style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px' }}>{n.type}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;