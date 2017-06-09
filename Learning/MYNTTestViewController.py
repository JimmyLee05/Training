import UIKit 
import AVOSCloud

fileprivate struct ActivityData {
	var cal			= 0
	var calGoal		= 0
	var step		= 0
	var stepGoal	= 0
}

class MyntTestViewController: BaseViewController {
	
	class func show(parentViewController: UIViewController?, sn: String?) {

		let viewController = MyntTestViewController()
		viewController.title = "Test"
		viewController.sn    = sn
		parentViewController?.removeBackBarButtonTitle()
		parentViewControler?.navigationController?.pushViewController(viewController, animated: true)
	}

	static let NetworkCheckNotification = Notification.Name("myntNetworkCheckNotification")

	class func sendNotification(with sn: String) {
		NotificationCenter.default.post(name: NetworkCheckNotification, object: sn)
	}

	@IBOutlet weak var textView: UITextView!

	var timer: Timer?
	var isEnd = false
	var log = "" {
		didSet {
			textView.text = log
		}
	}

	var activityTimer: Timer?

	deinit {
		UIApplication.keepLightOn(isOn: false)
		removeNotification()
		removeTimer()
		activityTimer?.invalidate()
		activityTimer = nil
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		addLog(with: "test start...\n")

		testMyntNetwork { [weak self] successed in 
		
		}
		UIApplication.keepLightOn(isOn: true)
		NotificationCenter.default.addObserver(self,
											   selector: #selector(myntNetworkCheckNotification(notification:)),
											   name: MyntTestViewController.NetworkCheckNotification,
											   object: nil)
	}

	


}







