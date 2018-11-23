//# sourceURL=biaowu.js
(function($,window){
    var dateForMonth = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'];
    var hostMyChart;
    var mileageStatisticsData = [];
    var thisMouthData = [];
    var lastMouthData = [];
    var vehicleIds = [];
    var mileageDate;
    var mileageVSData;
    var barWidth;
    var hotspoteChartData = [];
    var cycleDate;
    var sum = 0;
    var point = 0;
    //显示隐藏列
    var menu_text = "";
    var table = $("#dataTable tr th:gt(1)");
    // http://echartsjs.com/vendors/echarts/map/json/province/anhui.json
    
    var biaowu = {
        //测试数据
        ceshi: function(){
            // biaowu.hotspoteChart(hotspoteChartData,geoCoordMap);
            biaowu.pieChart();
            biaowu.waterattrPie();
            biaowu.generalInfo();
        },
        inquireClick: function (num) {
            $(".mileage-Content").css("display", "block");  //显示图表主体
            
            dataListArray = [];
            var url = "/reports/biaowu/biaowudata/";
            // var endTime = $("#endtime").val()

            var data = {"organ": "virvo_organization_rzav_ehou_yslh","dma_no":"301","endTime": "2018-11"};
            json_ajax("POST", url, "json", false, data, biaowu.reportDataCallback);     //发送请求
        },
        reportDataCallback:function (data) {
            if (data != null) {
                if (data.success) { // 成功！
                    cycleDate = [];
                    var obj = data.obj;
                    var vehicleCount = obj.vehicleCount; // 车辆数量
                    var totalMile = obj.totalMile;  // 里程
                    var totalTravelTime = obj.totalTravelTime; // 行驶时长
                    var totalDownTime = obj.totalDownTime; // 停驶时长
                    var totalOverSpeedTimes = obj.totalOverSpeedTimes; // 超速报警次数
                    var lastTotalMile = obj.lastTotalMile;  // 里程
                    var lastTotalTravelTime = obj.lastTotalTravelTime; // 行驶时长
                    var lastTotalDownTime = obj.lastTotalDownTime; // 停驶时长
                    var lastTotalOverSpeedTimes = obj.lastTotalOverSpeedTimes; // 超速报警次数
                    var mostDiligent = obj.mostDiligent; // 最勤奋的车
                    var mostLazy = obj.mostLazy; // 最懒惰的车
                    var mostFar = obj.mostFar; // 开得最远的车
                    var mintFar = obj.mintFar; // 几乎没动的车
                    var safe = obj.safe; // 最安全的车
                    var danger = obj.danger; // 最危险的车
                    var maxMile = obj.maxMile; // 最大里程
                    var minMile = obj.minMile; // 最小里程
                    cycleDate = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'];
                    thisMouthData = [];
                    lastMouthData = [];
                    var dailyMiles = obj.dailyMile;
                    var lastDailyMiles = obj.lastDailyMile;
                    var today = new Date();
                    today = today.getDate();
                    for(var i = 0; i < cycleDate.length; i++){
                        var flagJ = false;
                        var flagK = false;
                        if(i < today){
                            if (dailyMiles != null && dailyMiles != undefined && dailyMiles.length > 0) {
                                for(var j = 0; j < dailyMiles.length; j++){
                                    // 访问接口从大数据月表接口修改为平台原来接口时,monthDay字段要修改为day.反之修改为monthDay
                                    if((dailyMiles[j].monthDay)==i){
                                        flagJ = true;
                                        var dailyMilesGpsMile=biaowu.fiterNumber(dailyMiles[j].gpsMile.toFixed(1))
                                        thisMouthData.push(dailyMilesGpsMile);
                                    }
                                }
                            }
                            if(!flagJ){
                                thisMouthData.push(0);
                            }
                        }else{
                            thisMouthData.push(null);
                        }
                        if (lastDailyMiles != null && lastDailyMiles != undefined && lastDailyMiles.length > 0) {
                            for(var k = 0; k < lastDailyMiles.length; k++){
                                // 访问接口从大数据月表接口修改为平台原来接口时,monthDay字段要修改为day.反之修改为monthDay
                                if((lastDailyMiles[k].monthDay)==i){
                                    flagK = true;
                                    var dailyMilesGpsMile=biaowu.fiterNumber(lastDailyMiles[k].gpsMile.toFixed(1))
                                    lastMouthData.push(dailyMilesGpsMile);
                                }
                            }
                        }
                        if(!flagK){
                            lastMouthData.push(0);
                        }
                    }
                    biaowu.cycleVS(cycleDate,thisMouthData,lastMouthData);
                    $("#selectTotalVehicleCount").html("<font style='font-size:18px'> "+vehicleCount + "</font> 辆");
                    totalMile=biaowu.fiterNumber(totalMile.toFixed(1));
                    totalCount=biaowu.fiterNumber((totalMile/vehicleCount).toFixed(1));
                    $("#selectTotalMile").html(totalMile+"<font style='font-size:12px'> km</font>");
                    $("#mileageAvg").html(vehicleCount!=0?"<font style='font-size:18px'> "+totalCount+"</font>km":"<font style='font-size:18px'>0</font>km");
                    $("#selectTotalTravelTime").html(biaowu.formatSeconds(totalTravelTime,true));
                    $("#avgTravelTime").html(biaowu.formatSeconds(vehicleCount!=0?(totalTravelTime/vehicleCount):0,true));
                    $("#selectTotalDownTime").html(biaowu.formatSeconds(totalDownTime,true));
                    $("#avgDownTime").html(biaowu.formatSeconds(vehicleCount!=0?(totalDownTime/vehicleCount):0,true));
                    $("#selectTotalOverSpeedTimes").html(totalOverSpeedTimes+"<font style='font-size:12px'> 次</font>");
                    reportSpeedAvgCount=biaowu.fiterNumber((totalOverSpeedTimes/vehicleCount).toFixed(1));
                    $("#reportSpeedAvg").html(vehicleCount!=0?"<font style='font-size:18px'> "+reportSpeedAvgCount+"</font>次":"<font style='font-size:18px'> "+0+"</font>次");
                    $("#mostDiligent").html(mostDiligent!=""?mostDiligent:"无");
                    $("#mostLazy").html(mostLazy!=""?mostLazy:"无");
                    $("#mostFar").html(mostFar!=""?mostFar:"无");
                    $("#mintFar").html(mintFar!=""?mintFar:"无");
                    $("#safe").html(safe!=""?safe:"无");
                    $("#danger").html(danger!=""?danger:"无");
                    maxMile=biaowu.fiterNumber(maxMile);
                    minMile=biaowu.fiterNumber(minMile);
                    $("#maxMile").html(maxMile);
                    $("#minMile").html(minMile);
                    lastTotalMile=biaowu.fiterNumber(lastTotalMile.toFixed(1));
                    $("#lastTotalMile").html(lastTotalMile);
                    $("#lastTotalTravelTime").html(biaowu.formatSeconds(lastTotalTravelTime,false));
                    $("#lastTotalDownTime").html(biaowu.formatSeconds(lastTotalDownTime,false));
                    $("#lastTotalOverSpeedTimes").html(lastTotalOverSpeedTimes);
                    totalMile=biaowu.fiterNumber(totalMile.toFixed(1));
                    $("#totalMile").html(totalMile);
                    $("#totalTravelTime").html(biaowu.formatSeconds(totalTravelTime,false));
                    $("#totalDownTime").html(biaowu.formatSeconds(totalDownTime,false));
                    $("#totalOverSpeedTimes").html(totalOverSpeedTimes);
                    var differTotalMile = totalMile - lastTotalMile;  // 里程
                    var differTotalTravelTime = totalTravelTime - lastTotalTravelTime; // 行驶时长
                    var differTotalDownTime = totalDownTime - lastTotalDownTime; // 停驶时长
                    var differTotalOverSpeedTimes = totalOverSpeedTimes - lastTotalOverSpeedTimes; // 超速报警次数
                    if(differTotalTravelTime < 0){
                        differTotalTravelTime = "，比上月少" + biaowu.formatSeconds(Math.abs(differTotalTravelTime),true);
                    }else if(differTotalTravelTime == 0){
                        differTotalTravelTime = "";
                    }else{
                        differTotalTravelTime = "，比上月多" +biaowu.formatSeconds(differTotalTravelTime,true);
                    }
                    
                    if(differTotalDownTime < 0){
                        differTotalDownTime = "，比上月少" + biaowu.formatSeconds(Math.abs(differTotalDownTime),true);
                    }else if(differTotalDownTime == 0){
                        differTotalDownTime = "";
                    }else{
                        differTotalDownTime = "，比上月多" +biaowu.formatSeconds(differTotalDownTime,true);

                    }
                    if(differTotalMile < 0){
                        differTotalMile = "，比上月少<font style='font-size:18px;color:#6dcff6'>" + Math.abs(differTotalMile.toFixed(1))+"</font>km";
                    }else if(differTotalMile == 0){
                        differTotalMile = "";
                    }else{
                        differTotalMile = "，比上月多<font style='font-size:18px;color:#6dcff6;'> " +differTotalMile.toFixed(1)+" </font>km";

                    }
                    if(differTotalOverSpeedTimes < 0){
                        differTotalOverSpeedTimes = "，比上月少<font style='font-size:18px;color:#960ba3'> " + Math.abs(differTotalOverSpeedTimes)+" </font>次";
                    }else if(differTotalOverSpeedTimes == 0){
                        differTotalOverSpeedTimes = "";
                    }else{
                        differTotalOverSpeedTimes = "，比上月多<font style='font-size:18px'>" + differTotalOverSpeedTimes+"</font>次";
                    }
                    
                    $("#differTotalMile").html(differTotalMile);
                    $("#differTotalTravelTime").html(differTotalTravelTime);
                    $("#differTotalDownTime").html(differTotalDownTime);
                    $("#differTotalOverSpeedTimes").html(differTotalOverSpeedTimes);
                    //里程对比
                    mileageDate = obj.mileCompareBrands;
                    mileageVSData = obj.mileCompareMiles;
                    vehicleIds = obj.vehicleIds;
                    biaowu.mileageVS(mileageDate,mileageVSData);
                    validVehicleCount = obj.validVehicleCount; // 有数据的车辆数量
                    // 里程月统计图表：默认显示里程对比图表中的第一辆车的数据
                    if (null != mileageDate && ""!= mileageDate && typeof(mileageDate) != undefined && typeof(mileageDate) != "undefined") {
                        var params = new Object();
                        params.name = mileageDate[0];
                        params.id = vehicleIds[0];
                        biaowu.chartsEvent(params);
                    }else{
                         // 里程对比按车清空
                        $("#travelTimeByVehicle").html("<font style='font-size:18px'> 0</font>秒"); // 行驶时长
                        $("#downTimeByVehicle").html("<font style='font-size:18px'> 0</font>秒"); // 停驶时长
                        $("#mileByVehicle").html("<font style='font-size:18px'>0</font>km"); // 行驶里程
                        $("#travelTimesByVehicle").html("<font style='font-size:18px'> 0</font>次"); // 行驶次数
                        $("#alarmTimesByVehicle").html("<font style='font-size:18px'> 0</font>次"); // 报警次数
                        $("#milePercent").html("0%"); // 里程百分比
                        //里程月统计
                        $("#curCar").text("");
                        var mileageStatisticsDate = [];
                        var mileageStatisticsData = [];
                        biaowu.mileageStatistics(mileageStatisticsDate,mileageStatisticsData);
                    }
                    var log = obj.result;
                    sum = obj.sum;
                    $("#east").text(obj.east);
                    $("#west").text(obj.west);
                    $("#north").text(obj.north);
                    $("#south").text(obj.south);
                    var list =[];
                    if(log.length == 0) {
                        $("#one").text("");
                        $("#two").text("");
                        $("#three").text("");
                        $("#four").text("");
                        $("#five").text("");
                    }else{
                        point = log.length;
                        for (var i = 0; i < log.length; i++) {
                            var name = log[i].name;
                            var count;
                            if (log.length == 1) {
                                count = (log[i].count / sum) * 100;
                                count = count < 1 ? 1 : count;
                            } else if (log.length < 10 && log.length > 1) {
                                count = (log[i].count / sum) * 500;
                                count = count < 1 ? 1 : count;
                            } else {
                                count = (log[i].count / sum) * 1000;
                                count = count < 1 ? 1 : count;
                            }
                            var map = {};
                            map["name"] = name;
                            map["value"] = count;
                            list.push(map)
                            if (i == 0) {
                                $("#one").text("1." + name);
                                if (log.length == 1) {
                                    $("#two").text("");
                                    $("#three").text("");
                                    $("#four").text("");
                                    $("#five").text("");
                                }
                            } else if (i == 1) {
                                $("#two").text("2." + name);
                                if (log.length == 2) {
                                    $("#three").text("");
                                    $("#four").text("");
                                    $("#five").text("");
                                }
                            } else if (i == 2) {
                                $("#three").text("3." + name);
                                if (log.length == 3) {
                                    $("#four").text("");
                                    $("#five").text("");
                                }
                            } else if (i == 3) {
                                $("#four").text("4." + name);
                                if (log.length == 4) {
                                    $("#five").text("");
                                }
                            } else if (i == 4) {
                                $("#five").text("5." + name);
                            }

                        }
                    }
                    hotspoteChartData = list;
                    biaowu.hotspoteChart(hotspoteChartData,geoCoordMap);
                }else{
                    layer.msg(data.msg,{move:false});
                }
            }
        },

        // 综合信息
        generalInfo:function(){
            // var content = "<table>"
            // for(i=0; i<3; i++){
            //     content += '<tr><td>' + 'result ' +  i + '</td></tr>';
            // }
            // content += "</table>"
            var table = $('<table>').addClass('table table-stripped small m-t-md');
            for(i=0; i<3; i++){
                var row = $('<tr>').text(' 沙田水厂淡水DN800 ' + i);
                table.append(row);
            }

            $('#faultRank').append(table);
        },
        
        // 使用年限饼图
        pieChart:function(){
            var legend_stastic = {};

            option = {
                title : {
                    text: '使用年限饼状图',
                    x:'left'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    y : 'center',
                    formatter:function(a){
                        console.log(a)
                        return a + ' '+ legend_stastic[a] + '%';
                    },
                    data:['2017','2016','2015','2014','2013']
                },
                
                calculable : true,
                series : [
                    {
                        name:'使用年限',
                        type:'pie',
                        radius : '35%',
                        center: ['60%', '50%'],
                        itemStyle:{
                            normal : {
                                label : {
                                    show : false,
                                    position : 'outer',
                                    formatter : function(p){
                                        // console.log(p)
                                        legend_stastic[p.name] = p.percent;
                                        return p.name + p.percent;
                                    },
                                    textStyle: {
                                        baseline : 'bottom'
                                    }
                                },
                                labelLine : {
                                    show : false
                                }
                            }
                        },
                        data:[
                            {value:335, name:'2017'},
                            {value:310, name:'2016'},
                            {value:234, name:'2015'},
                            {value:135, name:'2014'},
                            {value:1548, name:'2013'}
                        ]
                    }
                ]
            };

            var yearsPie = echarts.init(document.getElementById('yearsPie'));
            yearsPie.setOption(option);
        },

        // 用水性质饼图
        waterattrPie:function(){
            var legend_stastic = {};

            option = {
                title : {
                    text: '用水性质',
                    x:'left'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    y : 'center',
                    formatter:function(a){
                        console.log(a)
                        return a + ' '+ legend_stastic[a] + '%';
                    },
                    data:['居民用水','工业用水','特种用水','商业用水','其他用水']
                },
                
                calculable : true,
                series : [
                    {
                        name:'用水性质',
                        type:'pie',
                        radius : '35%',
                        center: ['70%', '50%'],
                        itemStyle:{
                            normal : {
                                label : {
                                    show : false,
                                    position : 'outer',
                                    formatter : function(p){
                                        // console.log(p)
                                        legend_stastic[p.name] = p.percent;
                                        return p.name + p.percent;
                                    },
                                    textStyle: {
                                        baseline : 'bottom'
                                    }
                                },
                                labelLine : {
                                    show : false
                                }
                            }
                        },
                        data:[
                            {value:335, name:'居民用水'},
                            {value:310, name:'工业用水'},
                            {value:234, name:'特种用水'},
                            {value:135, name:'商业用水'},
                            {value:154, name:'其他用水'}
                        ]
                    }
                ]
            };

            var waterattrPie = echarts.init(document.getElementById('waterattrPie'));
            waterattrPie.setOption(option);
        },
        
        // 配表初始化
        init_table: function(){
            menu_text += "<li><label><input type=\"checkbox\" checked=\"checked\" class=\"toggle-vis\" data-column=\"" + parseInt(2) +"\" disabled />"+ table[0].innerHTML +"</label></li>"
            for(var i = 1; i < table.length; i++){
                menu_text += "<li><label><input type=\"checkbox\" checked=\"checked\" class=\"toggle-vis\" data-column=\"" + parseInt(i+2) +"\" />"+ table[i].innerHTML +"</label></li>"
            };
            $("#Ul-menu-text").html(menu_text);
            //表格列定义
            var columnDefs = [ {
                //第一列，用来显示序号
                "searchable" : false,
                "orderable" : false,
                "targets" : 0
            } ];
            var columns = [
                    {
                        //第一列，用来显示序号
                        "data" : null,
                        "class" : "text-center"
                    },
                    {
                        "data":"station_name",
                        "class":"text-center",
                        render : function(data, type, row, meta) {
                            if (data != null) {
                                return data;
                            } else{
                                return "";
                            }
                        }

                    },
                     {
                        "data" : "serialnumber",
                        "class" : "text-center",
                        render : function(data, type, row, meta) {
                            if (data != null) {
                                return data;
                            } else{
                                return "";
                            }
                        }
                    }, {
                        "data" : "simid",
                        "class" : "text-center",
                        render:function(data){
                            return html2Escape(data)
                        }
                    },{
                        "data" : "dn",
                        "class" : "text-center",
                        
                    } ,
                    // {
                    //     "data" : "version",
                    //     "class" : "text-center",
                        
                    // }, 
                    {
                        "data" : "metertype",
                        "class" : "text-center",
                        render : function(data, type, row, meta){
                            if(data == "0") {
                                return "水表";
                            }else if(data == "1"){
                                return "流量计";
                            }else{
                                return data;
                            }
                        }

                    },
                    {
                        "data":"belongto",
                    },
                     {
                        "data" : "mtype",
                        "class" : "text-center",
                        render : function(data, type, row, meta){
                            if(data == "0"){
                                return "电磁水表";
                            }else if(data == "1") {
                                return "超声水表";
                            }else if(data == "2"){
                                return "机械水表";
                            }else if(data == "3"){
                                return "插入电磁";
                            }else{
                                return data;
                            }
                        }

                    },{
                        "data" : "manufacturer",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "flow_today",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "flow_yestoday",
                        "class" : "text-center",
                        
                    }, {
                        "data" : "flow_b_yestoday",
                        "class" : "text-center",
                        
                    },{
                        "data" : "flow_tomon",
                        "class" : "text-center",
                        
                    
                    },{
                        "data":"flow_yestomon",
                        "class":"text-center",
                        
                    },{
                        "data":"flow_b_yestomon",
                        "class":"text-center",
                        

                    },{
                        "data":"station",
                        "class":"text-center",
                        render : function(data, type, row, meta) {
                            if (data != null) {
                                return data;
                            } else{
                                return "";
                            }
                        }

                    }];
            //ajax参数
            var ajaxDataParamFun = function(d) {
                d.simpleQueryParam = $('#simpleQueryParam').val(); //模糊查询
                // d.groupName = selectTreeId;
                // d.groupType = selectTreeType;

            };
            //表格setting
            var setting = {
                suffix  : '/',
                listUrl : '/reports/meter/list/',
                
                columnDefs : columnDefs, //表格列定义
                columns : columns, //表格列
                dataTableDiv : 'dataTable', //表格
                ajaxDataParamFun : ajaxDataParamFun, //ajax参数
                pageable : true, //是否分页
                showIndexColumn : true, //是否显示第一列的索引列
                enabledChange : true
            };
            //创建表格
            myTable = new TG_Tabel.createNew(setting);
            //表格初始化
            myTable.init();
        },

        
        
        formatSeconds : function (value,isFormate) { // 秒转时分秒
            var theTime = parseInt(value);// 秒
            var theTime1 = 0;// 分
            var theTime2 = 0;// 小时
            if(theTime > 60) {
                theTime1 = parseInt(theTime/60);
                theTime = parseInt(theTime%60);
                if(theTime1 > 60) {
                    theTime2 = parseInt(theTime1/60);
                    theTime1 = parseInt(theTime1%60);
                }
            }
            if (isFormate) {
                var result = "<font class='dateColr' style='font-size:18px'> "+parseInt(theTime)+" </font><font style='font-size:12px'>秒</font>";
                if(theTime1 > 0) {
                    result = "<font class='dateColr' style='font-size:18px'> "+parseInt(theTime1)+" </font><font style='font-size:12px'>分</font>"+result;
                }
                if(theTime2 > 0) {
                    result = "<font class='dateColr' style='font-size:18px'> "+parseInt(theTime2)+" </font><font style='font-size:12px'>小时</font>"+result;
                }
            }else{
                var result = parseInt(theTime)+"秒";
                if(theTime1 > 0) {
                    result = parseInt(theTime1)+"分"+result;
                }
                if(theTime2 > 0) {
                    result = parseInt(theTime2)+"小时"+result;
                }
            }
            return result;
        },
        
        windowResize: function(){
            // biaowu.cycleVS(cycleDate,thisMouthData,lastMouthData);
            // biaowu.mileageVS(mileageDate,mileageVSData);
            // biaowu.mileageStatistics(dateForMonth,mileageStatisticsData);
            // biaowu.hotspoteChart(hotspoteChartData,geoCoordMap);
        },
        fiterNumber : function(data){
            if(data==null||data==undefined||data==""){
                return data;
            }else{
                var data=data.toString();
                data=parseFloat(data);
                return data;
            }
        },
        // wjk 车牌号太长显示不完截取
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
        var validVehicleCount = 0; // 有数据的车辆数量
        // biaowu.inquireClick(1);
        biaowu.init_table();
        biaowu.ceshi();
        // $("#checkGroup").bind("click",biaowu.checkGroup);
        $(document).bind('click',biaowu.hideGroup);
        $(window).resize(biaowu.windowResize);
    })
})($,window)
