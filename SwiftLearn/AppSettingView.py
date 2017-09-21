import UIKit
import MYNTKit
import SlightechKit
import RealmSwift

enum CellType {
	
	case debug
	case laboratory
	case buy
	case safezone
	case faq

	var count: Int {
		switch self {
		case .debug, .buy, .laboratory:
			return 1
		case .faq:
			return 26
		default:
			return 0
		}
	}
}

class AppSettingView: UIView {
	
	var cellItems: [CellType] = [.buy, .safezone, .faq]
	var headerTitles = ["",
						MTLocalizedString("SECURE_AREA", comment: "安全区域"),
						MTLocalizedString("FAQ", comment: "常见问题")]

	weak var viewController: SettingViewController?

	@IBOutlet weak var tableView: UITableView!

	var safeZones: [SafeZone] {
		return MYNTKit.shared.safeZones
	}

	var versionLabel: UILabel!
	var safezoneSection = 0

	override func awakeFromNib() {
		super.awakeFromNib()

		if AppConfig.isDebugMode {
			headerTitles.insert("debug", at: 0)
			cellItems.insert(.debug, at: 0)
		}

		// headerTitles.insert("laboratory", at: 0)
		// cellItems.insert(.laboratory, at: 0)

		
	}
}



























