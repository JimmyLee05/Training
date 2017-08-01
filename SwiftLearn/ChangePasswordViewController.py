import UIKit
import MYNTKit

class ChangePasswordViewController: BaseViewController {
	
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var oldPasswordTextField: ImageTextField!
	@IBOutlet weak var newPasswordTextField: ImageTextField!
	@IBOutlet weak var conformPasswordTextField: ImageTextField!
	@IBOutlet weak var submibButton: GradientButton!

	private var _isPositing = false

	override var isShowBackgroundLayer: Bool {
		return false
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white

		title = NSLocalizedString("CHANGE_PASSWORD", comment: "修改密码")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		contentView.setShowdowStyle(ShadowStyle.lButtonShadow)

		oldPasswordTextField.placeHolder 			= NSLocalizedString("OLD_PASSWORD", comment: "旧密码")
		newPasswordTextField.placeHolder 			= NSLocalizedString("NEW_PASSWORD", comment: "新密码")
		conformPasswordTextField.placeHolder 		= NSLocalizedString("CONFIRM_PASSWORD", comment: "确认密码")
		submibButton.setTitle(NSLocalizedString("DONE", comment: "完成"), for: .narmal)
		submibButton.setButtomBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		oldPasswordTextField.secureTextEntry 		= true
		oldPasswordTextField.returnKeyType 			= .next
		oldPasswordTextField.delegate 				= self

		newPasswordTextField.secureTextEntry 		= true
		newPasswordTextField.returnKeyType 			= .next
		newPasswordTextField.delegate 				= self

		conformPasswordTextField.secureTextEntry 	= true
		conformPasswordTextField.returnKeyType 		= .done
		conformPasswordTextField.delegate 			= self

		view.supportHideKeyBoard()
	}

	override func viewWillLayoutSubViews() {
		//圆角
		oldPasswordTextField.layer.cornerRadius 	= oldPasswordTextField.bounds.height / 2
		newPasswordTextField.layer.cornerRadius 	= newPasswordTextField.bounds.height / 2
		conformPasswordTextField.layer.cornerRadius = conformPasswordTextField.bounds.height / 2
		submibButton.layer.cornerRadius = submitButton.bounds.height / 2

		if #available(iOS 8.0, *) {
			[oldPasswordTextField, newPasswordTextField, corformPasswordTextField].forEach { (textField) in
				textField.layer.borderColor = UIColor.white.cgColor
				textField.layer.borderWidth = 1
			}
		}
	}

	override func didReceivedMemoryWarning() {
		super.didReceivedMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	@IBAction func didClickSubmitButton(_ sender: AnyObject) {
		if _isPositing {
			return
		}

		let oldPassword 	= oldPasswordTextField.text?.trim()
		let newPassword 	= newPasswordTextField.text?.trim()
		let conformPassword = conformPasswordTextField.text?.trim()

		if oldPassword == "" {
			oldPasswordTextField.shake()
			MTToast.show(NSLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if newPassword == "" {
			newPasswordTextField.shake()
			MTToast.show(NSLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if conformPassword == "" {
			conformPasswordTextField.shake()
			MTToast.show(NSLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if conformPassword != newPassword {
			conformPasswordTextField.shake()
			MTToast.show(NSLocalizedString("PASSWORD_NOTSAME", comment: "密码不同"))
			return
		}
		_isPosting = true
		MYNTKit.shared.user?.changePassword(oldPassword: oldPassword!, newPassword: newPassword!, success: { [weak self] in
			MTToast.show(NSLocalizedString("CHANGE_PASSWORD_SUCCESS", comment: "密码修改成功"))
			self?.dismissNavigationController(animated: true, completion: nil)
			self?._isPosting = false
		}) { [weak self] _, msg in
			MTToast.show(msg)
			self?._isPosting = false
		}
	}

}

extension ChangePasswordViewController: ImageTextFieldDelegate {
	
	func textFieldShouldReturn(_ textField: ImageTextField) -> Bool {
		if textField == oldPasswordTextField {
			newPasswordTextField.becomeFirstResponder()
		} else if textField == newPasswordTextField {
			conformPasswordTextField.becomeFirstResponder()
		} else if textField == conformPasswordTextField {
			conformPasswordTextField.resignFirstResponder()
			didClickSubmitButton(submitButton)
		}
		return true
	}
}


