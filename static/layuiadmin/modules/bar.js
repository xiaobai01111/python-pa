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
					text: "职位关键字-柱形图",
					subtext: "职位数量"
				},
				tooltip: {
					trigger: "axis"
				},
				legend: {
					data: ["职位数量"]
				},
				xAxis: [{
					type: "category",
					data: ['物联网', 'python', '后端', 'java', '前端', 'web', 'c', 'android', 'c语言', '测试', '大数据']
				}],
				yAxis: [{
					type: "value"
				}],
				series: [{
					name: "职位数量",
					type: "bar",
					barWidth:50,
					data: [1453, 1547, 1363, 1520, 1440, 1049, 40, 1355, 1470, 1472, 1429],
					itemStyle: {
						  normal: {
							label: {
							  show: true, //开启显示
							  position: 'top', //在上方显示
							  textStyle: {
								//数值样式
								color: 'black',
								fontSize: 12,
							  },
							},
						  },
						},
				}]
			}],
			i = e("#LAY-index-dataview").children("div"),
			n = function(e) {
				l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
			};
			$.ajax({
				   type: 'GET',
				   url: '/bar/',
				   success: function (res) {
					   t[0].xAxis[0].data = res.bar_x;
					   t[0].series[0].data = res.bar_y;
					   l[0].setOption(t[0]); // 重新渲染图表
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   }),
			i[0] && n(0);
	}), e("console", {})
});