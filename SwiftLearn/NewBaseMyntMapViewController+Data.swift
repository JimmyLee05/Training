//
//  NewBaseMyntMapViewController+Data.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/1.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

extension BaseMyntMapViewController {
    
    func updateUserLocation() {
        if mynt?.state == .connected && !userCoordinate.isNull {
            var now = sourceTimeLines.first(where: { $0.isNowLocation })
            if now != nil {
                //如果已存在，则刷新
                now?.latitude   = userCoordinate.latitude
                now?.longitude  = userCoordinate.longitude
                now?.radius     = userCoordinateRadius
                now?.time       = Int(userCoordinateTime)
                // 过滤时间线
                filterTimeLines()
            } else {
                // 如果不存在，则添加
                addUserLocationInSourceTimeLine()
            }
        }
    }
    
    //添加用户位置
    func addUserLocationInSourceTimeLine() {
        if !selectedDate.isSameDay(Date()) { return }
        
        var timeline = MyntMapTimeLineView.TimeLine()
        timeline.latitude = userCoordinate.latitude
        timeline.longitude = userCoordinate.longitude
        timeline.radius = userCoordinateRadius
        timeline.time = Int(userCoordinateTime)
        timeline.type = .mobile
        sourceTimeLines.append(timeline)
        // 过滤时间线
        filterTimeLines()
    }
    
    // 删除用户位置
    func removeUserLocationInSourceTimeLine() {
        if let index = sourceTimeLines.index(where: { $0.isNowLocation }) {
            sourceTimeLines.remove(at: index)
            //过滤时间线
            filterTImeLines()
        }
    }
    
    //过滤时间线
    func filterTimeLines(_ locations: [Mynt.Path]? = nil) {
        // 进行转换
        if let locations = locations {
            sourceTimeLines = locations.map({ $0.timeline })
            // 进行检测，是否需要加入当前位置
            updateUserLocation()
        }
        if sourceTimeLines.isEmpty {
            //数据为空
            stopLoadData()
            removeRadiusCircle()
            removeMyntAnnotation()
            self.timeLines = []
            timeLineView.setData(timeLines)
            
            updateTimelineView()
            return
        }
        //开始继续筛选
        var resultTimeLines = [MyntMapTimeLineView.TimeLine]()
        
        // 是否需要过滤基站点
        if !self.isShowStationPoint {
            resultTimeLines = sourceTimeLines.filter({ $0.type != .station })
        } else {
            resultTimeLines = sourceTimeLines
        }
        // 进行数据排序组装
        filterSourceLocations(&resultTimeLines)
        // 排序
        resultTimeLines = resultTimeLines.sorted(by: { $0.time < $1.time })
        // TODO: - 进行数值比较，检测是否更新
        
        // 将数据赋值
        self.timeLines = resultTimeLines
        stopLoadData(hasData: !timeLines.isEmpty)
        
        updateTimelineView()
    }
    
    // 更新时间轴
    func updateTimelineView() {
        // 更新标签
        timeLineView.isHidden = timeLines.isEmpty
        noDataLabel.isHidden = !timeLines.isEmpty
        
        timeLineView.setData(timeLines, isReset: isResetTimeline)
        if timeLineView.selectedIndex == timeLines.count - 1 {
            timeLineView.moveToLast()
        }
        if isResetTimeline && isShowPath {
            showPath()
        }
        self.isResetTimeline = false
    }
}
