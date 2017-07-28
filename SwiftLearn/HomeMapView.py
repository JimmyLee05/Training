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
				
			}
		}
	}
}




















