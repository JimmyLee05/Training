import UIKit

class MyntSimCheckViewController: BaseViewController {
	
	public class func show(parentViewController: UIViewController?, sn: String?) {
		let viewController = MyntSimCheckViewController()
		viewController.sn  = sn
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: true,
									  completion: nil)
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = "SIM卡检测工具"
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		if sn?.mynt?.bluetoothState != .connected {
			let alert = UIAlertView(title: "", message: "设备蓝牙未连接！"， delegate: nil, cancelButtonTitle: nil, otherButtonTitle: "确认")
			alert.show()
			return
		}
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		dismiss(animated: true)
	}
}