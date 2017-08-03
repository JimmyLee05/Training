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

		messageLabel.numberOfLines = 0
		messageLabel.text = NSLocalizedString("SHARE_ASK_FRIEND_MESSAGE", comment: "求助")
		titleLabel.text   = NSLocalizedString("SHARE_ASK_FRIEND", comment: "求助")
		linkButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		wechatButton.setButtonBackgroundColorStyle(ColorStyle.kGreenGradientColor)
		linkButton.setTitle(NSLocalizedString("SHARE_APP_LINK", comment: "分享链接"), for: .normal)
		wechatButton.setTitle(NSLocalizedString("SHARE_TO_WECHAT", comment: "分享微信"), for: .normal)
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true)
	}

	@IBAction func didClickLinkButton(_ sender: Any) {
		self.gotoAskPreviewViewController(.link)
	}

	@IBAction func didClickWechatButton(_ sender: Any) {
		guard let mynt = sn?.mynt else { return }
		if mynt.hardwareType == .CC25XX {
			MTToast.show(NSLocalizedString("SHARE_FIRM_NOT_SUPPORT", comment: ""))
			return
		}
		if Int(mynt.software)! <= 25 {
			MTToast.show(NSLocalizedString("SHARE_PLEASE_UPDATE_FIRM", comment: ""))
			return
		}

		mynt.authorizeWechat(success: {
				self.gotoAskPreviewViewController(.wechat)
		}) { msg in
			MTToast.show(msg)
		}
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	/**
	求助帮找

	*/
	func gotoAskPreviewViewController(_ type: SCShareType) {
		let viewController 			= AskPreviewViewController()
		viewController.sn 			= sn
		viewController.shareType 	= type
		self.present(BaseNavigationController(rootViewController: viewController), animated: true, completion: nil)
	}
}


