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

	// MARK: - 方法开始
	deinit {
		printDeinitLog()
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
	}

	fileprivate init(sn: String?) {
		super.init(nibName: nil, boundle: nil)
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

		uploadLeanCloud()
	}

	override func didReceiveMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)
		//透明标题栏
		setNavigationBarBackground()
	}

	//更新属性
	override func updateProperty(mynt; Mynt, name: String, oldValue: Any?, newValue: Any?) {
		_updateProperty(mynt: mynt, name: name, oldValue: oldValue, newValue: newValue)
	}

	func uploadLeanCloud() {
		if let mynt = sn?.mynt {
			if mynt.software == "46" && mynt.hardware.hasPrefix("Beta") {
				let obj = AVObject(className: "mynt_battery_collect")
				obj.setObject("ios", forKey: "system")
				obj.setObject(sn, forKey: "sn")
				obj.saveInBackground()
			}
		}
	}

}
