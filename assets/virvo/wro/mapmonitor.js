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
    var vagueSearchlast = $("#userType").val();
    var overlay;
    var getdmamapusedata_flag = 0;
    var bindflowpressChart;

    var travelLineList,AdministrativeRegionsList,fenceIdList,
  administrativeAreaFence = [],district,googleMapLayer, buildings, satellLayer, realTimeTraffic, map, logoWidth, btnIconWidth, windowWidth,
    newwidth, els, oldMapHeight, myTabHeight, wHeight, tableHeight, mapHeight, newMapHeight, winHeight, headerHeight, dbclickCheckedId, oldDbclickCheckedId,
    onClickVId, oldOnClickVId, zTree, clickStateChar,logTime,operationLogLength, licensePlateInformation, groupIconSkin, markerListT = [], markerRealTimeT,
    zoom = 18, requestStrS, cheakNodec = [], realTimeSet = [], alarmSet = [], neverOline = [], lineVid = [], zTreeIdJson = {}, cheakdiyuealls = [], lineAr = [],
    lineAs = [], lineAa = [], lineAm = [], lineOs = [], changeMiss = [], diyueall = [], params = [], lineV = [], lineHb = [], cluster, fixedPoint = null, fixedPointPosition = null,
    flog = true, mapVehicleTimeW, mapVehicleTimeQ, markerMap, mapflog, mapVehicleNum, infoWindow, paths = null, uptFlag = true, flagState = true,
    videoHeight, addaskQuestionsIndex = 2, dbClickHeighlight = false, checkedVehicles = [], runVidArray = [], stopVidArray = [], msStartTime, msEndTime,
    videoTimeIndex,voiceTimeIndex,charFlag = true, fanceID = "", newCount = 1, mouseTool, mouseToolEdit, clickRectangleFlag = false, isAddFlag = false, isAreaSearchFlag = false, isDistanceCount = false, fenceIDMap, PolyEditorMap,
    sectionPointMarkerMap, fenceSectionPointMap, travelLineMap, fenceCheckLength = 0, amendCircle, amendPolygon, amendLine, polyFence, changeArray, trid = [], parametersID, brand, clickFenceCount = 0,
    clickLogCount = 0, fenceIdArray = [], fenceOpenArray = [], save, moveMarkerBackData, moveMarkerFenceId, monitoringObjMapHeight, carNameMarkerContentMap, carNameMarkerMap, carNameContentLUMap,
    lineSpotMap, isEdit = true, sectionMarkerPointArray, stateName = [], stateIndex = 1, alarmName = [], alarmIndex = 1, activeIndex = 1, queryFenceId = [], crrentSubV=[], crrentSubName=[],
    suFlag=true, administrationMap, lineRoute, contextMenu, dragPointMarkerMap, isAddDragRoute = false, misstype=false,misstypes = false, alarmString, saveFenceName, saveFenceType, alarmSub = 0, cancelList = [], hasBegun=[],
    isDragRouteFlag = false, flagSwitching = true, isCarNameShow = true, notExpandNodeInit,vinfoWindwosClickVid, $myTab = $("#myTab"), $MapContainer = $("#MapContainer"), $panDefLeft = $("#panDefLeft"), 
    $contentLeft = $("#content-left"), $contentRight = $("#content-right"), $sidebar = $(".sidebar"), $mainContentWrapper = $(".main-content-wrapper"), $thetree = $("#thetree"),
    $realTimeRC = $("#realTimeRC"), $goShow = $("#goShow"), $chooseRun = $("#chooseRun"), $chooseNot = $("#chooseNot"), $chooseAlam = $("#chooseAlam"), $chooseStop = $("#chooseStop"),
    $chooseOverSeep = $("#chooseOverSeep"), $online = $("#online"), $chooseMiss = $("#chooseMiss"), $scrollBar = $("#scrollBar"), $mapPaddCon = $(".mapPaddCon"), $realTimeVideoReal = $(".realTimeVideoReal"),
    $realTimeStateTableList = $("#realTimeStateTable"), $alarmTable = $("#alarmTable"), $logging=$("#logging"), $showAlarmWinMark = $("#showAlarmWinMark"), $alarmFlashesSpan = $(".alarmFlashes span"),
    $alarmSoundSpan = $(".alarmSound span"), $alarmMsgBox = $("#alarmMsgBox"), $alarmSoundFont = $(".alarmSound font"), $alarmFlashesFont = $(".alarmFlashes font"), $alarmMsgAutoOff = $("#alarmMsgAutoOff"),
    rMenu = $("#rMenu"), alarmNum = 0, carAddress, msgSNAck, setting, ztreeStyleDbclick, $tableCarAll = $("#table-car-all"), $tableCarOnline = $("#table-car-online"), $tableCarOffline = $("#table-car-offline"),
    $tableCarRun = $("#table-car-run"), $tableCarStop = $("#table-car-stop"), $tableCarOnlinePercent = $("#table-car-online-percent"),longDeviceType,tapingTime,loadInitNowDate = new Date(),loadInitTime,
    checkFlag = false,fenceZTreeIdJson = {},fenceSize,bindFenceSetChar,fenceInputChange,scorllDefaultTreeTop,stompClientOriginal = null, stompClientSocket = null, hostUrl, DblclickName, objAddressIsTrue = [];

    var dma_list = [];

    var pageLayout = {
        // 页面布局
        init: function(){
          var url = "/clbs/v/monitoring/getHost";
            // ajax_submit("POST", url, "json", true, {}, true, function(data){
            //  hostUrl = 'http://' + data.obj.host + '/F3/sockjs/webSocket';
            // });
            winHeight = $(window).height();//可视区域高度
            headerHeight = $("#header").height();//头部高度
            var tabHeight = $myTab.height();//信息列表table选项卡高度
            var tabContHeight = $("#myTabContent").height();//table表头高度
            var fenceTreeHeight = winHeight - 380;//围栏树高度
            $("#treeDemo").css('height',fenceTreeHeight + "px");//电子围栏树高度
            //地图高度
            newMapHeight = winHeight - headerHeight - tabHeight - 10;
            $MapContainer.css({
                "height": newMapHeight + 'px'
            });
            //车辆树高度
            var newContLeftH = winHeight - headerHeight;
            //sidebar高度
            $(".sidebar").css('height',newContLeftH + 'px');
            //计算顶部logo相关padding
            logoWidth = $("#header .brand").width();
            btnIconWidth = $("#header .toggle-navigation").width();
            windowWidth = $(window).width();
            newwidth = (logoWidth + btnIconWidth + 46) / windowWidth * 100;
            //左右自适应宽度
            $contentLeft.css({
                "width": newwidth + "%"
            });
            $contentRight.css({
                "width": 100 - newwidth + "%"
            });
            //加载时隐藏left同时计算宽度
            $sidebar.attr("class", "sidebar sidebar-toggle");
            //$mainContentWrapper.attr("class", "main-content-wrapper main-content-toggle-left");
            //操作树高度自适应
            var newTreeH = winHeight - headerHeight - 203;
            $thetree.css({
                "height": newTreeH + "px"
            });
            //视频区域自适应
            var mainContentHeight = $contentLeft.height();
            var adjustHeight = $(".adjust-area").height();
            videoHeight = (mainContentHeight - adjustHeight - 65) / 2;
            $(".videoArea").css("height", videoHeight + "px");
            //地图拖动改变大小
            oldMapHeight = $MapContainer.height();
            myTabHeight = $myTab.height();
            wHeight = $(window).height();
            // 页面区域定位
            $(".amap-logo").attr("href", "javascript:void(0)").attr("target", "");
            // 监听浏览器窗口大小变化
            var sWidth = $(window).width();
            if (sWidth < 1200) {
                $("body").css("overflow", "auto");
                $("#content-left,#panDefLeft").css("height", "auto");
                $panDefLeft.css("margin-bottom", "0px");
                if (sWidth <= 414) {
                    $sidebar.removeClass("sidebar-toggle");
                    $mainContentWrapper.removeClass("main-content-toggle-left");
                }
            } else {
                $("body").css("overflow", "hidden");
            };
            window.onresize=function(){
              winHeight = $(window).height();//可视区域高度
              headerHeight = $("#header").height();//头部高度
                var tabHeight = $myTab.height();//信息列表table选项卡高度
                var tabContHeight = $("#myTabContent").height();//table表头高度
                var fenceTreeHeight = winHeight - 193;//围栏树高度
                $("#treeDemo").css('height',fenceTreeHeight + "px");//电子围栏树高度
                //地图高度
                newMapHeight = winHeight - headerHeight - tabHeight - 10;
                $MapContainer.css({
                    "height": newMapHeight + 'px'
                });
                //车辆树高度
                var newContLeftH = winHeight - headerHeight;
                //sidebar高度
                $(".sidebar").css('height',newContLeftH + 'px');
                //计算顶部logo相关padding
                logoWidth = $("#header .brand").width();
                btnIconWidth = $("#header .toggle-navigation").width();
                windowWidth = $(window).width();
                newwidth = (logoWidth + btnIconWidth + 46) / windowWidth * 100;
                //左右自适应宽度
                $contentLeft.css({
                    "width": newwidth + "%"
                });
                $contentRight.css({
                    "width": 100 - newwidth + "%"
                });
              //操作树高度自适应
                var newTreeH = winHeight - headerHeight - 203;
                $thetree.css({
                    "height": newTreeH + "px"
                });
                //视频区域自适应
                var mainContentHeight = $contentLeft.height();
                var adjustHeight = $(".adjust-area").height();
                videoHeight = (mainContentHeight - adjustHeight - 65) / 2;
                $(".videoArea").css("height", videoHeight + "px");
        }
        },
    };

    var fenceOperation = {
        
        //行政区域选择后数据处理
        getData: function (data) {
            var bounds = data.boundaries;
            if (bounds) {
                // $('#administrativeLngLat').val(bounds.join('-'));
                for (var i = 0, l = bounds.length; i < l; i++) {
                    var polygon = new AMap.Polygon({
                        map: map,
                        strokeWeight: 1,
                        strokeColor: '#CC66CC',
                        fillColor: '#CCF3FF',
                        fillOpacity: 0.5,
                        path: bounds[i]
                    });
                    // administrativeAreaFence.push(polygon);
                    map.setFitView(polygon);//地图自适应
                }
                ;
            };
            
        },
        //显示行政区域
        drawAdministration: function (data, aId, showMap) {
            var polygonAarry = [];
            if (administrationMap.containsKey(aId)) {
                var this_fence = administrationMap.get(aId);
                map.remove(this_fence);
                administrationMap.remove(aId);
            }
            ;
            for (var i = 0, l = data.length; i < 1; i++) {
                var polygon = new AMap.Polygon({
                    map: map,
                    strokeWeight: 1,
                    strokeColor: '#CC66CC',
                    fillColor: '#CCF3FF',
                    fillOpacity: 0.5,
                    path: data
                });
                polygonAarry.push(polygon);
                administrativeAreaFence.push(polygon);
            }
            ;
            administrationMap.put(aId, polygonAarry);
            map.setFitView(polygon);//地图自适应
        },
        //收缩绑定列表
        bingListClick: function () {
            if ($(this).children('i').hasClass('fa-chevron-down')) {
                $(this).children('i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
                $("#MapContainer").animate({'height': newMapHeight + "px"});
            } else {
                $(this).children('i').removeClass('fa-chevron-up').addClass('fa-chevron-down');
                var trLength = $('#dataTableBind tbody tr').length;
                $("#MapContainer").animate({'height': (winHeight - 80 - trLength * 46 - 220) + "px"});
            }
            ;
        },
        TabCarBox: function () {
            monitoringObjMapHeight = $("#MapContainer").height();
            $("#carInfoTable").hide();
            $("#dragDIV").hide();
            $("#fenceBindTable").css("display", "block");
            
            var bingLength = $('#dataTableBind tbody tr').length;
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
            var nodes = treeObj.getSelectedNodes()
            var stype = nodes[0].type;
            console.log("tree selete type ",stype);

            // var checkNode = treeObj.getCheckedNodes(true);
            // if ( 0) {
            //     $("#MapContainer").css("height", newMapHeight + 'px');
            // } else {
            //     if ($('#bingListClick i').hasClass('fa fa-chevron-down')) {
            //         if (bingLength == 0) {
            //             $("#MapContainer").css("height", newMapHeight + 'px');
            //         } else {
            //             $("#MapContainer").css('height', (newMapHeight - 80 - 30 * bingLength - 105) + 'px');
            //         }
            //         ;
            //     } else {
            //         $("#MapContainer").css("height", newMapHeight + 'px');
            //     }
            //     ;
            // };
            if(stype == "dma"){
                $("#MapContainer").css('height', (newMapHeight - 80 - 30 * bingLength - 105) + 'px');
                $("#fenceBindTable").show();
                // findOperation.fenceBind();
            }
            else{
                // $("#fenceBindTable").hide();
                $("#MapContainer").css("height", newMapHeight + 'px');
                $("#searchBtn").hide()
                $("#searchInput").hide()

                // if ($('#bingListClick i').hasClass('fa fa-chevron-down')){
                //     $("#MapContainer").animate({'height': newMapHeight + "px"});
                // }
                
            }
            // $("#MapContainer").css('height', (newMapHeight - 80 - 44 * bingLength - 205) + 'px');
            // 订阅电子围栏
            // if (clickFenceCount == 0) {
            //     webSocket.subscribe(headers, "/user/" + $("#userName").text() + '/fencestatus', fenceOperation.updataFenceData, null, null);
            // };
            clickFenceCount = 1;
        },
        //围栏绑定
        fenceBind: function (fenceId, fenceName, fenceInfoId, fenceIdstr) {
            // fenceOperation.clearFenceBind();
            $("#fenceID").val(fenceId);
            $("#fenceName").val(fenceName);
            $("#fenceInfoId").val(fenceInfoId);
            // pageLayout.closeVideo();
            $("#fenceBind").modal('show');
            
            // json_ajax("post", '/clbs/m/functionconfig/fence/bindfence/getVehicleIdsByFenceId', "json", false, {"fenceId": fenceIdstr}, function (data) {
            //     oldFencevehicleIds = data.obj;
            // })
            return false;
        },
    }



    mapMonitor = {
         // 地图初始化
        amapinit: function () {
            console.log("$newMapHeight",$("#MapContainer").height());
            $contentLeft.css({
                "height": newMapHeight + "px",
            });
            console.log("$contentLeft",$contentLeft.height());
            var newContLeftH = winHeight - headerHeight ;

            $("#sidebar").css({
                "height": newMapHeight + "px"
            });
            console.log("$sidebar height",$(".sidebar").height());

            // $("#treeDemo").css({
            //     "height": 388 + "px"
            // });
            // 创建地图
            map = new AMap.Map("MapContainer", {
                resizeEnable: true,   //是否监控地图容器尺寸变化
                zoom: 18,       //地图显示的缩放级别
            });
            // // 输入提示
            // var startPoint = new AMap.Autocomplete({
            //     input: "startPoint"
            // });
            // startPoint.on('select', fenceOperation.dragRoute);
            // var endPoint = new AMap.Autocomplete({
            //     input: "endPoint"
            // });
            // endPoint.on('select', fenceOperation.dragRoute);
            // 行政区划查询
            adcode = $("#entadcode").val()
            if(adcode != ""){
                var entislocation = $("#entislocation").val()
                var entdistrictlevel = $("#entdistrictlevel").val()

                console.log(entislocation,entdistrictlevel,adcode)
                var opts = {
                    subdistrict: 0,   //获取边界不需要返回下级行政区
                    extensions: 'all',  //返回行政区边界坐标组等具体信息
                    level: 'district'  //查询行政级别为 市
                };
                district = new AMap.DistrictSearch(opts);//注意：需要使用插件同步下发功能才能这样直接使用
                district.search('china', function (status, result) {
                    console.log(status,result,result.districtList[0])
                    if (status == 'complete') {
                        fenceOperation.getData(result.districtList[0]);
                    }
                });
            }
            // 地图移动结束后触发，包括平移和缩放
            mouseTool = new AMap.MouseTool(map);
            // mouseTool.on("draw", fenceOperation.createSuccess);
            mouseToolEdit = new AMap.MouseTool(map);
            // 实例化3D楼块图层
            buildings = new AMap.Buildings();
            // 在map中添加3D楼块图层
            buildings.setMap(map);
            // 地图标尺
            var mapScale = AMap.plugin(['AMap.ToolBar', 'AMap.Scale'], function () {
                map.addControl(new AMap.ToolBar());
                map.addControl(new AMap.Scale());
            });
            // 卫星地图
            satellLayer = new AMap.TileLayer.Satellite();
            satellLayer.setMap(map);
            satellLayer.hide();
            // // 实时路况
            // realTimeTraffic = new AMap.TileLayer.Traffic({zIndex: 1});
            // realTimeTraffic.setMap(map);
            // realTimeTraffic.hide();
            // 当范围缩小时触发该方法
            // var clickEventListener = map.on('zoomend', amapOperation.clickEventListener);
            // 当拖拽结束时触发该方法
            // var clickEventListener2 = map.on('dragend', amapOperation.clickEventListener2);
            // 地图点击隐藏车辆树右键菜单
            map.on("click", function () {
                $("#rMenu").css("visibility", "hidden");
                $("#disSetMenu").slideUp();
                $("#mapDropSettingMenu").slideUp();
                $("#fenceTool>.dropdown-menu").hide();
            });
            infoWindow = new AMap.InfoWindow({isCustom: true, offset: new AMap.Pixel(100, -100), closeWhenClickMap: true});

            mapMonitor.loadGeodata(0)
        },

        loadGeodata:function(dflag){
            dma_no = $("#current_dma_no").val();
            current_organ = $("#current_organ_id").val()
            map.clearMap();
            map.remove(dma_list)
            dma_list=[]
            $.ajax({
                type: 'POST',
                url: '/gis/fence/bindfence/getDMAFenceDetails/',
                data: {"dma_no" : dma_no,"current_organ":current_organ,"dflag":dflag},
                async:false,
                dataType: 'json',
                success: function (data) {
                    var dataList = data.obj;
                    if (dataList != null && dataList.length > 0) {
                        
                        for(var j = 0;j < dataList.length;j++){
                            polygon = data.obj[j].fenceData;
                            dmaMapStatistic = data.obj[j].dmaMapStatistic
                            fillColor_seted = fillColor = data.obj[j].fillColor
                            strokeColor_seted = strokeColor = data.obj[j].strokeColor
                            if(fillColor === null){
                                fillColor_seted = fillColor = "#1791fc"
                            }
                            if(strokeColor === null){
                                strokeColor_seted = strokeColor = "#FF33FF"
                            }
                            var dataArr = new Array();
                            if (polygon != null && polygon.length > 0) {
                                for (var i = 0; i < polygon.length; i++) {
                                    dataArr.push([polygon[i].longitude, polygon[i].latitude]);
                                }
                            };
                            if(data.obj !== null){
                                polyFence = new AMap.Polygon({
                                    path: dataArr,//设置多边形边界路径
                                    strokeColor:strokeColor,// "#FF33FF", //线颜色
                                    strokeOpacity: 0.2, //线透明度
                                    strokeWeight: 3, //线宽
                                    fillColor:fillColor,// "#1791fc", //填充色
                                    fillOpacity: 0.35
                                    //填充透明度
                                });

                                // var position = new AMap.LngLat(polygon[0].longitude,polygon[0].latitude);
                                polyFence.on("mouseover",function(e){
                    
                                    var position = e.lnglat;
                                    // console.log(position);
                                    conts = mapMonitor.createStationInfo(dmaMapStatistic.dma_name, dmaMapStatistic)

                                    infoWindow.setContent(conts);
                                    // markerInfoWindow.setSize(AMap.Size(400,300));
                                    infoWindow.open(map,position);
                                });

                                polyFence.on("mouseout",function(){
                                    infoWindow.close();
                                })

                                dma_list.push(polyFence)
                                // polyFence.setMap(map);
                                // map.setFitView(polyFence);
                                
                            }
                        }

                        map.add(dma_list)
                        map.setFitView(dma_list);
                    }
                },      
            });
            
        },
        createStationInfo:function (title, content) {
            var info = document.createElement("div");
            info.className = "info";
     
            //可以通过下面的方式修改自定义窗体的宽高
            //info.style.width = "400px";
            // 定义顶部标题
            var stationname = document.createElement("div");
            stationname.innerHTML = "分区名称:" ;
            var span = document.createElement("span");
            span.className = "span2";
            span.innerHTML = content.dma_name;
            stationname.appendChild(span);
            info.appendChild(stationname);
            
            var belongto = document.createElement("div");
            belongto.innerHTML = "所属组织:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.belongto;
            belongto.appendChild(span);
            info.appendChild(belongto);
            
            var relatemeter = document.createElement("div");
            relatemeter.innerHTML = "分区层级:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.dma_level;
            relatemeter.appendChild(span);
            info.appendChild(relatemeter);
            
            
            var meterstate = document.createElement("div");
            meterstate.innerHTML = "状&nbsp; &nbsp; &nbsp; 态:";
            var span = document.createElement("span");
            // if(content.status == "在线"){
            //     span.className = "span3";
            // }else{
            //     span.className = "span4";
            // }
            span.innerHTML = content.state;
            meterstate.appendChild(span);
            info.appendChild(meterstate);
            
            var split = document.createElement("img");
            split.src = "/static/virvo/images/u3922.png";
            info.appendChild(split);

            

            var readtime = document.createElement("div");
            readtime.innerHTML = "分区流量:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.water_in;
            readtime.appendChild(span);
            info.appendChild(readtime);
            
            var flux = document.createElement("div");
            flux.innerHTML = "当月售水量:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.month_sale;
            flux.appendChild(span);
            info.appendChild(flux);
            
            var accumuflux = document.createElement("div");
            accumuflux.innerHTML = "上月售水量:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.last_month_sale;
            accumuflux.appendChild(span);
            info.appendChild(accumuflux);
            
            var press = document.createElement("div");
            press.innerHTML = "上月增长比例:";
            var span = document.createElement("span");
            span.className = "span1";
            span.innerHTML = content.last_add_ratio;
            press.appendChild(span);
            info.appendChild(press);
            
            
            // 定义底部内容
            var bottom = document.createElement("div");
            bottom.className = "info-bottom";
            bottom.style.position = 'relative';
            bottom.style.top = '10px';
            bottom.style.margin = '0 auto';
            var sharp = document.createElement("img");
            sharp.src = "http://webapi.amap.com/images/sharp.png";
            bottom.appendChild(sharp);
            info.appendChild(bottom);
            return info;
        },

        init: function(){
            // map
            var extent = [-2000, -2000, 2000, 2000];
            var projection = new ol.proj.Projection({
                code: 'xkcd-image',
                units: 'pixels',
                extent: extent
              });
            var centerr = ol.extent.getCenter(extent);
        
            map = new ol.Map({
                // layers: [
                //   new ol.layer.Image({
                //     source: new ol.source.ImageStatic({
                //       attributions: '© <a href="http://xkcd.com/license.html">xkcd</a>',
                //       url: "{% static 'virvo/images/bg_layer.png' %}",
                //       projection: projection,
                //       imageExtent: extent
                //     })
                //   })
                // ],
                view: new ol.View({
                    projection: projection,
                    center: ol.extent.getCenter(extent),
                    // center:  new ol.proj.transform(center,"EPSG:4326","EPSG:3857"),
                    maxZoom : 1,
                    zoom: 1
                }),
                // controls: ol.control.defaults({ attribution: false }).extend([attribution]),
                interactions: ol.interaction.defaults({mouseWheelZoom:false}),
                target:"js-map"
            });

            var extent2 = map.getView().calculateExtent(map.getSize());
            console.log("extent2:",extent2);

            map.addLayer(new ol.layer.Image({
                    source: new ol.source.ImageStatic({
                      attributions: '© <a href="http://xkcd.com/license.html">xkcd</a>',
                      url: "/static/virvo/images/bg_layer.png",
                      projection: projection,
                      imageExtent: extent2
                    })
                  }));

            var jingkai = new ol.Feature({
                geometry:new ol.geom.Point([-300,2200]),
                name:'经济开发区',
                population: 4000,
                rainfall: 500
            });
            var chengxizhu = new ol.Feature({
                geometry:new ol.geom.Point([-1000,-800]),
                name:'城西主城区片区',
                population: 4000,
                rainfall: 500
            });
            var gucheng = new ol.Feature({
                geometry:new ol.geom.Point([400,-300]),
                name:'古城片区',
                population: 4000,
                rainfall: 500
            });
            var piyunlu = new ol.Feature({
                geometry:new ol.geom.Point([-150,-1650]),
                name:'披云路片区',
                population: 4000,
                rainfall: 500
            });
            var chengxitie = new ol.Feature({
                geometry:new ol.geom.Point([-2350,150]),
                name:'皖赣铁路以西片区',
                population: 4000,
                rainfall: 500
            });
            var chengxigong = new ol.Feature({
                geometry:new ol.geom.Point([-2300,-1550]),
                name:'城西工业区片区',
                population: 4000,
                rainfall: 500
            });
            // var libya = new ol.Feature(new ol.geom.Point([512,384]));
            // var niger = new ol.Feature(new ol.geom.Point(ol.proj.transform([114.39709, 22.67306],"EPSG:4326","EPSG:3857")));

            
            chengxizhu.setStyle(mapMonitor.createIconStyle('chengxizhu','城西主城区'));
            jingkai.setStyle(mapMonitor.createIconStyle('jingkai','经济开发区'));
            chengxitie.setStyle(mapMonitor.createIconStyle('chengxitie','城西皖赣铁路以西片区'));
            gucheng.setStyle(mapMonitor.createIconStyle('gucheng','古城区'));
            piyunlu.setStyle(mapMonitor.createIconStyle('piyunlu','披云路片区'));
            chengxigong.setStyle(mapMonitor.createIconStyle('chengxigong','城西工业区'));

            var vectorLayer = new ol.layer.Vector({
                source: new ol.source.Vector({
                    features: [chengxizhu, jingkai, gucheng,piyunlu,chengxitie,chengxigong]
                })
            });

            map.addLayer(vectorLayer);

            // overlay
            overlay = new ol.Overlay({
                element:document.getElementById('js-overlay'),
                positioning: 'bottom-left',
            });

            

            overlay.setMap(map);
            map.on(['pointermove', 'singleclick'], mapMonitor.moveonmapevent);
            
        },
        moveonmapevent:function(evt) {
            var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                overlay.setPosition(evt.coordinate);
                // overlay.getElement().innerHTML = feature.get('name');
                // console.log(feature.get('text'));
                name = feature.get('name');
                
                return feature;
              });
              // console.log(feature);
              
              mapMonitor.rebuildoverlay(name);
              overlay.getElement().style.display = 'block';
              (feature) ? overlay.setPosition(mapMonitor.recalcposition(feature.getGeometry().getCoordinates())) : overlay.setPosition(undefined);

              // overlay.getElement().style.display = feature ? 'block' : 'none';
              // document.body.style.cursor = feature ? 'pointer' : '';
        },
        recalcposition:function(cord){
            console.log(cord);
            if(cord[1] < -1000){
                return [cord[0],cord[1]+800];
            }
            return cord;
        },
        createIconStyle:function(country,description) {
            return new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 46],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    // opacity: 0.75,
                    src: "/static/virvo/images/" + country + '.png'
                }),
                text: new ol.style.Text({
                        font: '20px Calibri,sans-serif',
                        fill: new ol.style.Fill({ color: '#000' }),
                        stroke: new ol.style.Stroke({
                        color: '#fff', width: 2
                    }),
                // get the text from the feature - `this` is ol.Feature
                // and show only under certain resolution
                text: description

                // text: map.getView().getZoom() > 12 ? this.get('description') : ''
              })
            })
        },
        rebuildoverlay:function(name){
            console.log('name:',name);
            $("#dma_name span").html(name);

            var tmpste = eval(statsinfo);
            
            if(tmpste != null){
                statistic = tmpste.statsinfo;
                for (var i = 0; i < statistic.length; i++){
                    if(name==statistic[i].dma_name){
                        $("#belongto span").html(statistic[i].belongto);
                        $("#dma_level span").html(statistic[i].dma_level);
                        $("#dma_status span").html(statistic[i].dma_status);
                        $("#dmaflow span").html(statistic[i].dmaflow);
                        $("#month_sale span").html(statistic[i].month_sale);
                        $("#lastmonth_sale span").html(statistic[i].lastmonth_sale);
                        $("#bili span").html(statistic[i].bili);
                    }
                }
            }
            
            // var data={"dma_name":name,'csrfmiddlewaretoken': '{{ csrf_token }}'};
            // var url="/dmam/getdmamapusedata/";
            // json_ajax("GET", url, "json", true,data,mapMonitor.updateoverlay);
        },
        updateoverlay:function(data){
            console.log('updateoverlay',data);
            if(data.dma_statics != null){
                statistic = data.dma_statics;
                // $("#dma_name span").html(name);
                // $("#dma_name span").html(name);
                $("#belongto span").html(statistic.belongto);
                $("#dma_level span").html(statistic.dma_level);
                $("#dma_status span").html(statistic.dma_status);
                $("#dmaflow span").html(statistic.dmaflow);
                $("#month_sale span").html(statistic.month_sale);
                $("#lastmonth_sale span").html(statistic.lastmonth_sale);
                $("#bili span").html(statistic.bili);
            }
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
                        "isDma" : "1",
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: mapMonitor.ajaxDataFilter
                },
                view : {
                    // addHoverDom : mapMonitor.addHoverDom,
                    // removeHoverDom : mapMonitor.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    // fontCss: setFontCss_ztree
                },
                edit : {
                    enable : true,
                    editNameSelectAll : true,
                    showRemoveBtn : false,//mapMonitor.showRemoveBtn,
                    showRenameBtn : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeDrag : mapMonitor.beforeDrag,
                    beforeEditName : mapMonitor.beforeEditName,
                    beforeRemove : mapMonitor.beforeRemove,
                    beforeRename : mapMonitor.beforeRename,
                    // onRemove : mapMonitor.onRemove,
                    onRename : mapMonitor.onRename,
                    onClick : mapMonitor.zTreeOnClick
                }
            };
            $.fn.zTree.init($("#treeDemo"), treeSetting, zNodes);
            var treeObj = $.fn.zTree.getZTreeObj('treeDemo');treeObj.expandAll(true);
           
        },

        beforeDrag: function(treeId, treeNodes){
            return false;
        },
        beforeEditName: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            return tg_confirmDialog(null,userGroupDeleteConfirm);
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
        beforeRemove: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            var result;
            layer.confirm(userGroupDeleteConfirm, {
                title :'操作确认',
                icon : 3, // 问号图标
                btn: ['确认','取消'] // 按钮
            }, function(index){
                selectTreeIdAdd="";
                var nodes = zTree.getSelectedNodes();
                var preNode = nodes[0].getPreNode();
                var nextNode = nodes[0].getNextNode();
                var parentNode = nodes[0].getParentNode();
                $.ajax({
                    type: 'POST',
                    url: 'district/delete/',
                    data: {"pId": treeNode.id},
                    async:false,
                    dataType: 'json',
                    success: function (data) {
                        var flag=data.success;      
                        if(flag==false){
                            layer.msg(data.msg,{move:false})
                        }
                        if(flag==true){
                            $('#simpleQueryParam').val("");
                            selectTreeId = "";
                            selectDistrictId = "";
                            $.ajax({
                                type: 'POST',
                                url: 'district/dmatree/',
                                data: {"isOrg" : "1"},
                                async:false,
                                dataType: 'json',
                                success: function (data) {
                                    var data2 = JSON.stringify(data);
                                    var addData = JSON.parse(data2);             
                                    var nodeName;
                                    if(preNode != null){
                                        nodeName = preNode.name;
                                    }else if(nextNode != null){
                                        nodeName = nextNode.name;
                                    }else{
                                        nodeName = parentNode.name;
                                    };
                                    $.fn.zTree.init($("#treeDemo"), treeSetting, addData);  
                                    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                                    var nodes = treeObj.getNodes();
                                    for(var j=0;j<nodes.length;j++){
                                         zTree.expandNode(nodes[j], true, true, true);
                                    }
                                    // pengwl delete group and user refresh tabale
                                    myTable.requestData();
                                },      
                            });
                        }
                        layer.close(index,{move:false});
                    },
                    error: function () {
                        layer.msg(systemError, {move: false});
                    }
                });
            }, function(index){
                layer.close(index,{move:false});
            });
            return false;
        },
        onRemove: function(e, treeId, treeNode){
            selectTreeIdAdd="";
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                + treeNode.name);
        },
        beforeRename: function(treeId, treeNode, newName, isCancel){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapMonitor.getTime()
                    + " beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                    + (isCancel ? "</span>" : ""));
            if (newName.length == 0) {
                layer.msg(userNodeNameNull, {move: false});
                var zTree = $.fn.zTree.getZTreeObj("treeDemo");
                setTimeout(function() {
                    zTree.editName(treeNode)
                }, 10);
                return false;
            }
            return true;
        },
        onRename: function(e, treeId, treeNode, isCancel){
            mapMonitor.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapMonitor.getTime()
                + " onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                + (isCancel ? "</span>" : ""));
        },
        // 显示删除组织按钮
        showRemoveBtn: function(treeId, treeNode){
            return treeNode.children==undefined;
        },
        showRenameBtn: function(treeId, treeNode){
            return !treeNode.isLastNode;
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
            selectTreeIdAdd=treeNode.uuid;
            $('#simpleQueryParam').val("");
            if(treeNode.type == "dma"){
                var pNode = treeNode.getParentNode();
                // $("#organ_name").attr("value",pNode.name);
                $("#current_dma_no").attr("value",treeNode.dma_no);
                organ = pNode.id;
                station = treeNode.id;

                mapMonitor.loadGeodata(2)
                $("#binddmaname").html(treeNode.name);
                mapMonitor.hydropressflowChart();
                // mapMonitor.showSearchBtn();
                $(".info-seach-btn").css("left","320px");
                $("#searchBtn").show();
            }else{
                $("#current_organ_id").attr("value",treeNode.id);
                $("#fenceBindTable").css("display", "none");
                mapMonitor.loadGeodata(1)
                $("#searchBtn").hide();
                $("#searchInput").hide();
            }
            
            fenceOperation.TabCarBox();
            // fenceOperation.fenceBind(treeNode.pId, treeNode.name, treeNode.type,treeNode.id);

        },
        // 搜索按钮
        showSearchBtn:function(){
            $("#searchBtn").show();
        },
        // ajax参数
        ajaxDataParamFun: function(d){
            d.simpleQueryParam = $('#simpleQueryParam').val(); // 模糊查询
            d.groupName = selectTreeId;
            d.districtId = selectDistrictId;
        },
        findDownKey:function(event){
            if(event.keyCode==13){
                mapMonitor.findOperation();
            }
        },
        // 水力分布流量和压力图标
        hydropressflowChart:function(){

            options = {
                backgroundColor: '#FFFFFF',
                
                title: {
                    text: '近7日流量压力曲线图',
                    left:'left',
                    textStyle:{
                        fontSize:12,
                        fontWeight:'100'
                    },
                },
                // tooltip: {
                //     trigger: 'axis',
                //     axisPointer: { // 坐标轴指示器，坐标轴触发有效
                //         type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                //     }
                // },
                
                legend: {
                    data: ['流量'],
                    
                },
                    grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                    },
                
                xAxis: [{
                    type: 'category',
                     boundaryGap: false,
                    //show:false,
                    data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','20','31','32','33','34','35','36','37','38','39','40'],
                    axisLabel:{
                        textStyle:{
                            fontSize:10
                        }
                    }
                }],
                yAxis: {
                    type: 'value',
                    //show:false,
                  //  name: '流量',
                    // min: 0,
                     max: 10,
                    interval: 10,
                    splitLine:{
                        show:false,
                    }
                },
                series: [{
                    name: 'flow',
                    type: 'line',
                    itemStyle: {
                        normal: {
                            color: '#7acf88',
                            // areaStyle:{type:'default'}
                        },
                    },
                    
                    data: [4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0,4,6,3,7,2,4,4,4,1,2,3,2,6,3,2,0,1,2,4,0]
                }]
            };

            var recent7flowpress = echarts.init(document.getElementById('recent7flowpress'));
            recent7flowpress.setOption(options);
            
        },
        // 水力分布流量和压力图标
        bindflowpress:function(){

            option = {
                // title : {
                //     text: '未来一周气温变化',
                //     subtext: '纯属虚构'
                // },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['MNF','流量','压力','背景漏损']
                },
                
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['2018-11-15','2018-11-16','2018-11-17','2018-11-18','2018-11-19','2018-11-20','2018-11-21']
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        name : '时用水量(m³/h)',
                        nameLocation : 'middle',
                        nameGap : 80,
                        axisLabel : {
                            formatter: '{value} '
                        }
                    }
                ],
                series : [
                    {
                        name:'MNF',
                        type:'line',
                        data:[11, 11, 15, 13, 12, 13, 10],
                        
                    },
                    {
                        name:'流量',
                        type:'line',
                        data:[10, 12, 7, 5, 9, 2, 6],
                        
                    },
                    {
                        name:'压力',
                        type:'line',
                        data:[2, 5, 8, 7, 9, 3, 10],
                        
                    },
                    {
                        name:'背景漏损',
                        type:'line',
                        data:[1, -2, 2, 5, 3, 2, 0],
                        
                    }
                ]
            };
                                

            bindflowpressChart = echarts.init(document.getElementById('bindflowpress'));
            bindflowpressChart.setOption(option);

            $('#fenceBind').on('shown.bs.modal',function(){
                bindflowpressChart.resize()
            })
            
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
                tMonth = mapMonitor.doHandleMonth(tMonth + 1);
                tDate = mapMonitor.doHandleMonth(tDate);
                var num = -(day + 1);
                startTime = tYear + "-" + tMonth + "-" + tDate + " "
                    + "00:00:00";
                var end_milliseconds = today.getTime() + 1000 * 60 * 60 * 24
                    * parseInt(num);
                today.setTime(end_milliseconds); //注意，这行是关键代码
                var endYear = today.getFullYear();
                var endMonth = today.getMonth();
                var endDate = today.getDate();
                endMonth = mapMonitor.doHandleMonth(endMonth + 1);
                endDate = mapMonitor.doHandleMonth(endDate);
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
                vMonth = mapMonitor.doHandleMonth(vMonth + 1);
                vDate = mapMonitor.doHandleMonth(vDate);
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
                    vendMonth = mapMonitor.doHandleMonth(vendMonth + 1);
                    vendDate = mapMonitor.doHandleMonth(vendDate);
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
        estimate: function () {
            var timeInterval = $('#timeInterval').val().split('--');
            sTime = timeInterval[0];
            eTime = timeInterval[1];
            mapMonitor.getsTheCurrentTime();
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

    }
    $(function(){
        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('treeDemo',id,'group');
            };
        });
        var map;
        pageLayout.init();
        mapMonitor.userTree();
        
        mapMonitor.amapinit();

        $('#timeInterval').dateRangePicker({dateLimit:30});
        mapMonitor.getsTheCurrentTime();  
        mapMonitor.startDay(-7);  
        $('#timeInterval').val(startTime + '--' + endTime);

        $("#bingListClick").bind("click", fenceOperation.bingListClick);

        $("#searchBtn").bind("click",function(){
                $(".info-seach-btn").css("left","710px");

            $("#searchInput").show()
        })

        $("#queryClick").bind("click",function(){
            $("#fenceBind").modal('show');
            mapMonitor.bindflowpress();

        })

        
        // mapMonitor.init();
        
        // map.on(['pointermove', 'singleclick'], mapMonitor.moveonmapevent);
        
    })
})($,window)
