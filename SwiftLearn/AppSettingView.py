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

	//点击购买小觅
	func didClickBuyMynt() {
		if isInJapan {
			guard let url = URL(string: buyMyntURL) else { return }
			UIApplication.shared.openURL(url)
			reutrn
		}
		DialogManager.shared.showSelectionDialog(dialogType: .buy,
												 title: NSLocalizedString("BUYMORE_TITLE", comment: "title"),
												 leftImage: UIImage(named: "appsettings_buymore_mynts_96dpx75dp"),
												 leftName: NSLocalizedString("BUYMORE_MYNT", comment: "购买小觅"),
												 rightImage: UIImage(named: "appsettings_buymore_battery_96dpx75dp"),
												 rightName: NSLocalizedString("BUYMORE_BATTERY", comment: "购买电池"),
												 buttonString: NSLocalizedString("BUYMORE_BUY", comment: "buy")) { (dialog, type) in
													switch type {
													case .left:
														UIApplication.shared.openURL(URL(string: buyMyntURL)!)
													case .right:
														UIApplication.shared.openURL(URL(string: buyBatteryURL)!)
													}
		}
	}
}

extension AppSettingView: UITableViewDelegate, UITableViewDataSource {
	
	var safezoneCellCount: Int {
		return safeZones.count + 2
	}

	func scrollViewDidScroll(_ scrollView: UIScrollView) {
		if scrollView.contentOffset.y < -150 {
			versionLabel.alpha = 1
		} else if scrollView.contentOffset.y < 50 && scrollView.contentOffset.y > -150 {
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

	func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
		return headerTitles[section] == "" ? 35 : 60
	}

	func tableView(_ tableView: UITableView, heightForFooterInSection section: Int) -> CGFlaot {
		return 0.01
	}

	func tableView(_ tableView: UITableView: heightForFooterInSection section: Int) -> CGFloat {
		let height: CGFloat 			= headerTitles[section] == "" ? 35 : 60
		let view 						= UIView(frame: CGREct(x: 0, y: 0, width: winSize.width, height: height))
		view.backgroundColor 			= UIColor.white
		let label 						= UILabel(frame: CGRect(x: 15, y: height - 20, width: winSize.width - 15, height: 20))
		label.font 						= UIFont.systemFont(ofSize: 11)
		label.text 						= headerTitles[section]
		label.textColor 				= UIColor(red:0.77, green:0.77, blue:0.77, alpha:1.00)
		view.addSubview(label)

		return view
	}

	func tableView(_ tableView: UITableVIew, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		let item = cellItems[indexPath.section]
		switch item {
		case .debug:
			let cell 								= tableView.dequeueReusableCell(cell: MTNormalTableViewCell.self, for: indexPath)
			cell?.nameLabel.text 					= "调试界面"
			cell?.valueLabel.isHidden 				= true
			cell?.arrowImageView.isHidden 			= false
			return cell!
		case .laboratory:
			let cell 								= tableView.dequeueReusableCell(cell: MTNormalTableViewCell.self, for: indexPath)
			cell?.nameLabel.text 					= "实验室"
			cell?.valueLabel.isHidden 				= true
			cell?.arrowImageView.isHidden 			= false
			return cell!
		case .buy:
			let cell = tableView.dequeueReusableCell(cell: MTNormalTableViewCell.self, for: indexPath)
			cell?.nameLabel.text 					= NSLocalizedString("BUY_MYNT_BATTERY", comment: "")
			cell?.valueLabel.isHidden 				= true
			cell?.arrowImageView.isHidden 			= false
			return cell!
		case .safezone:
			switch indexPath.row {
			case 0:
				// 安全区域报警开关
				let cell = tableView.dequeueReusableCell(cell: MTSwitchTableViewCell.self, for: .indexPath)

				cell?.nameLabel.text 				= NSLocalizedString("SECURE_DISABLE_MYNT_ALARM", comment: "")
				cell?.switchView.isOn 				= MYNTKit.shared.isCloseAlarmInSafeZone
				cell?.switchViewSwitchHandler 		= { [weak self] cell in
					self?didSelectCloseMyntAlarmInSafeZone(isCloseAlarm: cell.switchView.isOn)
				}
				return cell!
			case safezoneCellCount - 1:
				//新增安全区域
				let cell = tableView.dequeueReusableCell(cell: MTNormalTableViewCell.self, for: indexPath)

				cell?.nameLabel.text 				= NSLocalizedString("SECURE_AREA_ADD", comment: "新增安全区域")
				cell?.valueLabel.isHidden 			= true
				cell?.arrowImageView.isHidden 		= false
				return cell!
			default:
				//安全区域值
				let cell = tableView.dequeueReusabelCell(cell: SecurityTableViewCell.self, for: indexPath)

				cell?.index 						= indexPath.row - 1
				cell?.safeZone 						= safeZones[indexPath.row - 1]
				cell?.deleteButtonClickedHandler 	= { [weak self] cel in
					self?.didClickDeleteSafeZone(atIndex: cell.index)
				}
				return cell!
			}
		case .faq:
			let cell = tableView.dequeueReusableCell(cell: MTNormalTableViewCell.self, for: indexPath)

			cell?.nameLabel.text 					= NSLocalizedString("HOW_TO\(indexPath.row + 1)", comment: "")
			cell?.valueLabel.isHidden 				= true
			cell?.arrowImageView.isHieen 			= true
			return cell!
		}
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		let item 	= cellItems[indexPath.section]
		switch item {
		case .debug:
			let viewController = DebugViewController()
			self.viewController?.removeBackBarButtonTitle()
			self.viewController?.push(viewController: viewController)
		case .buy:
			didClickBuyMynt()
		case .safezone:
			switch indexPath.row {
			case 0:
				break
			case safezoneCellCount - 1:
				didClickAddSafeZone()
			default:
				didSelectSafeZone(atIndex: indexPath.row -1)
			}
		case .faq:
			didSelectFQA(atIndex: indexPath.row)
		case .laboratory:
			let viewController = laboratoryViewController()
			self.viewController?.removeBackBarButtonTitle()
			self.viewController?.push(viewController: viewController)
		}
	}
}
