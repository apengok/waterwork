(function($,window){
    var selectTreeId = '';
    var selectDistrictId = '';
    var selectTreeType = '';
    var zNodes = null;
    var log, className = "dark";
    var newCount = 1;
    var columnDefs;
    var columns;
    var setting;
    var treeSetting;
    var idStr;
    var OperationId;
    var selectTreeIdAdd="";
    var startOperation;// 点击运营资质类别的修改按钮时，弹出界面时运营资质类别文本的内容
    var expliant;// 点击运营资质类别的修改按钮时，弹出界面时说明文本的内容
    var vagueSearchlast = $("#operationType").val();

    var dataListArray = [];
    var dataListArray3 = [];
    var dataListArray4 = [];
    var dataListArray2 = [];
    var endTime;// 当天时间
    var sTime;
    var eTime;
    var key = true;
    var vid;
    var carLicense = [];
    var activeDays = [];
    var organ = '';
    var station = $("#station_id").val();
    var bflag = true;
    var zTreeIdJson = {};
    var barWidth;
    var number;
    var checkFlag = false; //判断组织节点是否是勾选操作
    var size;//当前权限监控对象数量
    var online_length;

    var week1color = 'rgba(204, 153, 255, 1)';
    var week2color = 'rgba(153, 255, 255, 1)';
    var week3color = 'rgba(204, 204, 204, 1)';
    var week4color = 'rgba(153, 204, 153, 1)';
    var week5color = 'rgba(153, 123, 235, 1)';

    dailyUse = {
        init: function(){
            console.log("dailyUse init");

            laydate.render({elem: '#compare_date1',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#compare_date1-error").hide();
                    console.log("comparedate 1 selected done",value,date,endDate);
                    dailyUse.inquireBydateselected(value);
                }
            });

            laydate.render({elem: '#compare_date2',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#compare_date2-error").hide();
                    dailyUse.inquireBydateselected(value);
                }
            });

            laydate.render({elem: '#compare_date3',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#compare_date3-error").hide();
                    dailyUse.inquireBydateselected(value);
                }
            });

            laydate.render({elem: '#compare_date4',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#compare_date4-error").hide();
                    dailyUse.inquireBydateselected(value);
                }
            });

            laydate.render({elem: '#compare_date5',
                theme: '#6dcff6',
                done: function(value, date, endDate){
                    $("#compare_date5-error").hide();
                    dailyUse.inquireBydateselected(value);
                }
            });
        },
        
        userTree : function(){
            // 初始化文件树
            treeSetting = {
                async : {
                    url : "/dmam/district/dmatree/",
                    type : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                    data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
                    otherParam : {  // 是否可选 Organization
                        "isOrg" : "1",
                        "isStation":"1",
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: dailyUse.ajaxDataFilter
                },
                view : {
                    // addHoverDom : dailyUse.addHoverDom,
                    // removeHoverDom : dailyUse.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    fontCss: setFontCss_ztree
                },
                edit : {
                    enable : true,
                    editNameSelectAll : true,
                    showRemoveBtn : false,//dailyUse.showRemoveBtn,
                    showRenameBtn : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    // beforeDrag : dailyUse.beforeDrag,
                    // beforeEditName : dailyUse.beforeEditName,
                    // beforeRemove : dailyUse.beforeRemove,
                    // beforeRename : dailyUse.beforeRename,
                    // onRemove : dailyUse.onRemove,
                    // onRename : dailyUse.onRename,
                    onClick : dailyUse.zTreeOnClick
                }
            };
            $.fn.zTree.init($("#treeDemo"), treeSetting, zNodes);
            var treeObj = $.fn.zTree.getZTreeObj('treeDemo');treeObj.expandAll(true);
           
        },

        
        // 组织树预处理函数
        ajaxDataFilter: function(treeId, parentNode, responseData){
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
            if (responseData) {
                for (var i = 0; i < responseData.length; i++) {
                        responseData[i].open = true;
                }
            }
            return responseData;
        },
        
        showLog: function(str){
            if (!log)
                log = $("#log");
                log.append("<li class='"+className+"'>" + str + "</li>");
            if (log.children("li").length > 8) {
                log.get(0).removeChild(log.children("li")[0]);
            }
        },
        getTime: function(){
            var now = new Date(), h = now.getHours(), m = now.getMinutes(), s = now
                .getSeconds(), ms = now.getMilliseconds();
            return (h + ":" + m + ":" + s + " " + ms);
        },
        selectAll: function(){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.treeSetting.edit.editNameSelectAll = $("#selectAll").attr("checked");
        },
        //点击节点
        zTreeOnClick: function(event, treeId, treeNode){
            selectTreeId = treeNode.id;
            selectTreeType = treeNode.type;
            selectDistrictId = treeNode.districtid;
            selectTreeIdAdd = treeNode.uuid;
            
            $('#simpleQueryParam').val("");
            
            if(treeNode.type == "station"){
                var pNode = treeNode.getParentNode();
                $("#organ_name").attr("value",pNode.name);
                $("#station_name").attr("value",treeNode.name);
                $("#station_id").attr("value",treeNode.id);
                organ = pNode.id;
                
                dailyUse.inquireClick(1);
            }

            
            // myTable.requestData();
        },
        // ajax参数
        ajaxDataParamFun: function(d){
            d.simpleQueryParam = $('#simpleQueryParam').val(); // 模糊查询
            d.groupName = selectTreeId;
            d.districtId = selectDistrictId;
        },
        findCallback:function(data){
            if(data.success){
                var operations=[];
                if(data.obj.operation != null || data.obj.operation.length>0){
                    var calldata = data.obj.operation;
                    var s=0;
                    for(var i=0;i<calldata.length;i++){
                        var list=[
                                 ++s,
                                 '<input type="checkbox" id="checkAllTwo" name="subChkTwo" value="'+calldata[i].id+'">',
                                 '<button onclick="dailyUse.findOperationById(\''+calldata[i].id+'\')" data-target="#updateType" data-toggle="modal"  type="button" class="editBtn editBtn-info"><i class="fa fa-pencil"></i>修改</button>&nbsp<button type="button"  onclick="dailyUse.deleteType(\''+calldata[i].id+'\')" class="deleteButton editBtn disableClick"><i class="fa fa-trash-o"></i>删除</button>',    
                                 calldata[i].operationType,
                                 calldata[i].explains
                                 ];
                        operations.push(list);
                    }
                }
                // reloadData(operations);
            }else{
                layer.msg(data.msg);
            }
        },
         doSubmit:function () {
            if(dailyUse.validates()){
                $("#eadOperation").ajaxSubmit(function(data) {
                    console.log('sdfe:',data);
                    if (data != null && typeof(data) == "object" &&
                        Object.prototype.toString.call(data).toLowerCase() == "[object object]" &&
                        !data.length) {//判断data是字符串还是json对象,如果是json对象
                            if(data.success == true){
                                $("#addType").modal("hide");//关闭窗口
                                layer.msg(publicAddSuccess,{move:false});
                                dailyUse.closeClean();//清空文本框
                                $("#operationType").val("");
                                dailyUse.findOperation();
                            }else{
                                layer.msg(data.msg,{move:false});
                            }
                    }else{//如果data不是json对象
                            var result = $.parseJSON(data);//转成json对象
                            if (result.success == true) {
                                    $("#addType").modal("hide");//关闭窗口
                                    layer.msg(publicAddSuccess,{move:false});
                                    $("#operationType").val("");
                                    dailyUse.closeClean();//清空文本框
                                    dailyUse.findOperation();
                            }else{
                                layer.msg(result.msg,{move:false});
                            }
                    }
                });
            }
        },
        updateDoSubmit:function () {
            dailyUse.init();
            if(dailyUse.upDateValidates()){
                var operationType=$("#updateOperationType").val();// 运营资质类型
                var explains=$("#updateDescription").val();// 说明
                var data={"id":OperationId,"operationType":operationType,"explains":explains};
                var url="/entm/group/updateOperation";
                json_ajax("POST", url, "json", true,data,dailyUse.updateCallback);
            }
        },
        
        
        inquireClick: function (num) {
            $(".mileage-Content").css("display", "block");  //显示图表主体
            number = num;
            // if (number == 0) {
            //     dailyUse.getsTheCurrentTime();
            // } else if (number == -1) {
            //     dailyUse.startDay(-1)
            // } else if (number == -3) {
            //     dailyUse.startDay(-3)
            // } else if (number == -7) {
            //     dailyUse.startDay(-7)
            // };
            
            dataListArray = [];
            dataListArray2 = [];
            var url = "/analysis/flowdata_dailyuse/";

            var station_id = $("#station_id").val();
            // var data = {"organ": organ,"treetype":selectTreeType,"station_id":station_id,"qmonth":number, 'startTime': sTime, "endTime": eTime};
            var data = {"station_id":station_id,"days":num};
            json_ajax("POST", url, "json", false, data, dailyUse.processFlows);     //发送请求
        },
        fillSeriaData:function(name,etype,lcolor,xind,yind,data){
            return  {
                        name: name,
                        yAxisIndex: yind,
                        xAxisIndex:xind,
                        type: etype,
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: lcolor //#6dcff6
                            }
                        },
                        data: data,
                        
                    }
        },
        processFlows: function (data) {//回调函数    数据组装
            var list = [];
            var myChart = echarts.init(document.getElementById('dailyUseGraphics'));
            var flow_data = "";
            var last_month = "";
            var before_last_month = "";
            var history = "";
            var hdates = [];
            var legend_list = [];
            var serias_list = [];
            var today_use = "-";
            var yestoday_use = "-";
            var before_yestoday_use = "-";
            var average = "-";
            var maxflow = "-";
            var minflow = "-";
            var color_list = ['rgba(22, 155, 213, 1)','rgba(122, 55, 13, 1)','rgba(212, 15, 113, 1)','rgba(221, 55, 113, 1)','rgba(122, 45, 85, 1)','rgba(98, 35, 148, 1)','rgba(121, 0, 119, 1)']
            var today_bar = [];
            if (data.obj != null && data.obj != "") {
                flow_data = data.obj.flow_data;
                
                pressure = data.obj.pressure;

                today_use = data.obj.today_use;
                yestoday_use = data.obj.yestoday_use;
                before_yestoday_use = data.obj.before_yestoday_use;
                maxflow = data.obj.maxflow;
                minflow = data.obj.minflow;
                average = data.obj.average;
                
            }
            if (data.success == true) {
                
                //当月
                dataListArray=[];
                if(flow_data.length > 0){
                    flow_current = []
                    list=[];
                    for (var i = 0; i < flow_data.length; i++) {
                        list =
                            [i + 1, 
                                flow_data[i].hdate,
                                flow_data[i].color,
                                flow_data[i].flow,
                                // online[i].allDays == null ? "0" : online[i].allDays,
                                flow_data[i].ratio == null ? "0" : flow_data[i].ratio,
                                flow_data[i].assignmentName == null ? "无" : flow_data[i].assignmentName,
                                
                            ]

                        dataListArray.push(list);                                       //组装完成，传入  表格
                    };
                    data_cnt = 0;
                    ci = 0
                    for (var j = 0; j < dataListArray.length; j++) {// 排序后组装到图表
                        hdates.push(dataListArray[j][1]);
                        flow_current.push(dataListArray[j][3]);
                        data_cnt += 1;
                        //每24个数据为一天
                        if(data_cnt == 24){
                            data_cnt = 0;
                            var datestr = hdates[j].substring(0,10);
                            
                            var nowDate = new Date();
                            var today = nowDate.getFullYear()
                            + "-"
                            + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                                + parseInt(nowDate.getMonth() + 1)
                                : parseInt(nowDate.getMonth() + 1))
                            + "-"
                            + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                                : nowDate.getDate());

                            nowDate.setDate(nowDate.getDate() - 1);
                            var yestoday = nowDate.getFullYear()
                            + "-"
                            + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                                + parseInt(nowDate.getMonth() + 1)
                                : parseInt(nowDate.getMonth() + 1))
                            + "-"
                            + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                                : nowDate.getDate());


                            if(datestr == today){
                                datestr = "今日曲线";
                                today_bar = flow_current;
                            }
                            if(datestr == yestoday){
                                datestr = "昨日曲线";
                            }

                            legend_list.push(datestr);
                            var tmp = dailyUse.fillSeriaData(datestr,'line',color_list[ci],0,0,flow_current);
                            serias_list.push(tmp);
                            console.log(datestr,flow_current);
                            flow_current = []
                            ci += 1;
                        }
                        
                    }
                    
                }
                

                // #press
                press=[];
                for (var i = 0; i < pressure.length; i++) {
                    list =
                        [i + 1, 
                            pressure[i].hdate,
                            pressure[i].color,
                            pressure[i].press,
                            // online[i].allDays == null ? "0" : online[i].allDays,
                            pressure[i].ratio == null ? "0" : pressure[i].ratio,
                            pressure[i].assignmentName == null ? "无" : pressure[i].assignmentName,
                            
                        ]

                    dataListArray2.push(list);                                       //组装完成，传入  表格
                };
                
                for (var j = 0; j < dataListArray2.length; j++) {// 排序后组装到图表
                    hdates.push(dataListArray2[j][1]);
                    press.push(dataListArray2[j][3]);
                    
                }
                legend_list.push("压力曲线");
                var tmp = dailyUse.fillSeriaData("压力曲线",'line','rgba(22, 155, 213, 1)',1,1,press);
                serias_list.push(tmp);

                legend_list.push("当日柱状图");
                var tmp = dailyUse.fillSeriaData("当日柱状图",'bar','rgba(22, 55, 13, 1)',1,1,today_bar);
                serias_list.push(tmp);

                // dailyUse.reloadData(dataListArray);
                $("#simpleQueryParam").val("");
                $("#search_button").click();
            } else {
                if (data.msg != null) {
                    layer.msg(data.msg, {move: false});
                }
                hdates = [];
                dosages = [];
                hdates.push("");
                dosages.push("");
                last_moth=[];
                last_moth.push("");
                
                press=[];
                press.push("");
                
            }

            var start;
            var end;
            var length;
            online_length = press.length;
            
            if (length < 4) {
                barWidth = "30%";
            } else if (length < 6) {
                barWidth = "20%";
            } else {
                barWidth = null;
            }
            ;
            if (length <= 200) {
                start = 0;
                end = 100;
            } else {
                start = 0;
                // end = 100 * (200 / length);
                end = 100;
            }
            ;
            // wjk
            //carLicense = dailyUse.platenumbersplitFun(carLicense);
            var option = {
                tooltip: {
                    show:true,
                    trigger: 'axis',
                    textStyle: {
                        fontSize: 20
                    },
                    // formatter: function (a) {
                    //     console.log(a);
                    //     var relVal = "";
                    //     //var relValTime = a[0].name;
                    //     var relValTime  =hdates[a[0].dataIndex];
                    //     if (a[0].data == 0) {
                    //         relVal = "无相关数据";
                    //         relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                    //         // relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;'></span>" + a[1].seriesName + "：" + a[1].value + " Mpa";
                    //     } else {
                    //         relVal = relValTime;
                    //         relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[0].color + "'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                    //         // relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[1].color + "'></span>" + a[1].seriesName + "：" + a[1].value + " Mpa";
                    //     }
                    //     ;
                    //     return relVal;
                    // }
                },
                legend: {
                    data: legend_list,   //['当月曲线','上月曲线',"压力曲线"],
                    left: 'auto',
                },
                toolbox: {
                    show: false
                },
                grid: {
                    left: '80',
                    bottom:'100'
                },
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,  // 让折线图从X轴0刻度开始
                    name: "",
                    axisLabel: {
                        show: true,
                        rotate: 0
                    },
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#483d8b',
                            type: 'dashed',
                            width: 1
                        }
                    },
                    // splitArea : {
                    //     show: true,
                    //     areaStyle:{
                    //         color:dailyUse.splitAreaColor(hdates)
                    //     }
                    // },
                    data: ['00','01','02','03','04','05','06','07','08','09,','10','11','12','13','14','15','16','17','18','19,','20','21','22','23'] //dailyUse.platenumbersplitYear(hdates)
                },
                {
                    type:'category',
                    show:true,
                    position:'bottom',
                    interval:0,
                    offset:20,
                    tooltip:{
                        show:false
                    },
                    axisTick:{
                        show:false
                    },
                    splitLine: {
                        show: false,
                        lineStyle: {
                            color: '#483d8b',
                            type: 'dashed',
                            width: 1
                        }
                    },
                    axisLabel: {
                        show: true,
                        interval:0,
                        rotate: 0
                    },
                    data:dailyUse.weekshowsplitFun(hdates)
                }],
                yAxis: [
                    {
                        type: 'value',
                        name: '时用水量 （m³）',
                        nameTextStyle:{
                            color: 'black',
                            fontFamily: '微软雅黑 Bold',
                            fontSize: 14,
                            fontStyle: 'normal',
                            fontWeight: 700
                        },
                        nameLocation:'middle',
                        nameGap:50,
                        scale: false,
                        position: 'left',
                        axisLabel : {
                            show:true,
                            interval: 'auto',    // {number}
                            rotate: 0,
                            margin: 18,
                            formatter: '{value}',    // Template formatter!
                            textStyle: {
                                color: 'black',
                                fontFamily: 'verdana',
                                fontSize: 10,
                                fontStyle: 'normal',
                                fontWeight: 'bold'
                            }
                        },
                        axisTick : {    // 轴标记
                            show:false,
                            length: 10,
                            lineStyle: {
                                color: 'green',
                                type: 'solid',
                                width: 2
                            }
                        },
                        splitLine: {
                            show: true
                        }
                    },

                    {
                        type : 'value',
                        splitNumber: 1,
                        name: 'Mpa',
                        nameLocation:'middle',
                        nameGap:30,
                        scale: false,
                        axisLabel: {
                            formatter: '{value}' + 'Mpa'
                        },
                        axisLine : {    // 轴线
                            show: true,
                            lineStyle: {
                                color: 'grey',
                                type: 'dashed',
                                width: 1
                            }
                        },
                        axisTick : {    // 轴标记
                            show:false,
                            length: 10,
                            lineStyle: {
                                color: 'green',
                                type: 'solid',
                                width: 2
                            }
                        },
                        
                        splitLine : {
                            show: false
                        },
                        offset : 20
                    }
                ],
                // dataZoom : [{
                //     show : true,
                //     realtime : true,
                //     //orient: 'vertical',   // 'horizontal'
                //     //x: 0,
                //     y: 550,
                //     //width: 400,
                //     height: 20,
                //     //backgroundColor: 'rgba(221,160,221,0.5)',
                //     //dataBackgroundColor: 'rgba(138,43,226,0.5)',
                //     //fillerColor: 'rgba(38,143,26,0.6)',
                //     //handleColor: 'rgba(128,43,16,0.8)',
                //     //xAxisIndex:[],
                //     //yAxisIndex:[],
                //     type: 'inside',
                //     start : start,
                //     end : end
                // },
                // {
                //     show : true,
                //     realtime : true,
                //     //orient: 'vertical',   // 'horizontal'
                //     //x: 0,
                //     y: 550,
                //     //width: 400,
                //     height: 20,
                //     //backgroundColor: 'rgba(221,160,221,0.5)',
                //     //dataBackgroundColor: 'rgba(138,43,226,0.5)',
                //     //fillerColor: 'rgba(38,143,26,0.6)',
                //     //handleColor: 'rgba(128,43,16,0.8)',
                //     //xAxisIndex:[],
                //     //yAxisIndex:[],
                //     type: 'slider',
                //     start : 0,
                //     end : 100
                // }],
                series: serias_list
            };
            myChart.setOption(option);
            
            
            $("#today_use span").html( today_use);
            $("#yestoday_use span").html( yestoday_use);
            $("#before_yestoday_use span").html( before_yestoday_use);
            $("#average span").html( average);
            $("#max_flow span").html( maxflow);
            $("#min_flow span").html( minflow);
            

            window.onresize = myChart.resize;
        },
        platenumbersplitYear:function(arr){

            
            var today = arr[arr.length - 1].substring(8,10);
            
            var newArr = [];
            var subitem = "";
            var new_item = "";
            arr.forEach(function(item){
                if (item.length > 8) {
                    subitem = item.substring(8,10)
                    weekday = new Date(item).getDay();
                    if (parseInt(subitem,10) > parseInt(today,10)) {
                        if(weekday == 1){
                            new_item = {
                                value:subitem,// + '\n\n星\n期\n一',
                                textStyle:{
                                    color:'red',
                                    
                                }
                            }
                        }else{
                            new_item = {
                                value:subitem,
                                textStyle:{
                                    color:'red',
                                    
                                }
                            }
                        }
                    }else{
                        if(weekday == 1){
                            new_item = subitem;// + monday;
                        }else{
                            new_item = subitem;
                        }
                    }
                }
                newArr.push(new_item)
            })
            return newArr
        },
        weekshowsplitFun:function(arr){
            this_month = parseInt(arr[arr.length - 1],10);
            // alert(new Date('2018/08/09').getDay());
            var today = arr[arr.length - 1].substring(8,10);
            var monday = '\n星\n期\n一';

            var statistext = '\n 本周用水量:284m3\n最大值：64m3\n最小值：12m3';

            var newArr = [];
            var subitem = "";
            var new_item = "";
            var weekcnt = 0;
            var weekcolor = [week1color,week2color,week3color,week4color,week5color]
            arr.forEach(function(item){
                if (item.length > 8) {
                    subitem = item.substring(8,10)
                    weekday = new Date(item).getDay();

                    
                    if(weekday == 1){
                        new_item = monday;
                        
                    }else if(weekday == 4){
                        new_item = {
                            value:statistext,
                            textStyle:{
                                color:weekcolor[weekcnt],
                                
                            }
                        
                        };
                        weekcnt += 1;
                    }else{
                        new_item = "";
                    }
                    
                }
                newArr.push(new_item)
            })
            return newArr
        },
        splitAreaColor:function(arr){
            
            var weekcnt = 0;
            var newArr = [];

            arr.forEach(function(item){

            })
            return ['rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)',
                    'rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)',
                    'rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)',
                    'rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)',
                    week5color,week5color,week5color,week5color,week5color,week5color,week5color
                    ];
        },
        compareshow:function(){
        
          if($('#checkbox1').is(":checked") == true){
            $('#compare_div').show();
            dailyUse.inquireCompare(1);
        }
          else
            $('#compare_div').hide();

        
        },
        inquireBydateselected:function(queryday){
            var url = "/analysis/flowdata_queryday/";

            var station_id = $("#station_id").val();
            // var data = {"organ": organ,"treetype":selectTreeType,"station_id":station_id,"qmonth":number, 'startTime': sTime, "endTime": eTime};
            var data = {"station_id":station_id,"queryday":queryday};
            json_ajax("POST", url, "json", false, data, dailyUse.processFlowsDayappend);     //发送请求
        },
        processFlowsDayappend:function(data){

        },
        inquireCompare: function (num) {
            $(".mileage-Content").css("display", "block");  //显示图表主体
            number = num;
            
            
            dataListArray = [];
            dataListArray2 = [];
            var url = "/analysis/flowdata_dailyuse_compare/";

            var station_id = $("#station_id").val();
            // var data = {"organ": organ,"treetype":selectTreeType,"station_id":station_id,"qmonth":number, 'startTime': sTime, "endTime": eTime};
            var data = {"station_id":station_id,"month":num};
            json_ajax("POST", url, "json", false, data, dailyUse.processFlowsCompare);     //发送请求
        },
        processFlowsCompare: function (data) {//回调函数    数据组装
            var list = [];
            var myChart2 = echarts.init(document.getElementById('dailyCompareGraphics'));
            var flow_data = "";
            var last_month = "";
            var before_last_month = "";
            var history = "";
            var hdates = [];
            var legend_list = [];
            var serias_list = [];
            var today_use = "-";
            var yestoday_use = "-";
            var before_yestoday_use = "-";
            var average = "-";
            var maxflow = "-";
            var minflow = "-";
            var color_list = ['rgba(22, 155, 213, 1)','rgba(122, 55, 13, 1)','rgba(212, 15, 113, 1)','rgba(221, 55, 113, 1)','rgba(122, 45, 85, 1)','rgba(98, 35, 148, 1)','rgba(121, 0, 119, 1)']
            var today_bar = [];
            if (data.obj != null && data.obj != "") {
                flow_data = data.obj.current_month;
                
               
                
            }
            if (data.success == true) {
                
                //当月
                dataListArray=[];
                if(flow_data.length > 0){
                    flow_current = []
                    list=[];
                    for (var i = 0; i < flow_data.length; i++) {
                        list =
                            [i + 1, 
                                flow_data[i].hdate,
                                flow_data[i].color,
                                flow_data[i].flow,
                                // online[i].allDays == null ? "0" : online[i].allDays,
                                flow_data[i].ratio == null ? "0" : flow_data[i].ratio,
                                flow_data[i].assignmentName == null ? "无" : flow_data[i].assignmentName,
                                
                            ]

                        dataListArray.push(list);                                       //组装完成，传入  表格
                    };
                    data_cnt = 0;
                    ci = 0
                    for (var j = 0; j < dataListArray.length; j++) {// 排序后组装到图表
                        hdates.push(dataListArray[j][1]);
                        flow_current.push(dataListArray[j][3]);
                        data_cnt += 1;
                        
                        
                    }
                    
                }
                // legend_list.push("压力曲线");
                var tmp = dailyUse.fillSeriaData("压力曲线",'line','rgba(22, 155, 213, 1)',0,0,flow_current);
                serias_list.push(tmp);

                

                // dailyUse.reloadData(dataListArray);
                $("#simpleQueryParam").val("");
                $("#search_button").click();
            } else {
                if (data.msg != null) {
                    layer.msg(data.msg, {move: false});
                }
                hdates = [];
                dosages = [];
                hdates.push("");
                dosages.push("");
                last_moth=[];
                last_moth.push("");
                
                press=[];
                press.push("");
                
            }

            var start;
            var end;
            var length;
            
            
            if (length < 4) {
                barWidth = "30%";
            } else if (length < 6) {
                barWidth = "20%";
            } else {
                barWidth = null;
            }
            ;
            if (length <= 200) {
                start = 0;
                end = 100;
            } else {
                start = 0;
                // end = 100 * (200 / length);
                end = 100;
            }
            ;
            // wjk
            //carLicense = dailyUse.platenumbersplitFun(carLicense);
            var option = {
                tooltip: {
                    show:true,
                    trigger: 'axis',
                    textStyle: {
                        fontSize: 20
                    },
                    // formatter: function (a) {
                    //     console.log(a);
                    //     var relVal = "";
                    //     //var relValTime = a[0].name;
                    //     var relValTime  =hdates[a[0].dataIndex];
                    //     if (a[0].data == 0) {
                    //         relVal = "无相关数据";
                    //         relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                    //         // relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;'></span>" + a[1].seriesName + "：" + a[1].value + " Mpa";
                    //     } else {
                    //         relVal = relValTime;
                    //         relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[0].color + "'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                    //         // relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[1].color + "'></span>" + a[1].seriesName + "：" + a[1].value + " Mpa";
                    //     }
                    //     ;
                    //     return relVal;
                    // }
                },
                legend: {
                    data: legend_list,   //['当月曲线','上月曲线',"压力曲线"],
                    left: 'auto',
                },
                toolbox: {
                    show: false
                },
                grid: {
                    left: '80',
                    bottom:'100'
                },
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,  // 让折线图从X轴0刻度开始
                    name: "",
                    axisLabel: {
                        show: true,
                        'interval':7,
                        rotate: 0
                    },
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#483d8b',
                            type: 'dashed',
                            width: 1
                        }
                    },
                    // splitArea : {
                    //     show: true,
                    //     areaStyle:{
                    //         color:dailyUse.splitAreaColor(hdates)
                    //     }
                    // },
                    data: hdates //dailyUse.platenumbersplitYear(hdates)
                },
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: 'm³',
                        // nameTextStyle:{
                        //     color: 'black',
                        //     fontFamily: '微软雅黑 Bold',
                        //     fontSize: 14,
                        //     fontStyle: 'normal',
                        //     fontWeight: 700
                        // },
                        // nameLocation:'middle',
                        // nameGap:50,
                        scale: false,
                        position: 'left',
                        axisLabel : {
                            show:true,
                            interval: 'auto',    // {number}
                            rotate: 0,
                            margin: 18,
                            formatter: '{value}',    // Template formatter!
                            textStyle: {
                                color: 'black',
                                fontFamily: 'verdana',
                                fontSize: 10,
                                fontStyle: 'normal',
                                fontWeight: 'bold'
                            }
                        },
                        axisTick : {    // 轴标记
                            show:false,
                            length: 10,
                            lineStyle: {
                                color: 'green',
                                type: 'solid',
                                width: 2
                            }
                        },
                        splitLine: {
                            show: true
                        }
                    },

                    
                ],
                // dataZoom : [{
                //     show : true,
                //     realtime : true,
                //     //orient: 'vertical',   // 'horizontal'
                //     //x: 0,
                //     y: 550,
                //     //width: 400,
                //     height: 20,
                //     //backgroundColor: 'rgba(221,160,221,0.5)',
                //     //dataBackgroundColor: 'rgba(138,43,226,0.5)',
                //     //fillerColor: 'rgba(38,143,26,0.6)',
                //     //handleColor: 'rgba(128,43,16,0.8)',
                //     //xAxisIndex:[],
                //     //yAxisIndex:[],
                //     type: 'inside',
                //     start : start,
                //     end : end
                // },
                // {
                //     show : true,
                //     realtime : true,
                //     //orient: 'vertical',   // 'horizontal'
                //     //x: 0,
                //     y: 550,
                //     //width: 400,
                //     height: 20,
                //     //backgroundColor: 'rgba(221,160,221,0.5)',
                //     //dataBackgroundColor: 'rgba(138,43,226,0.5)',
                //     //fillerColor: 'rgba(38,143,26,0.6)',
                //     //handleColor: 'rgba(128,43,16,0.8)',
                //     //xAxisIndex:[],
                //     //yAxisIndex:[],
                //     type: 'slider',
                //     start : 0,
                //     end : 100
                // }],
                series: serias_list
            };
            myChart2.setOption(option);
            
            window.onresize = myChart2.resize;
        },
    }
    $(function(){
        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('treeDemo',id,'group');
            };
        });
        
        dailyUse.userTree();
        
        dailyUse.init();
        
        dailyUse.inquireClick(1);
        $('#compare_div').hide();
        // IE9 end
        // $("#selectAll").bind("click", dailyUse.selectAll);
        // 组织架构模糊搜索
        $("#search_condition").on("input oninput",function(){
            search_ztree('treeDemo', 'search_condition','group');
        });       
        
        $('#checkbox1').bind('click',dailyUse.compareshow);
        
    })
})($,window)
