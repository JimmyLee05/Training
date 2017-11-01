//
//  NewBaseMyntMapViewController+Path.swift
//  MYNT
//
//  Created by 李南君 on 2017/11/1.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

extension CLLocationCoordinate2D {
    
    //计算角度
    func angle(to coordinate: CLLocationCoordinate2D) -> CGFloat {
        //计算角度
        var angle: Double = 0
        let start   = self
        let goal    = coordinate
        let x1      = start.longitude * Double.pi / 180
        let y1      = start.latitude * Double.pi / 180
        let x2      = goal.longitude * Double.pi / 180
        let y2      = godl.latitude * Double.pi / 180
        let yc      = (y1 + y2) / 2
        let a:  Double = 6378137.000
        let dx = a * (x2 - x1) * cos(yc)
        let dy = a * (y2 - y1)
        if dx == 0 && dy == 0 {
            angle = 0
        } else {
            angle = atan2(dy, dx)
        }
        angle *= -1
        return CGFloat(angle)
    }
}

// MARK: - 路径显示
extension BaseMyntMapViewController {
    
    // 隐藏路径
    public func hidePath() {
        isShowPath = false
        mapView.removeAnnotations(pathAnnotations)
        if let pathPolyLine = pathPolyLine {
            mapView.remove(pathPolyLine)
        }
        if let pathStartAnnotation = pathStartAnnotation {
            mapView.removeAnnotation(pathStartAnnotation)
        }
    }
    
    // 显示路径
    public func showPath() {
        if let pathPolyLine = pathPolyLine {
            mapView.remove(pathPolyLine)
        }
        if let pathStartAnnotation = pathStartAnnotation {
            mapView.removeAnnotation(pathStartAnnotation)
        }
        mapView.removeAnnotations(pathArrowAnnotations)
        
        if timeLines.count <= 1 {
            if let timeLine = timeLines.first {
                //如果只有一个点，则直接移动过去
                mapView.move(timeLine.coordinate.offsetLocation)
            }
            return
        }
        
        // 显示路径箭头
        if isShowPathDirection {
            pathArrowAnnotations = []
            for i in 1..<timeLines.count {
                let timeLine = timeLines[i]
                let annotation = MTAnnotation(coordinate: timeLine.coordinate.offsetLocation)
                annotation.tag = pathArrowAnnotationTag
                annotation.angle = timeLine.angle
                pathArrowAnnotations.append(annotation)
            }
            mapView.addAnnotations(pathArrowAnnotations)
        }
        
        //添加路径数据
        let polyLineCoors = timeLines.map { $0.coordinate.offsetLocation }
        pathPolyLine = MKPolyline(coordinates: polyLineCoors, count: polyLineCoors.count)
        mapView.show(polyLineCoors, animated: true)
        mapView.add(pathPolyLine!)
        
        if polyLineCoors.count >= 2 {
            pathStartAngle = timeLines[1].angle
            //添加起始点
            pathStartAnnotation = MTAnnotation(coordinate: polyLineCoors.first!)
            pathStartAnnotation?.tag = pathStartAnnotaationTag
            if let pathStartAnnotation = pathStartAnnotation {
                mapView.addAnnotation(pathStartAnnotation)
            }
        }
        isShowPath = true
    }
}

