/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */ ;
layui.define(["table", "form"], function(e) {
	var t = layui.$,
		i = layui.table,
		$=layui.jquery;
	layui.form;
	i.render({
		elem: "#LAY-app-forum-list",
		url: "/get_job_list/",
		cols: [
			[{
				field: "job_id",
				title: "#",
				width: 45,
				align: "center",
			}, {
				field: "name",
				title: "职位"
			}, {
				field: "salary",
				title: "薪资",
				width: 60
			}, {
				field: "education",
				title: "学历",
				width: 45
			}, {
				field: "experience",
				title: "经验",
				width: 50
			}, {
				field: "place",
				title: "地点",
				width: 55
			}, {
				field: "company",
				title: "公司"
			},{
				field: "label",
				title: "行业",
				width: 80
			},{
				field: "scale",
				title: "规模",
				width: 75
			},{
				title: "",
				width: 60,
				align: "center",
				toolbar: "#table-forum-list"
			}]
		],
		page: !0,
		limit: 15,
		limits: [15, 20, 30, 50],
		text: "对不起，加载出现异常！"
	}),  i.on("tool(LAY-app-forum-list)", function(e) {
		e.data;
		console.log(e.data.send_key)
		if("send" === e.event) layer.confirm("确定投递职位 "+e.data.name+" 吗？", function(t) {
			$.ajax({
				   type: 'POST',
				   data:{"job_id":e.data.job_id, "send_key":e.data.send_key},
				   url: '/send_job/',
				   success: function (res) {
					   layer.msg(res.msg);location.reload()
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   }),
				layer.close(t)
		});
		else if("send_1" === e.event) layer.confirm("确定取消投递 "+e.data.name+" 吗？", function(t){
			$.ajax({
				   type: 'POST',
				   data:{"job_id":e.data.job_id, "send_key":e.data.send_key},
				   url: '/send_job/',
				   success: function (res) {
					   layer.msg(res.msg);location.reload()
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   }),layer.close(t)
		});
	}),e("forum", {})
});
