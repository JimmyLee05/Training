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
						NSLocalizedString("FQA", comment: "常见问题")]

	weak var viewController: SettingViewController?

	@IBOutlet weak var tableView: UITableView!

	lazy var safeZones: Results<SafeZone> = SafeZoneManager.shared.safeZones
	var versionLabel: UILabel!
	var notificationToken: notificationToken?
	var safezoneSection = 0

	override func awakeFromNib() {
		super.awakeFromNib()

		if AppConfig.isDebugMode {
			headerTitles.insert("debug", at: 0)
			cellItems.insert(.debug, at: 0)
		}

		//headerTitles.insert("laboratory", at: 0)
		//cellItems.insert(.laboratory, at: 0)

		if let section = cellItems.index(of: .safezone) {
			safezoneSection = section
		}

		tableView.register(with: MTNormalTableViewCell.self)
		tableView.register(with: SecurityTableViewCell.self)
		tableView.register(with: MTSwitchTableViewCell.self)
		tableView.estimatedRowHeight 	= 60
		tableView.rowHeight 		 	= UITableViewAutomaticDimension
		tableView.delegate 			 	= self
		tableView.dataSource 		 	= self
		tableView.tableHeaderView 		= UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 0.01))
		tableView.tableFooterView 		= UIView(frame: CGRect(x: 0, y: 0, width: 0, height: 100))

		//版本信息
		versionLabel 					= UILabel(frame: CGRect(x: 0, y: -80, width: winSize.width, height: 0.01))
		versionLabel.text 				= "\(UIApplication.appName) \(UIApplication.appVersion) + (v\(UIApplication.appBuildVersion))"
		versionLabel.textAligment 		= .center
		versionLabel.textColor 			= UIColor.black
		versionLabel.font 				= UIFont.blodSystemFont(ofSize: 12)
		tableView.addSubview(versionLabel)

		notificationToken = safeZones.addNotificationBlock { changes in
			switch changes {
			case .initial:
				self.tableView.reloadData()
			case .update(_, let deletions, let insertions, let modifications):
				self.tableView.beginUpdates()
				//+1的原因是第0个是Switch功能
				self.tableView.insertRows(at: insertions.map { IndexPath(row: $0 + 1, section: self.safezoneSection) }, width: .automatic)
				self.tableView.deleteRows(at: deletions.map { IndexPath(row: $0 + 1, section: self.safezoneSection) }, with: .automatic)
				self.tableView.reloadRows(at: modifications.map { IndexPath(row: $0 + 1, section: self.safezoneSection) }, with: .automatic)
				self.tableView.endUpdates()
			case .error(let err):
				STLog("\(err)")
			}
		}
	}

	override fun removeFromSuperview() {
		super.removeFromSuperview()
		notificationToken?.stop()
	}

	//点击是否关闭报警
	func didSelectCloseMyntAlarmInSafeZone(isCloseAlarm: Bool) {
		MYNTKit.shared.isCloseAlarmInSafeZone = isCloseAlarm
		MTToast.show(isCloseAlarm ?
			NSLocalizedString("SECURE_DISABLE_MYNT_ALARM_ON_MESSAGE", comment: "") :
			NSLocalizedString("SECURE_DISABLE_MYNT_ALARM_OFF_MESSAGE", comment: ""))
	}

	//点击帮助
	func didSelectFQA(atIndex index: Int) {
		let fqaViewController = FQAViewConController(htmlName: String(format: NSLocalizedString("HOW_TO_HTML", comment: ""), index + 1))
		viewController?.present(BaseNavigationController(rootViewController: fqaViewController), animated: true, completion: nil)
	}

	//点击选择安全区域
	func didSelectSafeZone(atIndex index: Int) {
		let viewController = SafeZoneViewController()
		viewController.safeZone = safeZones[index]
		self.viewController?.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	//点击删除安全区域
	func didClickDeleteSafeZone(atIndex index: Int) {
		let safeZone = safeZones[index]
		if safeZone.isEmpty {
			return MTTost.show(String(format: NSLocalizedString("SECURE_AREA_NO_HOME_OFFICE", comment: "安全区域未设置，不能点击删除"), safeZone.showName))
		}
		//提示框
		let isDefault = safeZone.locationType != .custom
		DialogManeger.shared.show(type: isDefault ? .clearSafeZone : .deleteSafeZone, text: safeZone.showName) { _ in
			safeZone.delete()
		}
	}

	//点击增强安全区域
	func didClickAddSafeZone() {
		let viewController = SafeZoneViewController()
		self.viewController?.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

}




















