//
//  NewMyntMapViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/27.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class NewMyntMapViewController: UIViewController {
    
    func loadStyle() {
        fillColor       = UIColor(hexString: "000000", alpha: 0.06)
        strokeColor     = UIColor(hexString: "C0C0C0", alpha: 1)
        lineWidth       = 1.5
    }
}

extension SCDevice.SCLocation {
    
    init(latitude: CLLocationDegress, longitude: CLLocationDegress, time: Int) {
        self.latitude   = latitude
        self.longitude  = longitude
        self.updateTime = time
        self.type       = .none
        self.radius     = 0
    }
    
    var coordinate: CLLocationCoordinate2D {
        return CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
}

extension MyntMapViewController {
    
    @discardableResult
    class func show(parentViewController: UIViewController?,
                    mynt: Mynt?,
                    animated: Bool = true) -> MyntMapViewController {
        let viewController = MyntMapViewController()
        viewController.mynt = mynt
        parentViewController?.present(BaseNavigationController(rootViewController: viewController),
                                      animated: animated,
                                      completion: nil)
        return viewController
    }
}

class MyntMapViewController: MYNTKitBaseViewController {
    
    // scrollView当前高度
    let scrollViewHeight: CGFloat = 60
    
    // MARK: - 组件
    var mapView: MKMapView?
    // 父类
    
    
    
    // 触摸了地图
    fileprivate var isTouchedMap = false
    // 地图渲染完成
    fileprivate var isRenderMapDone = false
    
    // 半径圈
    fileprivate var radiusCircle: MKCircle?
    // 小觅图钉
    fileprivate var myntAnnotation: MTMyntAnnotation?
    // 小觅图钉照片
    fileprivate var myntAnnotationImage: UIImage?
    // 用户位置定位点
    fileprivate var userCoordinateTime: TimeInterval = 0
    // 用户位置(已偏移过)
    fileprivate var userCoordinate = CLLocationCoordinate2DZero
    // 选中位置(已偏移过)
    fileprivate var selectLocation: CoordinateProgressItem? {
        didSet {
            goView.isHidden = selectLocation == nil
            guard let selectLocation = selectLocation else { return }
            addAnnotation(coordinate: selectLocation.coordinate, time: selectLocation.time)
        }
    }
    // 数据源
    fileprivate var sourceLocations: [SCDevice.SCLocation] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        title = MTLocalizedString("MAP", comment: "地图")
        setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
        
        // 经纬度组件初始化
        coordinateProgressView.timeType = .merge
        coordinateProgressView.isReverse = false
        coordinateProgressView.isNeedPolymeric = false
        coordinateProgressView.setItemSelectedHandler { [weak self] items in
            //选择经纬度
            self?.selectLocation = items.first
        }
        
        scrollViewHeightConstraint.constant = 0
        // 初始化按钮
        buttonsView.mynt            = mynt
        buttonsView.viewController  = self
        
        backLocationButton.layer.masksToBounds      = true
        backLocationButton.layer.cornerRadius       = backLocationButton.bounds.height / 2
        backLocationButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
        
