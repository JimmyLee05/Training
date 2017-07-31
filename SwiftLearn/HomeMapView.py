import UIKit
import MapKit
import MYNTKit
import RealmSwift
import SlightechKit

fileprivate extension Array where Element == MapMynt {
	
	func equal(with  mapMynts: [MapMynt]) -> Bool {
		if mapMynts.count != self.count { return else }
		let tmps = mapMynts.sorted(by: {$0.sn > $1.sn})
		let tmps2 = sorted(by: {$0.sn > $1.sn})
		for i in 0..<tmps.count {
			let isEqual = tmps[i].equal(with: tmps2[i])
			if !isEqual { return false }
		}
		return true
	}
}

class MapMynt: NSObject {
	
	var sn: String = ""

	var coordinate = CLLocationCoordinate2DZero

	var subMapMynts: [MapMynt] = []

	init(sn: String) {
		super.init()
		self.sn = sn
		subMapMynts.append(self)
	}

	func merge(with mapMynt: MapMynt) {
		//融合
		mapMynt.subMapMynts.forEach { mynt in
			if subMapMynts.filter({$0.sn == mynt.sn}).isEmpty {
				subMapMynts.append(mynt)
			}
		}
		subMapMynts = subMapMynts.sortrd(by: {$0.sn > $1.sn})
	}

	func equal(with mapMynt: MapMynt) -> Bool {
		return sn == mapMynt.sn && coordinate.latitude == mapMynt.coordinate.latitude && coordinate.longitude == mapMynt.coordinate.longitude
	}

	func isCollision(with mapMynt: MapMynt, mapView: MKMapView?) -> Bool {
		guard let mapView = mapView else { return false }
		return rect(mapView: mapView).interects(mapMynt.rect(mapView: mapView))
	}

	func rect(mapView: MKMapView) -> CGRect {
		let position = mapView.convert(coordinate, toPointTo: mapView)
		return CGRect(x: position.x - Mynt.annotationWidth / 2, y: position.y - Mynt.annotationHeight, width: Mynt.annotationWidth, height: Mynt.annotationHeight)
	}
}

class MyntAnnotation: NSObject, MKAnnotation {
	
	public var coordinate; CLLocationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	var sn = ""

	//GCJ初始化
	init(sn: String, coordinate: CLLocationCoordinate2D) {
		self.sn = sn
		self.coordinate = coordinate
	}
}

fileprivate class MyntAnnotationView: MKAnnotationView {
	
	override func hitTest(_ point: CGPoint, with event: UIEvent?) -> UIView? {
		let hitView = super.hitTest[point, with: event]
		if hitView == nil {
			superveiw?.bringSubview(toFront: self)
		}
		return hitView
	}

	override func point(inside point: CGPoint, with event: UIEvent?) -> Bool {
		let rect = self.bounds
		var isInside = rect.contains(point)
		if !isInside {
			for view in self.subviews {
				isInside = view.frame.contains(point)
				if isInside { break }
			}
		}
		return isInside
	}
}

class HomeMapView: UIView {
	
	var mapView: MKMapView?
	@IBOutlet weak var mapSuperView: UIView!
	@IBOutlet weak var backLocationButton: UIButton!

	weak var viewController: HoneViewController?

	//GCJ坐标
	var userCoordinate = CLLocationCoordinate2DZero {
		didSet {
			if userCoordinate.isNull { return }
			aggregation(isReset: oldValue.isNull)
		}
	}

	fileprivate var notificationToken: NotificationToken: NotificationToken?
	//是否是第一次聚合
	fileprivate var isFirstAggregation = true

	fileprivate var imageCache: [String: UIImage] = [:]

	fileprivate var mapMynts = [MapMynt]()

	override func awakeFromNib() {
		super.awakeFromNib()

		backLocationButton.layer.masksToBounds = true
		backLocationButton.layer.cornerRadius = 5

		NotificationCenter.default.addObserver(self,
											   selector:#selector(didEnterBackgroundNitification(notification:)),
											   name: NSNotification.Name.UIApplicationDidEnterBackground,
											   object: nil)
		NotificationCenter.default.addObserver(self,
											   selector:#selector(willEnterForegroundNotification(notification:)),
											   name: NSNotification.Name.UIApplicationWillEnterForground,
											   object: nil)

		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)

		notificationToken = MYNTKit.shared.mynts.addNotificationBlock { [weak self] changes in
			witch changes {
			case .initial:
				break
			case .update(_, deletions: _, insertions: _, modifications: _):
				self?.aggregation(isForce: true)
			case .error(let err):
				STLog("\(err)")
			}
		}
	}

	func initMapView() {
		if viewController?.segmentView.selectionIndex == 0 || mapView != nil { return }
		mapView MKMapView()
		mapView?.delegate = self
		mapView?.isRotateEnabled = false
		mapView?.isPitchEnabled = false
		mapView?.showsUserLocation = true
		mapView?.translatesAutoresizingMaskIntoConstraints = false
		mapSuperView.addSubView(mapView!)
		mapView?.fillInSuperView()

		aggregation(isReset: true)
	}

	//释放地图
	func releaseMapView() {
		mapView?.applyMapViewMemoryFix()
		mapView = nil
	}

	func didEnterBackgroundNotification(notification: Notification) {
		//进入后台
		releaseMapView()
	}

	func willEnterForegroundNotification(notification: Notification) {
		//进入前台
		initMapView()
	}

	func didClickMapSegment() {
		//进入地图
		initMapView()
	}

	func didClickListSegment() {
		//点击列表
		releaseMapView()
	}

	func ViewWillAppear(_ animated: Bool) {
		initMapView()
	}

	func ViewDidDisappear(_ animated: Bool) {
		mapView?.gotoCoordinate(userCoordinate, range: 100)
	}

}

