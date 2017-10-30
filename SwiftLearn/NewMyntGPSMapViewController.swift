//
//  NewMyntGPSMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/30.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import SlightechKit

extension MyntGPSMapViewController {
    
    @discardableResult
    class func show(parentViewController: UIViewController?,
                    mynt: Mynt?,
                    animated: Bool = true) -> MyntGPSMapViewController {
        let viewController = MyntGPSMapViewController()
        viewController.mynt = mynt
        parentViewController?.present(BaseNavigationController(rootViewController: viewController),
                                      animated: animated,
                                      completion: nil)
        return viewController
    }
}

class MyntGPSMapViewController: BaseMyntMapViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
    }
    
    override func leftBarButtonClickedHandler() {
        super.leftBarButtonClickedHandler()
    }
    
    override func rightBarButtonClickedHandler() {
        super.rightBarButtonClickedHandler()
        showMenu()
    }
    
    override func initUIConfig() {
        super.initUIConfig()
    }
    
    override func loadSourceLocations() {
        super.loadSourceLocations()
        guard let mynt = mynt, mynt.myntType == .myntGPS else { return }
        let start   = selectedDate.startTimeInterval
        let end     = selectedDate.endTimeInterval
        startLoadData()
        // 加载云端经纬度
        mynt.downPath(start: Int(start),
                      end: Int(end),
                      success: { [weak self] paths in
                        if self?.selectedData.startTimeInterval != start { return }
                        self?.filterTimeLines(paths)
        }) { [weak self] _, _ in
            if self?.selectedDate.startTimeInterval != start { return }
            self?.filterTimeLines([])
        }
    }
    
    override func addNewCoordinate(_ coordinate: CLLocationCoordinate2D, time: TimeInterval) {
        //如果不是当天，则不进行加载
        if Date(timeIntervalSince1970: time).isSameDay(Date()) { return }
        
        filterTimeLines()
    }
    
    override func filterSourceLocations(_ resultTimeLines: inout [MyntMapTimeLineView.TimeLine]) {
        // 先进行排序
        resultTimeLines = resultTimeLines.sorted(by: { $0.time < $1.time })
        
        var result = [MyntMapTimeLineView.TimeLine]()
        
        if self.isMergeLocation {
            var lastTimeline: MyntMapTimeLineView.TimeLine?
            resultTimeLines.forEach { timeline in
                
                func new() {
                    if lastTimeline != nil {
                        result.append(lastTimeline!)
                    }
                    lastTimeline = timeline
                    lastTimeline?.items.append(timeline)
                }
                
                if let last = lastTimeline {
                    // 开始检测是否超出范围
                    if last.coordinate.distance(from: timeline.coordinate) > 100 {
                        //超过100米，进行重新分组
                        new()
                    } else {
                        lastTimeline?.items.append(timeline)
                    }
                } else {
                    new()
                }
            }
            if lastTimeline != nil {
                result.append(lastTimelint!)
            }
        } else {
            for i in 0..<resultTimeLines.count {
                resultTimeLines[i].items = [resultTimeLines[i]]
                result.append(resultTimeLines[i])
            }
        }
        
        var lastTimeline: MyntMapTimeLineView.TimeLine?
        // 重新进行赋值
        for i in 0..result.count {
            
            let timeline = result[i]
            result[i].items = timeline.items.sorted(by: { $0.time < $1 })
            
            // TODO: 理论上应该取一个半径最精确的, 等下一版本云端上线后修改
            // timeline.items.sorted(by: { $0.radius < $1.radius }).first
            
            let formatter = DateFormatter()
            formatter.dateFormat = "HH:mm"
            
            if let last = timeline.items.last {
                result[i].latitude      = last.latitude
                result[i].longitude     = last.longitude
                result[i].radius        = last.radius
                result[i].time          = last.time
                result[i].type          = last.type
                
                if timeline.items.count > 1 {
                    let start = formatter.string(from: Date(timeIntervalSince1970: TimeInterval(timeline.items.first!.time)))
                    let end = formatter.string(from: Date(timeIntervalSince1970: TimeInterval(timeline.items.last!.time)))
                    result[i].timeString = "\(start) - \(end)"
                } else if timeline.items.count == 1 {
                    result[i].timeString = formatter.string(from: Date(timeIntervalSince1970: TimeInterval(timeline.items.first!.time)))
                }
            }
            
            if let last = lastTimeline {
                //计算角度
                result[i].angle = last.coordinate.angle(to: timeline.coordinate)
            }
            lastTimeline = timeline
        }
        
        resultTimeLines = result
    }
}

extension MyntGPSMapViewController: UIActionSheetDelegate {
    
    // 显示菜单
    func showMenu() {
        let text = isShowPath ? MTLocalizedString("HIDE_STRACK", comment: "隐藏轨迹") :
            MTLocalizedString("SHOW_STRACK", comment: "显示轨迹")
        let actionSheet = UIActionSheet(title: nil,
                                        delegate: self,
                                        cancelButtonTitle:
                                            MTLocalizedString("SECURE_AREA_DELETE_CANCEL", comment: "取消"),
                                        destructiveButtonTitle: nil,
                                        otherButtonTitles: text)
        actionSheet.show(in: view)
    }
    
    public func actionSheet(_ actionSheet: UIActionSheet, clickedButtonAt buttonIndex: Int) {
        if buttonIndex == 1 {
            if isShowPath {
                hidePath()
            } else {
                showPath
            }
        }
    }
}

