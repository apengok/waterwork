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
    // http://echartsjs.com/vendors/echarts/map/json/province/anhui.json
    
    var biaowu = {
        //测试数据
        ceshi: function(){
            // biaowu.hotspoteChart(hotspoteChartData,geoCoordMap);
            biaowu.pieChart();
            biaowu.waterattrPie();
            
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
        
        // 水力分布图
        hydropowerChart:function() {
            var convertData = function (data) {
                var res = [];
                for (var i = 0; i < data.length; i++) {
                    var geoCoord = provinceCoordMap[data1[i].name];
                    if (geoCoord) {
                        res.push({
                            name: data[i].name,
                            value: geoCoord.concat(data1[i].value)
                        });
                    }
                }
                return res;
            };
            var name = 'hn';

            // myChart.showLoading();
            var uploadedDataURL = "/echarts/map/province/anhui.json";
            var hydropowerChart = echarts.init(document.getElementById('hydropowerChart'));

            $.get(uploadedDataURL, function(geoJson) {

                // myChart.hideLoading();
                g = JSON.parse(geoJson);
                var jsonobj = [],tmpobj={};
                if(g.features.length > 0 ){
                    for(var i = 0;i < g.features.length;i++){
                        name = g.features[i].properties.name;
                        cp = g.features[i].properties.cp;
                        tmpobj[name] = cp;
                    }
                    jsonobj.push(tmpobj);
                    console.log(jsonobj)
                }

                console.log(provinceCoordMap)
                provinceCoordMap = JSON.stringify(jsonobj)

                echarts.registerMap(name, geoJson);

                hydropowerChart.setOption(option = {
                   
                    title: {
                        text: "安徽省",
                        left: 'left'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        left: 'left',
                        // data: ['强', '中', '弱'],
                        // textStyle: {
                        //     color: '#ccc'
                        // }
                    },
                    //                 backgroundColor: {
                    //     type: 'linear',
                    //     x: 0,
                    //     y: 0,
                    //     x2: 1,
                    //     y2: 1,
                    //     colorStops: [{
                    //         offset: 0, color: '#0f2c70' // 0% 处的颜色
                    //     }, {
                    //         offset: 1, color: '#091732' // 100% 处的颜色
                    //     }],
                    //     globalCoord: false // 缺省为 false
                    // },
                    
                    series: [{
                        type: 'map',
                        mapType: name,
                        label: {
                            normal: {
                                show: true
                            },
                            emphasis: {
                                textStyle: {
                                    color: '#fff'
                                }
                            }
                        },
                        // itemStyle: {
                        //     normal: {
                        //         areaColor: '#031525',
                        //         borderColor: '#3B5077',
                        //         borderWidth: 1
                        //     },
                        //     emphasis: {
                        //         areaColor: '#0f2c70'
                        //     }
                        // },
                        animation: false,
                        
                    data:[
                        {name: '豪州市', value: 100},
                        {name: '淮北市', value: 10},
                        {name: '宿州市', value: 20},
                        {name: '阜阳市', value: 30},
                        {name: '蚌埠市', value: 40},
                        {name: '淮南市', value: 41},
                        {name: '滁州市', value: 15},
                        {name: '合肥市', value: 25},
                        {name: '六安市', value: 35},
                        {name: '马鞍山市', value: 35},
                        {name: '芜湖市', value: 35},
                        {name: '铜陵市', value: 35},
                        {name: '宣城市', value: 35},
                        {name: '池州市', value: 35},
                        {name: '安庆市', value: 35},
                        {name: '黄山市', value: 35},
                        
                    ]
                            
                    },
                    {
                        name: '城市',
                        type: 'scatter',
                        coordinateSystem: 'geo',
                        data: convertData(data1),
                        symbolSize: function (val) {
                            return val[2] / 20;
                        },
                        label: {
                            normal: {
                                formatter: '{b}',
                                position: 'right',
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: '#ddb926'
                            }
                        }
                    },
                    {
                       type: 'effectScatter',
                       coordinateSystem: 'geo',
                       data: [
                            {name: '豪州市', value: 100},
                            {name: '淮北市', value: 10},
                            {name: '宿州市', value: 20},
                            {name: '阜阳市', value: 30},
                            {name: '蚌埠市', value: 40},
                            {name: '淮南市', value: 41},
                            {name: '滁州市', value: 15},
                            {name: '合肥市', value: 25},
                            {name: '六安市', value: 35},
                            {name: '马鞍山市', value: 35},
                            {name: '芜湖市', value: 35},
                            {name: '铜陵市', value: 35},
                            {name: '宣城市', value: 35},
                            {name: '池州市', value: 35},
                            {name: '安庆市', value: 35},
                            {name: '黄山市', value: 35},
                            
                        ],
                       symbolSize: function (val) {
                           return val[2] / 10;
                       },
                       showEffectOn: 'render',
                       rippleEffect: {
                           brushType: 'stroke'
                       },
                       hoverAnimation: true,
                       label: {
                           normal: {
                               formatter: '{b}',
                               position: 'right',
                               show: true
                           }
                       },
                       itemStyle: {
                           normal: {
                               color: '#f4e925',
                               shadowBlur: 10,
                               shadowColor: '#333'
                           }
                       },
                       zlevel: 1
                   }],
                    
                });
            });


        },
        // 水力分布流量和压力图标
        hydropressflowChart:function(){

            options = [{
                backgroundColor: '#FFFFFF',
                title: {
                    text: '流量曲线图',
                    left:'left'
                },
                // tooltip: {
                //     trigger: 'axis',
                //     axisPointer: { // 坐标轴指示器，坐标轴触发有效
                //         type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                //     }
                // },
                
                legend: {
                    data: ['流量']
                },
                    grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                    },
                
                xAxis: [{
                    type: 'category',
                     boundaryGap: false,
                    //show:false,
                    data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','20','31','32','33','34','35','36','37','38','39','40']
                }],
                yAxis: {
                    type: 'value',
                    //show:false,
                    name: '流量',
                    // min: 0,
                    // max: 10,
                    interval: 10,
                },
                series: [{
                    name: 'flow',
                    type: 'line',
                    itemStyle: {
                        normal: {
                            color: '#7acf88',
                            areaStyle:{type:'default'}
                        },
                    },
                    // markPoint: {
                    //     data: [{
                    //             type: 'max',
                    //             name: '最大值'
                    //         },
                    //         {
                    //             type: 'min',
                    //             name: '最小值'
                    //         }
                    //     ]
                    // },
                    // markLine: {
                    //     data: [{
                    //         type: 'average',
                    //         name: '平均值'
                    //     }]
                    // },
                    data: [4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0,4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0]
                }]
            }, 
            {
                backgroundColor: '#FFFFFF',
                title: {
                    text: '压力曲线图',
                    left:'left'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['压力']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    //show:false,
                    data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','20','31','32','33','34','35','36','37','38','39','40']
                },
                yAxis: {
                    type: 'value',
                    //show:false,
                    name: '压力',
                    min: 0,
                    max: 10,
                    interval: 10,
                },
                series: [{
                        name: '同比',
                        type: 'line',
                        itemStyle: {
                            normal: {
                                color: '#eb8c82',
                                areaStyle:{type:'default'}
                            },
                        },
                        stack: '总量',
                        data: [4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0,4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0]

                    }
                ]
            }];

            var hydroflow = echarts.init(document.getElementById('hydroflow'));
            hydroflow.setOption(options[0]);
            var hydropress = echarts.init(document.getElementById('hydropress'));
            hydropress.setOption(options[1]);
        },
        // 大用户排行榜
        bigUserOrderly:function(){
            "use strict";
            var one1 ='<input style=" border:none; width: 28px;text-align:center;" value="1" readonly="true">';
            var one2 ='<input style=" border:none; width: 100%; margin-right:150px;text-align:center" value="徽州学校" readonly="true">';
            var one3 ='<input style=" border:none;  width: 100%;text-align:center" value="古城区" readonly="true">';
            var one4 ='<input type="text" style="-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width: 65px;border:none;text-align:center; background-color:#0099ff;color:#ffffff;" value="居民用水" readonly="true">'
            var one5 ='<input style=" border:none; width: 100%;text-align:center" value="5198.12" readonly="true">';
            var one6 ='<input style=" border:none; width: 100%;text-align:center" value="4.45" readonly="true">';
            
            var two1 ='<input style=" border:none; width:  28px;text-align:center;" value="2" readonly="true">';
            var two2 ='<input style=" border:none; width: 100%;text-align:center" value="黄山金磊新材料有限公司" readonly="true">';
            var two3 ='<input style=" border:none;  width:100%;text-align:center" value="城西工业区" readonly="true">';
            var two4 ='<input type="text" style="left:-30px;-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width:65px;border:none;text-align:center; background-color:#FF3300;color:#ffffff;" value="工业用水" readonly="true">'
            var two5 ='<input style=" border:none; width: 100%;text-align:center" value="4337.12" readonly="true">';
            var two6 ='<input style=" border:none; width: 100%;text-align:center" value="3.45" readonly="true">';       
           var e = [{
                rank: one1,
                client_name: one2,
                belongto: one3,
                watertype: one4 ,
                year_use: one5,
                zhanbi: one6
            }, 
            {
                rank: two1,
                client_name: two2,
                belongto: two3,
                watertype: two4,
                year_use: two5,
                zhanbi: two6
            },
            {
                rank: two1,
                client_name: two2,
                belongto: two3,
                watertype: two4,
                year_use: two5,
                zhanbi: two6
            },
             {
                rank: two1,
                client_name: two2,
                belongto: two3,
                watertype: two4,
                year_use: two5,
                zhanbi: two6
            },
             {
                rank: two1,
                client_name: two2,
                belongto: two3,
                watertype: two4,
                year_use: two5,
                zhanbi: two6
            },
             {
                rank: two1,
                client_name: two2,
                belongto: two3,
                watertype: two4,
                year_use: two5,
                zhanbi: two6
            },
            ];
            $("#exampleTableFromData").bootstrapTable({
                data: e,
                classes: 'table table-condensed table-no-bordered', 
                striped: false,
                height: "300"
            })
         
        },

        // 行业用水统计
        WWaterTypeUseOrderly:function(){
            "use strict";

             var progressstr1 = '<div class="progress" style="background-color:orange;width: 300px;">'+
                                  '<div class="progress-bar"   role="progressbar" style="width: 25%;background-color:#ff3266;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'+
                                '</div>';
            var progressstr2 = '<div class="progress" style="background-color:orange;width: 300px;">'+
                                  '<div class="progress-bar" role="progressbar" style="width: 35%;background-color:#0099ff;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'+
                                '</div>'
            var progressstr3 = '<div class="progress" style="background-color:orange;">'+
                                  '<div class="progress-bar" role="progressbar" style="width: 45%;background-color:#99cd00;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'+
                                '</div>'
            var progressstr4 = '<div class="progress" style="background-color:orange;">'+
                                  '<div class="progress-bar" role="progressbar" style="width: 5%;background-color:#cd66ff;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>'+
                                '</div>'                           
            var e = [
            {
                
                watertype: "居民用水",
                year_use: "5198.12",
                zhanbi: progressstr1
            }, 
            {
                watertype: "工业用水",
                year_use: "4337.12",
                zhanbi: progressstr2
            },{
                
                watertype: "特种行业用水",
                year_use: "5198.12",
                zhanbi: progressstr3
            }, 
            {
                watertype: "其他",
                year_use: "4337.12",
                zhanbi: progressstr4
            },];
            $("#waterusestatistic").bootstrapTable({
                data: e,
                classes: 'table table-condensed table-no-bordered', 
                striped: false,
                height: "300"
            })
            $("#waterusestatistic").bootstrapTable('hideLoading')
        },

        // 资产大数据图表
        realassetsForm:function(){
            var option = {
                tooltip: {
                    trigger: 'axis',
                    textStyle: {
                        fontSize: 20
                    },
                    // formatter: function (a) {
                    //     // console.log(a);
                    //     var tsale = parseFloat(a[0].value)*10000;
                    //     var tuncount = parseFloat(a[1].value)*10000;
                    //     var tleak = parseFloat(a[2].value)*10000;
                    //     var ttotal = tsale + tuncount + tleak;
                    //     var tleak_percent = 0;
                    //     if (ttotal == 0){
                    //         tleak_percent = 0
                    //     }else{
                    //         tleak_percent = (tleak/ttotal)*100;
                    //     }
                        
                    //     var relVal = "";
                    //     //var relValTime = a[0].name;
                    //     relVal = hdates[a[0].dataIndex] + ' 月';
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:grey'></span>供水量:" + ttotal.toFixed(2) + " m³";
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[0].color + "'></span>" + a[0].seriesName + "：" + tsale.toFixed(2) + " m³";
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[1].color + "'></span>未计费水量：" + tuncount.toFixed(2) + " m³";
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[2].color + "'></span>" + a[2].seriesName + "：" + tleak.toFixed(2) + " m³";
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:" + a[3].color + "'></span>" + a[3].seriesName + "：" + a[3].value[1] + "%";
                    //     relVal += "<br/><span style='display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:red'></span>漏损率:" + tleak_percent.toFixed(2) + "%";

                        
                    //     return relVal;
                    // }
                },
                legend: {
                    data: ['长度','大表数量'],
                    left: 'auto',
                },
                toolbox: {
                    show: false
                },
                grid: {
                    left: '80',
                    bottom:'50',
                    right:'80'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,  // 让折线图从X轴0刻度开始
                    name: "",
                    axisLabel: {
                        show: true,
                        interval: 0,
                        rotate: 0
                    },
                    axisTick:{
                        show:true,
                        inside:true,
                        length:200,
                        alignWithLabel:true ,    //让柱状图在坐标刻度中间
                        lineStyle: {
                            color: 'grey',
                            type: 'dashed',
                            width: 0.5
                        }
                    },
                    splitLine: {
                        show: false,
                        offset:5,
                        lineStyle: {
                            color: 'grey',
                            type: 'dashed',
                            width: 0.5
                        }
                    },
                    data: [40,50,80,100,150,200,250,300,400,500,600,800]
                },
                yAxis: [
                    {
                        type: 'value',
                        name: '总长度 （万m）',
                        nameTextStyle:{
                            color: 'black',
                            fontFamily: '微软雅黑 Bold',
                            fontSize: 14,
                            fontStyle: 'normal',
                            fontWeight: 700
                        },
                        nameLocation:'middle',
                        nameGap:60,
                        scale: false,
                        position: 'left',

                        axisTick : {    // 轴标记
                            show:false,
                            length: 10,
                            lineStyle: {
                                color: 'green',
                                type: 'solid',
                                width: 2
                            }
                        },
                        axisLabel : {
                            show:true,
                            interval: 'auto',    // {number}
                            rotate: 0,
                            margin: 18,
                            formatter: '{value}',    // Template formatter!
                            textStyle: {
                                color: 'grey',
                                fontFamily: 'verdana',
                                fontSize: 10,
                                fontStyle: 'normal',
                                fontWeight: 'bold'
                            }

                        },
                        splitLine: {
                            show: true
                        }
                    },
                    {
                        type : 'value',
                        name :'大表数量(台)',
                        nameTextStyle:{
                            color: 'black',
                            fontFamily: '微软雅黑 Bold',
                            fontSize: 14,
                            fontStyle: 'normal',
                            fontWeight: 700
                        },
                        nameLocation:'middle',
                        nameGap:35,
                        min: 0,
                        max: 100,
                        interval: 25,
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
                        splitLine: {
                            show: false
                        },
                        offset : 18
                    }
                ],
                barGap:'1%',
                // barCategoryGap:'10%',
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
                        name: '长度',
                        yAxisIndex: 0,
                        type: 'bar',
                        // stack:'dma',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#7cb4ed'
                            }
                        },
                        data: [3,2,1,4,3,2,2,3,4,5,1,2],
                        // markLine : {
                        //   symbol : 'none',
                        //   itemStyle : {
                        //     normal : {
                        //       color:'#1e90ff',
                        //       label : {
                        //         show:true
                        //       }
                        //     }
                        //   },
                        //   data : [{type : 'average', name: '平均值'}]
                        // }
                    },
                    {
                        name: '大表数量',
                        yAxisIndex: 1,
                        type: 'bar',
                        // stack:'dma',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            normal: {
                                color: '#474249'
                            }
                        },
                        data: [23,12,15,14,33,23,26,31,34,55,21,32]
                    }
                ]
            };

            var realassets = echarts.init(document.getElementById('realassets'));
            realassets.setOption(option);
        },
        // 抄表率readmeteratio
        readMeterRatio:function(){
            var labelTop = {
                normal : {
                    label : {
                        show : true,
                        position : 'center',
                        formatter : '{b}',
                        textStyle: {
                            baseline : 'bottom'
                        }
                    },
                    labelLine : {
                        show : false
                    }
                }
            };
            var labelFromatter = {
                normal : {
                    label : {
                        formatter : function (params){
                            return '+' + 100 - params.value + '%'
                        },
                        textStyle: {
                            baseline : 'top'
                        }
                    }
                },
            }
            var labelBottom = {
                normal : {
                    color: '#ccc',
                    label : {
                        show : true,
                        position : 'center'
                    },
                    labelLine : {
                        show : false
                    }
                },
                emphasis: {
                    color: 'rgba(0,0,0,0)'
                }
            };
            var radius = [50, 55];
            option = {
                legend: {
                    x : 'center',
                    y : 'bottom',
                    // show:false,
                    itemGap:80,
                    data:[
                        '抄表率','大表故障率','抄表率2'
                    ]
                },
                clockWise:true,
                // title : {
                //     text: 'The App World',
                //     subtext: 'from global web index',
                //     x: 'center'
                // },
                
                series : [
                    {
                        type : 'pie',
                        center : ['20%', '40%'],
                        radius : radius,
                        x: '0%', // for funnel
                        itemStyle : labelFromatter,
                        data : [
                            {name:'other', value:46, itemStyle :labelBottom  },
                            {name:'抄表率', value:54,itemStyle : labelTop}
                        ]
                    },
                    {
                        type : 'pie',
                        center : ['50%', '40%'],
                        radius : radius,
                        x:'20%', // for funnel
                        itemStyle : labelFromatter,
                        data : [
                            {name:'other', value:56, itemStyle : labelBottom},
                            {name:'大表故障率', value:44,itemStyle : labelTop}
                        ]
                    },
                    {
                        type : 'pie',
                        center : ['80%', '40%'],
                        radius : radius,
                        x:'40%', // for funnel
                        itemStyle : labelFromatter,
                        data : [
                            {name:'other', value:65, itemStyle : labelBottom},
                            {name:'抄表率2', value:35,itemStyle : labelTop}
                        ]
                    }
                ]
            };
            var readmeteratio = echarts.init(document.getElementById('readmeteratio'));
            readmeteratio.setOption(option);
        },
          // 二级分区漏损排行榜
        dma2leakage:function(){
            "use strict";
            var one6 ='<input type="text" style="-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width: 50px;border:none;text-align:center; background-color:#008100;color:#ffffff;" value="4.45" readonly="true">'
            var two6 ='<input type="text" style="-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width: 50px;border:none;text-align:center; background-color:#008100;color:#ffffff;" value="3.45" readonly="true">'
      
            
            var e = [{
                rank: "1",
                client_name: "徽州学校",
                belongto: "古城区",
                watertype: "居民用水",
                year_use: "5198.12",
                zhanbi:one6
            }, 
            {
                rank: "2",
                client_name: "黄山金磊新材料有限公司",
                belongto: "城西工业区",
                watertype: "工业用水",
                year_use: "4337.12",
                zhanbi: two6
            },];
            $("#dma2leakage").bootstrapTable({
                data: e,
                classes: 'table table-condensed table-no-bordered', 
                striped: false,
                height: "300"
            })
            $("#dma2leakage").bootstrapTable('hideLoading')
        },
        // 三级分区漏损排行榜
        dma3leakage:function(){
            "use strict";
            var one6 ='<input type="text" style="-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width: 50px;border:none;text-align:center; background-color:#008100;color:#ffffff;" value="4.45" readonly="true">'
            var two6 ='<input type="text" style="-moz-border-radius: 4px;-webkit-border-radius: 4px; border-radius: 4px;width: 50px;border:none;text-align:center; background-color:#008100;color:#ffffff;" value="3.45" readonly="true">'
      
            var e = [{
                rank: "1",
                client_name: "徽州学校",
                belongto: "古城区",
                watertype: "居民用水",
                year_use: "5198.12",
                zhanbi: one6
            }, 
            {
                rank: "2",
                client_name: "黄山金磊新材料有限公司",
                belongto: "城西工业区",
                watertype: "工业用水",
                year_use: "4337.12",
                zhanbi: two6
            },];
            $("#dma3leakage").bootstrapTable({
                data: e,
                classes: 'table table-condensed table-no-bordered', 
                striped: false,
                height: "300"
            })
            $("#dma3leakage").bootstrapTable('hideLoading')
        },

        //初始化
        init: function(){
            //初始化文件树
            var treeSetting = {
                async : {
                    url : "/dmam/district/dmatree/",
                    tyoe : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                    otherParam : {  // 是否可选  Organization 
                        "isOrg" : "1"
                    },
                },
                check: {
                    enable: true,
                    chkStyle: "radio",
                    chkboxType: {
                        "Y": "s",
                        "N": "s"
                    },
                    radioType: "all"
                },
                view : {
                    selectedMulti : false,
                    nameIsHTML: true, 
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    onClick : biaowu.zTreeOnClick,
                    onCheck: biaowu.onCheck,
                    onAsyncSuccess: biaowu.zTreeOnAsyncSuccess
                }
            };
            $.fn.zTree.init($("#treeDemo"), treeSetting, null);
        },
        //组织树点击事件
        zTreeOnClick: function(event, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            var isFlag = treeNode.checked;
            zTree.checkNode(treeNode, true, null, true);
            if(isFlag){
                biaowu.onCheck(event, treeId, treeNode);
            };
        },
        onCheck: function(e, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo"), nodes = zTree
                     .getCheckedNodes(true), v = "";
            zTree.checkNode(treeNode, true, null, true);
            for (var i = 0, l = nodes.length; i < l; i++) {
                 v += nodes[i].name + ",";
            };

            if($(".panel-body").is(":hidden")){
                $(".panel-body").show();
            }
            // 初始化企业数据
            var checkGroupNode = zTree.getCheckedNodes();
            if (checkGroupNode != null && checkGroupNode.lengtt != 0) {
                $("#selectGroup").html(checkGroupNode[0].name);
            }
            //调用后台取数据
            var url="getBigDataReportData";
            var parameter={"groupId": checkGroupNode[0].uuid};
            json_ajax("POST",url,"json",true,parameter, biaowu.reportDataCallback);
            
            $("#monment").hide();
         },
         zTreeOnAsyncSuccess:function (event, treeId, msg) {
             // 默认选择第一个节点
             var zTree = $.fn.zTree.getZTreeObj("treeDemo");
             var nodes = zTree.getNodes();
             zTree.expandNode(nodes[0], true);// 展看第一个节点
             var nodeArr = zTree.transformToArray(nodes);
             zTree.checkNode(nodes[0], true, true);
            // 初始化企业数据
            var checkGroupNode = zTree.getCheckedNodes();
            if (checkGroupNode != null && checkGroupNode.length != 0) {
                $("#selectGroup").html(checkGroupNode[0].name);
            }else{
                $("#selectGroup").html(nodes[0].name);
            }
            //调用后台取数据
            var url="getBigDataReportData";
            var parameter={"groupId": checkGroupNode[0].uuid};
            json_ajax("POST",url,"json",true,parameter, biaowu.reportDataCallback);
         },
        
        //选择组织
        checkGroup: function(){
            $("#monment").show();
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
        //隐藏组织树
        hideGroup: function(event){
            if (!(event.target.id == "treeDemo" || event.target.id == "monment" || $(event.target).parents("#checkGroup").length>0 || $(event.target).parents("#monment").length>0)) {
                $("#monment").hide();
            };
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
        // biaowu.init();
        biaowu.ceshi();
        // $("#checkGroup").bind("click",biaowu.checkGroup);
        $(document).bind('click',biaowu.hideGroup);
        $(window).resize(biaowu.windowResize);
    })
})($,window)
