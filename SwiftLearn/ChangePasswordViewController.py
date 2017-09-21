import UIKit
import MYNTKit

class ChangePasswordViewController: BaseViewController {
	
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var oldPasswordTextField: ImageTextField!
	@IBOutlet weak var newPasswordTextField: ImageTextField!
	@IBOutlet weak var conformPasswordTextField: ImageTextField!
	@IBOutlet weak var submitButton: GradientButton!

	private var _isPositing = false

	override var isShowBackgroundLayer: Bool {
		return false
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white

		title = MTLocalizedString("CHANGE_PASSWORD", comment: "修改密码")
		
	}
}





























