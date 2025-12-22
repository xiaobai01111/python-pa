/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */ ;
layui.define(function(e) {
	layui.use(["admin", "carousel"], function() {
		var e = layui.$,
			t = (layui.admin, layui.carousel),
			a = layui.element,
			i = layui.device();
		e(".layadmin-carousel").each(function() {
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
	}), layui.use(["carousel", "echarts"], function() {
		var e = layui.$,
			$ = layui.jquery,
			a = (layui.carousel, layui.echarts),
			l = [],
			t = [{
				title: {
					text: "薪资分布概览",
					left: "center",
					top: 20,
					textStyle: {
						color: '#e2e8f0',
						fontSize: 18,
						fontFamily: 'Inter, sans-serif'
					}
				},
				tooltip: {
					trigger: "item",
					backgroundColor: 'rgba(255, 255, 255, 0.95)',
					borderColor: '#f1f5f9',
					borderWidth: 1,
					textStyle: { color: '#334155' },
					formatter: "{b} : {c} ({d}%)"
				},
				color: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#6366f1'],
				series: [{
					name: "薪资待遇",
					type: "pie",
					radius: ["40%", "70%"],
					center: ["50%", "55%"],
					itemStyle: {
						borderRadius: 8,
						borderColor: 'rgba(30, 41, 59, 0.7)',
						borderWidth: 2
					},
					label: {
						show: true,
						color: '#94a3b8',
						formatter: '{b}\n{d}%',
						fontSize: 14
					},
					labelLine: {
						lineStyle: {
							color: '#475569'
						}
					},
					data: [{name: '5K及以下', value: 48},
						{name: '5-10K', value: 372},
						{name: '10K-15K', value: 1691},
						{name: '15K-20K', value: 2174},
						{name: '20K-30K', value: 4076},
						{name: '30-50K', value: 3264},
						{name: '50K以上', value: 1741}],
				}]
			}],
			i = e("#LAY-index-dataview").children("div"),
			n = function(e) {
				l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
			};
			$.ajax({
				   type: 'GET',
				   url: '/get_pie/',
				   success: function (res) {
					   t[0].series[0].data = res.salary_data;
					   l[0].setOption(t[0]); // 重新渲染图表
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   });
			i[0] && n(0);

	}), e("console", {})
});