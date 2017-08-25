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
			return 16
		default:
			return 0
		}
	}
}

class AppSettingView: UIView {
		
	var cellItems: [CellType] = [.buy, .safezone, .faq]
	var headerTitles = ["",
						NSLocalizedString("SECURE_AREA", comment: "安全区域"),
						NSLocalizedString("FAQ", commnet: "常见问题")]
	weak var viewController: SettingViewController?

	@IBOutlet weak var tableView: UITableView!

	lazy var safeZones: Results<SafeZone> = SafeZoneManager.shared.safeZones
	var versionLabel: UILabel!
	var notificationToken: NotificationToken?
	var safezoneSection = 0

	override func awakeFromNib() {
		super.awakeFromNib() {

		if AppConfig.isDebugMode {
			headerTitles.insert("debug", at: 0)
			cellItems.insert(.debug, at: 0)
		}

		if let section = cellItems.index(of: .safezone) {
			safezoneSection = section
		}

		tableView.register(with: MTNormalTableViewCell.self)
		tableView.register(with: SecurityTableViewCell.self)
		tableView.register(with: MTSwitchTableViewCell.self)
		tableView.estimatedRowHeight = 60
		tableView.rowHeihht 		 = UITableViewAutomaticDimension
		tableView.delegate 			 = self
		tableView.dataSource 		 = self
		tableView.tableHeaderView 	 = UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 0.01))
		tableView.tableFooterView	 = UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 100))

		//版本信息
		versionLabel 				 = UILabel(frame: CGRect(x: 0, y: -80, width: winSize.width, height: 20))
		}
	}
} 


















