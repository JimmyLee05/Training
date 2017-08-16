import Foundation
import STPermissionKit

extension STPermissionType {
	
	var dialogTitle: String {
		switch self {
		case .bluetooth:
			return NSLocalizedString("DETECTION_BLUETOOTH_TITLE", comment: "蓝牙")
		case .locationAlways:
			return NSLocalizedString("DETECTION_LOCATION_TITLE", comment: "定位")
		case .notifications:
			return NSLocalizedString("DETECTION_NOTIFICATION_TITLE", comment: "通知")
		case .backgroundRefresh:
			return NSLocalizedString("DETECTION_BACKGROUND_TITLE", comment: "后台刷新")
		default:
			return ""
		}
	}

	var dialogMessage: String {
		switch self {
		case .bluetooth:
			return NSLocalizedString("DETECTION_BLUETOOTH_TIPS", comment: "")
		case .locationAlways:
			return NSLocalizedString("DETECTION_LOCATION_TIPS", comment: "")
		case .notifications:
			return NSLocalizedString("DETECTION_NOTIFICATION_TIPS", comment: "")
		case .backgroundRefresh:
			return NSLocalizedString("DETECTION_BACKGROUND_TIPS", comment: "")
		default:
			return ""
		}
	}

	var homeListName: String {
		switch self {
		case .bluetooth:
			return NSLocalizedString("DETECTION_BLUETOOTH_TIPS", comment: "")
		case .locationAlways:
			return NSLocalizedString("DETECTION_LOCATION_TIPS", comment: "")
		case .notifications:
			return NSLocalizedString("DETECTION_NOTIFICATION_TIPS", comment: "")
		case .backgroundRefresh:
			return NSLocalizedString("DETECTION_BACKGROUND_TIPS", comment: "")
		default:
			return ""
		}
	}

	var image: UIImage? {
		switch self {
		case .bluetooth:
			return UIImage(named: "dialog_bluetooth")
		case .locationAlways:
			return UIImage(named: "dialog_location")
		case .notifications:
			return UIImage(named: "dialog_notice")
		case .backgroundRefresh:
			return UIImage(named: "dialog_refresh")
		default:
			return nil
		}
	}
}


