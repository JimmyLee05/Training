//
//  NewBaseMyntMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/31.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

public extension Date {
    
    var dateString: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: self)
    }
}

private extension SCDevice.SCLocation.LocType {
    
    var typeImage: UIImage? {
        switch self {
        case .gps:
            return UIImage(named: "map_type_gps")
        case .mobile:
            return UIImage(named: "map_type_mobile")
        case .station:
            return UIImage(named: "map_type_station")
        default:
            return nil
        }
    }
}

open class BaseMyntMapViewController: MYNTKitBaseViewController {
    
    // MARK: - 常量定义
    let pathStartAnnotationTag = 0
    let pathPointAnnotationTag = 1
    let pathArrowAnnotationTag = 2
    let maxRadius: Double = 2000
    // scrollView当前高度
    let scrollViewHeight: CGFloat = 60
    
    // MARK: - 组件
    lazy var mapView: MTMapView = {
        let mapView = MTMapView()
        mapView.showsUserLocation = true
        mapView.translatesAutoresizingMaskIntoConstraints = false
        self.mapSuperView.addSubview(mapView)
        mapView.fillInSuperView()
        return mapView
    }()
    
    // 父类
    @IBOutlet weak var mapSuperView: UIView!
    @IBOutlet weak var calendarSuperView: UIView!
    @IBOutlet weak var dataSuperView: UIView!
    // 日历控件
    @IBOutlet weak var calendarView: CalendarView!
    @IBOutlet weak var calendaDateLabel: UILabel!
    @IBOutlet weak var buttonsView: MyntButtonsView!
    // 地图时间轴控件
    @IBOutlet weak var timeLineView: MyntMapTimeLineView!
    @IBOutlet weak var goView: UIView!
    @IBOutlet weak var goLabel: UILabel!
    // 地理位置显示
    @IBOutlet weak var locationLabel: UILabel!
    // 地理位置显示时间
    @IBOutlet weak var dateLabel: UILabel!
    // 无数据时显示(无数据 Label)
    @IBOutlet weak var noDataLabel: UILabel!
    // debug模式下显示
    @IBOutlet weak var selectTimelineTypeImageView: UIImageView!
    // 约束 scrollView高度
    @IBOutlet weak var scrollViewHeightConstraint: NSLayoutConstraint!
    
    @IBOutlet weak var debugView: UIView!
    @IBOutlet weak var debugMessageLabel: UILabel!
    @IBOutlet weak var directionSwitchButton: UIButton!
    @IBOutlet weak var mergeSwitchButton: UIButton!
    @IBOutlet weak var stationSwitchButton: UIButton!
    
    // MARK: - 数据源 & 配置
    
    // 小觅图钉
    var myntAnnotation: MTMyntAnnotation?
    // 半径圈
    var radiusCircle: MKCircle?
    // 路径起始点角度
    var pathStartAngle: CGFloat = 0
    // 路径起始点
    var 
}























