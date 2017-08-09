import UIKit
import SlightechKit

//MARK: - 时间转换
extension Date {
	
	fileprivate var dateString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "yyyy-MM-dd"
		return formatter.string(from: self)
	}
}

fileprivate class PathAnnotation: NSObject, MKAnnotation {
	
	public var coordinate: CLLocationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	//GCJ初始化
	init(coordinate: CLLocationCoordinate2D) {
		self.coordinate = coordinate
	}
}

//开始指示图标
fileprivate class StartArrowAnnotation: NSObject, MKAnnotation {
	
	public var coordinate: CLLocationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	//GCJ初始化
	init(coordinate: CLLocationCoordinate2D) {
		self.coordinate = coordinate
	}
}

extension SCDevice.SCLocation {
	
	init() {
		self.latitude 	= 0
		self.longitude 	= 0
		self.updateTime = 0
		self.type 		= .none
	}

	//火星偏移坐标
	fileprivate var offsetLocation: SCDevice.SCLocation {

		let coordinate 			= self.coordinate.offsetLocation
		var scLocation 			= SCDevice.SCLocation()
		scLocation.latitude 	= coordinate.latitude
		scLocation.longitude 	= coordinate.longitude
		scLocation.updateTime 	= updateTime
		return scLocation
	}

	//转换到地图专用数据
	fileprivate var mapPosition: BaseMyntMapViewController.PositionItem {
		return BaseMyntMapViewController.PositionItem(location: self)
	}
}

//MRAK: - 时间转换
extension Int {
	
	fileprivate var timeString: String {
		let minute: Dounle 		= 60
		let hour: Double 		= minute * 60
		let day: Double 		= hour * 24
		let dValue: Double 		= abs(Date().timeIntervalSince1970 - Double(self))
		if dValue < 10800 {
			switch dValue {
			case 0..<hour:
				return String(format: NSLocalizedString("DISCONNECT_TIME_MINUTE", comment: "分钟"), dValue / minute)
			case hour..<day:
				return String(format: NSLocalizedString("DISCONNECT_TIME_HOUR", comment: "小时"), dValue / hour)
			default:
				return String(format: NSLocalizedString("DISCONNECT_TIME_DAY", comment: "天"), dValue / day)
			}
		} else {
			let formatter 			= DateFormatter()
			formatter.dateFormat 	= "HH:mm"
			return formatter.string(from: Date(timeIntervalSince1970: TimeInterval(self)))
		}
	}
}

class MyntGPSMapViewController: BaseMyntMapViewController {
	//是否显示路径
	fileprivate var isShowRoute = false
	//路径时间
	fileprivate var routeDate 	= Date() {
		didSet {
			calendaDateLabel.text = routeDate.dateString
			//抓取数据
			loadLocations()
			removeAnnotation()
		}
	}

	//路径
	fileprivate var routeLine: MKPolyline: MKPolyline?
	//开始指示图标
	fileprivate var startArrowAnnotation: StartArrowAnnotation?
	//大头针
	fileprivate var pathAnnotations: [PathAnnotation] = []
	//选中点是否为停留点（聚合点）
	fileprivate var isMergePoint: Bool = false
	//角度
	fileprivate var angle: Double = 0
	//更新云端经纬度
	override var locations: [BaseMyntMapViewController.PositionItem] {
		didSet {
			super.locations 		= locations
			dataSuperView.isHidden 	= locations.isEmpty
			noDataLabel.isHidden 	= !locations.isEmpty
			//删除路径
			hidePath()
			if locations.isEmpty {
				noDataLabel.text = NSLocalizedString("无定位数据可显示", comment: "")
				removeAnnotation()
				mapView?.gotoCoordinate(userCoordinate,  range: 3000)
				//缩小约束
			} else {
				sortedLocations = locations.sorted(by: { $0.time > $1.time }).filter { $0.locationType != .station }
			}
		}
	}

	//过滤的经纬度点
	fileprivate var sortedLocations: [BaseMyntMapViewController.PositionItem] = [] {
		didSet {
			noDataLabel.isHidden 	= !sortedLocations.isEmpty
			dataSuperView.isHidden 	= sortedLocations.isEmpty
			if let items = coordinateProgressView.items.first as? [BaseMyntMapViewController.PositionItem] {
				(items.count) > 1 ? (self.isMergePoint = true) : (self.isMergePoint = false)
				//聚合点再次加载
				self.setItemPoint(items: items)
			}
			if sortedLocations.isEmpty && !locations.isEmpty {
				selectedPosition?.coordinate = CLLocationCoordinate2DZero
				mapView?.gotoCoordinate(userCoordinate, range: 3000)
				noDataLabel.text = NSLocalizedString("基站数据为辅助定位,暂时不显示定位点", comment: "暂不显示")
			} else {
				selectedPosition = sortedLocations.first
				//
				addAnnotationJamp(coordinate: selectedPosition!.coordinate)
				calculationDistance()
			}
		}
	}