        goView.isHidden = true
        goView.layer.cornerRadius   = goView.bounds.height / 2
        goView.backgroundColor      = ColorStyle.kGreenGradientColor.start
        goView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickNavigationButton(_:))))
        
        goLabel.text                = MTLocalizedString("NAVIGATION_GO", comment: "导航")
        noDatalabel.text            = MTLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
        locationLabel.text          = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        dateLabel.text              = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        
        initMapView()
        updateAvatar()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        initMapView()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        loadReportLossData()
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        releaseMapView()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func leftBarButtonClickedHandler() {
        navigationController?.dismiss(animated: true, completion: nil)
        MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
        isFinishController = true
    }
    
    fileprivate func addAnnotation(coordinate: CLLocationCoordinate2D, time: TimeInterval) {
        if myntAnnotation == nil {
            myntAnnotation = MTMyntAnnotation(sn: mynt?.sn, coordinate: coordinate)
            mapView?.addAnnotation(myntAnnotation!)
        }
        myntAnnotation?.coordinate = coordinate
        
        if !isTouchedMap {
            // 如果没有拖动过地图，则移动地图到大头针位置
            moveToMyntCoordinate(coordinate: coordinate)
        }
        
        coordinate.china2World.reverseGeocodeLocation { [weak self] address, _ in
            self?.locationLabel.text = address
            
            if self?.mynt?.state == .connected {
                self?.dateLabel.text = MTLocalizedString("DISCONNECT_TIME_NOW", comment: "now")
            } else {
                let formater = DateFormatter()
                formater.dateFormat = "yyyy-MM-dd HH:mm"
                self?.dateLabel.text = formatter.string(from: Date(timeIntervalSince1970: TimeInterval(time)))
            }
        }
        addRadiusCircle()
    }
    
    fileprivate func addRadiusCircle() {
        if radiusCircle != nil {
            mapView?.remove(radiusCircle!)
        }
        if mynt?.state != .connected && !sourceLocations.isEmpty {
            if let mynt = mynt, selectLocation?.time == TimeInterval(mynt.lastDisconnectTime){
                radiusCircle = MKCircle(center: mynt.coordinate.offsetLocation, radius: CLLocationDistance(mynt.radius))
                mapView?.add(radiusCircle!)
            }
        }
    }
    
    fileprivate func startShowAnnotation() {
        if mynt?.state == .connected {
            DispatchQueue.global().async { [weak self] in
                while self?.userCoordinate.isNull == true && self?.isFinishController == false {
                    Thread.sleep(forTimeInterval: 0.1)
                }
                DispatchQueue.main.async { [weak self] in
                    // 开始显示经纬度
                    self.addAnnotation(coordinate: self!.userCoordinate, time: self!.userCoordinateTime)
                }
            }
        } else {
            // 显示最新位置
            if let coordinate = coordinateProgressView.items.last?.first {
                selectLocation = coordinate
                coordinateProgressView.selectedTime = coordinate.time
            }
        }
    }
    
    func showSliderView() {
        if isDidDisAppear {
            UIView.beginAnimations(nil, context: nil)
            UIView.setAnimationDuration(0.3)
            UIView.setAnimationCurve(.easeOut)
            scrollViewHeightConstraint?.constant = 0
            view.layoutIfNeeded()
            UIView.commitAnimations()
        } else {
            scrollViewHeightConstraint?.constant = 0
        }
        CoordinateProgressView.isHidden = true
        goView.isHidden = true
    }
    
    // 回到我的位置
    @IBAction func didClickUserLocationButton(_ sender: AnyObject) {
        if !isRenderMapDone { return }
        moveToMyntCoordinate(coordinate: userCoordinate)
    }
    
    // MARK: - 导航按钮事件
    @objc func didClickNavigationButton(_ sender: AnyObject) {
        if selectLocation?.coordinate.isNull == false {
            MapNavigationKit.shared.selectMapApp(fromCoordinate: userCoordinate,
                                                 toCoordinate: selectLocation!.coordinate,
                                                 view: view)
        }
    }
}

extension MyntMapViewController {
    
    func mynt(mynt: Mynt, didUpdateProperty name: String, oldValue: Any?, newValue: Any?) {
        if mynt != self.mynt { return }
        switch name {
        case "lostState":
            loadReportLossData()
        case "avatar":
            updateAvatar()
        default:
            break
        }
    }
}

// MARK: - 加载报丢路径
extension MyntMapViewController {
    
    fileprivate func loadReportLossData() {
        if mynt = mynt, mynt.lostState == .reportLost {
            mynt.lostAddressLost(success: { [weak self] locations in
                self?.loadReportLossUI(location: [])
            })
        } else {
            loadReportLossUI(locations: [])
        }
    }
    
    fileprivate func loadReportLossUI(locations: [SCDevice.SCLocation] = []) {
        sourceLocations = locations
        
        if sourceLocations.isEmpty {
            hideSliderView()
        } else {
            showSliderView()
        }
        // 加入断线位置
        if mynt != nil && mynt?.coordinate.isNull = false {
            let disconnectLocation = SCDevice.SCLocation(latitude: mynt!.lotitude, longitude: mynt!.logitude, time: mynt!.lastDisconnectTime)
            sourceLocations.append(disconnectLocation)
        } else {
            // 没有位置
            locationLabel.text = MTLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
            dateLabel.text     = MTlocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
        }
        
        let data = sourceLocations.map({ CoordinateProgressItem(coordinate: $0.coordinate.offsetLocation, time: Double($0.updateTime)) })
        coordinateProgressView.setData(items: data)
        
        DispatchQueue.global().async { [weak self] in
            while self?.isRenderMapDone == false && self?.isFinishController == false {
                Thread.sleep(forTimeInterval: 0.1)
            }
            DispatchQueue.main.async { [weak self] in
                self?.startShowAnnotation()
            }
        }
    }
    
