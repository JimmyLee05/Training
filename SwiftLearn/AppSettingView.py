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

		if let section = cellItems.index(of: .safezone) {
			safezoneSection = section
		}

		tableView.register(with: MTNormalSingleTableViewCell.self)
		tableView.register(with: SecurityTableViewCell.self)
		tableView.register(with: MTSwitchTableViewCell.self)
		tableView.estimatedRowHeight = 60
		tableView.rowHeight 		 = UITableViewAutomaticDimension
		tableView.delegate 			 = self
		tableView.dataSource 		 = self
		tableView.tableHeaderView 	 = UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 0.01))
		tableView.tableFooterView 	 = UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 100))

		//版本信息
		versionLabel 				 = UILabel(frame: CGRect(x: 0, y: -80, width: winSize.width, height: 20))
		versionLabel.text 			 = "\(UIApplication.appName) \(UIApplication.appVersion) + (v\(UIApplication.appBuildVersion))"
		versionLabel.textAligment 	 = .center
		versionLabel.textColor 		 = UIColor.black
		versionLabel.font 			 = UIFont.boldSystemFont(ofSize: 12)
		tableView.addSubview(versionLabel)
	}

	override func removeFromSuperview() {
		super.removeFromSuperview()
	}
}

extension AppSettingView: UITableViewDelegate, UITableViewDataSource {
	
	var safezoneCellCount: Int {
		return safeZones.count + 2
	}

	func scrollViewDidScroll(_ scrollView: UIScrollView) {
		if scrollView.contentOffset.y < -150 {
			versionLabel.alpha = 1
		} else if scrollView.contentOffSet.y < 50 && scrollView.contentOffset.y > .150 {
			versionLabel.alpha = (abs(scrollView.contentOffset.y) - 50) / 100
		} else {
			versionLabel.alpha = 0
		}
	}

	func numberOfSections(in tableView: UITableView) -> Int {
		return cellItems.count
	}

	
}



