	override var userCoordinate: CLLocationCoordinate2D {
		didSet {

		}
	}

	//移除通知
	deinit {
		NotificationCenter.default.removeObserver(self)
	}

	override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: "BaseMyntMapViewController", bundle: nibBundleOrNil)
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	} 

	override func viewDidLoad() {
		super.viewDidLoad()

		mapTopConstraint?.constant 						= calendarSuperView.bounds.height - 1
		scrollViewHeightConstraint?.constant 			= scrollViewHeight
		dataSuperView.isHidden 							= true
		noDataLabel.isHidden 							= true
		coordinateProgressView.timeType 				= .merge
		coordinateProgressView.isReverse 				= true
		coordinateProgressView.isNeedPolymeric 			= true
		coordinateProgressView.setItemSelectrdHandler { [weak self] items in
			//画圈策略： 如果时间轴上选中的点为第一个点 && 距离第一个点之前的点有基站位置，则开始计算
			if let items = items as? [BaseMyntMapViewController.PositionItem] {
				// items 大于1 表示此处为聚合点
				items.count > 1 ? (self?.isMergePoint = true) : (self?.isMergePoint = false)
				//业务
				self?.setItemPoint(items: items)
			}
		}

		//请求接口
		loadLocations()
		//初始化数据
		locations = []
		self.routeDate = Date()
		//接收经纬度通知
		NotificationCenter.default.addObserver(self,
											   selector: #selector(uploadLocationNitification(notification:)),
											   name: kUploadLocationNotification,
											   object: nil)
		//默认选择中点为过滤的第一个点
		if !scrollLocations.isEmpty {

		}
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func rightBarButtonClickHandler() {
		let text = isShowRoute ? NSLocalizedString("HIDE_STRACK", comment: "隐藏轨迹") : NSLocalizedString("SHOW_STRACK", comment: "显示轨迹")
		let actionSheet = UIActionSheet(title: nil,
										delegate: self,
										cancelButtonTitle: NSLocalizedString("SECURE_AREA_DELETE_CANCEL", comment: "取消"),
										destructiveButtonTitle: nil,
										otherButtonTitles: text)
		actionSheet.show(in: view)
	}

	//日历控件
	override func didSelectDay(calendarView: CalendarView, date: Date) {
		routeDate = date
		hideCircle()
		hidePath()
		guard let startArrowAnnotation = startArrowAnnotation else { return }
		mapView?.removeAnnotation(startArrowAnnotation)
	}

	//更新地理
	override func updateLabel(address: String?, time : Int?) {
		self.dateLabel.text = time?.timeString
	}

	override func didClickUserLocationButton(_ sender: AnyObject) {
		super.didClickUserLocationButton(sender)
	}

	//蓝牙状态
	override func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		if mynt.bluetoothState == .connected {
			hideCircle()
		} else if mynt.bluetoothState == .disconnected {
			//缩小行
		}
	}
}

// MRAK: - 业务逻辑
extension MyntGPSMapViewController {
	
	fileprivate func setItemPoint(items: [BaseMyntMapViewController.PositionItem]) {
		guard let selectedPoint = items.first else { return }
		self.selectedPositon = selectedPoint
		//选中时间轴的index，大头针跳转到位置
		if let index = sortedLocations.index(where: { $0.time == self.selectedPositon?.time }) {
			for i in 0..<index {
				addAnnotationJamp(coordinate: sortedLocations[i].coordinate)
			}
		}

		if selectedPoint = sortedLocations.first {
			calculationDistance()
		} else {
			hideCircle()
		}

		// 	if isShowRoute {
		//    // 路径点添加大头针
		//    pathAnnotations = sortedLocations.map { PathAnnotation(coordinate: $0.coordinate) }
		// 	  showPathAnnotations(pathAnnotations: pathAnnotations)
		//    // 选择跳转大头针
		//    if let selectedPosition = selectedPosition {
		//       removeAnnotation()
		// 		 addAnnotation(coordinate: selectedPosition.coordinate)
		// 		 mapView?.gotoCoordinate(selectedPosition.coordinate, range: 3000)
		//    }
		//  }
	}

