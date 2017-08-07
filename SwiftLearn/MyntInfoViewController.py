import UIKit
import AVOSCloud

class MyntInfoViewController: BaseViewController {
	
	class func push(sn: String?, parentViewController: UIViewController?) {
		DispatchQueue.main.async {
			let viewController = MyntInfoViewController(sn: sn)
			parentViewController?.removeBackBarButtonTitle()
			parentViewController?.push(viewController: viewController)
		}
	}

	override var isNeedAddMyntNotification: Bool { return true }

	override var isShowBackgroundLayer: Bool { return false }

	var contentView: MyntInfoView?

	//MARK: - 方法开始
	deinit {
		printDeinitLog()
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
	}

	fileprivate init(sn: String?) {
		super.init(nibName: nil, bnundle: nil)
		self.sn = sn 
	}

	fileprivate override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
	}

	internal required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		initNavigationBar()
		initView()

		initMyntListener()

		initData()

		uploadLeanClound()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		//透明标题栏
		setNavigationBarBackground()
	}

	//更新属性
	override func updateProperty(mynt: Mynt, name: String, oldValue: Any?, newValue: Any?) {
		execUpdateProperty(mynt: mynt, name: name, oldValue: oldValue, newValue: newValue)
	}

	func uploadLeanClound() {
		let userDefaults = UserDefaults.standard
		if let mynt = sn?.mynt,
			let software = Int(mynt.software), !userDefaults.bool(forKey: mynt.sn) {
			if software >= 29 && mynt.hardwareType == .CC26XX {
				let obj = AVObject(className: 'mynt_battery_collect')
				obj.setObject("ios", forKey: "system")
				obj.setObject(sn, forKey: "sn")
				obj.setObject(MYNTKit.shared.user?.userName, forKey: "name")
				obj.saveInBackground()
				userDefaults.set(true, forKey: mynt.sn)
				userDefaults.synchronize()
			}
		}
	}
}


