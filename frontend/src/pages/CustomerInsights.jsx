import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { API_BASE_URL } from '../config.js';

const FILTER_OPTIONS = [
  'YTD', 'MTD', 'Weekly', 'Daily', 'Monthly', 'Yesterday', 'Today', 'custom'
];

export default function Customer_Insight() {
  const [data, setData]       = useState({ metrics: [], charts: [] });
  const [loading, setLoading] = useState(true);
  const [filter, setFilter]   = useState(() => localStorage.getItem('customer_filter') || 'YTD');
  const [start, setStart]     = useState(() => localStorage.getItem('customer_start') || '');
  const [end, setEnd]         = useState(() => localStorage.getItem('customer_end') || '');

  useEffect(() => {
    fetchData();
  }, [filter, start, end]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = { filter_type: filter };
      if (filter === 'custom' && start && end) {
        params.start = start;
        params.end   = end;
      }

      const res = await axios.get(`${API_BASE_URL}/api/customer-insights`, { params });
      setData(res.data);
    } catch (err) {
      console.error('Error fetching customer insights data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (value) => {
    setFilter(value);
    localStorage.setItem('customer_filter', value);

    if (value !== 'custom') {
      setStart('');
      setEnd('');
      localStorage.removeItem('customer_start');
      localStorage.removeItem('customer_end');
    }
  };

  const handleStartChange = (value) => {
    setStart(value);
    localStorage.setItem('customer_start', value);
  };

  const handleEndChange = (value) => {
    setEnd(value);
    localStorage.setItem('customer_end', value);
  };

  const buildPieOption = (chart) => ({
    title: {
      text: chart.title,
      left: 'center',
      textStyle: { color: '#fff' }
    },
    tooltip: { trigger: 'item', formatter: '{b}: {c}' },
    legend: {
      bottom: 10,
      textStyle: { color: '#fff' },
      data: chart.data.map(d => d.name)
    },
    series: [{
      name: chart.title,
      type: 'pie',
      radius: ['40%', '70%'],
      label: { formatter: '{b}: {d}%' },
      data: chart.data.map(d => ({ name: d.name, value: d.value }))
    }],
    backgroundColor: '#111827'
  });

  const buildBarOption = (chart) => ({
    title: {
      text: chart.title,
      left: 'center',
      textStyle: { color: '#fff' }
    },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: chart.x,
      axisLabel: { color: '#fff', rotate: 20 }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#fff' }
    },
    series: [{
      data: chart.y,
      type: 'bar',
      barWidth: '50%',
      itemStyle: { color: '#3B82F6' },
      label: { show: true, position: 'top', color: '#fff' }
    }],
    backgroundColor: '#111827'
  });

  if (loading) {
    return <div className="text-white p-8">Loading…</div>;
  }

  return (
    <div className="p-8 space-y-6">
      {/* Filter controls */}
      <div className="flex items-center space-x-4">
        <select
          value={filter}
          onChange={e => handleFilterChange(e.target.value)}
          className="bg-[#1f2937] text-white border border-gray-600 rounded px-3 py-2"
        >
          {FILTER_OPTIONS.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>

        {filter === 'custom' && (
          <>
            <input
              type="date"
              value={start}
              onChange={e => handleStartChange(e.target.value)}
              className="bg-[#1f2937] text-white border border-gray-600 rounded px-2 py-1"
            />
            <span className="text-white">to</span>
            <input
              type="date"
              value={end}
              onChange={e => handleEndChange(e.target.value)}
              className="bg-[#1f2937] text-white border border-gray-600 rounded px-2 py-1"
            />
          </>
        )}
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-5">
        {data.metrics.map((m, i) => (
          <div
            key={i}
            className="bg-[#111827] p-6 rounded-lg min-h-[140px] flex flex-col justify-center"
          >
            <div className="text-gray-400 text-sm mb-2">{m.title}</div>
            <div className="text-white text-3xl font-semibold">{m.value}</div>
            {m.diff !== undefined && (
              <div className={`text-sm mt-2 ${m.diff >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {m.diff >= 0 ? '+' : ''}{m.diff}% vs previous
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {data.charts.map((chart, idx) => (
          <div key={idx} className="bg-[#111827] p-4 rounded-lg">
            {chart.type === 'pie' && (
              <ReactECharts option={buildPieOption(chart)} style={{ height: 350 }} />
            )}
            {chart.type === 'bar' && (
              <ReactECharts option={buildBarOption(chart)} style={{ height: 350 }} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
