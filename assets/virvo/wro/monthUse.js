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
    dailyUse = {
        init: function(){
            console.log("dailyUse init");
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
                var url="group/updateOperation";
                json_ajax("POST", url, "json", true,data,dailyUse.updateCallback);
            }
        },
        closeClean:function(){
            $("#addproperationtype").val("");
            $("#adddescription").val("");
            $("#addproperationtype-error").hide();//隐藏上次新增时未清除的validate样式
            $("#adddescription-error").hide();
        },
        updateClean:function () {
            $("#updateOperationType-error").hide();
            $("#updateDescription-error").hide();
        },
        updateCallback:function(data){
            if(data.success == true){
                $("#updateType").modal('hide');
                layer.msg("修改成功");
                dailyUse.findOperation();
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        deleteType:function(id){
            layer.confirm(publicDelete, {
                title :'操作确认',
                icon : 3, // 问号图标
                btn: [ '确定', '取消'] // 按钮
            }, function(){
                var url="group/deleteOperation";
                var data={"id" : id}
                json_ajax("POST", url, "json", false,data,dailyUse.deleteCallback);
            });
        },
        deleteCallback:function(data){
            if(data.success==true){
                layer.closeAll('dialog');
                dailyUse.findOperation();
            }else{
                layer.msg(publicError,{move:false});
            }
        },
        deleteTypeMore : function(){
            // 判断是否至少选择一项
            var chechedNum = $("input[name='subChkTwo']:checked").length;
            if (chechedNum == 0) {
                layer.msg(selectItem);
                return
            }
            var ids="";
            $("input[name='subChkTwo']:checked").each(function() {
                ids+=($(this).val())+",";
            });
            var url="group/deleteOperationMore";
            var data={"ids" : ids};
            layer.confirm(publicDelete, {
                title :'操作确认',
                icon : 3, // 问号图标
                btn: [ '确定', '取消'] // 按钮
            }, function(){
                json_ajax("POST", url, "json", false,data,dailyUse.deleteOperationMoreCallback);
                layer.closeAll('dialog');
            });
        },
        deleteOperationMoreCallback : function(data){
            if(data.success){
                layer.msg(publicDeleteSuccess);
                dailyUse.findOperation();
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        findOperationByVague:function(){
            dailyUse.findOperation();
        },
        findDownKey:function(event){
            if(event.keyCode==13){
                dailyUse.findOperation();
            }
        },
        checkAll : function(e){
            $("input[name='subChk']").not(':disabled').prop("checked", e.checked);

        },
        checkAllTwo : function(e){
            $("input[name='subChkTwo']").prop("checked", e.checked);
        },
        addId : function (){
            $("#addId").attr("href","stations/add/newuser?uuid="+selectTreeIdAdd+"");
        },

        //开始时间
        startDay: function (day) {
            var timeInterval = $('#timeInterval').val().split('--');
            var startValue = timeInterval[0];
            var endValue = timeInterval[1];
            if (startValue == "" || endValue == "") {
                var today = new Date();
                var targetday_milliseconds = today.getTime() + 1000 * 60 * 60
                    * 24 * day;

                today.setTime(targetday_milliseconds); //注意，这行是关键代码

                var tYear = today.getFullYear();
                var tMonth = today.getMonth();
                var tDate = today.getDate();
                tMonth = dailyUse.doHandleMonth(tMonth + 1);
                tDate = dailyUse.doHandleMonth(tDate);
                var num = -(day + 1);
                startTime = tYear + "-" + tMonth + "-" + tDate + " "
                    + "00:00:00";
                var end_milliseconds = today.getTime() + 1000 * 60 * 60 * 24
                    * parseInt(num);
                today.setTime(end_milliseconds); //注意，这行是关键代码
                var endYear = today.getFullYear();
                var endMonth = today.getMonth();
                var endDate = today.getDate();
                endMonth = dailyUse.doHandleMonth(endMonth + 1);
                endDate = dailyUse.doHandleMonth(endDate);
                endTime = endYear + "-" + endMonth + "-" + endDate + " "
                    + "23:59:59";
            } else {
                var startTimeIndex = startValue.slice(0, 10).replace("-", "/").replace("-", "/");
                var vtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * day;
                var dateList = new Date();
                dateList.setTime(vtoday_milliseconds);
                var vYear = dateList.getFullYear();
                var vMonth = dateList.getMonth();
                var vDate = dateList.getDate();
                vMonth = dailyUse.doHandleMonth(vMonth + 1);
                vDate = dailyUse.doHandleMonth(vDate);
                startTime = vYear + "-" + vMonth + "-" + vDate + " "
                    + "00:00:00";
                if (day == 1) {
                    endTime = vYear + "-" + vMonth + "-" + vDate + " "
                        + "23:59:59";
                } else {
                    var endNum = -1;
                    var vendtoday_milliseconds = Date.parse(startTimeIndex) + 1000 * 60 * 60 * 24 * parseInt(endNum);
                    var dateEnd = new Date();
                    dateEnd.setTime(vendtoday_milliseconds);
                    var vendYear = dateEnd.getFullYear();
                    var vendMonth = dateEnd.getMonth();
                    var vendDate = dateEnd.getDate();
                    vendMonth = dailyUse.doHandleMonth(vendMonth + 1);
                    vendDate = dailyUse.doHandleMonth(vendDate);
                    endTime = vendYear + "-" + vendMonth + "-" + vendDate + " "
                        + "23:59:59";
                }
            }
        },
        doHandleMonth: function (month) {
            var m = month;
            if (month.toString().length == 1) {
                m = "0" + month;
            }
            return m;
        },
        //当前时间
        getsTheCurrentTime: function () {
            var nowDate = new Date();
            startTime = nowDate.getFullYear()
                + "-"
                + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                    + parseInt(nowDate.getMonth() + 1)
                    : parseInt(nowDate.getMonth() + 1))
                + "-"
                + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                    : nowDate.getDate()) + " " + "00:00:00";
            endTime = nowDate.getFullYear()
                + "-"
                + (parseInt(nowDate.getMonth() + 1) < 10 ? "0"
                    + parseInt(nowDate.getMonth() + 1)
                    : parseInt(nowDate.getMonth() + 1))
                + "-"
                + (nowDate.getDate() < 10 ? "0" + nowDate.getDate()
                    : nowDate.getDate())
                + " "
                + ("23")
                + ":"
                + ("59")
                + ":"
                + ("59");
            var atime = $("#atime").val();
            if (atime != undefined && atime != "") {
                startTime = atime;
            }
        },
        unique: function (arr) {
            var result = [], hash = {};
            for (var i = 0, elem; (elem = arr[i]) != null; i++) {
                if (!hash[elem]) {
                    result.push(elem);
                    hash[elem] = true;
                }
            }
            return result;
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
            if (num != 1) {
                $('#timeInterval').val(startTime + '--' + endTime);
            }
            if (!dailyUse.validates()) {
                return;
            }
            dailyUse.estimate();
            dataListArray = [];
            dataListArray2 = [];
            var url = "/analysis/flowdata_monthuse/";

            var station_id = $("#station_id").val();
            // var data = {"organ": organ,"treetype":selectTreeType,"station_id":station_id,"qmonth":number, 'startTime': sTime, "endTime": eTime};
            var data = {"station_id":station_id};
            json_ajax("POST", url, "json", false, data, dailyUse.findOnline);     //发送请求
        },
        validates: function () {
            return $("#hourslist").validate({
                rules: {
                    organ_name: {
                        required: true
                    },
                    stationname: {
                        required: true,
                        // compareDate: "#timeInterval",
                    }
                },
                messages: {
                    organ_name: {
                        required: "所属组织不能为空",
                    },
                    stationname: {
                        required: "站点不能为空",
                        // compareDate: endtimeComStarttime,
                    }
                }
            }).form();
        },

        estimate: function () {
            var timeInterval = $('#timeInterval').val().split('--');
            sTime = timeInterval[0];
            eTime = timeInterval[1];
            dailyUse.getsTheCurrentTime();
            if (eTime > endTime) {                              //查询判断
                layer.msg(endTimeGtNowTime, {move: false});
                key = false
                return;
            }
            if (sTime > eTime) {
                layer.msg(endtimeComStarttime, {move: false});
                key = false;
                return;
            }
            var nowdays = new Date();                       // 获取当前时间  计算上个月的第一天
            var year = nowdays.getFullYear();
            var month = nowdays.getMonth();
            if (month == 0) {
                month = 12;
                year = year - 1;
            }
            if (month < 10) {
                month = "0" + month;
            }
            var firstDay = year + "-" + month + "-" + "01 00:00:00";//上个月的第一天
            if (sTime < firstDay) {                                 //查询判断开始时间不能超过       上个月的第一天
                $("#timeInterval-error").html(starTimeExceedOne).show();
                /*layer.msg(starTimeExceedOne, {move: false});
                key = false;*/
                return;
            }
            $("#timeInterval-error").hide();
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");       //遍历树节点，获取vehicleID 存入集合
            var nodes = treeObj.getCheckedNodes(true);
            vid = "";
            for (var j = 0; j < nodes.length; j++) {
                if (nodes[j].type == "vehicle") {
                    vid += nodes[j].id + ",";
                }
            }
            key = true;
        },
        reloadData: function (dataList) {
            var currentPage = myTable.page()
            myTable.clear()
            myTable.rows.add(dataList)
            myTable.page(currentPage).draw(false);
        },
        findOnline: function (data) {//回调函数    数据组装
            var list = [];
            var myChart = echarts.init(document.getElementById('onlineGraphics'));
            var flow_tody = "";
            
            
            if (data.obj != null && data.obj != "") {
                flow_tody = data.obj.flow_tody;
                pressure = data.obj.pressure;
            }
            if (data.success == true) {
                // carLicense = [];
                // activeDays = [];
                hdates = [];
                dosages = [];
                press = [];
                
                for (var i = 0; i < flow_tody.length; i++) {
                    list =
                        [i + 1, 
                            flow_tody[i].hdate,
                            flow_tody[i].color,
                            flow_tody[i].flow,
                            // online[i].allDays == null ? "0" : online[i].allDays,
                            flow_tody[i].ratio == null ? "0" : flow_tody[i].ratio,
                            flow_tody[i].assignmentName == null ? "无" : flow_tody[i].assignmentName,
                            
                        ]

                    dataListArray.push(list);                                       //组装完成，传入  表格
                };
                for (var j = 0; j < dataListArray.length; j++) {// 排序后组装到图表
                    hdates.push(dataListArray[j][1]);
                    dosages.push(dataListArray[j][3]);
                    
                }

                // #press
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
                    data: ['当月曲线',"压力曲线"],
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
                    splitArea : {
                        show: true,
                        areaStyle:{
                            color:dailyUse.splitAreaColor(hdates)
                        }
                    },
                    data: dailyUse.platenumbersplitYear(hdates)
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
                        name: '月用水量 （m³）',
                        nameTextStyle:{
                            color: 'black',
                            fontFamily: '微软雅黑 Bold',
                            fontSize: 14,
                            fontStyle: 'normal',
                            fontWeight: 700
                        },
                        nameLocation:'middle',
                        nameGap:80,
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
                series: [
                    {
                        name: '当月曲线',
                        yAxisIndex: 0,
                        xAxisIndex:0,
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: 'rgba(22, 155, 213, 1)'  //#6dcff6
                            }
                        },
                        data: dosages,
                        
                    },
                    
                    {
                        name: '压力曲线',
                        yAxisIndex: 1,
                        xAxisIndex: 1,
                        type: 'line',
                        tooltip:{
                            show:false
                        },
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#cc1cae'
                            }
                        },
                        data: press
                    }
                ]
            };
            myChart.setOption(option);
            
            // $("#maxflow span").html( maxflow);
            // $("#averflow span").html( average);
            // $("#today_use span").html( today_use);
            // $("#yestoday_use span").html( yestoday_use);
            // $("#last_year_same span").html( last_year_same);
            // $("#tongbi span").html( tongbi);
            // $("#huanbi span").html( huanbi);
            // $("#average span").html( average);
            // $("#max_flow span").html( maxflow);
            // $("#min_flow span").html( minflow);
            // $("#mnf span").html( mnf);
            // $("#mnf_add span").html( mnf_add);
            // $("#back_leak span").html( back_leak);
            // $("#ref_mnf span").html( ref_mnf);
            // $("#alarm_set span").html( alarm_set);

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
                    if (parseInt(subitem,10) >= parseInt(today,10)) {
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
            arr.forEach(function(item){
                if (item.length > 8) {
                    subitem = item.substring(8,10)
                    weekday = new Date(item).getDay();
                    
                    if(weekday == 1){
                        new_item = monday;
                    }else if(weekday == 4){
                        new_item = statistext;
                    }else{
                        new_item="";
                    }
                    
                }
                newArr.push(new_item)
            })
            return newArr
        },
        splitAreaColor:function(arr){
            var week1color = 'rgba(204, 153, 255, 1)';
            var week2color = 'rgba(153, 255, 255, 1)';
            var week3color = 'rgba(204, 204, 204, 1)';
            var week4color = 'rgba(153, 204, 153, 1)';
            var weekcnt = 0;
            var newArr = [];

            arr.forEach(function(item){

            })
            return ['rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)','rgba(204, 153, 255, 1)',
                    'rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)','rgba(153, 255, 255, 1)',
                    'rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)','rgba(204, 204, 204, 1)',
                    'rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)','rgba(153, 204, 153, 1)'
                    ];
        }
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
        $('#timeInterval').dateRangePicker({dateLimit:30});
        dailyUse.getsTheCurrentTime();  
        dailyUse.startDay(-7);  
        $('#timeInterval').val(startTime + '--' + endTime);
        dailyUse.inquireClick(1);
        // dailyUse.findOperation();
        // IE9
        if(navigator.appName=="Microsoft Internet Explorer" && navigator.appVersion.split(";")[1].replace(/[ ]/g,"")=="MSIE9.0") {
            dailyUse.refreshTable();
            var search;
            $("#search_condition").bind("focus",function(){
                search = setInterval(function(){
                    search_ztree('treeDemo', 'search_condition','group');
                },500);
            }).bind("blur",function(){
                clearInterval(search);
            });
        }
        // IE9 end
        // $("#selectAll").bind("click", dailyUse.selectAll);
        // 组织架构模糊搜索
        $("#search_condition").on("input oninput",function(){
            search_ztree('treeDemo', 'search_condition','group');
        });       
        
        
        $("#addId").on("click",dailyUse.addId);
        $("#closeAdd").on("click",dailyUse.closeClean);
        $("#updateClose").on("click",dailyUse.updateClean);
    })
})($,window)
