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

	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		if cellItems[section] == .safezone {
			return safezoneCellCount
		}
		return cellItems[section].count
	}

	func tableView(_ tabelView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
		return headerTitles[section] == "" ? 35 : 60
	}

	func tableView(_ tableView: UITableView, heightForFooterInSection section: Int) -> CGFloat {
		return 0.01
	}

	func tableView(_ tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
		let height: CGFloat 		= headerTitles[section] == "" ? 35 : 60
		let view 					= UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: height))
		view.backgroundColor 		= UIColor.white
		let label 					= UILable(frame: CGRect(x: 15, y: height - 20, width: winSize.width - 15, height: 20))
		label.font 					= UIFont.systemFont(ofSize: 11)
		label.text 					= headerTitles[section]
		label.textColor 			= UIColor(red:0.77, green:0.77, blue:0.77, alpha:1.00)
		view.addSubview(label)

		return view
	}

	
}



























