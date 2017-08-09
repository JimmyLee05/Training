import UIKit
import SlightechKit

public class RealMapPathAnno: NSObject, MKAnnotation {
	
	public var coordinate: CLLocationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	init(coordinate: CLLocationCoordinate2D) {
		self.coordinate = coordinate
	}
}

//实时定位模块
class MyntRealMapViewController: BaseViewController {
	
	@discardableReasult
	class func show(parentViewController: UIViewController?,
					sn: String?,
					animated: Bool = true) -> MyntRealMapViewController {
		let viewController 	= MyntRealMapViewController()
		viewController.sn 	= sn
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: animated,
									  completion: nil)
		return viewController
	}

	enum State: Int {
		//无
		case none
		//等待中
		case waiting
		//定位中
		case location
		//暂停中
		case pause
		//停止
		case stop
	}

	var mapView: MKMapView?

	@IBOutlet weak var mapSuperView: UIView!
	@IBOutlet weak var backLocationButton: GradientButton!
	@IBOutlet weak var buttonsView: MyntButtonView!
	@IBOutlet weak var goView: UIView!
	@IBOutlet weak var goLabel: UILabel!
	@IBOutlet weak var locationLabel: UILabel!
	//现在
	@IBOutlet weak var dateLabel: UILabrl!
	@IBOutlet weak var realStateView: UIView!
	@IBOutlet weak var realStateLabel: UILabel!
	@IBOutlet weak var debugLabel: UILabel!

	//用户位置(已偏移过)
	var userCoordinate = CLLocationCoordinate2DZero
	//选择位置(已偏移过)
	var selectedCoordinate: CLLocationCoordinate2D? {
		didSet {
			//更新大头针图标位置
			removeAnnotation()
			if let coordinate = self.selectedCoordinate {
				self.addAnnotation(coordinate: coordinate)
				self.mapView?.gotoCoordinate(coordinate, range: 3000)
				//更新位置坐标
				coordinate.reverseGeocodeLocation { [weak self] address in
					self?.locationLabel.text = address
				}
				//加入数组
				locations.append(coordinate)
			}
		}
	}

	//图钉图片
	var annotationImage: UIImage?
	//底部圆圈
	fileprivate var myntCircleAnnotation: MyntCircleAnnotation?
	//小觅图标
	fileprivate var myntAnnotation: MyntAnnotation?
	//启动实时定位时间
	var beginTime: TimeInterval = 0
	//第一次获取经纬度时间
	var firstLocationTime: TimeInterval = 0

	var timer: Timer?

	var state: State = .none {
		didSet {
			if state == oldValue { return }
			switch state {
			case .none:
				break
			case .waiting:
				setNavigationBarBackground(color: navigationBarColor)
				realStateView.backgroundColor = navigationBarColor
				realStateLabel.text = NSLocalizedString("正在启动实时定位，请稍后..."， comment: "")

				startRealMode()
			case .location:
				setNavigationBarBackground(color: UIColor(red:0.16, green:0.88, blue:0.53, alpha:1.00))
				realStateView.backgroundColor = UIColor(red:0.16, green:0.88, blue:0.53, alpha:1.00)
				realStateLabel.text = NSLocalizedString("正在实时定位中...", comment: "")
			case .pause:
				setNavigationBarBackground(color: navigationBarColor)
				realStateView.backgroundColor = navigationBarColor
				realStateLabel.text = NSLocalizedString("设备信号较差，正在尝试获取新的坐标点", comment: "")
			case .stop:
				setNavigationBarBackground(color: navigationBarColor)
				realStateView.backgroundColor = navigationBarColor
				realSateLabel.text = NSLocalizedString("设备定位时间已结束", comment: "")

				stopRealMode()
			}
		}
	}

	//灰色大头针
	var realMapPathAnnos = [realMapPathAnno]()

	//realMap 路径数据源
	var locations = [CLLocationCoordinate2D]() {
		didSet {
			mapView?.removeAnnotation(realMapPathAnnos)
			// 划线 && 大头针
			let polyLineCoors = locations?.map { CLLocationCoordinate2DMake($0.latitude, $0.longitude) }
			let polyLine = MKPolyline(coordinate: polyLineCoors, count: polyLineCoors.count)

			if let overLays = mapView?.overLays.filter({ ($0 is MKPolyline) }) {
				mapView?.removeOverlays(overlays)
			}
			mapView?.add(polyLine)
			//删除大头针
			mapView?.removeAnnotations(realMapPathAnnos)
			//将路径放大到全屏
			mapView?.zoomMapViewToFitAnnotations(polyLineCoors.rect, animated: true)
			//添加大头针
			realMapPathAnnos = locations.map { RealMapPathAnno(coordinate: $0) }
			mapView?.addAnnotations(realMapPathAnnos)
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		//初始化UI
		initUI()
		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
		state = .waiting
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		navigationController?.dismiss(animated: true, completion: nil)
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
		timer?.invalidate()
		timer = nil
		state = .stop
	}

	func initUI() {
		title = NSLocalizedString("MAP", comment: "地图")
		setLeftBarButtonItem(image: UIImage(named: "titlebar_realtime_off"))
		//初始化按钮
		buttonView.sn 				= sn
		buttonView.viewController   = self

		backLocationButton.layer.masksToBounds 		= true
		backLocationButton.layer.cornerRadius 		= backLocationButton.bounds.height / 2
		backLocationButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		goView.layer.cornerRadius 	= goView.bounds.height / 2
		goView.backgroundColor 		= ColorStyle.kGreenGradientColor.start
		goView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickGoViewButton(_:))))

		goLabel.text 				= NSLocalizedString("NAVIGATION_GO", comment: "导航")
		locationLabel.text 			= NSLocalizedString("NO_LOCATION_TITLE", comment: "未获取到位置信息")
		dateLabel.text 				= NSLocalizedString("DISCONNECT_TIME_NOW", comment: "现在")
		//加载mynt图标
		loadAvatar()
		initMapView()
	}

	//加载地图
	func initMapView() {
		if mapView != nil { return }
		mapView 													= MKMapView()
		mapView?.delegate  											= self
		mapView?.isRotateEnabled 									= false
		mapView?.isPitchEnabled 									= false
		mapView?.showsUserLocation 									= true
		mapView?.isZoomEnabled 										= true
		mapView?.translatesAutoresizingMaskIntoConstraints 			= false
		mapSuperView.addSubview(mapView!)
		mapView?.fillInSuperView()
	}

	//释放地图
	func releaseMapView() {
		mapView?.applyMapViewMemoryFix()
		mapView = nil
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		initMapView()
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
		releaseMapView()
	}

	//导航按钮事件
	func didClickGoViewButton(_ sender: AnyObject) {
		if let selectedCoordinate = selectedCoordinate {
			MapNavigationKit.shared.selectMapApp(fromCoordinate: userCoordinate,
												 toCoordinate: selectedCoordinate,
												 view: view)
		}
	}

	@IBOutlet func didClickUserLocationButton(_ sender: Any) {
		gotoUserLocation()
	}

	func gotoUserLocation() {
		if !userCoordinate.isNull {
			mapView?.gotoCoordinate(userCoordinate, range: 3000)
		}
	}

	//开始定位
	fileprivate func startRealMode() {
		beginTime = Date().timeIntervalSince1970
		resetTimer()
		getLocation()
	}

	//停止定位
	fileprivate func stopRealMode() {
		timer?.invalidate()
		timer = nil
		sn?.mynt?.stopRealTimeLocation(success: {

			}, failure: { _ in
		})
	}

	//获取经纬度
	func getLocation() {
		guard let mynt = sn?.mynt else { return }
		//请求实时定位超时
		let isWaitTimeout = firstLocationTime == 0 && Date().timeIntervalSince1970 - beginTime > Double(mynt.usageValue.locationFrequency.time * 60)
		//定位时间结束
		let isLocationEnd = firstLocationTime == 0 && Date().timeIntervalSince1970 - firstLocationTime > 300

		if isWaitTimeout || isLocationEnd {
			//距离第一次定位超过300秒
			state = .stop
			updateDebugLabel(NSLocalizedString("停止定位", comment: ""))
			return
		}
		sn?.mynt?.startRealTimeLocation(beginTime: Int(beginTime),
										success: { [weal self] location in
											NSLog("实时定位获取到的经纬度为---->\(location.longitude),\(location.latitude)", location.type.typeName)
											if location.updateTime == 0 {
												self?.updateDebugLabel(NSLocalizedString("实时定位暂时未获取到经纬度，正在继续尝试" comment: ""))
												return
											}

											self?.updateDebugLabel("实时: \(location.longitude), \(location.latitude)")
											//开始获取到位置
											self.state = .location
											if self?.firstLocationTime == 0 {
												self?.firstLocationTime = TimeInterval(location.updateTime)
											}
											self?.resetTimer()
											//实时定位点
											self?.selectedCoordinate = CLLocationCoordinate2DMake(location.latitude, location.longitude)
		}, failure: { _ in

		})
	}

	func resetTimer() {
		timer?.invalidate()
		timer = nil
		timer = Timer.scheduledTimer(timeInterval: 5, target: self, selector: #selector(getLocation), userInfo: nil, repeats: true)
	}

	func updateDebugLabel(_message: String) {
		let formatter = DateFormatter()
		formatter.dateFormat = "HH:mm:ss"
		debugLabel.text = "\(formatter.string(from: Date()))\(message)"
	}

	//删除大头针
	func removeAnnotation() {
		if let annotation = self.myntAnnotation {
			mapView?.removeAnnotation(annotation)
		}
		if let annotation = self.myntCircleAnnotation {
			mapView?.removeAnnotation(annotation)
		}
	}

	//添加大头针
	func addAnnotation(coordinate: CLLocationCoordinate2D) {
		if let sn = sn {
			myntAnnotation = myntAnnotation(sn: sn, coordinate: coordinate)
			mapView?.addAnnotation(myntAnnotation!)

			myntCircleAnnotation = MyntCircleAnnotation(coordinate: coordinate)
			mapView?.addAnnotation(myntCircleAnnotation!)
		}
	}
}

