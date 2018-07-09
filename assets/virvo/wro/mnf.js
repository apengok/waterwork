(function($,window){
    var selectTreeId = '';
    var selectDistrictId = '';
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
    var endTime;// 当天时间
    var sTime;
    var eTime;
    var key = true;
    var vid;
    var carLicense = [];
    var activeDays = [];
    var organ = '';
    var station = '';
    var bflag = true;
    var zTreeIdJson = {};
    var barWidth;
    var number;
    var checkFlag = false; //判断组织节点是否是勾选操作
    var size;//当前权限监控对象数量

    analysisMnf = {
        init: function(){
            console.log("analysisMnf init");
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
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: analysisMnf.ajaxDataFilter
                },
                view : {
                    // addHoverDom : analysisMnf.addHoverDom,
                    // removeHoverDom : analysisMnf.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    fontCss: setFontCss_ztree
                },
                edit : {
                    enable : true,
                    editNameSelectAll : true,
                    showRemoveBtn : false,//analysisMnf.showRemoveBtn,
                    showRenameBtn : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    // beforeDrag : analysisMnf.beforeDrag,
                    // beforeEditName : analysisMnf.beforeEditName,
                    // beforeRemove : analysisMnf.beforeRemove,
                    // beforeRename : analysisMnf.beforeRename,
                    // onRemove : analysisMnf.onRemove,
                    // onRename : analysisMnf.onRename,
                    onClick : analysisMnf.zTreeOnClick
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
            selectDistrictId = treeNode.districtid;
            selectTreeIdAdd = treeNode.uuid;
            $('#simpleQueryParam').val("");
            if(treeNode.type == "district"){
                var pNode = treeNode.getParentNode();
                $("#organ_name").attr("value",pNode.name);
                $("#station_name").attr("value",treeNode.name);
                organ = pNode.id;
                station = treeNode.id;
            }

            analysisMnf.inquireClick(1);
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
                                 '<button onclick="analysisMnf.findOperationById(\''+calldata[i].id+'\')" data-target="#updateType" data-toggle="modal"  type="button" class="editBtn editBtn-info"><i class="fa fa-pencil"></i>修改</button>&nbsp<button type="button"  onclick="analysisMnf.deleteType(\''+calldata[i].id+'\')" class="deleteButton editBtn disableClick"><i class="fa fa-trash-o"></i>删除</button>',    
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
            if(analysisMnf.validates()){
                $("#eadOperation").ajaxSubmit(function(data) {
                    console.log('sdfe:',data);
                    if (data != null && typeof(data) == "object" &&
                        Object.prototype.toString.call(data).toLowerCase() == "[object object]" &&
                        !data.length) {//判断data是字符串还是json对象,如果是json对象
                            if(data.success == true){
                                $("#addType").modal("hide");//关闭窗口
                                layer.msg(publicAddSuccess,{move:false});
                                analysisMnf.closeClean();//清空文本框
                                $("#operationType").val("");
                                analysisMnf.findOperation();
                            }else{
                                layer.msg(data.msg,{move:false});
                            }
                    }else{//如果data不是json对象
                            var result = $.parseJSON(data);//转成json对象
                            if (result.success == true) {
                                    $("#addType").modal("hide");//关闭窗口
                                    layer.msg(publicAddSuccess,{move:false});
                                    $("#operationType").val("");
                                    analysisMnf.closeClean();//清空文本框
                                    analysisMnf.findOperation();
                            }else{
                                layer.msg(result.msg,{move:false});
                            }
                    }
                });
            }
        },
        updateDoSubmit:function () {
            analysisMnf.init();
            if(analysisMnf.upDateValidates()){
                var operationType=$("#updateOperationType").val();// 运营资质类型
                var explains=$("#updateDescription").val();// 说明
                var data={"id":OperationId,"operationType":operationType,"explains":explains};
                var url="group/updateOperation";
                json_ajax("POST", url, "json", true,data,analysisMnf.updateCallback);
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
                analysisMnf.findOperation();
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
                json_ajax("POST", url, "json", false,data,analysisMnf.deleteCallback);
            });
        },
        deleteCallback:function(data){
            if(data.success==true){
                layer.closeAll('dialog');
                analysisMnf.findOperation();
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
                json_ajax("POST", url, "json", false,data,analysisMnf.deleteOperationMoreCallback);
                layer.closeAll('dialog');
            });
        },
        deleteOperationMoreCallback : function(data){
            if(data.success){
                layer.msg(publicDeleteSuccess);
                analysisMnf.findOperation();
            }else{
                layer.msg(data.msg,{move:false});
            }
        },
        findOperationByVague:function(){
            analysisMnf.findOperation();
        },
        findDownKey:function(event){
            if(event.keyCode==13){
                analysisMnf.findOperation();
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
                tMonth = analysisMnf.doHandleMonth(tMonth + 1);
                tDate = analysisMnf.doHandleMonth(tDate);
                var num = -(day + 1);
                startTime = tYear + "-" + tMonth + "-" + tDate + " "
                    + "00:00:00";
                var end_milliseconds = today.getTime() + 1000 * 60 * 60 * 24
                    * parseInt(num);
                today.setTime(end_milliseconds); //注意，这行是关键代码
                var endYear = today.getFullYear();
                var endMonth = today.getMonth();
                var endDate = today.getDate();
                endMonth = analysisMnf.doHandleMonth(endMonth + 1);
                endDate = analysisMnf.doHandleMonth(endDate);
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
                vMonth = analysisMnf.doHandleMonth(vMonth + 1);
                vDate = analysisMnf.doHandleMonth(vDate);
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
                    vendMonth = analysisMnf.doHandleMonth(vendMonth + 1);
                    vendDate = analysisMnf.doHandleMonth(vendDate);
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
            //     analysisMnf.getsTheCurrentTime();
            // } else if (number == -1) {
            //     analysisMnf.startDay(-1)
            // } else if (number == -3) {
            //     analysisMnf.startDay(-3)
            // } else if (number == -7) {
            //     analysisMnf.startDay(-7)
            // };
            // if (num != 1) {
            //     $('#timeInterval').val(startTime + '--' + endTime);
            // }
            if (!analysisMnf.validates()) {
                return;
            }
            // analysisMnf.estimate();
            dataListArray = [];
            var url = "/analysis/flowdata_mnf/";

            var data = {"organ": organ,"station":station,"qmonth":number, 'startTime': sTime, "endTime": eTime};
            json_ajax("POST", url, "json", false, data, analysisMnf.findOnline);     //发送请求
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
            analysisMnf.getsTheCurrentTime();
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
            var online = "";
            if (data.obj != null && data.obj != "") {
                online = data.obj.online;
            }
            if (data.success == true) {
                // carLicense = [];
                // activeDays = [];
                hdates = [];
                dosages = [];
                maxflows = [];
                averages = [];
                for (var i = 0; i < online.length; i++) {
                    list =
                        [i + 1, online[i].hdate,
                            online[i].color,
                            online[i].dosage,
                            // online[i].allDays == null ? "0" : online[i].allDays,
                            online[i].ratio == null ? "0" : online[i].ratio,
                            online[i].assignmentName == null ? "无" : online[i].assignmentName,
                            // online[i].professionalNames == "" ? "无" : online[i].professionalNames,
                            online[i].maxflow,
                            online[i].average,
                            
                        ]

                    dataListArray.push(list);                                       //组装完成，传入  表格
                };
                for (var j = 0; j < dataListArray.length; j++) {// 排序后组装到图表
                    hdates.push(dataListArray[j][1]);
                    dosages.push(dataListArray[j][3]);
                    maxflows.push(dataListArray[j][6]);
                    averages.push(dataListArray[j][7]);
                }
                console.log(dosages);
                console.log(hdates);

                // analysisMnf.reloadData(dataListArray);
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
                maxflows = [];
                averages = [];
                maxflows.push("");
                averages.push("");
            }
            var start;
            var end;
            var length;
            length = online.length;
            if (length < 4) {
                barWidth = "30%";
            } else if (length < 6) {
                barWidth = "20%";
            } else {
                barWidth = null;
            }
            ;
            if (length <= 20) {
                start = 0;
                end = 100;
            } else {
                start = 0;
                end = 100 * (20 / length);
            }
            ;
            // wjk
            //carLicense = analysisMnf.platenumbersplitFun(carLicense);
            var option = {
                tooltip: {
                    trigger: 'axis',
                    textStyle: {
                        fontSize: 20
                    },
                    formatter: function (a) {
                        var relVal = "";
                        //var relValTime = a[0].name;
                        var relValTime  =hdates[a[0].dataIndex];
                        if (a[0].data == 0) {
                            relVal = "无相关数据";
                            relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[0].color + "'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                        } else {
                            relVal = relValTime;
                            relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[0].color + "'></span>" + a[0].seriesName + "：" + a[0].value + " m³/h";
                        }
                        ;
                        return relVal;
                    }
                },
                legend: {
                    data: ['MNF','最大流量','平均流量'],
                    left: 'auto',
                },
                toolbox: {
                    show: false
                },
                grid: {
                    left: '120',
                    bottom:'100'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,  // 让折线图从X轴0刻度开始
                    name: "",
                    axisLabel: {
                        show: true,
                        interval: 0,
                        rotate: 45
                    },
                    data: hdates //analysisMnf.platenumbersplitFun(hdates)
                },
                yAxis: [
                    {
                        type: 'value',
                        name: '瞬时流量 （m³/h）',
                        scale: false,
                        position: '',
                        axisLabel: {
                            formatter: '{value}'
                        },
                        splitLine: {
                            show: true
                        }
                    },
                ],
                // dataZoom: [{
                //     type: 'inside',
                //     start: start,
                //     end: end
                // }, {

                //     show: true,
                //     height: 20,
                //     type: 'slider',
                //     top: 'top',
                //     xAxisIndex: [0],
                //     start: 0,
                //     end: 10,
                //     showDetail: false,
                // }],
                series: [
                    {
                        name: 'MNF',
                        yAxisIndex: 0,
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#6dcff6'
                            }
                        },
                        data: dosages
                    },
                    {
                        name: '最大流量',
                        yAxisIndex: 0,
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#422d0c'
                            }
                        },
                        data: maxflows
                    },
                    {
                        name: '平均流量',
                        yAxisIndex: 0,
                        xAxisIndex: 0,
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#e00d1f'
                            }
                        },
                        data: averages
                    }
                ]
            };
            myChart.setOption(option);
            console.log('max:',maxflows[0]);
            $("#maxflow span").html( maxflows[0]);
            $("#averflow span").html( averages[0]);
            window.onresize = myChart.resize;
        },
        platenumbersplitFun:function(arr){
            var newArr = [];
            arr.forEach(function(item){
                if (item.length > 8) {
                    item = item.substring(0,7) + '...'
                }
                newArr.push(item)
            })
            return newArr
        }
    }
    $(function(){
        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('treeDemo',id,'group');
            };
        });
        
        analysisMnf.userTree();
        
        analysisMnf.init();
        analysisMnf.inquireClick(1);
        // analysisMnf.findOperation();
        // IE9
        if(navigator.appName=="Microsoft Internet Explorer" && navigator.appVersion.split(";")[1].replace(/[ ]/g,"")=="MSIE9.0") {
            analysisMnf.refreshTable();
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
        // $("#selectAll").bind("click", analysisMnf.selectAll);
        // 组织架构模糊搜索
        $("#search_condition").on("input oninput",function(){
            search_ztree('treeDemo', 'search_condition','group');
        });       
        
        
        $("#addId").on("click",analysisMnf.addId);
        $("#closeAdd").on("click",analysisMnf.closeClean);
        $("#updateClose").on("click",analysisMnf.updateClean);
    })
})($,window)
