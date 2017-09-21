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
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		contentView.setShowdowStyle(ShadowStyle.kButtonShadow)

		oldPasswordTextField.placeHolder 			= MTLocalizedString("OLD_PASSWORD", comment: "旧密码")
		newPasswordTextField.placeHolder 			= MTLocalizedString("NEW_PASSWORD", comment: "新密码")
		conformPasswordTextField.placeHolder 		= MTLocalizedString("CONFIRM_PASSWORD", comment: "确认密码")
		submitButton.setTitle(MTLocalizedString("DONE", comment: "完成"), for: .normal)
		submitButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)

		oldPasswordTextField.secureTextEntry 		= true
		oldPasswordTextField.returnKeyType 			= .next
		oldPasswordTextField.delegate 				= self

		newPasswordTextField.secureTextEntry 		= true
		newPasswordTextField.returnKeyType 			= .done
		conformPasswordTextField.delegate 			= self

		conformPasswordTextField.secureTextEntry 	= true
		conformPasswordTextField.returnKeyType 		= .done
		conformPasswordTextField.delegate 			= self

		view.supportHideKeyBoard()
	}

	override func viewWillLayoutSubviews() {
		//圆角
		oldPasswordTextField.layer.cornerRadius 	= oldPasswordTextField.bounds.height / 2
		newPasswordTextField.layer.cornerRadius 	= newPasswordTextField.bounds.height / 2
		conformPasswordTextField.layer.cornerRaiuds = conformPasswordTextField.bounds.height / 2
		submitButton.layer.cornerRadius 			= submitButton.bounds.height / 2

		if #available(iOS 8.0, *) {
			[oldPasswordTextField, newPasswordTextField, conformPasswordTextField].forEach { (textField) in
				textField.layer.borderColor 		= UIColor.white.cgColor
				textField.layer.borderWidth 		= 1
			}
		} 
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	@IBAction func didClickSubmitButton(_ sender: AnyObject) {
		if _isPositing {
			return
		}
		let oldPassword  		= oldPasswordTextField.text?.trim()
		let newPassword 		= newPasswordTextField.text?.trim()
		let conformPassword 	= conformPasswordTextField.text?.trim()

		if oldPassword 	== "" {
			newPasswordTextField.shake()
			MTToast.show(MTLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if newPassword == "" {
			newPasswordTextField.shake()
			MTToast.show(MTLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if conformPassword == "" {
			conformPasswordTextField.shake()
			MTToast.show(MTLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
			return
		}
		if conformPassword != newPassword {
			conformPasswordTextField.shake()
			MTToast.show(MTLocalizedString("PASSWORD_NOTSAME", comment: "密码不同"))
			return
		}
		_isPositing = true
		MYNTKit.shared.user?.changePassword(oldPassword: oldPassword!, newPassword: newPassword!, success: { [weak self] in
			MTToast.show(MTLocalizedString("CHANGE_PASSWORD_SUCCESS", comment: "密码修改成功"))
			self?.dismissNavigationController(animated: true, completion: nil)
			self?._isPositing = false
		}) { [weak self] _, msg in
			MTToast.show(msg)
			self?._isPositing = false
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
			conformPasswordTextField.resignFristResponder()
			didClickSubmitButton(submitButton)
		}
		return true
	}
}

