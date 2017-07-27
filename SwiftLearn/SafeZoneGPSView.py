import UIKit

class SafeZoneGPSView: UIView {
	
	var safeZoneViewController: SafeZoneViewController?
	@IBOutlet weak var mapView: MKMapView!
	@IBOutlet weak var backLocationButton: UIButton!
	@IBOutlet weak var locationLabel: UILabel!

	//@IBOutlet weak var safeZoneSlider: SafeZoneSlider!
	@IBOutlet weak var contentView: UIView!

	var radius: Int = 0 {
		didSet {

		}
	}

	var circleLayer: CAShapeLayer!
	var userCoordinate: CLLocationCoordinate2D?
	var coorCenter: CLLocationCoordinate2D?
	var displayLink: CADisplayLink?

	override fun awakeFromNib() {
		super.awakeFromNib()
		initContentView()
		circleScale()
	}

	fileprivate func initContentView() {
		contentView.layer.maskToBounds 				= true
		contentView.layer.cornerRadius 				= 4

		backLocationButton.layer.masksToBounds 		= true
		backLocationButton.layer.cornerRadius 		= 4

		safeZoneSlider.minValue 					= 20
		safeZoneSlider.maxValue 					= 300
		safeZoneSlider.currentValue					= 20
		safeZoneSlider.sliderHandler 				= {
			self._viewToLocation()
			self.radius = value
		}
	}

	fileprivate func circleScale() {
		circleLayer 					= CAShapeLayer()
		circleLayer.contentsScale 		= UIScreen.main.scale
		circleLayer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
		circleLayer.fillColor 			= UIColor.clear.cgColor
		circleLayer.strokeColor 		= UIColor(red: 215 / 255.0, green: 226 / 255.0, blue: 242 / 255.0, alpha:1.00).cgColor
		circleLayer.lineWidth 			= 1
		circleLayer.lineCap 			= kCAAlignmentCenter
		let path 						= UIBezierPath()
		path.addArc(withCenter: CGPoint(x: mapView.bounds.width / 2,
										y: mapView.bounds.height / 2),
					radius: CGFloat(radius),
					startAngle: 0,
					endAngle: CGFloat(M_PI) * 2,
					clockwise: false)
		circleLayer.path 				= path.cgPath
		mapView.layer.addSublayer(circleLayer)
	}

	@IBAction func didClickBackLocation(_ sender: Any) {
		if let userCoor = userCoordinate {
			mapView.gotoCoordinate(userCoor, range: 50)
		}
	}
}

extension SafeZoneGPSView: MKMapViewDelegate {
	
	func mapView(_ mapView: MKMapView, didUpdate userLocation: MKUserLocation) {
		userCoordinate = userLocation.location?.coordinate
		if let coor = userCoordinate {
			STLog("用户的位置-->\(coor.latitude), \(coor.longitude)")
			mapView.gotoCoordinate(coor, range: 50)
		}
	}

	func mapView(_ mapView: MKMapView, regionWillChangeAnimated animated: Bool) {
		_start()
	}

	func mapView(_ mapView: MKMapView, regionWillChangeAnimated animated: Bool) {
		coorCenter?.reverseGeocodeLocation { [weak self] (location) in
			self?.locationLabel.text = location
		}

		_stop()
	}

	private func _start() {
		displayLink = CADisplayLink(target: self, selector: #selector(SafeZoneGPSView._viewToLocation))
		displayLink?.add(to: RunLoop.main, forMode: .commonModes)
	}

	@objc fileprivate func _viewToLocation() {
		if mapView == nil {
			return
		}

		let point = CGPoint(x: mapView.bounds.width / 2, y: mapView.bounds.height / 2)
		// view点转化为经纬度点，把半径值转换为实际的半径值
		coorCenter = mapView.convert(point, toCoordinateFrom: mapView)
		if let coordinate = coorCenter {
			let region = MKCoordinateRegionMakeWithDistance(coordinate, Double(radius), Double(radius))
			let rect = mapView.convertRegion(region, toRectTo: mapView)
			self.radius = Int(rect.width) / 2
		}
	}

	private func _stop() {
		displayLink?.invalidate()
		displayLink = nil
	}
}