// MARK: - 加载大头针头像
extension MyntRealMapViewController {
	
	func loadAvatar(block: (() -> Void)? = nil) {
		sn?.mynt?.annotationImage(block: { [weak self] image in
			self?.annotationImage = image
			block?()
		})
	}
}

// MARK: -MYNTKitDelegate
extension MyntRealMapViewController: MYNTKitDelegate {
	
	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		loadAvatar()
	}
}

extension MyntRealMapViewController: MKMapViewDelegate {
	
	func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
		userCoordinate = userLocation.coordinate
	}

	func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {

		if let polyline = overlay as? MKPolyline {
			let polylineRenderer 				= MKPolylineRenderer(polyline: polyline)
			polylineRenderer.strokeColor 		= UIColor(red:0.40, green:0.58, blue:0.94, alpha:1.00)
			polylineRenderer.lineWidth 			= 6
			return polylineRenderer
		} 
		return MKOverlayRenderer()
	}

	//更新大头针新点
	func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotation? {
		if annotation is MKUserLocation {
			(annotation as? MKUserLocation)?.title = ""
			return nil
		}
		if annotation is MyntAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "annotation")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "annotation")
				view?.canShowCallout = false
				view?.centerOffset = CGPoint(x: 0, y: -50) 
			}
			view?.image = annotationImage
			return view
		}

		if annotation is MyntCircleAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "pathAnnotation")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "pathAnnotation")
				view?.canShowCallout = false
			}
			view?.image = UIImage(named: "mpa_point_selected")
			return view
		}

		if annotation is RealMapPathAnno {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: "real")
			if view == nil {
				view = MKAnnotationView(annotation: annotation, reuseIdentifier: "real")
				view?.canShowCallout = false
			}
			view?.image = UIImage(named: "mpa_point_unselected")
			return view
		}
		return MKAnnotationView()
	}
}



