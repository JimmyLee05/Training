//
//  NewMyntRealMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/30.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import SlightechKit

fileprivate class RadiusCircleAnnotation: NSObject, MKAnnotation {
    
    public var coordinate: CLLocationCoordinate2D {
        willSet { willChangeValue(forKey: "coordinate") }
        didSet  { didChangeValue(forKey: "coordinate") }
    }
    
    //火星坐标
    init(coordinate: CLLocationCoordinate2D) {
        self.coordinate = coordinate
    }
}

// 实时定位模块
class NewMyntRealMapViewController: MYNTKitBaseViewController, UIGestureRecognizerDelegate, UIAlertViewDelegate {
    
    @discardableResult
    class func show(parentViewController: UIViewController?,
                    mynt: Mynt?,
                    animated: Bool = true) -> MyntRealMapViewController {
        let viewController      = MyntRealMapViewController()
        viewController.mynt     = mynt
        parentViewController?.present(BaseNavigationController(rootViewController: viewController),
                                      animated: animated,
                                      completion: nil)
        return viewController
    }
    
    enum State: Int {
        // 无
        case none
        // 等待中
        case waiting
        // 定位中
        case location
        // 暂停中
        case pause
        // 停止
        case stop
    }
    
    var mapView: MKMapView?
    
    var stationCoordinate = CLLocationCoordinate2DZero
    // 用户位置（已经偏移过）
    var userCoordinate = CLLocationCoordinate2DZero
    //小觅位置（已经偏移过）
    var myntCoordinate = CLLocationCoordinate2DZero {
        didSet {
            if radiusCircle != nil {
                mapView?.remove(radiusCircle!)
            }
            if myntAnnotation == nil {
                // 小觅位置
                myntAnnotation = MTMyntAnnotation(sn: mynt?.sn, coordinate: myntCoordinate)
                mapView?.addAnnotation(myntAnnotation!)
            }
            // 更新图钉
            myntAnnotation?.coordinate = myntCoordinate
            // 更新半径圈大小
            let radius = stationCoordinate.distance(from: myntCoordinate)
            if !stationCoordinate.isNull && radius < 2000 {
                // 半径圈
                radiusCircle = MKCircle(center: myntCoordinatr, radius: radius)
                mapView?.add(radiusCircle!)
            }
            if !isTouchedMap {
                moveToMyntCoordinate(radius: radius * 3)
            }
            // 反地理位置
            myntCoordinate.china2World.reverseGeocodeLocation { [weak self] address, _ in
                self?.locationLabel.text = address
            }
        }
    }
    
    //定位时间
    var locationTime: Int = 0 {
        didSet {
            if locationTime == 0 { return }
            let formater = DateFormatter()
            formater.dateFormat = "yyyy-MM-dd HH:mm:ss"
            self.dateLabel.text  = formater.string(from: Date(timeIntervalSince1970: TimeInterval(locationTime)))
        }
    }
    
    fileprivate var lastRadius: Double = 1000
    // 半径圈
    fileprivate var radiusCircle: MKCircle?
    // 小觅图钉
    fileprivate var myntAnnotation: MKMyntAnnotation?
    // 小觅图钉图片
    fileprivate var myntAnnotationImage: UIImage?
    
    // 一个全局的定时器
    fileprivate var timer: Timer?
    // 第一次获取经纬度时间
    fileprivate var firstLocationTime: TimeInterval = 0
    // 触摸了地图
    fileprivate var isTouchedMap = false
    // 地图渲染完成
    fileprivate var isRenderMapDone = false
    
