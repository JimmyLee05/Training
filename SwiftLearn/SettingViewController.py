import UIKit
import MYNTKit
import SlightechKit

class SettingViewController: MYNTKitBaseViewController, SegmentViewDelegate {
	
	@IBOutlet weak var segmentView: SegmentView!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var maskView: GradientView!
	@IBOutlet weak var qaButton: GradientButton!

	var appSettingView: AppSettingView!
	var accountView: AccountView!

	override func viewDidLoad() {
		super.viewDidLoad()

		title = MTLocalizedString("APP_SETTINGS", comment: "设置")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		appSettingView ?= AppSettingView.createFromXib()
		appSettingView.viewController 	= self
		appSettingView.isHidden 		= false
		appSettingView.translatesAutoresizingMaskIntoConstraints = false
		appSettingView.fillInSuperView()

		accountView ?= AccountView.createFromXib()
		accountView.viewController 		= self
		accountView.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubview(accountView!)
		accountView.fillInSuperView()

		//初始化segmentView
		let appsettings 				= MTLocalizedString("APPLICATION_SETTINGS", comment: "")
		let accountSettings 			= MTLocalizedString("ACCOUNT_SETTINGS", comment: "")
		segmentView.delegate 			= self
		segmentView.font 				= UIFont.boldSystemFont(ofSize: 15)
		segmentView.setTextColor(color: UIColor(red:0.79, green:0.79, blue:0.79, alpha:1.00), state: .normal)
		segmentView.setTextColor(color: UIColor.black, state: .selected)
		segmentView.setBackgroundColor(color: UIColor(red:0.97, green:0.97, blue:0.97, alpha:1.00), state: .normal)
		segmentView.setBackgroundColor(color: UIColor.white, state: .selected)

		//初始化客服按钮
		qaButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		qaButton.setTitle(" " + MTLocalizedString("Q_A", comment: ""), for: .normal)
		//遮罩
		maskView.loadTableViewMaskStyle()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true)
		MYNTKik.shared.removeMyntKitDelegate(key: selfKey)
	}

	@IBAction func didClickQAButton(_ sender: UIButton) {
		CustomerCareKit.open(self)
	}

	func segment(segmentView: SegmentView, didSelectIndex index: Int) {
		appSettingView.isHidden 	= index == 1
		accountView.isHidden 		= index == 0
	}
}

extension SettingViewController {
	
	//点击是否关闭报警
	func didSelectCloseMyntAlarmInSafeZone(isCloseAlarm: Bool) {
		MYNTKit.shared.isCloseAlarmSafeZone = isCloseAlarm
		MTToast.show(isCloseAlarm ?
			MTLocalizedString("SECURE_DISABLE_MYNT_ALARM_ON_MESSAGE", comment: "") :
			MTLocalizedString("SECURE_DISABLE_MYNT_ALARM_OFF_MESSAGE", comment: ""))
	}

	//点击帮助
	func didSelectFAQ(atIndex index: Int) {
		let faqViewController = FAQViewController(htmlName: String(format: MTLocalizedString("HOW_TO_HTML", comment: ""), index + 1))
		present(BaseNavigationController(rootViewController: faqViewController), animated: true, completion: nil)
	}

	//点击选择安全区域
	func didSelectSafeZone(atIndex index: Int) {
		let viewController = safeZoneViewController()
		viewController.safeZone = MYNTKit.shared.safeZones[index]
		present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	//点击删除安全区域
	func didClickDeleteSafeZone(atIndex index: Int) {
		let safeZone = MYNTKit.shared.safeZones[index]
		if safeZone.isEmpty {
			return MTToast.show(String(format: MTLocalizedString("SECURE_AREA_NO_HOME_OFFICE", comment: "安全区域未设置，不能点击删除"),
				safeZone.showName))
		}
		//提示框
		let isDefault = safeZone.locationType != .custom
		DialogManager.shared.show(type: isDefault ? .clearSafeZone : .deleteSafeZone, text: safeZone.showName) { _ in
			safeZone.delete()
		}
	}

	//点击新增安全区域
	func didClickAddSafeZone() {
		let viewController = SafeZoneViewController()
		present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}

	//点击购买小觅
	func didClickBuyMynt() {
		if isInJapan {
			guard let url = URL(string: buyMyntURL) else { return }
			UIApplication.shared.openURL(url)
			return
		}
		DialogManager.shared.showSelectionDialog(dialogType: .buy,
												 title: MTLocalizedString("BUYMORE_TITLE", comment: "title"),
												 leftImage: UIImage(named: "appsettings_buymore_mynts_96dpx75dp"),
												 leftName: MTLocalizedString("BUYMORE_MYNT", comment: "购买小觅"),
												 rightImage: UIImage(named: "appsettings_buymore_battery_96dpx75dp"),
												 rightName: MTLocalizedString("BUYMORE_BATTERY", comment: "购买电池"),
												 buttonString: MTLocalizedString("BUYMORE_BUY", comment: "buy")) { _ type in
													switch type {
													case .left:
														UIApplication.shared.openURL(URL(string: buyMyntURL)!)
													case .right:
														UIApplication.shared.openURL(URL(string: buyBatteryURL)!)
													}
		}
	}
}

extension SettingViewController {
	
	func didAddSafeZone(safeZone: SafeZone) {
		appSettingView.tableView.reloadData()
	}

	func didRemoveSafeZone(safeZone: SafeZone) {
		addSettingView.tableView.reloadData()
	}

	func didUpdateZone(safeZone: SafeZone) {
		appSettingView.tableView.reloadData()
	}

	func myntKit(myntKit: MYNTKit, didAddMynt mynt: Mynt) {
		accountView.updateMyntCount()
	}

	func myntKit(myntKit: MYNTKit, didRemoveMynt mynt: Mynt) {
		accountView.updateMyntCount()
	}

	func user(user: User, didUpdateAvatar avatar: UIImage?) {
		accountView.avatarImageView.image = avatar
	}

	func didLoginUser(user: user) {
		accountView.updateInfo()
	}
}

