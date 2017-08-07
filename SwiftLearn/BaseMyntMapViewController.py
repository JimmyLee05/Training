import UIKit
import Foundation
import MYNTKit
import SCloudKit
import MapKit
import RealmSwift
import SlightechKit
 
extension SCDevice.SCLocation. `Type` {
	
	var typeName: String {
		switch self {
		case .gps:
			return NSLocalizedString("GPS定位", comment: "")
		case .station:
			return NSLocalizedString("基站定位", comment: "")
		case .mobile:
			return NSLocalizedString("手机定位", comment: "")
		default:
			return ""
		}
	}
}

// MRAK: - Location转CLLocationCoordinate2D
extension SCDevice.SCLocation {
	
	var coordinate: CLLocationCoordinate2D {
		return CLLocationCoordinate2DMake(latitude, longitude)
	}
}

struct MyntMapLocation {
	//经纬度
	var coordinate = CLLocationCoordinate2DZero
}

//底部圆圈
public class MyntCircleAnnotation: NSObject, MKAnnotation {
	
	public var coordinate: CLLovationCoordinate2D {
		willSet {
			willChangeValue(forKey: "coordinate")
		}
		didSet {
			didChangeValue(forKey: "coordinate")
		}
	}

	//GCD初始化
	init(coordinate: CLLocationCoordinate2D) {
		self.coordinate = coordinate
	}
}

class BaseMyntMapViewController: BaseViewController {
	
	class PositionItem: NSObject, CoordinateItemProtocol {

		var time: TimeInterval = 0

		var coordinate: CLLocationCoordinate2D = CLLocationCoordinate2DMake(0, 0)
		var locationType: SCDevice.SCLocation. `Type` = .none

		init(location: SCDevice.SCLocation) {
			self.time 			= TimeInterval(location.updateTime)
			self.coordinate 	= CLLocationCoordinate2DMake(location.latitude, location.longitude).offsetLocation
			self.locationType 	= location.type
		}

		init(userCoordinate: CLLocationCoordinate2D) {
			self.item 			= 0
			self.coordinate 	= userCoordinate
		}

		
	}
}