    func updateAvatar() {
        mynt?.annotationImage(showOffline: false, color: UIColor(red:0.50, green:0.67, blue:0.99, alpha:1.00)) { [weak self] image in
            self?.myntAnnotationImage = image
        }
    }
}

extension MyntMapViewController {
    
    func mynt(mynt: Mynt, didDisconnected error: Error?) {
        if mynt != self.mynt { return }
        addRadiusCircle()
        loadReportLossData()
    }
    
    func didConnected(mynt: Mynt) {
        if mynt != self.mynt { return }
        addRadiusCircle()
        hideSliderView()
    }
}

extension MyntMapViewController: MKMapViewDelegate, UIGestureRecognizerDelegate {
    
    func  moveToMyntCoordinate(coordinate: CLLocationCoordinate2D, radius: Double = 1000) {
        if coordinate.isNull { return }
        mapView?.gotoCoordinate(coordinate, range: radius)
    }
    
    // 加载地图
    func initMapView() {
        if mapView != nil { return }
        mapView                                             = MKMapView()
        mapView?.delegate                                   = self
        mapView?.isRotateEnabled                            = false
        mapView?.isPitchEnabled                             = false
        mapView?.showsUserLocation                          = true
        mapView?.translatesAutoresizingMaskIntoConstraints  = false
        // 进行mapVie手势添加，用于在拖动之后，不进行缩放
        let gestures: [UIGestureRecognizer] = [UIPanGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UISwipeGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UIPinchGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UITapGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:))),
                                               UIRotationGestureRecognizer(target: self, action: #selector(gestureRecognizerHandler(gestureRecognizer:)))]
        gestures.forEach({ $0.delegate = self })
        gestures.forEach({ mapView?.addGestureRecognizer($0) })
        mapSuperView.addSubview(mapView!)
        mapView?.fillInSuperView()
    }
    
    // 释放地图
    func releaseMapView() {
        mapView?.applyMapViewMemoryFix()
        mapView = nil
        isRenderMapDone = false
        isTouchedMap = false
        myntAnnotation = nil
    }
    
    func gestureRecognizer(_ gestureRecognizer: UIGestureRecognizer, shouldRecognizeSimultaneouslyWith otherGestureRecognizer: UIGestureRecognizer) -> Bool {
        return true
    }
    
    @objc func gestureRecognizerHandler(gestureRecognizer: UIGestureRecognizer) {
        isTouchedMap = true
    }
    
    func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
        userCoordinateTime = Date().timeIntervalSince1970
        userCoordinate = userLocation.coordinate
        if mynt?.state == .connected {
            addAnnotation(coordiante: userCoordinate, time: userCoordinateTime)
        }
    }
    
    func mapView(_ ,mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
        if let circle = overlay as? MKCircle {
            let circleView = MKCircleRenderer(circle: circle)
            circleView.loadStyle()
            return circleView
        }
        return MKOverlayRenderer()
    }
    
    // 更新大头针点
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        if annotation is MKUserLocation {
            (annotation as? MKUserLocation)?.title = ""
            return nil
        }
        if annotation is MTMyntAnnotation && myntAnnotationImage != nil {
            var view = mapView.dequeueReusableAnnotationView(withIdentifier: "mynt")
            if view == nil {
                view = MKAnnotationView(annotation: annotation, reuseIdentifier: "mynt")
                view?.canShowCellout = false
                view?.centerOffset = CGPoint(x: 0, y: -myntAnnotationImage!.size.height / 2 + 10)
            }
            view?.image = myntAnnotationImage
            return view
        }
        return MKAnnotationView()
    }
    
    func mapViewDidFinishRenderingMap(_ mapView: MKMapView, fullyRendered: Bool) {
        isRenderMapDone = true
    }
}