	//计算距离，处理的原始点（locations）到（sortedLocations）的半径
	fileprivate func calculationDistance() {
		if let index = locations.index(where: { $0.time == selectedPosition?.time }) {
			for i in 0..index {
				let item = locations[i]
				if items.locationType == .station {
					let distance = item.coordinate.distance(from: sortedLocations.first!.coordiante)
					if distance < 2500 {
						self.centerPointItem(centerPoint: sortedLocations.first!.coordinate, distance: distance)
						// NSLog("选中的经纬度--->\(item.coordinate)")
						return
					}
				}
			}
		}
	}


	//中心点位置，大头针跳转至此位置，绘制圆圈
	func centerPointItem(centerPoint: CLLocationCoordinate2D, distance: CLLocationDistance?) {
		if let overlays = mapView?.overlays.filter({ !($0 is MKPolyline) }) {
			mapView?.removeOverlays(overlays)
		}
		if let centerPoint = centerPoint, let distance = distance {
			addAnnotationJamp(coordinate: centerPoint)
			let circle = MKCircle(center: centerPoint, radius: distance)
			mapView?.add(circle, level: .aboveLabels)
		}
	}

	//更新通知点
	func uploadLocationNotification(notification: Nitification) {
		let location 				= notification.object as? [String : Any]
		guard let latitude 			= location?["STPUSH_LATITUDE"] as? Double else { return }
		guard let longitude 		= location?["STPUSH_LATITUDE"] as? Double else { return }
		gurad let updateTime 		= location?["STOUSH_LATITUDE"] as? Int else { return }
		gurad let type 				= location?["STPUSH_LATITude"] as? Int else { return }
		guard let locationType 		= SCDevice.SCLocation.Type(rawValue: type) else { return }
		let positionItem = PositionItem(time: TimeInterval(updateTime),
										coordinate: CLLocationCoordinate2D(latitude: latitude, longitude: longitude),
										type: locationType)
		locations.append(positionItem)  
	}
}

// MARK: - 请求地理位置
extension MyntGPSMapViewController {
	
	func loadLocations() {
		guard let mynt = sn?.mynt, mynt.myntType == .myntGPS else { return }
		let start 	   = routeDate.startTimeInterval
		let end 	   = routeDate.endTimeInterval
		//加载云端经纬度
		mynt.downStepLocations(start: Int(start),
							   end: Int(end),
							   success: { [weak self] location in
							   	if self?.routeDate.startTimeInterval == start {
							   		self?.locations = locations.sorted(by: { $0.updateTime }).map({ $0.mapPosition })
							   	}
		}) { [weak self] _ in
			if self?.routeDate.startTimeInterval == start {
				self?.locations = []
			}
		}
	}
}

//MARK: - 路径规划
extension MyntGPSMapViewController {
	
	override func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
		if let circle 			= overlay as? MKCircle {
			let circleRend 			= MKCircleRenderer(circle: circle)
			circleRend.alpha 		= 0.6
			circleRend.fillColor 	= UIColor(red:0.70, green:0.80, blue:1.00, alpha:0.40)
			circleRend.strokeColor 	= UIColor.blue
			return circleRend
		}

		if let polyline = overlay as? MKPolyline {
			let polylineRenderer 			= MKPolylineRenderer(polyline: polyline)
			polylineRenderer.strokeColor 	= UIColor(red:0.40, green:0.58, blue:0.94, alpha:1.00)
			polylineRenderer.lineWidth 		= 6
			return polylineRenderer
		}
		return MKOverlayRenderer()
	}

	override func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
		if annotation is PathAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "pathAnnotation")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "pathAnnotation")
				view?.canShowCallout = false
			}
			view?.image = UIImage(named: "map_point_unselected")
			return view
		}

		if annotation is MyntCircleAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "pathAnnotation")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "pathAnnotation")
				view?.canShowCallout = false
			}

			//停留点显示黄色
			if isMergePoint {
				view?.image = UIImage(named: "map_path_dot_yellow")
			} else {
				view?.image = UIImage(named: "map_point_selected")
			}
			return view
		}

		//划线开始指向点
		if annotation is StartArrowAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "arrowAnnotation")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "arrowAnnotation")
				view?.canShowCallout = false
				view?.centerOffset 	 = CGPoint(x: 0, y: 0)
			}
			view?.image = UIImage(named: "map_start")
			
		}
	}
}























