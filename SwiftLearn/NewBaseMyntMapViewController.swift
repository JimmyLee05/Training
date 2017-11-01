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
    var pathStartAnnotation: MTAnnotation?
    // 轨迹点(灰色)
    var pathAnnotations: [MTAnnotation] = []
    // 轨迹箭头(箭头)
    var pathArrowAnnotations: [MTAnnotation] = []
    // 路径
    var pathPolyLine: MKPolyline?
    
    // 数据源(用过这个数据进行筛选)
    var sourceTimeLines: [MyntMapTimeLineView.TimeLine] = []
    // 过滤后的数组
    var timeLines: [MyntMapTimeLineView.TimeLine] = []
    // 用户位置定位时间
    var userCoordinateTime: TimeInterval = 0
    // 用户位置半径
    var userCoordinateRadius = 0
    // 用户位置
    var userCoordinate = CLLocationCoordinate2DZero
    // 选中位置
    var selectTimeLine: MyntMapTimeLineView.TimeLine?
    // 是否显示轨迹
    var isShowPath = false
    
    // 选择时间
    var selectedDate = Date() {
        didSet {
            calendaDateLabel.text = selectedDate.dateString
        }
    }
    
    // 小觅图钉图片
    var myntAnnotationImage: UIImage? {
        didSet {
            if let myntAnnotation = myntAnnotation {
                mapView.removeAnnotation(myntAnnotation)
                mapView.addAnnotation(myntAnnotation)
            }
        }
    }
    
    // MARK: - DEBUG选项
    // 是否显示基站点
    var isShowStationPoint: Bool {
        set { AppConfig.isShowMapStation = newValue }
        get { return AppConfig.isShowMapStation }
    }
    // 是否聚合数据点
    var isMergeLocation: Bool {
        set { AppConfig.isShowAllMapPostition = !newValue }
        get { return !AppConfig.isShowMapPathArrow }
    }
    
    // 是否显示路径方向
    var isShowPathDirection: Bool {
        set { AppConfig.isShowMapPathArrow = newValue }
        get { return AppConfig.isShowMapPathArrow }
    }
    
    var isResetTimeline = false
    
    // MARK: - 初始化方法
    
    deinit {
        
    }
    
    override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
        super.init(nibName: "BaseMyntMapViewController", bundle: nil)
    }
    
    required public init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override open func viewDidLoad() {
        super.viewDidLoad()
        
        debugView.layer.cornerRadius = 6
        debugView.layer.masksToBounds = true
        debugMessageLabel.isHidden = !AppConfig.isDebugMode
        debugView.isHidden = !AppConfig.isDebugMode
        selectTimelineTypeImageView.isHidden = !AppConfig.isDebugMode
        updateDebugState()
        
        title = MTLocalizedString("MAP", comment: "地图")
        setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))
        setRightBarButtonItem(image: UIImage(named: "titlebar_more"))
        
        timeLineView.timeLineDelegate = self
        calendarView.delegate = self
        mapView.delegate = self
        // 初始化按钮
        buttonsView.mynt            = mynt
        buttonsView.viewController  = self
        
        goView.isHidden = true
        goView.layer.cornerRadius   = goView.bounds.height / 2
        goView.backgroundColor      = ColorStyle.kGreenGradientColor.start
        goView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickNavigationButton(_:))))
        
        goLabel.text                = MTLocalizedString("NAVIGATION_GO", comment: "导航")
        startLoadData()
        
        // 初始化UI配置
        initUIConfig()
        
        selectedDate = Date()
        updateAvatar()
        
        // 注册监听设备位置
        mynt?.registerLocationListener { [weak self] location in
            // 地图没有完成渲染，则不加载
            if self?.mapView.isRenderMapDone == false { return }
            self?.addNewCoordinate(location.coordinate, time: TimeInterval(location.updateTime))
        }
    }
    
    override open func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override open func leftBarButtonClickedHandler() {
        navigationController?.dismiss(animated: true, completion: nil)
        MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
        isFinishController = true
        mynt?.unregisterLocationListener()
        releaseMapView()
    }
    
    override open func rightBarButtonClickedHandler() {
        
    }
    
    private func updateDebugState() {
        let selectedColor = UIColor(red:0.86, green:0.86, blue:0.86, alpha:1.00)
        let normalColor   = UIColor.clear
        directionSwitchButton.backgroundColor = isShowPathDirection ? selectedColor : normalColor
        mergeSwitchButton.backgroundColor = isMergeLocation ? selectedColor : normalColor
        stationSwitchButton.backgroundColor = isShowStationPoint ? selectedColor : normalColor
    }
    
    @IBAction func didClickDirectionSwitchButton(_ sender: UIButton) {
        isShowPathDirection = !isShowPathDirection
        loadSourceLocations()
        updateDebugState()
    }
    
    @IBAction func didClickMergeSwitchButton(_ sender: UIButton) {
        isMergeLocation = !isMergeLocation
        loadSourceLocations()
        updateDebugState()
    }
    
    @IBAction func didClickStationSwitchButton(_ sender: UIButton) {
        isShowStationPoint = !isShowStationPoint
        loadSourceLocations()
        updateDebugState()
    }
    
    // MARK: - 导航按钮事件
    @objc func didClickNavigationButton(_ sender: AnyObject) {
        if selectTimeLine != nil && selectTimeLine?.coordinate.isNull == false {
            MapNavigationKit.shared.selectMapApp(fromCoordinate: userCoordinate,
                                                 toCoordinate: selectTimeLine!.coordinate.offsetLocation,
                                                 view: view)
        }
    }
    
    public func didConnected(mynt: Mynt) {
        // 连接成功
        addUserLocationInSourceTimeLine()
    }
    
    public func mynt(mynt: Mynt, didDisconnected error: Error?) {
        // 断开连接
        removeUserLocationInSourceTimeLine()
    }
    
    func initUIConfig() {
        
    }
    
    func addNewCoordinate(_ coordinate: CLLocationCoordinate2D, time: TimeInterval) {
        
    }
    
    func loadSourceLocations() {
        isResetTimeline = true
    }
    
    func filterSourceLocations(_ resultTimeLines: inout [MyntMapTimeLineView.TimeLine]) {
        
    }
    
    func startLoadData() {
        goView.isHidden = true
        noDataLabel.text            = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        locationLabel.text          = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        dataLabel.text              = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
    }
    
    func stopLoadData(hasData: Bool = false) {
        if !hasData {
            noDataLabel.isHidden = false
            timeLineView.isHidden = true
            noDataLabel.text        = MTLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
            locationLabel.text      = MTLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
            dateLabel.text          = MTLocalizedString("MYNTSETTING_MAP_NODATA", comment: "没有数据")
        } else {
            noDataLabel.isHidden = true
            locationLabel.text   = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
            dateLabel.text       = MTLocalizedString("MAP_ADDRESS_UPDATING", comment: "数据更新中")
        }
    }
}

// MARK: - CalendarViewDelegate, MyntMapTimeLineViewDelegate
extension BaseMyntMapViewController: CalendarViewDelegate, MyntMapTimeLineViewDelegate {
    public func didSelectDay(calendarView: CalendarView, date: Date) {
        if selectedDate.timeInterval1970 != date.timeIntervalSince1970 {
            selectedDate = date
            loadSourceLocations()
        }
    }
    
    func mapTimeLineView(timelineView: MyntMapTimeLineView, didSelectIndex index: Int) {
        let item = timeLines[index]
        selectTimeLine = item
        selectTimelineTypeImageView.image = item.type.typeImage
        goView.isHidden = false
        updateAvatar(color: item.color)
        updateMyntAnnotation(coordinate: item.coordinate,
                             item: item,
                             isNeedOffset: !item.isNowLocation)
    }
}
