import UIKit
import SlightechKit

class ShareViewController: BaseViewController {
	
	class func present(parentViewController: UIViewController?, sn: String?) {
		
		let viewController = ShareViewController()
		viewController.sn  = sn
		parentViewController?.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)	
	}

	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var messageLabel: UILabel!

	@IBOutlet weak var linkButton: GradientButton!

	@IBOutlet weak var wechatButton: GradientButton!
	override var isNeedAddMyntNotification: Bool { return true }
	override var isShowBackgroundLayer: Bool { return false }

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("SHARE_ASK_FRIEND", comment: "求助")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		
	}
}