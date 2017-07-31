import UIKit
import MYNTKit
import SlightechKit

// App设置和用户界面设置
class SettingViewController: BaseViewController, SegmentViewDelegate {
	
	@IBOutlet weak var segmentView: SegmentView!
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var maskView: GradientView!
	@IBOutlet weak var qaButton: GradientButton!

	var appSettingView: AppSettingView!
	var accountView: AccountView!

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		title = NSLocalizedString("APP_SETTINGS", comment: "设置")
		setLeftBatButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		appSettingView ?= AppSettingView.createFromXib()
		appSettingView.viewController 	= self
		appSettingView.isHidden 		= false
		appSettingView.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubview(appSettingView!)
		appSettingView.fileInSuperView()

		accountView ?= AccountView.createFromXib()
		accountView.viewController 		= self
		accountView.isHidden 			= true
		accountView.translatesAutoresizingMaskIntoConstraints = false
		contentView.addSubview(accountView!)
		accountView.fillInSuperView()

		//初始化segmentView
		let appsettings 	= NSLocalizedString("APPLICATION_SETTINGS", commnet: "")
		let accountSettings = NSLocalizedString("ACCOUNT_SETTINGS", comment: "")
		segmentView.titles 		= [appsettings, accountSettings]
		segmentView.delegate 	= self
		segmentView.font 		= UIFont.boldSystemFont(ofSize: 15)
		segmentView.setTextColor(color: UIColor(red:0.79, green:0.79, blue:0.79, alpha:1.00), state: .normal)
		segmentView.setTextColor(color: UIColor.black, state: .selected)
		segmentView.setBackgroundColor(color: UIColor(red:0.97, green:0.97, blue:0.97, alpha:1.00), state: .normal)
		segmentView.setBackgroundColor(color: UIColor.white, state: .selected)

		//初始化客服按钮
		qaButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		qaButton.setTitle(" " + NSLocalizedString("Q_A", comment: ""), for: .normal)
		//遮罩
		maskView.loadTableViewMaskStyle()
	}　　　　　　　　　　　　　　　　　　　　　　　

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}　　　　　　　　　　　　　　　　　　 

	override func leftBarButtonClickHandler() {
		dismissNavigationController(animated: true)
	}

	override func didClickQAButton(_ sender: UIButton) {
		CustomerCareKit.open(self)
	}

	func segment(segmentView: SegmentView, didSelectIndex index: Int) {
		appSettingView.isHidden 	= index == 1
		accountView.isHidden 		= index == 0
	}
}


