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
					text: "学历要求分布",
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
					name: "学历要求",
					type: "pie",
					radius: "80%",
					center: ["50%", "50%"],
					data: [{name: '博士', value: 46},
						{name: '硕士', value: 554},
						{name: '本科', value: 11282},
						{name: '大专', value: 1589},
						{name: '不限', value: 618}]
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
					   t[0].series[0].data = res.edu_data;
					   l[0].setOption(t[0]); // 重新渲染图表
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   });
			i[0] && n(0);

	}), e("console", {})
});