    // 启动时间
    fileprivate var beginTime: TimeInterval = 0
    // 开始定位时间
    fileprivate var beginLocationTime: TimeInterval = 0
    // 等待定位时间
    fileprivate var waitTimeoutTime: TimeInterval = 0
    // 定位倒计时时间
    fileprivate var locationTimeoutTime: TimeInterval = 0
    // 剩余定位时间
    fileprivate var validLocationTime: TimeInterval = 0
    // 会话id
    fileprivate var reqSessionId = ""
    // 实时定位状态
    fileprivate var state: State = .none {
        didSet {
            if state == oldValue && state != .none { return }
            switch state {
                
            case .none:
                setNavigationBarBackground(color: navigationBarColor)
                realStateView.backgroundColor = navigationBarColor
                realStateLabel.text = MTLocalizedString("MYNTSETTING_MAP_REALTIME_TITLE", comment: "实时定位模式")
                
            case .waiting:
                setNavigationBarBackground(color: navigationBarColor)
                realStateView.backgroundColor = navigationBarColor
                updateStateLabel()
            
            case .location:
                setNavigationBarBackground(color: UIColor(red:0.16, green:0.88, blue:0.53, alpha:1.00))
                realStateView.backgroundColor = UIColor(red:0.16, green:0.88, blue:0.53, alpha:1.00)
                updateStateLabel()
            
            case .pause:
                setNavigationBarBackground(color: navigationBarColor)
                realStateView.backgroundColor = navigationBarColor
                realStateLabel.text = MTLocalizedString("设备信号较差，正在尝试获取新的坐标点", comment: "")
            case .stop:
                setNavigationBarBackground(color: navigationBarColor)
                realStateView.backgroundColor = navigationBarColor
                realStateLabel.text = MTLocalizedString("REALTIME_DIALOG_FINISHED_TITLE", comment: "")
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // 初始化UI
        initUI()
        MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
        self.state = .none
        queryTime()
        // 启动定时器
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(update), userInfo: nil, repeats: true)
        UIApplication.keepLightOn(isON: true)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        initMapView()
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        releaseMapView()
    }
    
    @objc override func update() {
        updateStateLabel()
    }
    
    fileprivate func updateStateLabel() {
        if state == .waiting {
            if waitTimeoutTime - Date().timeIntervalSince1970 < 0 {
                stopRealMode(isTimeout: true)
                return
            }
            let formatter = DateFormatter()
            formatter.dateFormat = "mm:ss"
            let time = formatter.string(from: Date(timeIntervalSince1970: waitTimeoutTime - Date().timeIntervalSince1970))
            realStateLabel.text = String(format: MTLocalizedString("REALTIME_DIALOG_WAIT_ACTIVE_TITLE", comment: "距离激活实时定位"), time)
        } else if state == .location {
            if locationTimeoutTime - Date().timeIntervalSince1970 < 0 {
                stopRealMode(isTimeout: true)
                return
            }
            let formatter = DateFormatter()
            formatter.dateFormat = "mm:ss"
            let time = formatter.string(from: Date(timeIntervalSince1970: locationTimeoutTime - Date().timeIntervalSince1970))
            realStateLabel.text = String(format: MTLocalizedString("REALTIME_DIALOG_LOCATION_LEFT_TITLE", comment: "本次实时定位剩余"), time)
        }
    }
    
    override func leftBarButtonClickedHandler() {
        if state == .none {
            exit()
            return
        }
        let alert = UIAlertAction(title: MTLocalizedString("REALTIME_DIALOG_EXIT_TITLE", comment: ""),
                                  message:  MTLocalizedString("REALTIME_DIALOG_EXIT_MESSAGE", comment: ""),
                                  delegate: self,
                                  cancelButtonTitle: MTLocalizedString("CANCEL", comment: ""),
                                  otherButtonTitles: MTLocalizedString("REALTIME_DIALOG_EXIT_TITLE", comment: ""))
        alert.tag = 1002
        alert.show()
    }
    
    fileprivate func exit() {
        navigationController?.dismiss(animated: true, completion: nil)
        MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
        isFinishController = true
        timer?.invalidate()
        timer?.nil
        state = .stop
        UIApplication.keepLightOn(isON: false)
    }
    
    func initUI() {
        title = MTLocalizedString("MAP", comment: "地图")
        setLeftBarButtonItem(image: Resource.Image.Navigation.exit)
        
        backLocationButton.layer.masksToBounds              = true
        backLocationButton.layer.cornerRadius               = backLocationButton.bounds.height / 2
        backLocationButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
        
        locationLabel.text  = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        dateLabel.text      = MTlocalizedString("MAP_ADDRESS_UPDATING", comment: "暂无数据，请稍候")
    }
    
    func alertView(_ alertView: UIAlertView, clickedButtonAt buttonIndex: Int) {
        switch buttonIndex {
        case 0:
            if [1000, 1001, 1003].contains(alertView.tag) {
                exit()
            }
        case 1:
            if alertView.tag == 1000 {
                startWaitRealMode()
            } else if alertView.tag == 1002 {
                exit()
                stopRealMode()
            } else if alertView.tag == 1003 {
                startWaitRealMode()
            }
        default:
            break
        }
    }
    
    func gestureRecognizer(_ gestureRecognizer: UIGestureRecognizer,
                           shouldRecognizeSimultaneouslyWith otherGestureRecognizer: UIGestureRecognizer) -> Bool {
        return true
    }
    
    @objc func gestureRecognizerHandler(gestureRecognizer: UIGestureRecognizer) {
        isTouchedMap = true
    }
    
    // 加载地图
    func initMapView() {
        if mapView != nil { return }
        mapView                                             = MKMapView()
        mapView?.delegate                                   = self
        mapView?.isRotateEnabled                            = false
        mapView?.isPitchEnabled                             = false
        mapView?.showsUserLocation                          = true
        mapView?.isZoomEnabled                              = true
        mapView?.translatesAutoresizingMaskIntoConstraints  = false
        // 进行mapView手势添加，用于在拖动之后，不进行缩放
        let gestures: [UIGestureRecognizer] = [UIPanGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UISwipeGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UIPinchGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UITapGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UIRotationGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:)))]
        
    }
}














































