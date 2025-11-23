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
					text: "薪资分布",
					x: "left",
					textStyle: {
						fontSize: 14
					}
				},
				tooltip: {
					trigger: "item",
					formatter: "{a} <br/>{b} : {c} ({d}%)"
				},
				series: [{
					name: "薪资待遇",
					type: "pie",
					radius: "80%",
					center: ["50%", "50%"],
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