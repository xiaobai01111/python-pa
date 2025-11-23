/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */ ;
layui.define(["table", "form"], function(e) {
	var t = layui.$,
		i = layui.table,
		$=layui.jquery;
	layui.form;
	i.render({
		elem: "#LAY-app-forum-list",
		url: "http://127.0.0.1:8000/send_list/",
		cols: [
			[{
				field: "job_id",
				title: "职位编号",
				width: 90,
				fixed: "left",
				align: "center",
			}, {
				field: "name",
				title: "职位名称"
			}, {
				field: "salary",
				title: "薪资待遇",
				width: 150
			}, {
				field: "education",
				title: "学历要求",
				width: 150
			}, {
				field: "experience",
				title: "经验要求",
				width: 150
			}, {
				field: "place",
				title: "工作地点",
				width: 200
			},  {
				field: "company",
				title: "公司名称"
			},{
				field: "label",
				title: "所属行业",
				width: 150,
			},{
				field: "scale",
				title: "公司规模",
				width: 150,
				align: "left"
			},{
				title: "操作",
				width: 130,
				align: "center",
				fixed: "right",
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
