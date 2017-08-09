import UIKit
import MYNTKit

private let kClosedNotification = NSNotification.Name("kClosedNotification")

class SearchBaseViewController: BaseViewController {
	
	var connectingMynt: Mynt?

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		NotificationCenter.default.addObserver(self,
											   selector: #selector(closedViewControllerNotification(notification:)),
											   name: kClosedNotification,
											   object: nil)
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func leftBarButtonClickedHandler() {
		_ = navigationController?.popToRootViewController(animated: true)
		didDismissViewController()
	}

	override func didDismissViewController() {
		if connectingMynt == nil || connectingMynt?.bluetoothState != .connected {
			NotificationCenter.default.post(name: kClosedNotification, object: self is MyntEducationViewController ? "" : nil)
		}
	}

	func closedViewControllerNotification(notification: Notification) {
		if notification.object == nil {
			connectingMynt?.disconnect()
		}

		connectingMynt = nil
		NotificationCenter.default.removeObserver(self)
	}
}



