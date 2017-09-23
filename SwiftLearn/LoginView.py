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
		//设置箭头向下
		triangleView.direction 				= .Bottom

		//多语言
		loginButton.setTitle(MTLocalizedString("LOGIN", comment: "登录"), for: .normal)
		switchLoginButton.setTitle(MTLocalizedString("LOGIN", comment: "登录"), for: .normal)
		switchSignButton.setTitle(MTLocalizedString("REGISTER", comment: "注册"), for: .normal)
		forgetLabel.text = MTLocalizedString("FORGET_PASSWORD", comment: "忘记密码")
		emailTextField.placeHolder = MTLocalizedString("EMAIL_ADDRESS", comment: "密码邮箱")
		usernameTextField.placeHolder =	MTLocalizedString("USER_NAME", comment: "用户名")
		passwordTextField.placeHolder = MTLocalizedString("PASSWORD", comment: "密码")

		emailTextField.keyboardType 		= .emailAddress
		emailTextField.retrunKeyType 		= .next
		emailTextField.delegate 			= self
		usernameTextField.retrunKeyType 	= .next
		usernameTextField.delegate 			= self
		passwordTextField.returnKeyType 	= self
	}

	
}
























