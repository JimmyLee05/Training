import UIKit
import MYNTKit

class LoginView: UIView, ImageEmailTextFieldDelegate, ImageTextFieldDelegate {
	
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var triangleView: TriangleView!
	@IBOutlet weak var emailTextField: ImageEmailTextField!
	@IBOutlet weak var usernameTextField: ImageTextField!
	@IBOutlet weak var passwordTextField: ImageTextField!
	@IBOutlet weak var loginButton: GradientButton!
	@IBOutlet weak var switchLoginButton: UIButton!
	@IBOutlet weak var switchSignButton: UIButton!
	@IBOutlet weak var switchForgetView: UIView!
	@IBOutlet weak var forgetLabel: UILabel!

	@IBOutlet weak var contentBootomConstrint: NSLayoutConstraint!

	@IBOutlet weak var usernameHeightConstraint: NSLayoutConstraint!
	@IBOutlet weak var usernameTopConstraint: NSLayoutConstraint!

	@IBOutlet weak var triangleLeftConstraint: NSLayoutConstraint!

	var loginHandler: ((_ isRegister: Bool) -> Void)?

	let selectedTextColor 	= UIColor(red:0.41, green:0.41, blue:0.42, alpha:1.00)
	let unselectedTextColor = UIColor(red:0.57, green:0.57, blue:0.58, alpha:1.00)

	override func awakeFromNib() {
		layer.masksToBounds = true
		//初始化
		usernameTopConstraint.constant 		= 0
		usernameHeightConstraint 			= 0
		
	}
}
























