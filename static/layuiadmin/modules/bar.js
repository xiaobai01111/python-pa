/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */;
layui.define(function (e) {
	layui.use(["admin", "carousel"], function () {
		var e = layui.$,
			t = (layui.admin, layui.carousel),
			a = layui.element,
			i = layui.device();
		e(".layadmin-carousel").each(function () {
			var a = e(this);
			t.render({
				elem: this,
				width: "100%",
				arrow: "none",
				interval: a.data("interval"),
				autoplay: a.data("autoplay") === !0,
				trigger: i.ios || i.android ? "click" : "hover",
				anim: a.data("anim")
			})
		}), a.render("progress")
	}), layui.use(["carousel", "echarts"], function () {
		var e = layui.$,
			$ = layui.jquery,
			a = (layui.carousel, layui.echarts),
			l = [],
			t = [{
				title: {
					text: "职位关键字分布概览",
					subtext: "热门技术栈统计",
					left: "center",
					top: 10,
					textStyle: {
						color: '#fff',
						fontSize: 18,
						fontFamily: 'Inter, sans-serif'
					},
					subtextStyle: {
						color: '#94a3b8'
					}
				},
				tooltip: {
					trigger: "axis",
					backgroundColor: 'rgba(255, 255, 255, 0.95)',
					borderColor: '#f1f5f9',
					borderWidth: 1,
					textStyle: { color: '#0f172a' },
					axisPointer: {
						type: 'line'
					}
				},
				grid: {
					left: '3%',
					right: '4%',
					bottom: '10%',
					top: '20%',
					containLabel: true
				},
				xAxis: [{
					type: "category",
					data: ['java', 'web', '测试', '前端', 'android', 'c', 'c语言', '后端', 'python', '大数据'],
					axisLine: {
						lineStyle: { color: '#94a3b8' }
					},
					axisLabel: {
						textStyle: {
							color: '#e2e8f0',
							fontSize: 14
						},
						interval: 0,
						rotate: 30
					},
					axisTick: { show: false },
					splitLine: { show: false }
				}],
				yAxis: [{
					type: "value",
					axisLine: { show: false },
					axisLabel: {
						textStyle: {
							color: '#e2e8f0',
							fontSize: 14
						}
					},
					splitLine: {
						lineStyle: {
							color: 'rgba(255, 255, 255, 0.08)',
							type: 'dashed'
						}
					}
				}],
				series: [{
					name: "职位数量",
					type: "line",
					smooth: true,
					symbol: 'circle',
					symbolSize: 8,
					data: [1197, 1153, 1127, 1059, 1037, 1033, 1031, 1022, 1016, 411],
					lineStyle: {
						width: 3,
						color: '#22d3ee'
					},
					itemStyle: {
						color: '#22d3ee',
						borderColor: '#fff',
						borderWidth: 2
					},
					areaStyle: {
						color: {
							type: 'linear',
							x: 0, y: 0, x2: 0, y2: 1,
							colorStops: [
								{ offset: 0, color: 'rgba(34, 211, 238, 0.4)' },
								{ offset: 1, color: 'rgba(34, 211, 238, 0.05)' }
							]
						}
					},
					label: {
						show: true,
						position: 'top',
						color: '#fff',
						fontSize: 11
					}
				}]
			}],
			i = e("#LAY-index-dataview").children("div"),
			n = function (e) {
				l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
			};
		$.ajax({
			type: 'GET',
			url: '/bar/',
			success: function (res) {
				if (res && res.bar_x && res.bar_x.length > 0) {
					t[0].xAxis[0].data = res.bar_x;
					t[0].series[0].data = res.bar_y;
					l[0].setOption(t[0]);
				}
			},
			error: function (response) {
				console.error("Failed to fetch chart data:", response);
			}
		});
		i[0] && n(0);

	}), e("bar", {})
});