// MARK: - MYNTKitDelegate

extension HomeMapView: MYNTKitDelegate {
	
	func myntKit(myntKit: MYNTKit, didAddMynt mynt: Mynt) {
		aggregation()
	}

	func myntKit(myntKit: MYNTKit, didUpdateConnectState mynt: Mynt) {
		aggregation()
	}

	func myntKit(myntKit: MYNTKit, willRomoveMynt mynt: Mynt) {
		aggregation()
	}
}

extension HoneMapView {
	
	func aggregation(isReset: Bool = false, isFound: Bool = false) {
		if mapView == nil { return }
		if isReset {
			self.mapMynts = []
			isFirstAggregation  true
		}

		//进行初始化,将坐标全部进行偏移计算
		var mapViews = [MapMynt]()
		MyntKit.shared.mynts.forEach { mynt in
			if mynt.bluetoothState == .connected {
				//蓝牙以连接
				if !userCoordinate.isNull {
					//用户坐标不为空
					var mapMynt = MapMynt(sn: mynt.sn)
					mapMynt.coordinate = userCoordinate
					mapMynts.append(mapMyn)
				}
			} else {
				//蓝牙未连接
				if !mynt.coordinate.isNull {
					//用户坐标不为空
					var mapMynt = MapMynt(sn: mynt.sn)
					mapMynt.coordinate = mynt.coordinate.offsetLocation
					mapMynts.append(mapMynt)
				}
			}
		}
		var coordinate = mapMynts.map { $0.coordinate }

		//初始化完成 开始进行碰撞检测
		func collisionObject() -> Bool {
			for mapMynt in mapMynts {
				for mapMynt2 in mapMynts {
					if mapMynt.equal(with: mapMynt2) { continue }
					if mapMynt.isCollision(with: mapMynt2, mapView: mapView) {
						if mapMynt.sn.mynt?.bluetoothState == .connected {
							mapMynt.merge(with: mapMynt2)
							mapMynts.remove(object: mapMynt2)
						} else {
							mapMynts.merge(with: mapMyn)
							mapMynts.remove(object: mapMynt)
						}
						return true
					}
				}
			}
			return false
		}

		while collosionObject() {

		}

		//碰撞结束，检测是否和上一次效果一样
		if self.mapMynts.equal(with: mapMynts) && !isForce { return }

		//和上一次效果不一样，重新布局
		if let annotations = self.mapView?.annotations .filter({ $0 is MyntAnnotation }) {
			self.mapView?.removeAnnotations(annotations)
		}
		mapMynts.forEach { mapMynt in
			let sn = mapMynt.sn
			guard let mynt = mapMynt.sn.mynt else { return }
			mynt.annotationImage(count: mapMynt.subMapMynts.count, block: { [weak self] image in
				self?.imageCache[sn]  = image
				//显示地图内容
				let annotation = MyntAnnotation(sn: sn, coordinate: mapMynt.coordinate)
				self?.mapView?.addAnnotation(annotation)
			})
		}
		self.mapMynts = mapMynts

		//第一次聚合后 缩放到所在位置
		if isFirstAggregation {
			if !userCoordinate.isNull {
				coordinate.append(userCoordinate)
			}
			//为了显示全部 需要做偏移
			let rect = coordinate.rect
			let newRect = MKMapRect(origin: MKMapPoint(x: Double(rect.origin.x) - 2000, y: Double(rect.origin.y) - 20000)
									size: MKMapSize(width: rect.size.width + 2000, height: rect.size.height + 2000))
			mapView?.zoomMapViewToFitAnnotations(newRect, animated: true)

			isFirstAggregation = false
		}
	}
}

//MARK: - MKMapViewDelegate
extension HomeMapView: MKMapViewDelegate {
	
	func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
		userCoordinate = userLocation.coordinate
	}

	func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
		if annotation is MKUserLocation {
			(annotation as? MKUserLocation)?.title = ""
			return nil
		}
		if let annotation = annotation as? MyntAnnotation {
			var view = mapView.dequeueReusableAnnotationView(withIdentifier: annotation.sn)
			if view == nil {
				view = MyntAnnotationView(annotation: annotation, reuseIdentifier: annotation.sn)
				view?.canShowCallout = false
				view?.centerOffset = CGPoint(x: 0, y: -35)
			}
			view?.image = imageCache(annotation.sn)
			return view
		}
		return nil
	}
	func mapView(_ mapView: MKMapView, didSelect view: MKAnnotationView) {
		if view.annotation is MKUserLocation { return }

		if let annotation = view.annotation as? MyntAnnotation,
			let mapMynt = mapMynts.first(where: { $0.sn == annotation.sn }) {
			if mapMynt.subMapMynts.count > 1 {
				view.showMapMyntCollectionView(mapMynts: mapMynt.subMapMynts)
			}
		}
	}

	func mapView(_ mapView: MKMapView, didDeselect view: MKAnnotationView) {
		if view is MyntAnnotationView {
			for subview in view.subviews {
				subview.removeFromSuperview()
			}
		}
	}

	func mapView(_ mapView: MKMapview, regionDidChangeAnimated animated: Bool) {
		aggregation()
	}
}

